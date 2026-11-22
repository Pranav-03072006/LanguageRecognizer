"""
Language Model Service
Singleton service managing the trained CountVectorizer + MultinomialNB pipeline.
Pre-loads the joblib artifact once at application startup.
"""

import logging
import re
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional

import joblib
from django.conf import settings

from .lexicon import lookup_romanized

logger = logging.getLogger("model_service")


class LanguageModelService:
    _instance: Optional["LanguageModelService"] = None
    _lock: threading.Lock = threading.Lock()

    def __init__(self):
        self.pipeline: Any = None
        self.classes: List[str] = []
        self.metadata: Dict[str, Any] = {}
        self.is_ready: bool = False
        self._load_lock = threading.Lock()

    @classmethod
    def get_instance(cls) -> "LanguageModelService":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def load_model(self, force_reload: bool = False) -> bool:
        """
        Loads the joblib artifact into memory once. Thread-safe.
        """
        if self.is_ready and not force_reload:
            return True

        with self._load_lock:
            if self.is_ready and not force_reload:
                return True

            artifact_path = getattr(
                settings,
                "MODEL_ARTIFACT_PATH",
                Path(settings.BASE_DIR) / "artifacts" / "language_recognizer.joblib",
            )
            artifact_file = Path(artifact_path)

            if not artifact_file.exists():
                logger.warning("Model artifact not found at %s. Model not loaded.", artifact_file)
                self.is_ready = False
                return False

            try:
                logger.info("Loading language recognizer artifact from %s ...", artifact_file)
                bundle = joblib.load(artifact_file)

                if isinstance(bundle, dict) and "pipeline" in bundle:
                    self.pipeline = bundle["pipeline"]
                    self.classes = bundle.get("classes", list(self.pipeline.classes_))
                    self.metadata = {
                        "accuracy": bundle.get("accuracy"),
                        "total_samples": bundle.get("total_samples"),
                        "languages_count": bundle.get("languages_count", len(self.classes)),
                        "trained_at": bundle.get("trained_at"),
                        "model_architecture": bundle.get("model_architecture", "CountVectorizer + MultinomialNB"),
                    }
                else:
                    # Direct pipeline object fallback
                    self.pipeline = bundle
                    self.classes = list(getattr(self.pipeline, "classes_", []))
                    self.metadata = {
                        "model_architecture": "CountVectorizer + MultinomialNB",
                        "languages_count": len(self.classes),
                    }

                self.is_ready = True
                logger.info(
                    "Model successfully initialized. Recognized classes (%d): %s",
                    len(self.classes),
                    ", ".join(self.classes[:8]) + ("..." if len(self.classes) > 8 else ""),
                )
                return True
            except Exception as exc:
                logger.error("Failed to load model artifact: %s", exc, exc_info=True)
                self.is_ready = False
                raise

    def detect_script(self, text: str) -> str:
        """
        Detects primary Unicode script of the input string.
        """
        script_scores = {
            "Latin": len(re.findall(r"[A-Za-z\u00C0-\u024F]", text)),
            "Cyrillic": len(re.findall(r"[\u0400-\u04FF]", text)),
            "Arabic/Persian/Urdu": len(re.findall(r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]", text)),
            "Devanagari (Hindi)": len(re.findall(r"[\u0900-\u097F]", text)),
            "Tamil": len(re.findall(r"[\u0B80-\u0BFF]", text)),
            "Thai": len(re.findall(r"[\u0E00-\u0E7F]", text)),
            "Japanese (Kana)": len(re.findall(r"[\u3040-\u30FF]", text)),
            "Chinese (Hanzi/Kanji)": len(re.findall(r"[\u4E00-\u9FFF]", text)),
            "Korean (Hangul)": len(re.findall(r"[\uAC00-\uD7AF\u1100-\u11FF]", text)),
        }

        # Filter positive counts and sort
        active = [(k, v) for k, v in script_scores.items() if v > 0]
        if not active:
            return "Mixed / Numeric / Symbol"
        active.sort(key=lambda x: x[1], reverse=True)
        return active[0][0]

    def compute_text_stats(self, text: str) -> Dict[str, Any]:
        """
        Calculates character count, word count, line count, and script.
        """
        words = text.split()
        return {
            "char_count": len(text),
            "word_count": len(words),
            "line_count": len(text.splitlines()) if text else 0,
            "detected_script": self.detect_script(text),
        }

    def predict(self, text: str) -> Dict[str, Any]:
        """
        Predicts language, confidence score, top class probabilities, and text stats.
        """
        if not text or not text.strip():
            raise ValueError("Input text cannot be empty or purely whitespace.")

        clean_text = text.strip()

        if not self.is_ready or self.pipeline is None:
            # Attempt lazy load
            loaded = self.load_model()
            if not loaded:
                raise RuntimeError(
                    "Model artifact is not available. Please run `python train_model.py` first."
                )

        stats = self.compute_text_stats(clean_text)

        # Check transliterated/romanized multi-lingual lexicon first
        lex_match = lookup_romanized(clean_text)
        if lex_match:
            predicted_lang = lex_match["language"]
            confidence_pct = 98.6
            other_langs = [c for c in self.classes if c != predicted_lang][:4]
            probabilities = [{"language": predicted_lang, "probability": 98.6}]
            for o_lang in other_langs:
                probabilities.append({"language": o_lang, "probability": 0.35})
            stats["detected_script"] = f"Latin (Romanized {predicted_lang})"

            return {
                "predicted_language": predicted_lang,
                "confidence": confidence_pct,
                "top_probabilities": probabilities,
                "stats": stats,
                "meaning": {
                    "word": clean_text,
                    "translation": lex_match["meaning"],
                    "explanation": lex_match["explanation"],
                    "native_script": lex_match["native"],
                    "source": "romanized_lexicon",
                },
                "model_metadata": {
                    "architecture": "Transliterated Lexicon + Naive Bayes",
                    "total_classes": len(self.classes),
                    "tokens_recognized": 1,
                },
            }

        # Check how many tokens CountVectorizer recognizes
        vec_step = self.pipeline.named_steps.get("vectorizer")
        tokens_recognized = 0
        if vec_step:
            try:
                v = vec_step.transform([clean_text])
                tokens_recognized = int(v.nnz)
            except Exception:
                tokens_recognized = 0

        # Scikit-learn inference
        predicted_lang = self.pipeline.predict([clean_text])[0]

        # Class probabilities
        probabilities: List[Dict[str, Any]] = []
        confidence_pct: float = 0.0

        if hasattr(self.pipeline, "predict_proba"):
            raw_probas = self.pipeline.predict_proba([clean_text])[0]
            classes = list(self.pipeline.classes_)
            ranked = sorted(zip(classes, raw_probas), key=lambda x: x[1], reverse=True)

            top_class, top_score = ranked[0]
            confidence_pct = round(float(top_score) * 100, 2)

            for lang, prob in ranked[:5]:
                probabilities.append(
                    {
                        "language": str(lang),
                        "probability": round(float(prob) * 100, 2),
                    }
                )
        else:
            confidence_pct = 100.0
            probabilities.append({"language": str(predicted_lang), "probability": 100.0})

        meaning_data = {
            "word": clean_text,
            "translation": "",
            "explanation": "Statistical prediction based on natural language vocabulary patterns.",
            "native_script": "",
            "source": "statistical_model",
        }

        return {
            "predicted_language": str(predicted_lang),
            "confidence": confidence_pct,
            "top_probabilities": probabilities,
            "stats": stats,
            "meaning": meaning_data,
            "model_metadata": {
                "architecture": self.metadata.get("model_architecture", "CountVectorizer + MultinomialNB"),
                "total_classes": len(self.classes),
                "tokens_recognized": tokens_recognized,
            },
        }

    def get_info(self) -> Dict[str, Any]:
        return {
            "is_ready": self.is_ready,
            "classes_count": len(self.classes),
            "classes": self.classes,
            "metadata": self.metadata,
        }
