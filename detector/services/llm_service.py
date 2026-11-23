"""
Direct LLM Service (No LangChain, No RAG).
Calls official Python SDKs directly (google-genai or openai).
Includes a comprehensive rule/template fallback covering all 22 supported languages
when LLM_API_KEY is not set or network/API calls fail.
"""

import json
import logging
import re
from typing import Any, Dict, Optional

from django.conf import settings

from .lexicon import lookup_romanized

logger = logging.getLogger("llm_service")

# Curated linguistic profiles for all 22 languages from the dataset
FALLBACK_LINGUISTIC_PROFILES: Dict[str, Dict[str, Any]] = {
    "English": {
        "native_name": "English",
        "family": "Indo-European -> Germanic -> West Germanic",
        "script": "Latin (26 letters)",
        "speakers": "~1.5 billion (native & L2)",
        "word_order": "SVO (Subject-Verb-Object)",
        "features": "Non-tonal, minimal inflectional morphology, analytic grammar, highly expansive vocabulary.",
        "overview": (
            "English is a global lingua franca belonging to the West Germanic branch, "
            "heavily influenced by Old Norse, Anglo-Norman French, and Latin."
        ),
        "fun_fact": "Nearly 30% of English words have French roots, and another 30% are directly derived from Latin.",
    },
    "French": {
        "native_name": "Français",
        "family": "Indo-European -> Romance -> Gallo-Romance",
        "script": "Latin (with accents: é, è, ê, ë, à, â, î, ï, ô, ù, û, ç)",
        "speakers": "~320 million worldwide",
        "word_order": "SVO (Subject-Verb-Object)",
        "features": "Grammatical gender (masculine/feminine), synthetic verb conjugations, liaison, nasal vowels.",
        "overview": (
            "French is an official language in 29 countries and international diplomatic institutions, "
            "descended from Vulgar Latin."
        ),
        "fun_fact": (
            "For over 300 years following the Norman Conquest of 1066, French was the official language "
            "of the English Royal Court and law."
        ),
    },
    "Spanish": {
        "native_name": "Español (Castellano)",
        "family": "Indo-European -> Romance -> Ibero-Romance",
        "script": "Latin (with ñ and accented vowels: á, é, í, ó, ú)",
        "speakers": "~590 million worldwide",
        "word_order": "SVO (Flexible, pro-drop)",
        "features": "Two grammatical genders, subjunctive mood, rich verb conjugations, phonetic orthography.",
        "overview": (
            "Spanish is the second most spoken native language globally, originating in the Iberian Peninsula "
            "and widespread across Latin America."
        ),
        "fun_fact": (
            "Spanish contains approximately 4,000 words of Arabic origin due to eight centuries of Moorish presence "
            "in Iberia (e.g. azúcar, ojalá, almohada)."
        ),
    },
    "German": {
        "native_name": "Deutsch",
        "family": "Indo-European -> Germanic -> West Germanic",
        "script": "Latin (including ä, ö, ü and ß)",
        "speakers": "~130 million worldwide",
        "word_order": "V2 in main clauses, SOV in subordinate clauses",
        "features": (
            "Three grammatical genders (der, die, das), four grammatical cases "
            "(Nominative, Accusative, Dative, Genitive), compound nouns."
        ),
        "overview": (
            "German is the most widely spoken native language in the European Union, "
            "renowned for precise terminology and compound word formation."
        ),
        "fun_fact": "All nouns in German are capitalized, regardless of whether they are proper or common nouns.",
    },
    "Dutch": {
        "native_name": "Nederlands",
        "family": "Indo-European -> Germanic -> West Germanic",
        "script": "Latin (digraph 'ij' treated as a single letter in some contexts)",
        "speakers": "~25 million worldwide",
        "word_order": "V2 in main clauses, SOV in subordinate clauses",
        "features": "Two genders (common and neuter), extensive compounding, guttural fricative sounds.",
        "overview": (
            "Dutch occupies a linguistic bridge between English and German, spoken primarily in the Netherlands, "
            "Flanders (Belgium), and Suriname."
        ),
        "fun_fact": "Afrikaans, spoken in South Africa and Namibia, evolved directly from 17th-century Dutch dialects.",
    },
    "Russian": {
        "native_name": "Русский язык",
        "family": "Indo-European -> Slavic -> East Slavic",
        "script": "Cyrillic (33 letters)",
        "speakers": "~255 million worldwide",
        "word_order": "SVO (Highly flexible due to extensive case endings)",
        "features": (
            "Six grammatical cases, three genders, grammatical verbal aspect (imperfective/perfective), "
            "palatalized consonants."
        ),
        "overview": (
            "Russian is the most geographically widespread language of Eurasia and the largest native language "
            "in Europe."
        ),
        "fun_fact": (
            "Russian cosmonauts and international astronauts aboard the International Space Station must be fluent "
            "in Russian to operate the Soyuz spacecraft."
        ),
    },
    "Hindi": {
        "native_name": "हिन्दी",
        "family": "Indo-European -> Indo-Iranian -> Indo-Aryan",
        "script": "Devanagari (Abugida, left-to-right)",
        "speakers": "~600 million speakers",
        "word_order": "SOV (Subject-Object-Verb)",
        "features": "Split ergativity, two grammatical genders, postpositions, rich retroflex consonant inventory.",
        "overview": (
            "Hindi is an official language of the Government of India, sharing a common colloquial base with Urdu "
            "known historically as Hindustani."
        ),
        "fun_fact": (
            "In Devanagari script, characters hang downwards from a continuous horizontal line known as the "
            "'shirorekha'."
        ),
    },
    "Arabic": {
        "native_name": "العَرَبِيَّة",
        "family": "Afroasiatic -> Semitic -> Central Semitic",
        "script": "Arabic script (Abjad, written right-to-left)",
        "speakers": "~420 million worldwide",
        "word_order": "VSO in Classical / Modern Standard Arabic; SVO in many dialects",
        "features": (
            "Root-and-pattern (triconsonantal root) morphology, grammatical dual number, "
            "pharyngeal and emphatic consonants."
        ),
        "overview": (
            "Arabic is a liturgical language of Islam and an official UN language, exhibiting rich diglossia "
            "between Modern Standard Arabic and regional dialects."
        ),
        "fun_fact": (
            "Virtually every Arabic word is derived from a 3-letter (triconsonantal) root conveying a fundamental "
            "semantic concept (e.g. K-T-B relates to writing)."
        ),
    },
    "Chinese": {
        "native_name": "中文 (汉语)",
        "family": "Sino-Tibetan -> Sinitic",
        "script": "Chinese Characters (Simplified / Traditional Hanzi)",
        "speakers": "~1.3 billion worldwide",
        "word_order": "SVO (Subject-Verb-Object, topic-prominent)",
        "features": (
            "Tonal language (4 main tones in Standard Mandarin), isolating/analytic grammar, classifier (measure) words, "
            "no noun declensions or verb tenses."
        ),
        "overview": (
            "Chinese encompasses a family of related varieties, with Standard Mandarin being the national lingua franca "
            "of China, Taiwan, and Singapore."
        ),
        "fun_fact": (
            "Chinese characters constitute one of the oldest continuously used systems of writing in human history, "
            "dating back over 3,000 years to oracle bone inscriptions."
        ),
    },
    "Japanese": {
        "native_name": "日本語 (Nihongo)",
        "family": "Japonic",
        "script": "Mixed: Kanji (logograms), Hiragana (syllabary), and Katakana (syllabary for loanwords)",
        "speakers": "~125 million worldwide",
        "word_order": "SOV (Subject-Object-Verb)",
        "features": "Agglutinative morphology, complex honorific hierarchy (keigo), mora-timed rhythm, pitch accent.",
        "overview": (
            "Japanese is spoken almost exclusively in Japan, characterized by a unique combination of three concurrent "
            "writing scripts and intricate grammatical honorifics."
        ),
        "fun_fact": (
            "Written Japanese uses no spaces between words; readers differentiate boundaries by switching between "
            "Kanji, Hiragana, and Katakana scripts."
        ),
    },
    "Korean": {
        "native_name": "한국어 (Hangugeo)",
        "family": "Koreanic (Language isolate or Altaic hypothesis)",
        "script": "Hangul (featural alphabet organized into syllabic blocks)",
        "speakers": "~80 million worldwide",
        "word_order": "SOV (Subject-Object-Verb)",
        "features": "Agglutinative morphology, subject-honorific system, postpositions, vowel harmony remnants.",
        "overview": (
            "Korean is spoken in North and South Korea and significant diaspora communities, celebrated for "
            "King Sejong's brilliant 15th-century creation of Hangul."
        ),
        "fun_fact": (
            "Hangul letters were scientifically shaped to mimic the anatomical positions of the tongue, teeth, "
            "lips, and throat when producing each sound."
        ),
    },
    "Turkish": {
        "native_name": "Türkçe",
        "family": "Turkic -> Oghuz",
        "script": "Latin (adopted in 1928, includes ç, ğ, ı, ö, ş, ü)",
        "speakers": "~88 million worldwide",
        "word_order": "SOV (Subject-Object-Verb)",
        "features": "Extensive agglutinative suffixing, strict vowel harmony, no grammatical gender.",
        "overview": (
            "Turkish is the most widely spoken Turkic language, standardized during the 1920s reforms under "
            "Mustafa Kemal Atatürk."
        ),
        "fun_fact": (
            "Because Turkish is intensely agglutinative, long words can express entire sentences "
            "(e.g. 'Muvaffakiyetsizleştiricilerindenmişsinizcesine')."
        ),
    },
    "Thai": {
        "native_name": "ภาษาไทย (Phasa Thai)",
        "family": "Kra-Dai -> Southwestern Tai",
        "script": "Thai script (Abugida, 44 consonants, 15 vowel symbols, 4 tone marks)",
        "speakers": "~60 million worldwide",
        "word_order": "SVO (Subject-Verb-Object)",
        "features": (
            "Five distinct phonemic tones (low, mid, high, falling, rising), isolating analytic grammar, "
            "lack of inflection."
        ),
        "overview": (
            "Thai is the national language of Thailand, historically influenced by Sanskrit, Pali, and Old Khmer."
        ),
        "fun_fact": (
            "Traditional Thai text contains no punctuation and no spaces between words; spaces serve only as "
            "punctuation to denote clause breaks or sentences."
        ),
    },
    "Tamil": {
        "native_name": "தமிழ் (Tamiḻ)",
        "family": "Dravidian -> South Dravidian",
        "script": "Tamil script (Abugida, 12 vowels, 18 consonants, 1 special letter)",
        "speakers": "~85 million worldwide",
        "word_order": "SOV (Subject-Object-Verb)",
        "features": (
            "Agglutinative grammar, diglossia between formal and spoken forms, retroflex consonants, "
            "classical literary antiquity."
        ),
        "overview": (
            "Tamil is one of the world's longest-surviving classical languages, spoken in Tamil Nadu (India), "
            "Sri Lanka, Singapore, and Malaysia."
        ),
        "fun_fact": (
            "With documented literary works dating back over 2,500 years to the Sangam era, Tamil is recognized "
            "as one of the oldest living classical languages in existence."
        ),
    },
    "Indonesian": {
        "native_name": "Bahasa Indonesia",
        "family": "Austronesian -> Malayo-Polynesian",
        "script": "Latin (26 letters, fully phonetic)",
        "speakers": "~200 million (primarily as a unifying national L2)",
        "word_order": "SVO (Subject-Verb-Object)",
        "features": (
            "Agglutinative prefix/suffix system, no grammatical gender, no grammatical tense "
            "(uses temporal adverbs), reduplication for plurals."
        ),
        "overview": (
            "Indonesian is a standardized register of Malay adopted in 1945 to unite the multilingual archipelago "
            "of Indonesia's 17,000 islands."
        ),
        "fun_fact": (
            "To make a noun plural in Indonesian, you simply repeat the word (e.g. 'anak' = child, 'anak-anak' = children)."
        ),
    },
    "Portugese": {
        "native_name": "Português",
        "family": "Indo-European -> Romance -> Ibero-Romance",
        "script": "Latin (with ç, ã, õ, and accent marks: á, é, í, ó, ú, â, ê, ô, à)",
        "speakers": "~260 million worldwide",
        "word_order": "SVO (Subject-Verb-Object)",
        "features": (
            "Two grammatical genders, nasal vowels, personal infinitive mood, distinct European and Brazilian dialects."
        ),
        "overview": (
            "Portuguese is the principal language of Portugal and Brazil, and an official language across Angola, "
            "Mozambique, and Cape Verde."
        ),
        "fun_fact": (
            "Portuguese is one of the rare European languages to possess a 'personal infinitive', allowing the "
            "infinitive verb form to be conjugated for person and number."
        ),
    },
    "Portuguese": {
        "native_name": "Português",
        "family": "Indo-European -> Romance -> Ibero-Romance",
        "script": "Latin (with ç, ã, õ, and accent marks)",
        "speakers": "~260 million worldwide",
        "word_order": "SVO (Subject-Verb-Object)",
        "features": "Two grammatical genders, nasal vowels, personal infinitive mood.",
        "overview": "Portuguese is the principal language of Portugal and Brazil, spoken across 4 continents.",
        "fun_fact": "Over 80% of Portuguese speakers reside in Brazil.",
    },
    "Romanian": {
        "native_name": "Română",
        "family": "Indo-European -> Romance -> Eastern Romance",
        "script": "Latin (with special characters: ă, â, î, ș, ț)",
        "speakers": "~25 million worldwide",
        "word_order": "SVO (Subject-Verb-Object)",
        "features": (
            "Preserves Latin grammatical cases (Nominative/Accusative and Genitive/Dative), postfixed definite "
            "articles (e.g. om = man, omul = the man), three genders."
        ),
        "overview": (
            "Romanian is the only principal Eastern Romance language to survive into modern times, surrounded "
            "predominantly by Slavic-speaking neighbors."
        ),
        "fun_fact": (
            "Unlike Western Romance languages, Romanian appends the definite article to the END of nouns rather than "
            "placing it before (e.g. 'lup' -> 'lupul')."
        ),
    },
    "Estonian": {
        "native_name": "Eesti keel",
        "family": "Uralic -> Finno-Ugric -> Finnic",
        "script": "Latin (with ä, ö, ü, õ, š, ž)",
        "speakers": "~1.2 million worldwide",
        "word_order": "SVO (Flexible with V2 tendencies)",
        "features": (
            "14 grammatical noun cases, no future tense, no grammatical gender, three distinct phonemic vowel "
            "and consonant lengths (short, long, overlong)."
        ),
        "overview": (
            "Estonian is closely related to Finnish and distantly to Hungarian, belonging to the non-Indo-European "
            "Uralic language family."
        ),
        "fun_fact": (
            "Estonian has three distinct lengths of vowels and consonants: short, long, and overlong, where changing "
            "the duration completely alters the meaning of a word."
        ),
    },
    "Swedish": {
        "native_name": "Svenska",
        "family": "Indo-European -> Germanic -> North Germanic",
        "script": "Latin (with å, ä, ö)",
        "speakers": "~10 million worldwide",
        "word_order": "V2 (Verb-second in main clauses)",
        "features": (
            "Pitch accent (tonal word accent distinguishing minimal pairs), two grammatical genders (en / ett), "
            "postfixed definite articles."
        ),
        "overview": (
            "Swedish is a North Germanic Scandinavian language spoken in Sweden and parts of Finland, mutually "
            "intelligible to a high degree with Norwegian and Danish."
        ),
        "fun_fact": (
            "Swedish uses a pitch accent system where speaking a word with a different melodic musical contour "
            "changes its definition entirely (e.g. 'anden' meaning 'the duck' vs 'the spirit')."
        ),
    },
    "Latin": {
        "native_name": "Lingua Latina",
        "family": "Indo-European -> Italic -> Latino-Faliscan",
        "script": "Classical Latin alphabet (originally 23 letters, without J, U, W in Antiquity)",
        "speakers": "Scholarly, liturgical, and historical usage; official in the Holy See (Vatican City)",
        "word_order": "SOV (Classical literary), highly flexible in poetry and rhetoric",
        "features": (
            "Six grammatical cases (Nominative, Vocative, Accusative, Genitive, Dative, Ablative), "
            "three genders, synthetic verb conjugation system."
        ),
        "overview": (
            "Latin was the language of the Roman Republic and Empire, the direct ancestor of all modern Romance "
            "languages, and the foundational language of Western science, law, and medicine."
        ),
        "fun_fact": (
            "Latin continues to be used for the binomial nomenclature of every officially cataloged biological "
            "species on Earth."
        ),
    },
    "Urdu": {
        "native_name": "اُردُو",
        "family": "Indo-European -> Indo-Iranian -> Indo-Aryan",
        "script": "Perso-Arabic in Nasta'liq calligraphic style (right-to-left)",
        "speakers": "~230 million worldwide",
        "word_order": "SOV (Subject-Object-Verb)",
        "features": (
            "Mutual intelligibility with colloquial spoken Hindi, substantial Persian and Arabic literary vocabulary, "
            "polite honorific registers."
        ),
        "overview": (
            "Urdu is the national language and lingua franca of Pakistan and an officially recognized language "
            "of India, renowned for its rich poetry (Ghazals)."
        ),
        "fun_fact": (
            "Urdu is conventionally handwritten and typeset in the sweeping diagonal 'Nasta'liq' style, considered "
            "one of the most artistic calligraphic forms of the Arabic script."
        ),
    },
    "Persian": {
        "native_name": "فارسی (Fārsī)",
        "family": "Indo-European -> Indo-Iranian -> Iranian",
        "script": "Perso-Arabic script (32 letters, right-to-left)",
        "speakers": "~130 million worldwide (Farsi in Iran, Dari in Afghanistan, Tajik in Tajikistan)",
        "word_order": "SOV (Subject-Object-Verb)",
        "features": "No grammatical gender, agglutinative suffixing, enclitics, poetic ta'arof etiquette.",
        "overview": (
            "Persian is an ancient Indo-European language with an illustrious poetic tradition encompassing "
            "Hafez, Rumi, Saadi, and Ferdowsi."
        ),
        "fun_fact": (
            "Despite being written in Arabic script, Persian is structurally an Indo-European language, "
            "genealogically closer to English and French than to Arabic."
        ),
    },
    "Pushto": {
        "native_name": "پښتو (Pax̌tō / Pashto)",
        "family": "Indo-European -> Indo-Iranian -> Iranian -> Eastern Iranian",
        "script": "Pashto alphabet (modified Perso-Arabic with 44 letters)",
        "speakers": "~50 million across Afghanistan and Pakistan",
        "word_order": "SOV (Subject-Object-Verb)",
        "features": "Split ergativity in past tenses, two grammatical genders, complex retroflex phonology.",
        "overview": (
            "Pashto is one of the two official languages of Afghanistan, spoken natively by the Pashtun people."
        ),
        "fun_fact": (
            "The Pashto alphabet features distinct modified letters with ring diacritics (like ښ and ڼ) "
            "to represent retroflex sounds not found in Arabic or Persian."
        ),
    },
}


