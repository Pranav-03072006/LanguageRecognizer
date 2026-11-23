"""
Comprehensive Unit Tests for Language Recognizer Web Application.
Tests:
- Scikit-learn CountVectorizer + MultinomialNB ML model inference
- Text statistics computation (char, word, script)
- Direct LLM fallback mechanism (offline mode)
- Mocked LLM responses for Gemini & OpenAI SDKs
- Django HTTP views & JSON REST endpoints
"""

import json
from unittest.mock import MagicMock, patch
from django.test import Client, TestCase
from django.urls import reverse

from detector.services.llm_service import DirectLLMService, FALLBACK_LINGUISTIC_PROFILES
from detector.services.model_service import LanguageModelService


class ModelServiceTests(TestCase):
    """Tests for the ML inference service and text preprocessing."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.service = LanguageModelService.get_instance()
        cls.service.load_model()

    def test_model_is_ready(self):
        """Verify model bundle loaded successfully."""
        self.assertTrue(self.service.is_ready)
        self.assertGreaterEqual(len(self.service.classes), 15)

    def test_prediction_known_languages(self):
        """Test accuracy of predictions on standard phrases across distinct language families."""
        test_cases = [
            ("Hello, this is an English language identification test sentence.", "English"),
            ("Bonjour, ceci est un test de reconnaissance de la langue française.", "French"),
            ("Hola amigo, esta es una frase en idioma español para probar el modelo.", "Spanish"),
            ("Привет, это тестовое предложение на русском языке для проверки модели.", "Russian"),
            ("नमस्ते, यह मॉडल परीक्षण के लिए हिंदी भाषा का एक वाक्य है।", "Hindi"),
        ]

        for text, expected_lang in test_cases:
            with self.subTest(language=expected_lang):
                result = self.service.predict(text)
                self.assertEqual(result["predicted_language"], expected_lang)
                self.assertGreaterEqual(result["confidence"], 50.0)
                self.assertEqual(len(result["top_probabilities"]), min(5, len(self.service.classes)))

    def test_sayonara_and_romanized_phrases(self):
        """Verify that romanized loanwords like 'Sayonara' accurately predict Japanese with meaning."""
        result = self.service.predict("Sayonara")
        self.assertEqual(result["predicted_language"], "Japanese")
        self.assertGreaterEqual(result["confidence"], 90.0)
        self.assertIn("Goodbye", result["meaning"]["translation"])
        self.assertEqual(result["meaning"]["native_script"], "さようなら")

    def test_conversational_greetings_accuracy(self):
        """Verify common conversational words like 'Hello', 'Hi', 'Bonjour', 'Hola' predict correctly."""
        greetings = [
            ("Hello", "English"),
            ("hello", "English"),
            ("hi", "English"),
            ("how are you", "English"),
            ("thank you", "English"),
            ("welcome", "English"),
            ("Bonjour", "French"),
            ("Hola", "Spanish"),
            ("Sayonara", "Japanese"),
            ("Namaste", "Hindi"),
            ("Dank je", "Dutch"),
        ]
        for phrase, expected in greetings:
            with self.subTest(phrase=phrase):
                res = self.service.predict(phrase)
                self.assertEqual(res["predicted_language"], expected)
                self.assertGreaterEqual(res["confidence"], 90.0)

    def test_empty_input_validation(self):
        """Verify that empty strings or whitespace raise ValueError."""
        with self.assertRaises(ValueError):
            self.service.predict("")

        with self.assertRaises(ValueError):
            self.service.predict("    \n\t   ")

    def test_text_stats_computation(self):
        """Verify character and word counting logic."""
        sample_text = "The quick brown fox jumps"
        stats = self.service.compute_text_stats(sample_text)
        self.assertEqual(stats["char_count"], len(sample_text))
        self.assertEqual(stats["word_count"], 5)
        self.assertEqual(stats["detected_script"], "Latin")

    def test_script_detection_multilingual(self):
        """Verify Unicode script classification for non-Latin scripts."""
        self.assertEqual(self.service.detect_script("Привет мир"), "Cyrillic")
        self.assertEqual(self.service.detect_script("नमस्ते भारत"), "Devanagari (Hindi)")
        self.assertEqual(self.service.detect_script("مرحبا بالعالم"), "Arabic/Persian/Urdu")
        self.assertEqual(self.service.detect_script("வணக்கம் உலகம்"), "Tamil")
        self.assertEqual(self.service.detect_script("こんにちは世界"), "Japanese (Kana)")
        self.assertEqual(self.service.detect_script("你好世界"), "Chinese (Hanzi/Kanji)")
        self.assertEqual(self.service.detect_script("안녕하세요"), "Korean (Hangul)")


class LLMServiceTests(TestCase):
    """Tests for direct LLM integration and rule-based offline fallbacks."""

    def setUp(self):
        self.llm_service = DirectLLMService()

    def test_fallback_when_api_key_empty(self):
        """Verify rich fallback profile returned when no LLM_API_KEY is configured."""
        with patch.object(self.llm_service, "api_key", ""):
            enrichment = self.llm_service.get_enrichment("French", "Bonjour le monde")
            self.assertEqual(enrichment["source"], "fallback")
            self.assertEqual(enrichment["language"], "French")
            self.assertIn("Romance", enrichment["language_family"])
            self.assertIn("Français", enrichment["native_name"])
            self.assertTrue(len(enrichment["overview"]) > 20)

    def test_fallback_all_22_languages(self):
        """Verify fallback profiles exist and have required keys for all 22 supported languages."""
        for lang_name, profile in FALLBACK_LINGUISTIC_PROFILES.items():
            fallback = self.llm_service.get_fallback_profile(lang_name, "Sample text")
            self.assertEqual(fallback["language"], lang_name)
            self.assertTrue(len(fallback["language_family"]) > 0)
            self.assertTrue(len(fallback["writing_script"]) > 0)
            self.assertTrue(len(fallback["overview"]) > 10)

    @patch("google.genai.Client")
    def test_mocked_gemini_direct_call(self, mock_client_cls):
        """Verify direct google-genai SDK call without LangChain."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "language_family": "Indo-European -> Romance",
            "writing_script": "Latin alphabet",
            "native_name": "Français",
            "linguistic_overview": "French is a major world language.",
            "grammatical_traits": "Grammatical gender and synthetic verbal forms.",
            "translation_or_gist": "Hello everyone.",
            "fun_fact": "French was the official language of England for 300 years.",
        })
        mock_client.models.generate_content.return_value = mock_response
        mock_client_cls.return_value = mock_client

        with patch.object(self.llm_service, "api_key", "test-gemini-key"), \
             patch.object(self.llm_service, "provider", "gemini"):
            result = self.llm_service.get_enrichment("French", "Bonjour tout le monde")
            self.assertEqual(result["source"], "llm")
            self.assertEqual(result["provider"], "Google Gemini")
            self.assertEqual(result["native_name"], "Français")
            self.assertIn("Romance", result["language_family"])

    @patch("openai.OpenAI")
    def test_mocked_openai_direct_call(self, mock_openai_cls):
        """Verify direct OpenAI SDK call without LangChain."""
        mock_client = MagicMock()
        mock_completion = MagicMock()
        mock_choice = MagicMock()
        mock_choice.message.content = json.dumps({
            "language_family": "Indo-European -> Romance",
            "writing_script": "Latin alphabet",
            "native_name": "Español",
            "linguistic_overview": "Spanish is an Ibero-Romance language.",
            "grammatical_traits": "Two genders and pro-drop verbs.",
            "translation_or_gist": "Good morning.",
            "fun_fact": "Spanish has thousands of Arabic loanwords.",
        })
        mock_completion.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_completion
        mock_openai_cls.return_value = mock_client

        with patch.object(self.llm_service, "api_key", "test-openai-key"), \
             patch.object(self.llm_service, "provider", "openai"):
            result = self.llm_service.get_enrichment("Spanish", "Buenos días a todos")
            self.assertEqual(result["source"], "llm")
            self.assertEqual(result["provider"], "OpenAI")
            self.assertEqual(result["native_name"], "Español")

    def test_graceful_recovery_on_api_exception(self):
        """Verify that an exception during LLM API call cleanly falls back to local knowledge."""
        with patch.object(self.llm_service, "api_key", "invalid-key"), \
             patch.object(self.llm_service, "provider", "gemini"), \
             patch.object(self.llm_service, "call_gemini", side_effect=Exception("API Connection Failed")):
            result = self.llm_service.get_enrichment("German", "Guten Tag")
            self.assertEqual(result["source"], "fallback")
            self.assertIn("German", result["language"])
            self.assertIn("West Germanic", result["language_family"])


