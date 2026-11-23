"""
Views for Language Recognizer Web Application.
Provides index dashboard rendering, JSON API endpoints for prediction,
sample languages, and health checks.
"""

import json
import logging
from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST

from .services.llm_service import DirectLLMService, FALLBACK_LINGUISTIC_PROFILES
from .services.model_service import LanguageModelService

logger = logging.getLogger("detector.views")

# Curated sample phrases for the UI sample chips
SAMPLE_PHRASES = [
    {
        "language": "English",
        "label": "English",
        "flag": "🇬🇧",
        "text": "The quick brown fox jumps over the lazy dog in the sunny afternoon.",
    },
    {
        "language": "French",
        "label": "Français",
        "flag": "🇫🇷",
        "text": "Bonjour tout le monde, j'espère que vous passez une merveilleuse journée ensoleillée.",
    },
    {
        "language": "Spanish",
        "label": "Español",
        "flag": "🇪🇸",
        "text": "Hola amigo, ¿cómo estás hoy? La inteligencia artificial está transformando nuestro mundo.",
    },
    {
        "language": "German",
        "label": "Deutsch",
        "flag": "🇩🇪",
        "text": "Guten Tag, das Wetter heute ist wirklich herrlich und die Natur erwacht zum Leben.",
    },
    {
        "language": "Dutch",
        "label": "Nederlands",
        "flag": "🇳🇱",
        "text": "Goedemiddag allemaal, welkom in Nederland en geniet van een heerlijke kop koffie.",
    },
    {
        "language": "Russian",
        "label": "Русский",
        "flag": "🇷🇺",
        "text": "Привет! Наука и технологии открывают удивительные горизонты для будущего человечества.",
    },
    {
        "language": "Hindi",
        "label": "हिन्दी",
        "flag": "🇮🇳",
        "text": "नमस्ते, भाषा पहचान प्रणाली कृत्रिम बुद्धिमत्ता और मशीन लर्निंग द्वारा संचालित है।",
    },
    {
        "language": "Arabic",
        "label": "العربية",
        "flag": "🇸🇦",
        "text": "مرحباً بك في تطبيق التعرف على اللغات الطبيعية باستخدام خوارزميات التعلم الآلي الحديثة.",
    },
    {
        "language": "Japanese",
        "label": "日本語",
        "flag": "🇯🇵",
        "text": "エノが行きがかりでバスに乗ってしまい、気分が悪くなった際に助けるが、今すぐバスを降りたいと運転手に頼む際、本当のことを言ってしまうと彼女が恥ずかしい思いをすると察した。",
    },
    {
        "language": "Chinese",
        "label": "中文",
        "flag": "🇨🇳",
        "text": "胡赛尼本人和小说的主人公阿米尔一样，都是出生在阿富汗首都喀布尔，少年时代便离开了这个国家。胡赛尼直到年小说出版之后才首次回到已经离开年的祖国。",
    },
    {
        "language": "Korean",
        "label": "한국어",
        "flag": "🇰🇷",
        "text": "안녕하세요! 자연어 처리와 인공지능 기반 언어 인식 웹 애플리케이션에 오신 것을 환영합니다.",
    },
    {
        "language": "Turkish",
        "label": "Türkçe",
        "flag": "🇹🇷",
        "text": "Merhaba! Doğal dil işleme ve makine öğrenimi modelleri dünyayı birbirine yakınlaştırıyor.",
    },
    {
        "language": "Thai",
        "label": "ภาษาไทย",
        "flag": "🇹🇭",
        "text": "สวัสดีครับ ยินดีต้อนรับสู่ระบบตรวจจับภาษาด้วยการเรียนรู้ของเครื่องและปัญญาประดิษฐ์",
    },
    {
        "language": "Tamil",
        "label": "தமிழ்",
        "flag": "🇮🇳",
        "text": "வணக்கம்! இயற்கை மொழி செயலாக்கம் மற்றும் இயந்திர கற்றல் மூலம் மொழி அடையாளம் காணப்படுகிறது.",
    },
    {
        "language": "Latin",
        "label": "Latina",
        "flag": "🏛️",
        "text": "Omnia vincit amor et nos cedamus amori. Scientia potentia est in saecula saeculorum.",
    },
    {
        "language": "Indonesian",
        "label": "Bahasa Indonesia",
        "flag": "🇮🇩",
        "text": "Selamat datang di aplikasi pengenal bahasa berbasis kecerdasan buatan dan pembelajaran mesin.",
    },
    {
        "language": "Portugese",
        "label": "Português",
        "flag": "🇵🇹",
        "text": "Olá a todos! Esta aplicação combina modelos estatísticos com inteligência artificial generativa.",
    },
    {
        "language": "Romanian",
        "label": "Română",
        "flag": "🇷🇴",
        "text": "Bună ziua tuturor! Limba română este o limbă romanică orientală cu o istorie fascinantă.",
    },
    {
        "language": "Estonian",
        "label": "Eesti",
        "flag": "🇪🇪",
        "text": "Tere päevast! Masinõppel põhinev keeletuvastuse rakendus töötab kiiresti ja täpselt.",
    },
    {
        "language": "Swedish",
        "label": "Svenska",
        "flag": "🇸🇪",
        "text": "Hej och välkommen till ett modernt verktyg för språkkonstatering och lingvistisk analys.",
    },
    {
        "language": "Urdu",
        "label": "اُردُو",
        "flag": "🇵🇰",
        "text": "خوش آمدید! قدرتی زبان کی شناخت اور جدید لسانی بصیرت کا جامع اور خودکار نظام۔",
    },
    {
        "language": "Persian",
        "label": "فارسی",
        "flag": "🇮🇷",
        "text": "سلام و درود! زبان فارسی یکی از کهن‌ترین زبان‌های زنده جهان با پیشینه‌ای پرشکوه است.",
    },
]


