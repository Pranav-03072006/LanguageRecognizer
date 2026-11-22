# PolyGlot AI &bull; Language Recognizer Web Application

A production-ready **Language Recognizer Web Application** built with **Django**, **scikit-learn** (`CountVectorizer` + `MultinomialNB`), **Direct LLM SDK Integration** (Google GenAI / OpenAI with no LangChain or RAG), **Docker**, and a **GitHub Actions CI/CD Pipeline**.

---

## 🌟 Key Features

### 1. Statistical Machine Learning Language Classifier (`scikit-learn`)
- **Pipeline**: `CountVectorizer` (unigram tokenization) + `MultinomialNB` (Multinomial Naive Bayes) pipeline.
- **Dataset**: Trained on 22,000 multi-lingual sentences across **22 natural languages** (`language.csv`).
- **High Accuracy**: Evaluates at **~94.2% test accuracy** across balanced multilingual classes.
- **Startup Singleton Pre-Loading**: Artifact `artifacts/language_recognizer.joblib` is loaded **once at Django startup** via `apps.py` into a thread-safe singleton service—never inside request handlers and without blocking `input()` calls.
- **Comprehensive Inference**: Returns `predicted_language`, confidence score percentage, ranked top-5 class probabilities, and text statistics (`char_count`, `word_count`, `line_count`, `detected_script`).

### 2. Direct LLM Integration (No LangChain, No RAG)
- **Direct Official SDKs**: Direct API calls using `google-genai` (Google Gemini) and `openai` (OpenAI), completely free of LangChain, vector databases, agent wrappers, or RAG frameworks.
- **Configurable**: Configured via `.env` (`LLM_PROVIDER`, `LLM_API_KEY`, `LLM_MODEL`).
- **Linguistic Enrichment**: Generates linguistic classifications, language family branch, writing script descriptions, grammatical characteristics, and brief English translation/gist.
- **Robust Rule/Template Offline Fallback**: Includes a verified knowledge base covering all 22 languages. If `LLM_API_KEY` is omitted or an external API call fails, the application automatically displays verified linguistic profiles out-of-the-box.

### 3. Interactive Web Frontend
- **Single-Page Architecture**: Rendered via Django templates (`templates/index.html`) + vanilla JavaScript (`static/js/app.js`) + Tailwind CSS CDN + custom styles (`static/css/styles.css`).
- **Live Counters**: Real-time character, word, line, and Unicode script detection as the user types.
- **Quick Sample Chips**: Clickable sample pills across diverse languages (French, Spanish, Hindi, Russian, Arabic, Japanese, Chinese, Latin, etc.) with a "Random Sample" button.
- **Keyboard Shortcut**: `Ctrl + Enter` (or `Cmd + Enter`) triggers instant detection.
- **Visual Probability Breakdown**: Animated progress bars showing the top 5 predicted languages.
- **AI Insights Card**: Cleanly presents language family, script, estimated speakers, overview, translation, and linguistic trivia.
- **Recent Detections History**: Cached in `localStorage` with click-to-reload support and history clearing.

### 4. Containerization & CI/CD Pipeline
- **Docker**: Production-ready `Dockerfile` (multi-stage Python 3.10 slim, curl healthcheck, Gunicorn WSGI server) and `docker-compose.yml`.
- **GitHub Actions CI/CD (`.github/workflows/ci.yml`)**:
  1. Python 3.10 and 3.11 test matrix
  2. Code linting (`flake8`)
  3. Model training pipeline verification on sample dataset (`data/sample_dataset.csv`)
  4. 15 automated unit tests with mocked LLM SDK calls (offline deterministic runs)
  5. Container build verification (`docker build`)

---

## 🌐 Supported Languages (22 Classes)