LANG_CODE_MAP: Dict[str, str] = {
    "English": "en", "French": "fr", "Spanish": "es", "German": "de",
    "Dutch": "nl", "Russian": "ru", "Hindi": "hi", "Arabic": "ar",
    "Japanese": "ja", "Chinese": "zh", "Korean": "ko", "Turkish": "tr",
    "Italian": "it", "Swedish": "sv", "Indonesian": "id", "Portuguese": "pt",
    "Portugese": "pt", "Romanian": "ro", "Estonian": "et", "Latin": "la",
    "Tamil": "ta", "Urdu": "ur", "Persian": "fa", "Thai": "th",
}


def attempt_free_translation(text: str, source_lang: str) -> Optional[str]:
    """
    Attempts a fast free translation to English as an offline/no-key fallback.
    Fails quickly and silently without raising exceptions.
    """
    if not text or not text.strip():
        return None
    try:
        import urllib.parse
        import urllib.request
        sl = LANG_CODE_MAP.get(source_lang, "auto")
        clean = text.strip()[:300]
        encoded = urllib.parse.quote(clean)
        url = f"https://api.mymemory.translated.net/get?q={encoded}&langpair={sl}|en"
        req = urllib.request.Request(url, headers={"User-Agent": "PolyGlot/1.0"})
        with urllib.request.urlopen(req, timeout=2.5) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
            translated = payload.get("responseData", {}).get("translatedText", "")
            if translated and translated.strip() and "MYMEMORY" not in translated.upper():
                return translated.strip()
    except Exception:
        pass
    return None