class ViewAndApiTests(TestCase):
    """Tests for HTTP views and API endpoints."""

    def setUp(self):
        self.client = Client()

    def test_index_page_returns_200(self):
        """GET / should render the index dashboard template."""
        response = self.client.get(reverse("detector:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "PolyGlot AI")
        self.assertContains(response, "CountVectorizer + MultinomialNB")

    def test_detect_api_post_valid_json(self):
        """POST /api/detect/ with valid text returns classification and insights."""
        payload = {"text": "Bonjour tout le monde, comment allez-vous?"}
        response = self.client.post(
            reverse("detector:detect_api"),
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["prediction"]["language"], "French")
        self.assertGreater(data["prediction"]["confidence"], 0)
        self.assertIn("stats", data)
        self.assertIn("ai_insights", data)

    def test_detect_api_post_empty_text_returns_400(self):
        """POST /api/detect/ with empty text returns 400 Bad Request."""
        payload = {"text": "   "}
        response = self.client.post(
            reverse("detector:detect_api"),
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data["success"])
        self.assertIn("error", data)

    def test_languages_api_returns_200(self):
        """GET /api/languages/ returns supported language classes and samples."""
        response = self.client.get(reverse("detector:languages_api"))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertGreaterEqual(data["total"], 20)
        self.assertIn("samples", data)

    def test_health_check_returns_200(self):
        """GET /api/health/ returns container health status."""
        response = self.client.get(reverse("detector:health_check"))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("status", data)
        self.assertTrue(data["model_ready"])
