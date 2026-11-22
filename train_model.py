"""
Language Recognizer Training Script
Trains a CountVectorizer + MultinomialNB pipeline on text data (language.csv)
and exports the serialized model bundle to artifacts/language_recognizer.joblib.
"""

import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("train_model")

SCRIPT_DIR = Path(__file__).resolve().parent


def parse_args():
    parser = argparse.ArgumentParser(description="Train Language Recognizer Model")
    parser.add_argument(
        "--data-path",
        type=str,
        default=str(SCRIPT_DIR / "data" / "language.csv"),
        help="Path to training CSV file (must contain 'Text' and 'language' columns)",
    )
    parser.add_argument(
        "--output-path",
        type=str,
        default=str(SCRIPT_DIR / "artifacts" / "language_recognizer.joblib"),
        help="Path to save the fitted joblib artifact",
    )
    parser.add_argument(
        "--test-size",
        type=float,
        default=0.33,
        help="Proportion of dataset to include in test split (default: 0.33)",
    )
    parser.add_argument(
        "--random-state",
        type=int,
        default=45,
        help="Random seed for train/test split reproducibility (default: 45)",
    )
    parser.add_argument(
        "--sample-size",
        type=int,
        default=None,
        help="Optional: sample only N rows (useful for fast CI verification)",
    )
    return parser.parse_args()


def train_model(
    data_path: str,
    output_path: str,
    test_size: float = 0.33,
    random_state: int = 45,
    sample_size: int = None,
):
    """
    Loads data, trains the CountVectorizer + MultinomialNB pipeline,
    evaluates performance, and serializes the bundle.
    """
    data_file = Path(data_path)
    if not data_file.exists():
        if not data_file.is_absolute() and (SCRIPT_DIR / data_file).exists():
            data_file = SCRIPT_DIR / data_file
        elif Path(r"D:\language\language.csv").exists():
            data_file = Path(r"D:\language\language.csv")
        else:
            raise FileNotFoundError(f"Training data file not found at: {data_path}")

    logger.info("Step 1: Loading dataset from %s ...", data_path)
    df = pd.read_csv(data_file)
    logger.info("Loaded %d rows and %d columns.", len(df), len(df.columns))

    # Verify required columns
    required_cols = {"Text", "language"}
    if not required_cols.issubset(set(df.columns)):
        raise ValueError(
            f"Dataset missing required columns. Expected {required_cols}, found {list(df.columns)}"
        )

    # Clean null / empty entries
    null_count = df.isnull().sum().to_dict()
    logger.info("Null values per column: %s", null_count)
    df = df.dropna(subset=["Text", "language"])
    df["Text"] = df["Text"].astype(str).str.strip()
    df["language"] = df["language"].astype(str).str.strip()
    df = df[df["Text"].str.len() > 0]

    if sample_size and sample_size < len(df):
        logger.info("Sampling %d rows for rapid training / test verification...", sample_size)
        df = df.groupby("language", group_keys=False).apply(
            lambda x: x.sample(min(len(x), max(2, sample_size // df["language"].nunique())), random_state=random_state)
        )

    logger.info("Distinct languages count: %d", df["language"].nunique())
    class_distribution = df["language"].value_counts().to_dict()
    logger.info("Class distribution (top 5): %s", dict(list(class_distribution.items())[:5]))

    x = df["Text"].values
    y = df["language"].values

    logger.info("Step 2: Splitting dataset (test_size=%.2f, random_state=%d) ...", test_size, random_state)
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=test_size, random_state=random_state, stratify=y if df["language"].nunique() > 1 else None
    )
    logger.info("Training samples: %d, Testing samples: %d", len(x_train), len(x_test))

    logger.info("Step 3: Building CountVectorizer + MultinomialNB Pipeline ...")
    pipeline = Pipeline(
        [
            (
                "vectorizer",
                CountVectorizer(
                    ngram_range=(1, 1),
                    lowercase=True,
                ),
            ),
            ("classifier", MultinomialNB(alpha=1.0)),
        ]
    )

    logger.info("Fitting pipeline on training data...")
    pipeline.fit(x_train, y_train)

    logger.info("Step 4: Evaluating model on test set...")
    y_pred = pipeline.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)
    logger.info("Model Accuracy: %.5f (%.2f%%)", accuracy, accuracy * 100)

    # Detailed report for visibility
    report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
    logger.info("Macro avg F1-score: %.4f", report.get("macro avg", {}).get("f1-score", 0.0))

    # Package artifact bundle
    bundle = {
        "pipeline": pipeline,
        "classes": sorted(list(pipeline.classes_)),
        "accuracy": float(accuracy),
        "total_samples": int(len(df)),
        "languages_count": int(len(pipeline.classes_)),
        "trained_at": datetime.utcnow().isoformat() + "Z",
        "model_architecture": "CountVectorizer + MultinomialNB",
    }

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    logger.info("Step 5: Saving model bundle to %s (compress=3) ...", output_path)
    joblib.dump(bundle, output_file, compress=3)
    logger.info("Model artifact successfully saved (%d bytes).", output_file.stat().st_size)

    # Test sample predictions
    sample_tests = [
        ("Hello, how are you today? Hope all is well.", "English"),
        ("Bonjour tout le monde, comment allez-vous aujourd'hui?", "French"),
        ("Hola amigo, ¿cómo estás hoy? Todo bien.", "Spanish"),
        ("Привет, как ваши дела сегодня? Надеюсь, все хорошо.", "Russian"),
        ("नमस्ते, आप आज कैसे हैं? सब कुछ ठीक है।", "Hindi"),
    ]
    logger.info("Running sample validation checks:")
    for text, expected in sample_tests:
        pred = pipeline.predict([text])[0]
        logger.info("  Sample: '%s' -> Predicted: %s (Expected: %s)", text[:30] + "...", pred, expected)

    return bundle


if __name__ == "__main__":
    args = parse_args()
    train_model(
        data_path=args.data_path,
        output_path=args.output_path,
        test_size=args.test_size,
        random_state=args.random_state,
        sample_size=args.sample_size,
    )