class DirectLLMService:
    """
    Direct LLM caller using official Python SDKs (google-genai or openai).
    No LangChain, No RAG, No vector stores.
    """

    def __init__(self, api_key: Optional[str] = None, provider: Optional[str] = None):
        self.provider = (provider or getattr(settings, "LLM_PROVIDER", "gemini")).lower()
        self.api_key = (api_key if api_key is not None else getattr(settings, "LLM_API_KEY", "")).strip()
        self.model_name = getattr(settings, "LLM_MODEL", "gemini-2.5-flash").strip()

    def get_fallback_profile(self, language: str, text: str, reason: str = "") -> Dict[str, Any]:
        """
        Returns rich curated linguistic knowledge and translations when LLM API key is absent.
        """
        lex_match = lookup_romanized(text)
        target_lang = lex_match["language"] if lex_match else language

        profile = None
        for key, val in FALLBACK_LINGUISTIC_PROFILES.items():
            if key.lower() == target_lang.lower():
                profile = val.copy()
                break

        if not profile:
            profile = {
                "native_name": target_lang,
                "family": "Natural Human Language",
                "script": "Standard Orthography",
                "speakers": "Global Community",
                "word_order": "Variable / Canonical",
                "features": "Standard phonological and morphosyntactic inventory.",
                "overview": f"{target_lang} is a recognized world language detected by the classifier.",
                "fun_fact": f"{target_lang} possesses distinct orthographic and phonetic patterns.",
            }

        # Always use the language's own autonym (e.g. "Français") — not the word's native script
        native_name = profile.get("native_name", target_lang)

        if lex_match:
            translation = lex_match["meaning"]
            overview = lex_match["explanation"]
            word_native_script = lex_match["native"]
        elif target_lang.lower() == "english":
            # For English sentences, the translation is the text itself
            translation = text.strip()
            overview = f"English sentence: \"{text.strip()}\". {profile.get('overview', '')}"
            word_native_script = text.strip()
        else:
            # For non-English sentences, try auto-translation fallback
            auto_trans = attempt_free_translation(text, target_lang)
            if auto_trans:
                translation = auto_trans
                overview = f"Translated: \"{auto_trans}\". {profile.get('overview', '')}"
                word_native_script = text.strip()
            else:
                translation = f"Sample in {target_lang}: \"{text.strip()[:60]}\""
                overview = profile.get("overview", "")
                word_native_script = ""

        return {
            "source": "fallback",
            "provider": "rule_based_knowledge_base",
            "status": "ready",
            "reason": reason or "Running in offline/curated mode (no external LLM key required).",
            "language": target_lang,
            "native_name": native_name,
            "word_native_script": word_native_script,
            "language_family": profile.get("family", "Unknown"),
            "writing_script": profile.get("script", "Unknown"),
            "speakers_estimate": profile.get("speakers", "Unknown"),
            "word_order": profile.get("word_order", "SVO"),
            "linguistic_features": profile.get("features", ""),
            "overview": overview,
            "fun_fact": profile.get("fun_fact", ""),
            "translation_or_gist": translation,
            "meaning": translation,
        }

    def call_gemini(self, language: str, text: str) -> Dict[str, Any]:
        """
        Calls official Google GenAI SDK (google-genai) directly.
        """
        from google import genai

        client = genai.Client(api_key=self.api_key)
        prompt = (
            f"You are an expert computational linguist and translator. The user provided this sample text snippet:\n"
            f"\"\"\"{text[:600]}\"\"\"\n\n"
            f"The ML classifier detected the language as: '{language}'.\n\n"
            f"Please respond in valid JSON format ONLY, with the following exact keys:\n"
            f"1. 'language_family': Linguistic branch (e.g. 'Indo-European -> Romance')\n"
            f"2. 'writing_script': Script name and brief note\n"
            f"3. 'native_name': Autonym/native name of the language (e.g. 'Français')\n"
            f"4. 'linguistic_overview': 2-3 concise sentences on classification, origin, and spread.\n"
            f"5. 'grammatical_traits': 1-2 key structural traits.\n"
            f"6. 'translation_or_gist': Precise English translation and full meaning of the user's snippet.\n"
            f"7. 'fun_fact': One engaging, true linguistic trivia fact about this language.\n\n"
            f"Return pure JSON without markdown code fences or backticks."
        )

        candidate_models = [self.model_name, "gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
        seen = set()
        models_to_try = [m for m in candidate_models if m and not (m in seen or seen.add(m))]

        last_exc = None
        for model in models_to_try:
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                )
                raw_text = response.text or ""
                return self._parse_llm_json(raw_text, language, text, provider_name="Google Gemini")
            except Exception as exc:
                last_exc = exc
                continue

        if last_exc:
            raise last_exc
        return self.get_fallback_profile(language, text, reason="Gemini models could not be reached.")

    def call_openai(self, language: str, text: str) -> Dict[str, Any]:
        """
        Calls official OpenAI SDK directly.
        """
        from openai import OpenAI

        client = OpenAI(api_key=self.api_key)
        prompt = (
            f"You are an expert computational linguist. The user provided this sample text snippet:\n"
            f"\"\"\"{text[:400]}\"\"\"\n\n"
            f"The ML classifier detected the language as: '{language}'.\n\n"
            f"Respond in valid JSON format ONLY with keys:\n"
            f"'language_family', 'writing_script', 'native_name', 'linguistic_overview', "
            f"'grammatical_traits', 'translation_or_gist', 'fun_fact'.\n"
            f"Return pure JSON without markdown backticks."
        )

        model = self.model_name or "gpt-4o-mini"
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a professional linguistic analysis engine. Output valid JSON."},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
        )

        raw_text = completion.choices[0].message.content or ""
        return self._parse_llm_json(raw_text, language, text, provider_name="OpenAI")

    def _parse_llm_json(
        self, raw_text: str, language: str, text: str, provider_name: str
    ) -> Dict[str, Any]:
        """
        Cleans and parses JSON output from LLM, falling back cleanly if JSON is invalid.
        """
        clean = raw_text.strip()
        if clean.startswith("```"):
            clean = re.sub(r"^```(?:json)?\s*", "", clean)
            clean = re.sub(r"\s*```$", "", clean)

        try:
            data = json.loads(clean)
            return {
                "source": "llm",
                "provider": provider_name,
                "model": self.model_name,
                "language": language,
                "native_name": data.get("native_name", language),
                "language_family": data.get("language_family", "Unknown"),
                "writing_script": data.get("writing_script", "Standard script"),
                "linguistic_features": data.get("grammatical_traits", ""),
                "overview": data.get("linguistic_overview", ""),
                "translation_or_gist": data.get("translation_or_gist", ""),
                "fun_fact": data.get("fun_fact", ""),
                "status": "success",
            }
        except Exception as exc:
            logger.warning("Failed to parse LLM JSON response: %s. Raw: %s", exc, raw_text[:200])
            fallback = self.get_fallback_profile(language, text, reason="LLM output formatting issue; loaded profile.")
            fallback["source"] = "llm_raw_fallback"
            fallback["raw_llm_text"] = raw_text
            return fallback

    def get_enrichment(self, language: str, text: str) -> Dict[str, Any]:
        """
        Main entry point for enriching a language detection result.
        Returns live LLM insights if configured, otherwise falls back gracefully.
        """
        if not self.api_key:
            return self.get_fallback_profile(
                language=language,
                text=text,
                reason="No LLM_API_KEY configured in environment. Using verified linguistic profile.",
            )

        provider = self.provider.lower()

        try:
            logger.info("Calling direct LLM SDK (%s / model: %s)...", provider, self.model_name)
            if provider in ("gemini", "google"):
                return self.call_gemini(language, text)
            elif provider in ("openai", "chatgpt"):
                return self.call_openai(language, text)
            else:
                return self.get_fallback_profile(
                    language=language,
                    text=text,
                    reason=f"Unsupported LLM_PROVIDER '{self.provider}'. Supported: gemini, openai.",
                )
        except Exception as exc:
            logger.error("Direct LLM call failed: %s. Falling back to local linguistic knowledge.", exc)
            return self.get_fallback_profile(
                language=language,
                text=text,
                reason=f"LLM API call error ({type(exc).__name__}). Offline fallback activated.",
            )