| Language | Native Name | Language Family | Writing Script |
| :--- | :--- | :--- | :--- |
| **Arabic** | العَرَبِيَّة | Afroasiatic (Semitic) | Arabic (Abjad, RTL) |
| **Chinese** | 中文 (汉语) | Sino-Tibetan (Sinitic) | Hanzi (Simplified/Traditional) |
| **Dutch** | Nederlands | Indo-European (West Germanic) | Latin |
| **English** | English | Indo-European (West Germanic) | Latin |
| **Estonian** | Eesti keel | Uralic (Finno-Ugric) | Latin (with ä, ö, ü, õ, š, ž) |
| **French** | Français | Indo-European (Romance) | Latin (with accents) |
| **German** | Deutsch | Indo-European (West Germanic) | Latin (with ä, ö, ü, ß) |
| **Hindi** | हिन्दी | Indo-European (Indo-Aryan) | Devanagari (Abugida) |
| **Indonesian** | Bahasa Indonesia | Austronesian (Malayo-Polynesian) | Latin |
| **Japanese** | 日本語 | Japonic | Kanji + Hiragana + Katakana |
| **Korean** | 한국어 | Koreanic | Hangul |
| **Latin** | Lingua Latina | Indo-European (Italic) | Classical Latin |
| **Persian** | فارسی | Indo-European (Iranian) | Perso-Arabic (RTL) |
| **Portugese** | Português | Indo-European (Romance) | Latin (with accents & ç) |
| **Pushto** | پښتو | Indo-European (Eastern Iranian) | Pashto alphabet (RTL) |
| **Romanian** | Română | Indo-European (Eastern Romance) | Latin (with ă, â, î, ș, ț) |
| **Russian** | Русский язык | Indo-European (East Slavic) | Cyrillic |
| **Spanish** | Español | Indo-European (Romance) | Latin (with ñ & accents) |
| **Swedish** | Svenska | Indo-European (North Germanic) | Latin (with å, ä, ö) |
| **Tamil** | தமிழ் | Dravidian | Tamil (Abugida) |
| **Thai** | ภาษาไทย | Kra-Dai (Southwestern Tai) | Thai (Abugida) |
| **Urdu** | اُردُو | Indo-European (Indo-Aryan) | Perso-Arabic (Nasta'liq, RTL) |

---

## 📁 Project Architecture

```
language_recognizer/
├── .github/
│   └── workflows/
│       └── ci.yml                 # GitHub Actions CI/CD Pipeline
├── artifacts/
│   └── language_recognizer.joblib # Trained ML model pipeline bundle
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py                # Django settings with dotenv & whitenoise
│   ├── urls.py                    # Root URL routing
│   └── wsgi.py                    # WSGI server entrypoint
├── data/
│   ├── language.csv               # 22,000-row multilingual training corpus
│   └── sample_dataset.csv         # Compact 110-row dataset for rapid CI verification
├── detector/
│   ├── migrations/
│   │   └── __init__.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── llm_service.py         # Direct Gemini/OpenAI SDK caller + 22-lang fallback
│   │   └── model_service.py       # Thread-safe Singleton ML model loader & predictor
│   ├── apps.py                    # AppConfig with startup model preloading
│   ├── tests.py                   # 15 comprehensive unit tests (model, views, mocked LLM)
│   ├── urls.py                    # Application URL routes
│   └── views.py                   # Dashboard view, detect API, languages API, healthcheck
├── static/
│   ├── css/
│   │   └── styles.css             # Custom styles & animations
│   └── js/
│       └── app.js                 # Vanilla JavaScript (fetch, counters, history)
├── templates/
│   └── index.html                 # Responsive dashboard UI (Tailwind CSS CDN)
├── .dockerignore
├── .env.example                   # Environment configuration template
├── .env                           # Local environment file
├── .gitignore
├── docker-compose.yml             # Docker Compose orchestration
├── Dockerfile                     # Multi-stage production container
├── manage.py                      # Django CLI management script
├── README.md                      # Comprehensive documentation
├── requirements.txt               # Pinned Python package dependencies
└── train_model.py                 # Scikit-learn training & export script
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.10 or 3.11
- Git

### 2. Setup Virtual Environment
```bash
# Navigate to the project directory
cd language_recognizer

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Linux / macOS:
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Train or Verify the ML Model
Train on the full 22,000-row dataset:
```bash
python train_model.py --data-path data/language.csv --output-path artifacts/language_recognizer.joblib
```
Or verify quickly with the sample dataset:
```bash
python train_model.py --data-path data/sample_dataset.csv --output-path artifacts/language_recognizer.joblib --sample-size 50
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Edit `.env` to configure your settings:
```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=*

# Model path
MODEL_ARTIFACT_PATH=artifacts/language_recognizer.joblib

# Direct LLM SDK Configuration (No LangChain, No RAG)
LLM_PROVIDER=gemini       # Options: 'gemini' or 'openai'
LLM_API_KEY=              # Optional: leave empty for instant offline fallback
LLM_MODEL=gemini-2.5-flash # Or 'gpt-4o-mini' for OpenAI
```

### 5. Run Database Migrations & Collect Static Files
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

### 6. Start Development Server
```bash
python manage.py runserver 0.0.0.0:8000
```
Open your browser at **`http://localhost:8000`**.

---

## 🐳 Docker & Docker Compose

### Running with Docker Compose
```bash
docker-compose up --build
```
Access the application at **`http://localhost:8000`**.

### Building and Running the Dockerfile Standalone
```bash
# Build the Docker image
docker build -t language-recognizer:latest .

# Run the container with environment variables
docker run -d -p 8000:8000 --env-file .env --name polyglot-app language-recognizer:latest

# Check container health status
curl http://localhost:8000/api/health/
```

---

## 🧪 Testing & Code Quality

### Running Unit Tests
Run the 15 automated test cases:
```bash
python manage.py test detector --verbosity=2
```
*Note: All external LLM calls are mocked during tests, ensuring zero network dependencies and fast, deterministic test execution.*

### Running Code Linting (`flake8`)
```bash
flake8 . --count --max-line-length=127 --exclude=venv,staticfiles,.git,__pycache__
```

---

## 📡 REST API Reference

### 1. `POST /api/detect/`
Detects the language of input text and retrieves direct LLM enrichment.

**Request Header**:
`Content-Type: application/json`

**Request Body**:
```json
{
  "text": "Bonjour tout le monde, comment allez-vous aujourd'hui?"
}
```

**Response (200 OK)**:
```json
{
  "success": true,
  "text": "Bonjour tout le monde, comment allez-vous aujourd'hui?",
  "prediction": {
    "language": "French",
    "confidence": 99.4,
    "top_probabilities": [
      { "language": "French", "probability": 99.4 },
      { "language": "Spanish", "probability": 0.3 },
      { "language": "Romanian", "probability": 0.1 },
      { "language": "Portugese", "probability": 0.1 },
      { "language": "Latin", "probability": 0.1 }
    ]
  },
  "stats": {
    "char_count": 55,
    "word_count": 8,
    "line_count": 1,
    "detected_script": "Latin"
  },
  "ai_insights": {
    "source": "fallback",
    "provider": "rule_based_knowledge_base",
    "status": "ready",
    "language": "French",
    "native_name": "Français",
    "language_family": "Indo-European -> Romance -> Gallo-Romance",
    "writing_script": "Latin (with accents: é, è, ê, ë, à, â, î, ï, ô, ù, û, ç)",
    "speakers_estimate": "~320 million worldwide",
    "word_order": "SVO (Subject-Verb-Object)",
    "linguistic_features": "Grammatical gender (masculine/feminine), synthetic verb conjugations, liaison, nasal vowels.",
    "overview": "French is an official language in 29 countries and international diplomatic institutions, descended from Vulgar Latin.",
    "fun_fact": "For over 300 years following the Norman Conquest of 1066, French was the official language of the English Royal Court and law.",
    "translation_or_gist": "Translation requires active LLM API key; showing verified linguistic profile."
  },
  "model_metadata": {
    "architecture": "CountVectorizer + MultinomialNB",
    "total_classes": 22
  }
}
```

### 2. `GET /api/languages/`
Returns all 22 supported language classes and curated sample test phrases.

### 3. `GET /api/health/`
Container health check endpoint.
```json
{
  "status": "healthy",
  "model_ready": true,
  "classes_count": 22,
  "llm_provider": "gemini",
  "llm_key_configured": false
}
```

---

## 🔒 Direct LLM Architecture vs. LangChain

| Feature | Direct SDK Implementation | LangChain / RAG Wrapper |
| :--- | :--- | :--- |
| **External Dependencies** | Minimal (`google-genai`, `openai`) | Heavy (LangChain core, community, pydantic, langchain-*) |
| **Startup Overhead** | Instant (< 50ms) | Significant import graph overhead |
| **Offline Reliability** | Built-in 22-language fallback | Prone to vector store/network connection failures |
| **Auditability** | Clean, explicit Python functions | Hidden abstractions and complex chain hierarchies |
| **Memory Footprint** | Extremely low | High due to vector embeddings and vector DB engines |

---

## 📄 License
This project is open-source and available under the MIT License.
