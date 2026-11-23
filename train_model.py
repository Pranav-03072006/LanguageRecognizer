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

    # Augment with conversational phrases across 22 classes so common words
    # (like hello, hi, thank you, please, etc.) are properly represented
    conversational_samples = [
        # English
        ("hello how are you doing today? hello everyone and welcome to our community.", "English"),
        ("hi there, hello and good morning to all of you, hope you are having a wonderful day.", "English"),
        ("thank you very much for your kind help and support, thanks a lot for everything.", "English"),
        ("please let me know if you need anything else, you are welcome anytime, thank you.", "English"),
        ("goodbye, see you soon, bye for now, take care and have a great weekend.", "English"),
        ("yes that is right, yeah sure absolutely no problem at all, okay great.", "English"),
        ("what is your name? my name is John, nice to meet you, where are you from?", "English"),
        ("good evening and good night, sleep well and see you tomorrow morning.", "English"),
        ("hello world, this is a test greeting, welcome to the language recognizer application.", "English"),
        ("how are you feeling today? i am doing fine, thank you for asking.", "English"),
        ("excuse me, pardon me, sorry about that, no worries, it is totally okay.", "English"),
        ("cheers, congratulations on your great success, happy birthday and best wishes.", "English"),
        # Dutch
        ("hallo hoe gaat het met jou vandaag? hallo allemaal en welkom hier.", "Dutch"),
        ("goedemorgen allemaal, ik wens jullie een hele fijne en prettige dag toe.", "Dutch"),
        ("hartelijk dank voor uw hulp en ondersteuning, dank je wel voor alles.", "Dutch"),
        ("alsjeblieft, graag gedaan, tot ziens en een prettige dag verder.", "Dutch"),
        ("ja dat klopt inderdaad, nee dat is niet waar, geen enkel probleem.", "Dutch"),
        ("wat is jouw naam? mijn naam is Jan, aangenaam kennis te maken.", "Dutch"),
        ("goedenavond en welterusten voor straks, tot morgenochtend allemaal.", "Dutch"),
        # French
        ("bonjour comment allez-vous aujourd'hui? bonjour à tous et bienvenue.", "French"),
        ("salut tout le monde, bonjour et bonne journée à vous tous.", "French"),
        ("merci beaucoup pour votre aide précieuse, merci infiniment pour tout.", "French"),
        ("s'il vous plaît, je vous en prie, de rien, avec grand plaisir.", "French"),
        ("au revoir, à bientôt, à plus tard, prenez bien soin de vous.", "French"),
        ("comment vous appelez-vous? je m'appelle Pierre, enchanté de faire votre connaissance.", "French"),
        # Spanish
        ("hola cómo estás hoy? hola a todos y bienvenidos a nuestra comunidad.", "Spanish"),
        ("buenos días a todos, espero que tengan un excelente y maravilloso día.", "Spanish"),
        ("muchas gracias por toda tu ayuda y apoyo, gracias de todo corazón.", "Spanish"),
        ("por favor dime si necesitas algo, de nada, un placer ayudarte.", "Spanish"),
        ("adiós, hasta luego, hasta pronto, nos vemos luego, cuídate mucho.", "Spanish"),
        ("cómo te llamas? me llamo Carlos, mucho gusto en conocerte, de dónde eres?", "Spanish"),
        # Latin
        ("salve quomodo vales hodie? salvete omnes et bene venistis ad nos.", "Latin"),
        ("bonum mane omnibus vobis, opto ut diem felicissimum habeatis.", "Latin"),
        ("gratias maximas tibi ago pro auxilio tuo et benevolentia tua.", "Latin"),
        ("quaeso te, libenter feci, nihil est, gaudeo te iuvisse.", "Latin"),
        ("vale, valete omnes, in proximum videmus, cura ut valeas.", "Latin"),
        # Swedish
        ("hej hur mår du idag? hej alla och varmt välkomna hit till oss.", "Swedish"),
        ("god morgon allihopa, jag hoppas att ni har en riktigt trevlig och bra dag.", "Swedish"),
        ("tack så mycket för all din hjälp och ditt stöd, stort tack för allt.", "Swedish"),
        ("varsågod, det var så lite så, ha en fortsatt fin och trevlig dag.", "Swedish"),
        ("hej då, vi ses snart igen, ta hand om dig och ha en underbar helg.", "Swedish"),
        # Portugese
        ("olá como você está hoje? olá a todos e bem-vindos à nossa comunidade.", "Portugese"),
        ("bom dia a todos, espero que vocês tenham um dia maravilhoso e produtivo.", "Portugese"),
        ("muito obrigado por toda a sua ajuda e apoio, agradeço muito por tudo.", "Portugese"),
        ("por favor me avise se precisar, de nada, foi um prazer te ajudar.", "Portugese"),
        ("adeus, até logo, até breve, até mais, tchau tchau, cuide-se bem.", "Portugese"),
        # Russian
        ("привет как дела сегодня? здравствуйте всем и добро пожаловать к нам.", "Russian"),
        ("доброе утро всем, желаю вам отличного и продуктивного дня.", "Russian"),
        ("большое спасибо за вашу помощь и поддержку, спасибо за все.", "Russian"),
        ("пожалуйста, не за что, рад был помочь, обращайтесь в любое время.", "Russian"),
        ("до свидания, пока, до скорой встречи, берегите себя и удачи.", "Russian"),
        # Hindi
        ("नमस्ते आप आज कैसे हैं? आप सभी का यहाँ हार्दिक स्वागत है।", "Hindi"),
        ("शुभ प्रभात, आशा है कि आपका दिन बहुत अच्छा और सुखद रहेगा।", "Hindi"),
        ("आपकी सहायता और सहयोग के लिए बहुत-बहुत धन्यवाद, शुक्रिया।", "Hindi"),
        ("कृपया मुझे बताएं, आपका स्वागत है, कोई बात नहीं, खुशी हुई।", "Hindi"),
        ("अलविदा, फिर मिलेंगे, अपना ख्याल रखें और सुरक्षित रहें।", "Hindi"),
        # Arabic
        ("مرحباً كيف حالك اليوم؟ أهلاً وسهلاً بكم جميعاً في موقعنا.", "Arabic"),
        ("صباح الخير للجميع، أتمنى لكم يوماً سعيداً ومميزاً وموفقاً.", "Arabic"),
        ("شكراً جزيلاً لك على كل مساعدتك ودعمك الكريم، شكراً لك.", "Arabic"),
        ("من فضلك أخبرني، عَفواً، على الرحب والسعة، لا شكر على واجب.", "Arabic"),
        ("مع السلامة، إلى اللقاء قريباً، دمتم بخير وفي رعاية الله.", "Arabic"),
        # Japanese
        ("こんにちは今日はどうですか？皆さんようこそいらっしゃいました。", "Japanese"),
        ("おはようございます、今日も良い一日をお過ごしください。", "Japanese"),
        ("ご親切な支援をいただき、本当にありがとうございました。", "Japanese"),
        ("さようなら、また会いましょう、どうぞお元気でお過ごしください。", "Japanese"),
        # Chinese
        ("你好今天怎么样？欢迎大家来到我们的网站，大家辛苦了。", "Chinese"),
        ("早上好，祝愿大家今天都有一个非常愉快顺利的一天。", "Chinese"),
        ("非常感谢您的帮助与大力支持，十分感谢您的付出。", "Chinese"),
        ("再见，期待下次再会，请大家多多保重身体，一路顺风。", "Chinese"),
        # Korean
        ("안녕하세요 오늘 어떻게 지내세요? 여러분 모두를 진심으로 환영합니다.", "Korean"),
        ("좋은 아침입니다, 오늘 하루도 행복하고 즐거운 시간 보내세요.", "Korean"),
        ("도와주셔서 진심으로 감사드립니다, 정말 대단히 감사합니다.", "Korean"),
        ("안녕히 계세요, 다음에 또 만나요, 항상 건강하시길 바랍니다.", "Korean"),
        # Turkish
        ("merhaba bugün nasılsın? herkese merhaba ve aramıza hoş geldiniz.", "Turkish"),
        ("günaydın arkadaşlar, hepinize harika ve verimli bir gün dilerim.", "Turkish"),
        ("tüm yardımlarınız ve desteğiniz için çok teşekkür ederim, sağ olun.", "Turkish"),
        ("hoşça kalın, güle güle, yakında görüşmek üzere, kendinize iyi bakın.", "Turkish"),
    ]

    aug_rows = []
    for txt, lng in conversational_samples:
        for _ in range(5):
            aug_rows.append({"Text": txt, "language": lng})
    if aug_rows:
        aug_df = pd.DataFrame(aug_rows)
        df = pd.concat([df, aug_df], ignore_index=True)
        logger.info("Added %d conversational augmented rows for key vocabularies.", len(aug_rows))

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
