"""
Transliterated / Romanized Multi-Lingual Lexicon
Provides accurate language identification, native script representations,
and English translations for common romanized phrases, greetings, and loanwords.
"""

from typing import Any, Dict, Optional

ROMANIZED_LEXICON: Dict[str, Dict[str, Any]] = {
    # Japanese
    "sayonara": {
        "language": "Japanese",
        "native": "さようなら",
        "meaning": "Goodbye / Farewell",
        "explanation": (
            "'Sayonara' is a traditional Japanese farewell typically used when parting for an extended period, "
            "definitively, or on formal occasions."
        ),
    },
    "sayounara": {
        "language": "Japanese",
        "native": "さようなら",
        "meaning": "Goodbye / Farewell",
        "explanation": "'Sayounara' is the standard phonetic Hepburn romanization of the Japanese farewell さようなら.",
    },
    "konnichiwa": {
        "language": "Japanese",
        "native": "こんにちは",
        "meaning": "Hello / Good afternoon",
        "explanation": "'Konnichiwa' is the standard Japanese greeting used during the daytime from late morning until dusk.",
    },
    "konichiwa": {
        "language": "Japanese",
        "native": "こんにちは",
        "meaning": "Hello / Good afternoon",
        "explanation": "Common alternative spelling for 'Konnichiwa' (こんにちは).",
    },
    "arigato": {
        "language": "Japanese",
        "native": "ありがとう",
        "meaning": "Thank you",
        "explanation": "'Arigatō' is the casual Japanese way to express gratitude.",
    },
    "arigatou": {
        "language": "Japanese",
        "native": "ありがとう",
        "meaning": "Thank you",
        "explanation": "Phonetic spelling of 'Arigatō' (ありがとう).",
    },
    "arigato gozaimasu": {
        "language": "Japanese",
        "native": "ありがとうございます",
        "meaning": "Thank you very much (polite)",
        "explanation": "Polite and formal expression of gratitude in Japanese.",
    },
    "ohayo": {
        "language": "Japanese",
        "native": "おはよう",
        "meaning": "Good morning",
        "explanation": "Casual morning greeting used among friends and family in Japan.",
    },
    "ohayou": {
        "language": "Japanese",
        "native": "おはよう",
        "meaning": "Good morning",
        "explanation": "Standard romanization of おはよう.",
    },
    "ohayo gozaimasu": {
        "language": "Japanese",
        "native": "おはようございます",
        "meaning": "Good morning (polite)",
        "explanation": "Formal and respectful morning greeting in Japan.",
    },
    "oyasumi": {
        "language": "Japanese",
        "native": "おやすみ",
        "meaning": "Good night",
        "explanation": "Used before going to sleep or leaving someone late at night in Japan.",
    },
    "itadakimasu": {
        "language": "Japanese",
        "native": "いただきます",
        "meaning": "I humbly receive (said before eating)",
        "explanation": "A ritual phrase expressing gratitude to the ingredients, cook, and nature before beginning a meal.",
    },
    "gochisosama": {
        "language": "Japanese",
        "native": "ごちそうさまでした",
        "meaning": "Thank you for the delicious meal",
        "explanation": "Polite phrase uttered after finishing a meal in Japan.",
    },
    "sugoi": {
        "language": "Japanese",
        "native": "すごい",
        "meaning": "Amazing / Incredible / Great",
        "explanation": "Exclamation expressing admiration or astonishment in Japanese.",
    },
    "kawaii": {
        "language": "Japanese",
        "native": "かわいい",
        "meaning": "Cute / Adorable",
        "explanation": "Prominent cultural concept and adjective describing cuteness in Japanese.",
    },
    "sumimasen": {
        "language": "Japanese",
        "native": "すみません",
        "meaning": "Excuse me / I'm sorry / Thank you",
        "explanation": (
            "Versatile Japanese polite phrase used to apologize, get someone's attention, or express polite gratitude."
        ),
    },
    "gomen nasai": {
        "language": "Japanese",
        "native": "ごめんなさい",
        "meaning": "I am sorry / Forgive me",
        "explanation": "Direct and personal apology in Japanese.",
    },
    "senpai": {
        "language": "Japanese",
        "native": "先輩",
        "meaning": "Senior / Elder colleague or mentor",
        "explanation": "Honorific title for someone senior in rank, school, or experience.",
    },
    "sensei": {
        "language": "Japanese",
        "native": "先生",
        "meaning": "Teacher / Master / Doctor",
        "explanation": "Honorific title for teachers, doctors, lawyers, and masters of arts.",
    },
    "yamete": {
        "language": "Japanese",
        "native": "やめて",
        "meaning": "Stop it / Please stop",
        "explanation": "Imperative Japanese verb form asking someone to cease an action.",
    },
    "nani": {
        "language": "Japanese",
        "native": "何",
        "meaning": "What?",
        "explanation": "Informal Japanese interrogative pronoun meaning 'what'.",
    },
    "baka": {
        "language": "Japanese",
        "native": "馬鹿",
        "meaning": "Fool / Idiot / Silly",
        "explanation": "Common Japanese colloquial insult or affectionate teasing term.",
    },

    # Spanish
    "hola": {
        "language": "Spanish",
        "native": "Hola",
        "meaning": "Hello / Hi",
        "explanation": "Universal friendly greeting in the Spanish language.",
    },
    "adios": {
        "language": "Spanish",
        "native": "Adiós",
        "meaning": "Goodbye",
        "explanation": "Standard farewell in Spanish, literally derived from 'a Dios' (to God).",
    },
    "gracias": {
        "language": "Spanish",
        "native": "Gracias",
        "meaning": "Thank you",
        "explanation": "Standard expression of gratitude across the Spanish-speaking world.",
    },
    "muchas gracias": {
        "language": "Spanish",
        "native": "Muchas gracias",
        "meaning": "Thank you very much",
        "explanation": "Emphatic expression of gratitude in Spanish.",
    },
    "por favor": {
        "language": "Spanish",
        "native": "Por favor",
        "meaning": "Please",
        "explanation": "Polite request phrase in Spanish.",
    },
    "de nada": {
        "language": "Spanish",
        "native": "De nada",
        "meaning": "You're welcome",
        "explanation": "Common polite response to 'gracias' in Spanish, literally meaning 'of nothing'.",
    },
    "buenos dias": {
        "language": "Spanish",
        "native": "Buenos días",
        "meaning": "Good morning / Good day",
        "explanation": "Morning greeting in Spanish.",
    },
    "buenas noches": {
        "language": "Spanish",
        "native": "Buenas noches",
        "meaning": "Good evening / Good night",
        "explanation": "Evening greeting and bedtime farewell in Spanish.",
    },
    "hasta luego": {
        "language": "Spanish",
        "native": "Hasta luego",
        "meaning": "See you later",
        "explanation": "Friendly Spanish farewell implying you will meet again soon.",
    },
    "amigo": {
        "language": "Spanish",
        "native": "Amigo",
        "meaning": "Friend (male)",
        "explanation": "Spanish noun for a male friend or acquaintance.",
    },

    # French
    "bonjour": {
        "language": "French",
        "native": "Bonjour",
        "meaning": "Hello / Good day",
        "explanation": "Standard French greeting used from morning until late afternoon, literally 'good day'.",
    },
    "bonsoir": {
        "language": "French",
        "native": "Bonsoir",
        "meaning": "Good evening",
        "explanation": "Polite French greeting used after dusk.",
    },
    "au revoir": {
        "language": "French",
        "native": "Au revoir",
        "meaning": "Goodbye",
        "explanation": "Formal French farewell, literally meaning 'until we see each other again'.",
    },
    "merci": {
        "language": "French",
        "native": "Merci",
        "meaning": "Thank you",
        "explanation": "Standard French word for thank you.",
    },
    "merci beaucoup": {
        "language": "French",
        "native": "Merci beaucoup",
        "meaning": "Thank you very much",
        "explanation": "Emphatic expression of gratitude in French.",
    },
    "s'il vous plait": {
        "language": "French",
        "native": "S'il vous plaît",
        "meaning": "Please (polite/formal)",
        "explanation": "Formal French phrase meaning 'if it pleases you'.",
    },
    "salut": {
        "language": "French",
        "native": "Salut",
        "meaning": "Hi / Bye (informal)",
        "explanation": "Casual greeting and farewell among friends in French.",
    },
    "c'est la vie": {
        "language": "French",
        "native": "C'est la vie",
        "meaning": "That's life / Such is life",
        "explanation": "Philosophical French idiom acknowledging that life has unavoidable ups and downs.",
    },

    # Hindi / Urdu
    "namaste": {
        "language": "Hindi",
        "native": "नमस्ते",
        "meaning": "Hello / Greetings (I bow to the divine in you)",
        "explanation": "Venerable ancient Sanskrit-derived greeting accompanied by hands pressed together in Anjali Mudra.",
    },
    "namaskar": {
        "language": "Hindi",
        "native": "नमस्कार",
        "meaning": "Respectful greetings",
        "explanation": "Formal and traditional greeting in Hindi and across Indian languages.",
    },
    "shukriya": {
        "language": "Hindi",
        "native": "शुक्रिया",
        "meaning": "Thank you",
        "explanation": "Common spoken thank you in Hindi and Urdu, derived from Arabic/Persian roots.",
    },
    "dhanyavaad": {
        "language": "Hindi",
        "native": "धन्यवाद",
        "meaning": "Thank you (formal)",
        "explanation": "Formal Sanskrit-derived expression of thanks in Hindi.",
    },
    "alvida": {
        "language": "Hindi",
        "native": "अलविदा",
        "meaning": "Goodbye / Farewell",
        "explanation": "Poetic and formal farewell in Hindi and Urdu.",
    },
    "kaise ho": {
        "language": "Hindi",
        "native": "कैसे हो?",
        "meaning": "How are you?",
        "explanation": "Colloquial Hindi question asking someone how they are doing.",
    },

    # Arabic
    "marhaba": {
        "language": "Arabic",
        "native": "مرحباً",
        "meaning": "Hello / Welcome",
        "explanation": "Friendly and secular Arabic greeting used across the Arab world.",
    },
    "ahlan": {
        "language": "Arabic",
        "native": "أهلاً",
        "meaning": "Welcome / Hello",
        "explanation": "Common warm welcome greeting in Arabic.",
    },
    "shukran": {
        "language": "Arabic",
        "native": "شكراً",
        "meaning": "Thank you",
        "explanation": "Universal Arabic expression of gratitude.",
    },
    "habibi": {
        "language": "Arabic",
        "native": "حبيبي",
        "meaning": "My love / My dear friend",
        "explanation": "Affectionate Arabic term used for friends, family, and loved ones.",
    },
    "assalamu alaikum": {
        "language": "Arabic",
        "native": "السلام عليكم",
        "meaning": "Peace be upon you",
        "explanation": "Traditional Islamic peace greeting exchanged across the Muslim world.",
    },
    "ma'a salama": {
        "language": "Arabic",
        "native": "مع السلامة",
        "meaning": "Goodbye (Go in safety)",
        "explanation": "Standard polite Arabic farewell wishing the departure in peace and safety.",
    },

    # Korean
    "annyeong": {
        "language": "Korean",
        "native": "안녕",
        "meaning": "Hi / Bye (informal)",
        "explanation": "Casual greeting used among peers and close friends in Korea.",
    },
    "annyeonghaseyo": {
        "language": "Korean",
        "native": "안녕하세요",
        "meaning": "Hello / Peace be with you (polite)",
        "explanation": "Standard polite honorific greeting used in Korean society.",
    },
    "kamsahamnida": {
        "language": "Korean",
        "native": "감사합니다",
        "meaning": "Thank you (polite/formal)",
        "explanation": "Standard polite expression of gratitude in Korean.",
    },
    "saranghae": {
        "language": "Korean",
        "native": "사랑해",
        "meaning": "I love you",
        "explanation": "Korean phrase expressing love and affection.",
    },
    "daebak": {
        "language": "Korean",
        "native": "대박",
        "meaning": "Awesome / Incredible / Jackpot",
        "explanation": "Popular Korean slang exclamation expressing wonder, shock, or congratulations.",
    },

    # Chinese (Pinyin)
    "ni hao": {
        "language": "Chinese",
        "native": "你好",
        "meaning": "Hello (literally 'you good')",
        "explanation": "Standard polite Mandarin Chinese greeting.",
    },
    "nihao": {
        "language": "Chinese",
        "native": "你好",
        "meaning": "Hello",
        "explanation": "Merged pinyin form of 你好.",
    },
    "xie xie": {
        "language": "Chinese",
        "native": "谢谢",
        "meaning": "Thank you",
        "explanation": "Standard expression of gratitude in Mandarin Chinese.",
    },
    "xiexie": {
        "language": "Chinese",
        "native": "谢谢",
        "meaning": "Thank you",
        "explanation": "Continuous pinyin form of 谢谢.",
    },
    "zai jian": {
        "language": "Chinese",
        "native": "再见",
        "meaning": "Goodbye (literally 'again see')",
        "explanation": "Standard Mandarin Chinese farewell meaning 'see you again'.",
    },
    "zaijian": {
        "language": "Chinese",
        "native": "再见",
        "meaning": "Goodbye",
        "explanation": "Merged pinyin form of 再见.",
    },

    # Russian (Transliterated)
    "privet": {
        "language": "Russian",
        "native": "Привет",
        "meaning": "Hi / Hello (casual)",
        "explanation": "Informal Russian greeting used between friends and family.",
    },
    "spasibo": {
        "language": "Russian",
        "native": "Спасибо",
        "meaning": "Thank you",
        "explanation": "Standard Russian thank you, historically contracted from 'Спаси Бог' (God save you).",
    },
    "spasiba": {
        "language": "Russian",
        "native": "Спасибо",
        "meaning": "Thank you",
        "explanation": "Phonetic transliteration of Russian Спасибо.",
    },
    "poka": {
        "language": "Russian",
        "native": "Пока",
        "meaning": "Bye / See you (casual)",
        "explanation": "Informal Russian farewell.",
    },
    "dasvidaniya": {
        "language": "Russian",
        "native": "До свидания",
        "meaning": "Goodbye",
        "explanation": "Polite Russian farewell, literally meaning 'until our next meeting'.",
    },

    # German
    "guten tag": {
        "language": "German",
        "native": "Guten Tag",
        "meaning": "Good day / Hello",
        "explanation": "Standard formal daytime greeting in the German language.",
    },
    "danke": {
        "language": "German",
        "native": "Danke",
        "meaning": "Thank you",
        "explanation": "Standard German expression of gratitude.",
    },
    "auf wiedersehen": {
        "language": "German",
        "native": "Auf Wiedersehen",
        "meaning": "Goodbye",
        "explanation": "Formal German farewell meaning 'until we see each other again'.",
    },
    "bitte": {
        "language": "German",
        "native": "Bitte",
        "meaning": "Please / You're welcome",
        "explanation": "Versatile German courtesy word used for both 'please' and 'you're welcome'.",
    },

    # Thai
    "sawasdee": {
        "language": "Thai",
        "native": "สวัสดี",
        "meaning": "Hello / Greetings / Goodbye",
        "explanation": "Universal respectful Thai greeting coined in the 1930s from Sanskrit 'svasti' (well-being).",
    },
    "khop khun": {
        "language": "Thai",
        "native": "ขอบคุณ",
        "meaning": "Thank you",
        "explanation": "Standard expression of gratitude in the Thai language.",
    },

    # Turkish
    "merhaba": {
        "language": "Turkish",
        "native": "Merhaba",
        "meaning": "Hello",
        "explanation": "Standard Turkish greeting used any time of day.",
    },
    "tesekkurler": {
        "language": "Turkish",
        "native": "Teşekkürler",
        "meaning": "Thank you",
        "explanation": "Polite plural form expressing gratitude in Turkish.",
    },

    # Indonesian
    "terima kasih": {
        "language": "Indonesian",
        "native": "Terima kasih",
        "meaning": "Thank you",
        "explanation": "Standard Indonesian thank you, literally meaning 'receive love/affection'.",
    },

    # Italian / Latin
    "ciao": {
        "language": "Italian",
        "native": "Ciao",
        "meaning": "Hello / Goodbye",
        "explanation": "World-famous informal Italian greeting and farewell.",
    },
    "carpe diem": {
        "language": "Latin",
        "native": "Carpe diem",
        "meaning": "Seize the day",
        "explanation": "Classic Latin aphorism from the Roman poet Horace urging one to enjoy the present moment.",
    },
    "veni vidi vici": {
        "language": "Latin",
        "native": "Veni, vidi, vici",
        "meaning": "I came, I saw, I conquered",
        "explanation": "Famous Latin phrase attributed to Julius Caesar describing his swift victory at the Battle of Zela.",
    },
}


def lookup_romanized(text: str) -> Optional[Dict[str, Any]]:
    """
    Looks up a text snippet in the romanized lexicon.
    Supports clean lowercase, punctuation-stripped matching.
    """
    if not text:
        return None

    clean = text.strip().lower()
    # Remove common surrounding punctuation
    clean_stripped = clean.strip("!?.,:;\"'()[]{}~`")

    # Exact full match
    if clean_stripped in ROMANIZED_LEXICON:
        entry = ROMANIZED_LEXICON[clean_stripped].copy()
        entry["matched_term"] = clean_stripped
        return entry

    # Word-by-word search for multi-word phrases
    for term, data in ROMANIZED_LEXICON.items():
        if term == clean_stripped or f" {term} " in f" {clean_stripped} ":
            entry = data.copy()
            entry["matched_term"] = term
            return entry

    return None