@ensure_csrf_cookie
def index(request: HttpRequest) -> HttpResponse:
    """
    Renders the single-page application dashboard.
    """
    model_service = LanguageModelService.get_instance()
    info = model_service.get_info()

    context = {
        "model_ready": info["is_ready"],
        "languages_count": info["classes_count"] or 22,
        "supported_languages": info["classes"] or sorted(list(FALLBACK_LINGUISTIC_PROFILES.keys())),
        "sample_phrases": SAMPLE_PHRASES,
        "llm_provider": getattr(settings, "LLM_PROVIDER", "gemini"),
        "has_llm_key": bool(getattr(settings, "LLM_API_KEY", "")),
        "llm_model": getattr(settings, "LLM_MODEL", "gemini-2.5-flash"),
    }
    return render(request, "index.html", context)


@require_POST
def detect_api(request: HttpRequest) -> JsonResponse:
    """
    POST API endpoint to classify text language and retrieve direct LLM insights.
    Accepts JSON body `{"text": "..."}` or POST form data.
    """
    # Parse payload
    input_text = ""
    request_api_key = ""
    if request.content_type == "application/json":
        try:
            body = json.loads(request.body.decode("utf-8"))
            input_text = body.get("text", "")
            request_api_key = (
                body.get("api_key")
                or request.headers.get("X-LLM-API-Key")
                or getattr(settings, "LLM_API_KEY", "")
            )
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON format in request body."}, status=400)
    else:
        input_text = request.POST.get("text", "")
        request_api_key = (
            request.POST.get("api_key")
            or request.headers.get("X-LLM-API-Key")
            or getattr(settings, "LLM_API_KEY", "")
        )

    # Input validation
    if not input_text or not input_text.strip():
        return JsonResponse(
            {
                "success": False,
                "error": "Please provide some text to identify. Input cannot be empty or only whitespace.",
            },
            status=400,
        )

    clean_text = input_text.strip()
    if len(clean_text) > 15000:
        clean_text = clean_text[:15000]

    # Perform Machine Learning prediction
    try:
        model_service = LanguageModelService.get_instance()
        prediction_result = model_service.predict(clean_text)
    except Exception as exc:
        logger.error("ML prediction error: %s", exc, exc_info=True)
        return JsonResponse(
            {
                "success": False,
                "error": f"Model inference error: {str(exc)}",
            },
            status=500,
        )

    # Perform Direct LLM enrichment (with user key, environment key, or graceful fallback)
    predicted_language = prediction_result["predicted_language"]
    llm_service = DirectLLMService(api_key=request_api_key)
    ai_insights = llm_service.get_enrichment(language=predicted_language, text=clean_text)

    # Consolidate meaning and translation data
    meaning_data = prediction_result.get("meaning", {})
    if not meaning_data.get("translation") and ai_insights.get("translation_or_gist"):
        meaning_data["translation"] = ai_insights.get("translation_or_gist", "")
    if not meaning_data.get("native_script"):
        meaning_data["native_script"] = ai_insights.get("word_native_script") or ai_insights.get("native_name", "")
    if not meaning_data.get("explanation") or meaning_data.get("explanation", "").startswith("Statistical prediction"):
        if ai_insights.get("overview"):
            meaning_data["explanation"] = ai_insights.get("overview", "")

    response_payload = {
        "success": True,
        "text": clean_text,
        "prediction": {
            "language": predicted_language,
            "confidence": prediction_result["confidence"],
            "top_probabilities": prediction_result["top_probabilities"],
        },
        "meaning": meaning_data,
        "stats": prediction_result["stats"],
        "ai_insights": ai_insights,
        "model_metadata": prediction_result["model_metadata"],
    }
    return JsonResponse(response_payload)


@require_GET
def languages_api(request: HttpRequest) -> JsonResponse:
    """
    GET API endpoint returning supported languages and sample test phrases.
    """
    model_service = LanguageModelService.get_instance()
    info = model_service.get_info()

    return JsonResponse(
        {
            "success": True,
            "languages": info["classes"] or sorted(list(FALLBACK_LINGUISTIC_PROFILES.keys())),
            "total": info["classes_count"] or len(FALLBACK_LINGUISTIC_PROFILES),
            "samples": SAMPLE_PHRASES,
        }
    )


@require_GET
def health_check(request: HttpRequest) -> JsonResponse:
    """
    GET endpoint for container health probes and monitoring.
    """
    model_service = LanguageModelService.get_instance()
    info = model_service.get_info()

    return JsonResponse(
        {
            "status": "healthy" if info["is_ready"] else "degraded",
            "model_ready": info["is_ready"],
            "classes_count": info["classes_count"],
            "llm_provider": getattr(settings, "LLM_PROVIDER", "gemini"),
            "llm_key_configured": bool(getattr(settings, "LLM_API_KEY", "")),
        }
    )
