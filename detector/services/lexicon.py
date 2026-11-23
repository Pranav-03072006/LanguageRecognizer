"""
Multi-Lingual Conversational & Romanized Lexicon.
Provides accurate language identification, native script representations,
and English translations for common conversational greetings, loanwords,
and phrases across 22+ languages.
"""

import re
from typing import Any, Dict, Optional

ROMANIZED_LEXICON: Dict[str, Dict[str, Any]] = {
    # ==========================================
    # English (Conversational & Common Phrases)
    # ==========================================
    "hello": {
        "language": "English",
        "native": "Hello",
        "meaning": "Hello / Universal Greeting",
        "explanation": "Standard English greeting used universally to initiate conversation or acknowledge someone.",
    },
    "hello world": {
        "language": "English",
        "native": "Hello, World!",
        "meaning": "Hello World / Famous programmer greeting",
        "explanation": "Iconic programming phrase used since 1972 to demonstrate basic output functionality.",
    },
    "hi": {
        "language": "English",
        "native": "Hi",
        "meaning": "Hi / Informal Greeting",
        "explanation": "Friendly and casual English greeting used universally among friends and colleagues.",
    },
    "hey": {
        "language": "English",
        "native": "Hey",
        "meaning": "Hey / Casual Greeting",
        "explanation": "Informal English exclamation and greeting to catch someone's attention.",
    },
    "howdy": {
        "language": "English",
        "native": "Howdy",
        "meaning": "Howdy / Colloquial Greeting",
        "explanation": "Informal regional English greeting originated as an abbreviation of 'How do ye?'.",
    },
    "good morning": {
        "language": "English",
        "native": "Good morning",
        "meaning": "Good morning / Daytime Greeting",
        "explanation": "Polite English morning greeting typically used from sunrise until midday.",
    },
    "good afternoon": {
        "language": "English",
        "native": "Good afternoon",
        "meaning": "Good afternoon / Midday Greeting",
        "explanation": "Polite English greeting used between midday and early evening.",
    },
    "good evening": {
        "language": "English",
        "native": "Good evening",
        "meaning": "Good evening / Evening Greeting",
        "explanation": "Polite English greeting used after dusk.",
    },
    "good night": {
        "language": "English",
        "native": "Good night",
        "meaning": "Good night / Nocturnal Parting",
        "explanation": "Universal English parting well-wish uttered before sleeping or parting late at night.",
    },
    "goodbye": {
        "language": "English",
        "native": "Goodbye",
        "meaning": "Goodbye / Parting Farewell",
        "explanation": "Standard English farewell, historically contracted from 'God be with ye'.",
    },
    "bye": {
        "language": "English",
        "native": "Bye",
        "meaning": "Bye / Casual Farewell",
        "explanation": "Shortened informal English farewell.",
    },
    "bye bye": {
        "language": "English",
        "native": "Bye bye",
        "meaning": "Bye bye / Friendly Farewell",
        "explanation": "Affectionate reduplicated English parting farewell.",
    },
    "thank you": {
        "language": "English",
        "native": "Thank you",
        "meaning": "Thank you / Expression of Gratitude",
        "explanation": "Standard English polite formula acknowledging a kindness, favor, or service.",
    },
    "thank you very much": {
        "language": "English",
        "native": "Thank you very much",
        "meaning": "Thank you very much / Deep Gratitude",
        "explanation": "Emphatic English expression expressing sincere and deep appreciation.",
    },
    "thanks": {
        "language": "English",
        "native": "Thanks",
        "meaning": "Thanks / Informal Gratitude",
        "explanation": "Common informal English expression of appreciation.",
    },
    "thanks a lot": {
        "language": "English",
        "native": "Thanks a lot",
        "meaning": "Thanks a lot / Casual Appreciation",
        "explanation": "Casual and expressive English phrase expressing gratitude.",
    },
    "welcome": {
        "language": "English",
        "native": "Welcome",
        "meaning": "Welcome / Cordial Reception",
        "explanation": "Warm greeting extended to visitors or a polite acknowledgement of gratitude.",
    },
    "you are welcome": {
        "language": "English",
        "native": "You are welcome",
        "meaning": "You're welcome / Courtesy Reply",
        "explanation": "Polite English courtesy response offered after receiving thanks.",
    },
    "you're welcome": {
        "language": "English",
        "native": "You're welcome",
        "meaning": "You're welcome / Courtesy Reply",
        "explanation": "Contracted colloquial English courtesy response after receiving thanks.",
    },
    "please": {
        "language": "English",
        "native": "Please",
        "meaning": "Please / Polite Request Marker",
        "explanation": "Standard English etiquette particle used to make requests polite.",
    },
    "excuse me": {
        "language": "English",
        "native": "Excuse me",
        "meaning": "Excuse me / Polite Interjection",
        "explanation": "Polite English expression used to apologize for small interruptions or seek attention.",
    },
    "sorry": {
        "language": "English",
        "native": "Sorry",
        "meaning": "Sorry / Apology or Sympathy",
        "explanation": "Universal English expression of remorse, regret, or mild apology.",
    },
    "yes": {
        "language": "English",
        "native": "Yes",
        "meaning": "Yes / Affirmation",
        "explanation": "Standard English affirmative response indicating agreement or confirmation.",
    },
    "yeah": {
        "language": "English",
        "native": "Yeah",
        "meaning": "Yeah / Informal Affirmation",
        "explanation": "Colloquial conversational English affirmative.",
    },
    "yep": {
        "language": "English",
        "native": "Yep",
        "meaning": "Yep / Casual Affirmation",
        "explanation": "Casual English affirmative variation.",
    },
    "no": {
        "language": "English",
        "native": "No",
        "meaning": "No / Negation",
        "explanation": "Standard English negative response indicating disagreement or refusal.",
    },
    "nope": {
        "language": "English",
        "native": "Nope",
        "meaning": "Nope / Casual Negation",
        "explanation": "Informal English negative response.",
    },
    "okay": {
        "language": "English",
        "native": "Okay",
        "meaning": "Okay / Agreement or Approval",
        "explanation": "World-famous English loanword signifying agreement, compliance, or satisfaction.",
    },
    "ok": {
        "language": "English",
        "native": "OK",
        "meaning": "OK / Assent or Approval",
        "explanation": "Global abbreviation for approval or assent originating in 19th-century American English.",
    },
    "how are you": {
        "language": "English",
        "native": "How are you?",
        "meaning": "How are you? / Friendly Inquiry",
        "explanation": "Standard English greeting inquiry regarding a person's health, mood, or situation.",
    },
    "how are you doing": {
        "language": "English",
        "native": "How are you doing?",
        "meaning": "How are you doing? / Casual Greeting",
        "explanation": "Casual conversational English greeting inquiring after someone's state.",
    },
    "what is your name": {
        "language": "English",
        "native": "What is your name?",
        "meaning": "What is your name? / Identity Question",
        "explanation": "Direct and polite English question asking for someone's name.",
    },
    "what's up": {
        "language": "English",
        "native": "What's up?",
        "meaning": "What's up? / Informal Greeting",
        "explanation": "Very common informal English greeting among friends and peers.",
    },
    "see you": {
        "language": "English",
        "native": "See you",
        "meaning": "See you / Casual Farewell",
        "explanation": "Informal English parting phrase.",
    },
    "see you later": {
        "language": "English",
        "native": "See you later",
        "meaning": "See you later / Farewell",
        "explanation": "Everyday English parting expression indicating intent to meet again.",
    },
    "see you soon": {
        "language": "English",
        "native": "See you soon",
        "meaning": "See you soon / Warm Farewell",
        "explanation": "Warm English parting phrase expecting a prompt reunion.",
    },
    "take care": {
        "language": "English",
        "native": "Take care",
        "meaning": "Take care / Parting Well-Wish",
        "explanation": "Affectionate English parting farewell expressing care and goodwill.",
    },
    "cheers": {
        "language": "English",
        "native": "Cheers",
        "meaning": "Cheers / Toast, Thanks, or Goodbye",
        "explanation": "Multipurpose British/Commonwealth expression used as a drinking toast, thank you, or casual farewell.",
    },
    "congratulations": {
        "language": "English",
        "native": "Congratulations",
        "meaning": "Congratulations / Praise on Achievement",
        "explanation": "Formal English celebration of someone's success or happy milestone.",
    },
    "happy birthday": {
        "language": "English",
        "native": "Happy birthday",
        "meaning": "Happy birthday / Annual Celebration Wish",
        "explanation": "Standard English celebratory well-wish for a person's birthday.",
    },
    "i love you": {
        "language": "English",
        "native": "I love you",
        "meaning": "I love you / Declaration of Affection",
        "explanation": "Universal English declaration expressing deep personal love.",
    },

    # ==========================================
    # Japanese (Kanji/Kana & Romanized Romaji)
    # ==========================================
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
        "explanation": "'Konnichiwa' is the standard Japanese daytime greeting used from late morning until dusk.",
    },
    "konichiwa": {
        "language": "Japanese",
        "native": "こんにちは",
        "meaning": "Hello / Good afternoon",
        "explanation": "Common alternative spelling for 'Konnichiwa' (こんにちは).",
    },
    "konbanwa": {
        "language": "Japanese",
        "native": "こんばんは",
        "meaning": "Good evening",
        "explanation": "Standard Japanese evening greeting used after nightfall.",
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
        "explanation": "Iconic Japanese cultural concept denoting cuteness, charm, and innocence.",
    },
    "senpai": {
        "language": "Japanese",
        "native": "先輩",
        "meaning": "Senior mentor / Upperclassman",
        "explanation": "Japanese honorific title for an elder peer or mentor in school, sports, or work.",
    },
    "sensei": {
        "language": "Japanese",
        "native": "先生",
        "meaning": "Teacher / Master / Doctor",
        "explanation": "Title of deep respect accorded to educators, physicians, lawyers, and masters of arts.",
    },
    "gomen nasai": {
        "language": "Japanese",
        "native": "ごめんなさい",
        "meaning": "I am sorry / Forgive me",
        "explanation": "Common sincere Japanese apology.",
    },
    "sumimasen": {
        "language": "Japanese",
        "native": "すみません",
        "meaning": "Excuse me / Thank you / Sorry",
        "explanation": (
            "Indispensable multipurpose Japanese polite phrase used for apologies, attracting attention, or polite thanks."
        ),
    },
    "jaa ne": {
        "language": "Japanese",
        "native": "じゃあね",
        "meaning": "See you later / Bye",
        "explanation": "Very common casual Japanese parting phrase among peers.",
    },
    "mata ne": {
        "language": "Japanese",
        "native": "またね",
        "meaning": "See you again",
        "explanation": "Warm informal Japanese farewell.",
    },

    # ==========================================
    # French
    # ==========================================
    "bonjour": {
        "language": "French",
        "native": "Bonjour",
        "meaning": "Hello / Good day",
        "explanation": "Universal French greeting used politely from morning until late afternoon.",
    },
    "salut": {
        "language": "French",
        "native": "Salut",
        "meaning": "Hi / Bye (informal)",
        "explanation": "Very common casual French greeting and farewell among friends and youth.",
    },
    "merci": {
        "language": "French",
        "native": "Merci",
        "meaning": "Thank you",
        "explanation": "Standard French word for expressing gratitude.",
    },
    "merci beaucoup": {
        "language": "French",
        "native": "Merci beaucoup",
        "meaning": "Thank you very much",
        "explanation": "Emphatic French polite expression of gratitude.",
    },
    "bonsoir": {
        "language": "French",
        "native": "Bonsoir",
        "meaning": "Good evening",
        "explanation": "Polite French greeting used upon meeting someone after sunset.",
    },
    "bonne nuit": {
        "language": "French",
        "native": "Bonne nuit",
        "meaning": "Good night",
        "explanation": "French parting phrase uttered before going to bed.",
    },
    "au revoir": {
        "language": "French",
        "native": "Au revoir",
        "meaning": "Goodbye / Until we meet again",
        "explanation": "Standard polite French farewell literally meaning 'to the seeing-again'.",
    },
    "s'il vous plait": {
        "language": "French",
        "native": "S'il vous plaît",
        "meaning": "Please (polite / plural)",
        "explanation": "Formal French courtesy phrase literally meaning 'if it pleases you'.",
    },
    "s'il vous plaît": {
        "language": "French",
        "native": "S'il vous plaît",
        "meaning": "Please (polite / plural)",
        "explanation": "Standard accented French courtesy phrase.",
    },
    "de rien": {
        "language": "French",
        "native": "De rien",
        "meaning": "You're welcome / It's nothing",
        "explanation": "Common French response downplaying a favor after receiving thanks.",
    },
    "je vous en prie": {
        "language": "French",
        "native": "Je vous en prie",
        "meaning": "You are very welcome",
        "explanation": "Formal and elegant French response to thanks.",
    },
    "comment allez-vous": {
        "language": "French",
        "native": "Comment allez-vous ?",
        "meaning": "How are you? (polite / formal)",
        "explanation": "Standard polite French greeting inquiry.",
    },
    "comment ca va": {
        "language": "French",
        "native": "Comment ça va ?",
        "meaning": "How are things? / How's it going?",
        "explanation": "Everyday casual French conversational greeting.",
    },
    "comment ça va": {
        "language": "French",
        "native": "Comment ça va ?",
        "meaning": "How are things? / How's it going?",
        "explanation": "Accented everyday casual French conversational greeting.",
    },
    "c'est la vie": {
        "language": "French",
        "native": "C'est la vie",
        "meaning": "That's life / Such is life",
        "explanation": "Famous French philosophical idiom expressing acceptance of life's unpredictable fortunes.",
    },

    # ==========================================
    # Spanish
    # ==========================================
    "hola": {
        "language": "Spanish",
        "native": "¡Hola!",
        "meaning": "Hello / Hi",
        "explanation": "Universal Spanish greeting used across all Spanish-speaking countries.",
    },
    "buenos dias": {
        "language": "Spanish",
        "native": "Buenos días",
        "meaning": "Good morning / Good day",
        "explanation": "Polite Spanish morning greeting used until midday.",
    },
    "buenos días": {
        "language": "Spanish",
        "native": "Buenos días",
        "meaning": "Good morning / Good day",
        "explanation": "Accented standard Spanish morning greeting.",
    },
    "buenas tardes": {
        "language": "Spanish",
        "native": "Buenas tardes",
        "meaning": "Good afternoon",
        "explanation": "Polite Spanish greeting used from noon until nightfall.",
    },
    "buenas noches": {
        "language": "Spanish",
        "native": "Buenas noches",
        "meaning": "Good evening / Good night",
        "explanation": "Dual-purpose Spanish phrase used both as an evening greeting and as a bedtime farewell.",
    },
    "gracias": {
        "language": "Spanish",
        "native": "Gracias",
        "meaning": "Thank you",
        "explanation": "Universal Spanish expression of gratitude.",
    },
    "muchas gracias": {
        "language": "Spanish",
        "native": "Muchas gracias",
        "meaning": "Thank you very much",
        "explanation": "Emphatic Spanish gratitude expression.",
    },
    "de nada": {
        "language": "Spanish",
        "native": "De nada",
        "meaning": "You're welcome / It's nothing",
        "explanation": "Standard Spanish courtesy response to thanks.",
    },
    "por favor": {
        "language": "Spanish",
        "native": "Por favor",
        "meaning": "Please",
        "explanation": "Universal Spanish polite request convention.",
    },
    "adios": {
        "language": "Spanish",
        "native": "¡Adiós!",
        "meaning": "Goodbye / Farewell",
        "explanation": "Classic Spanish farewell, historically derived from 'a Dios' (unto God).",
    },
    "adiós": {
        "language": "Spanish",
        "native": "¡Adiós!",
        "meaning": "Goodbye / Farewell",
        "explanation": "Standard accented Spanish farewell.",
    },
    "hasta luego": {
        "language": "Spanish",
        "native": "Hasta luego",
        "meaning": "See you later",
        "explanation": "Very common Spanish parting phrase.",
    },
    "hasta mañana": {
        "language": "Spanish",
        "native": "Hasta mañana",
        "meaning": "See you tomorrow",
        "explanation": "Spanish farewell expecting to meet the next day.",
    },
    "hasta manana": {
        "language": "Spanish",
        "native": "Hasta mañana",
        "meaning": "See you tomorrow",
        "explanation": "Unaccented Spanish farewell.",
    },
    "como estas": {
        "language": "Spanish",
        "native": "¿Cómo estás?",
        "meaning": "How are you? (informal)",
        "explanation": "Friendly Spanish greeting question.",
    },
    "cómo estás": {
        "language": "Spanish",
        "native": "¿Cómo estás?",
        "meaning": "How are you? (informal)",
        "explanation": "Accented Spanish greeting question.",
    },
    "que tal": {
        "language": "Spanish",
        "native": "¿Qué tal?",
        "meaning": "What's up? / How are you?",
        "explanation": "Informal Spanish conversational opening.",
    },
    "qué tal": {
        "language": "Spanish",
        "native": "¿Qué tal?",
        "meaning": "What's up? / How are you?",
        "explanation": "Accented informal Spanish conversational opening.",
    },
    "mucho gusto": {
        "language": "Spanish",
        "native": "Mucho gusto",
        "meaning": "Nice to meet you",
        "explanation": "Polite Spanish phrase used when introduced to someone.",
    },
    "amigo": {
        "language": "Spanish",
        "native": "Amigo",
        "meaning": "Friend (male)",
        "explanation": "Universal Spanish word for friend.",
    },

    # ==========================================
    # German
    # ==========================================
    "hallo": {
        "language": "German",
        "native": "Hallo",
        "meaning": "Hello / Hi",
        "explanation": "Universal German greeting used informally and semi-formally throughout German-speaking nations.",
    },
    "guten tag": {
        "language": "German",
        "native": "Guten Tag",
        "meaning": "Good day / Hello (polite)",
        "explanation": "Standard formal German greeting used throughout the daytime.",
    },
    "guten morgen": {
        "language": "German",
        "native": "Guten Morgen",
        "meaning": "Good morning",
        "explanation": "Polite German morning greeting.",
    },
    "guten abend": {
        "language": "German",
        "native": "Guten Abend",
        "meaning": "Good evening",
        "explanation": "Polite German greeting used in the evening.",
    },
    "gute nacht": {
        "language": "German",
        "native": "Gute Nacht",
        "meaning": "Good night",
        "explanation": "German parting phrase spoken before sleeping.",
    },
    "danke": {
        "language": "German",
        "native": "Danke",
        "meaning": "Thank you / Thanks",
        "explanation": "Universal German expression of gratitude.",
    },
    "vielen dank": {
        "language": "German",
        "native": "Vielen Dank",
        "meaning": "Many thanks / Thank you very much",
        "explanation": "Formal and warm German expression of thanks.",
    },
    "danke schön": {
        "language": "German",
        "native": "Dankeschön",
        "meaning": "Thank you kindly",
        "explanation": "Common polite German phrase expressing gratitude.",
    },
    "danke schon": {
        "language": "German",
        "native": "Dankeschön",
        "meaning": "Thank you kindly",
        "explanation": "Unaccented spelling of German Dankeschön.",
    },
    "bitte": {
        "language": "German",
        "native": "Bitte",
        "meaning": "Please / You're welcome",
        "explanation": "Multipurpose German courtesy word used for 'please', 'you're welcome', and 'here you go'.",
    },
    "auf wiedersehen": {
        "language": "German",
        "native": "Auf Wiedersehen",
        "meaning": "Goodbye / Until we see again",
        "explanation": "Standard formal German farewell.",
    },
    "tschuss": {
        "language": "German",
        "native": "Tschüss",
        "meaning": "Bye / Goodbye (casual)",
        "explanation": "Most common informal German farewell used across Germany, Austria, and Switzerland.",
    },
    "tschüss": {
        "language": "German",
        "native": "Tschüss",
        "meaning": "Bye / Goodbye (casual)",
        "explanation": "Accented informal German farewell.",
    },

    # ==========================================
    # Dutch
    # ==========================================
    "hoi": {
        "language": "Dutch",
        "native": "Hoi",
        "meaning": "Hi / Hello (casual)",
        "explanation": "Popular informal greeting in the Netherlands and Flanders.",
    },
    "goedemorgen": {
        "language": "Dutch",
        "native": "Goedemorgen",
        "meaning": "Good morning",
        "explanation": "Standard polite Dutch morning greeting.",
    },
    "goedemiddag": {
        "language": "Dutch",
        "native": "Goedemiddag",
        "meaning": "Good afternoon",
        "explanation": "Standard Dutch afternoon greeting.",
    },
    "goedenavond": {
        "language": "Dutch",
        "native": "Goedenavond",
        "meaning": "Good evening",
        "explanation": "Polite Dutch evening greeting.",
    },
    "welterusten": {
        "language": "Dutch",
        "native": "Welterusten",
        "meaning": "Good night / Sleep well",
        "explanation": "Affectionate Dutch bedtime wish.",
    },
    "tot ziens": {
        "language": "Dutch",
        "native": "Tot ziens",
        "meaning": "Goodbye / See you",
        "explanation": "Standard polite Dutch farewell.",
    },
    "doei": {
        "language": "Dutch",
        "native": "Doei",
        "meaning": "Bye / See you (informal)",
        "explanation": "Common casual Dutch farewell.",
    },
    "dank je": {
        "language": "Dutch",
        "native": "Dank je",
        "meaning": "Thank you (informal)",
        "explanation": "Informal Dutch expression of gratitude.",
    },
    "dank u": {
        "language": "Dutch",
        "native": "Dank u",
        "meaning": "Thank you (polite)",
        "explanation": "Polite Dutch expression of gratitude.",
    },
    "dankjewel": {
        "language": "Dutch",
        "native": "Dankjewel",
        "meaning": "Thank you very much",
        "explanation": "Warm and friendly Dutch gratitude phrase.",
    },
    "alsjeblieft": {
        "language": "Dutch",
        "native": "Alsjeblieft",
        "meaning": "Please / Here you are (informal)",
        "explanation": "Informal Dutch courtesy word.",
    },
    "alstublieft": {
        "language": "Dutch",
        "native": "Alstublieft",
        "meaning": "Please / Here you are (polite)",
        "explanation": "Formal Dutch courtesy word.",
    },
    "graag gedaan": {
        "language": "Dutch",
        "native": "Graag gedaan",
        "meaning": "You're welcome / My pleasure",
        "explanation": "Standard Dutch reply downplaying a favor after receiving thanks.",
    },
    "hoe gaat het": {
        "language": "Dutch",
        "native": "Hoe gaat het?",
        "meaning": "How are you? / How's it going?",
        "explanation": "Standard Dutch inquiry of well-being.",
    },

    # ==========================================
    # Italian
    # ==========================================
    "ciao": {
        "language": "Italian",
        "native": "Ciao",
        "meaning": "Hello / Goodbye (informal)",
        "explanation": "World-famous Italian greeting and farewell originated from Venetian 's-ciavo vostro' (your servant).",
    },
    "buongiorno": {
        "language": "Italian",
        "native": "Buongiorno",
        "meaning": "Good morning / Good day",
        "explanation": "Polite Italian daytime greeting.",
    },
    "buonasera": {
        "language": "Italian",
        "native": "Buonasera",
        "meaning": "Good evening",
        "explanation": "Polite Italian evening greeting.",
    },
    "buonanotte": {
        "language": "Italian",
        "native": "Buonanotte",
        "meaning": "Good night",
        "explanation": "Italian bedtime farewell wish.",
    },
    "grazie": {
        "language": "Italian",
        "native": "Grazie",
        "meaning": "Thank you",
        "explanation": "Universal Italian expression of gratitude.",
    },
    "grazie mille": {
        "language": "Italian",
        "native": "Grazie mille",
        "meaning": "Thank you very much (A thousand thanks)",
        "explanation": "Warm and enthusiastic Italian gratitude phrase.",
    },
    "prego": {
        "language": "Italian",
        "native": "Prego",
        "meaning": "You're welcome / Please / After you",
        "explanation": "Polite Italian courtesy formula.",
    },
    "arrivederci": {
        "language": "Italian",
        "native": "Arrivederci",
        "meaning": "Goodbye / Until we see each other again",
        "explanation": "Standard polite Italian farewell.",
    },
    "come stai": {
        "language": "Italian",
        "native": "Come stai?",
        "meaning": "How are you?",
        "explanation": "Informal Italian greeting inquiry.",
    },

    # ==========================================
    # Latin
    # ==========================================
    "salve": {
        "language": "Latin",
        "native": "Salve",
        "meaning": "Hello / Hail (to one person)",
        "explanation": "Classical Latin greeting literally wishing health and well-being ('be well').",
    },
    "salvete": {
        "language": "Latin",
        "native": "Salvete",
        "meaning": "Hello / Hail (to multiple people)",
        "explanation": "Plural form of the Classical Latin greeting Salve.",
    },
    "ave": {
        "language": "Latin",
        "native": "Ave",
        "meaning": "Hail / Welcome",
        "explanation": "Classical Latin ceremonial greeting or salutation of honor.",
    },
    "vale": {
        "language": "Latin",
        "native": "Vale",
        "meaning": "Goodbye / Farewell",
        "explanation": "Classical Latin farewell formula literally meaning 'be healthy / be strong'.",
    },
    "valete": {
        "language": "Latin",
        "native": "Valete",
        "meaning": "Goodbye / Farewell (plural)",
        "explanation": "Plural form of the Classical Latin farewell Vale.",
    },
    "carpe diem": {
        "language": "Latin",
        "native": "Carpe diem",
        "meaning": "Seize the day",
        "explanation": "Famous Latin aphorism from Horace urging enjoyment of the present moment.",
    },
    "veni vidi vici": {
        "language": "Latin",
        "native": "Veni, vidi, vici",
        "meaning": "I came, I saw, I conquered",
        "explanation": "Julius Caesar's famous laconic report describing his rapid military victory at Zela.",
    },

    # ==========================================
    # Russian (Cyrillic & Romanized Transliteration)
    # ==========================================
    "privet": {
        "language": "Russian",
        "native": "Привет",
        "meaning": "Hi / Hello (informal)",
        "explanation": "Popular Russian informal greeting used among peers and close acquaintances.",
    },
    "spasibo": {
        "language": "Russian",
        "native": "Спасибо",
        "meaning": "Thank you",
        "explanation": "Universal Russian word for thank you, contracted from 'Спаси Бог' (God save you).",
    },
    "spasiba": {
        "language": "Russian",
        "native": "Спасибо",
        "meaning": "Thank you",
        "explanation": "Phonetic spelling of Russian Спасибо.",
    },
    "dasvidaniya": {
        "language": "Russian",
        "native": "До свидания",
        "meaning": "Goodbye",
        "explanation": "Standard formal Russian farewell meaning 'until our next meeting'.",
    },
    "poka": {
        "language": "Russian",
        "native": "Пока",
        "meaning": "Bye / See ya",
        "explanation": "Casual Russian farewell used among friends.",
    },
    "kak dela": {
        "language": "Russian",
        "native": "Как дела?",
        "meaning": "How are things? / How are you?",
        "explanation": "Very common informal Russian conversational inquiry.",
    },
    "dobroye utro": {
        "language": "Russian",
        "native": "Доброе утро",
        "meaning": "Good morning",
        "explanation": "Polite Russian morning greeting.",
    },

    # ==========================================
    # Hindi (Devanagari & Romanized Transliteration)
    # ==========================================
    "namaste": {
        "language": "Hindi",
        "native": "नमस्ते",
        "meaning": "Hello / Respectful Greetings",
        "explanation": "Venerated ancient Indian greeting literally meaning 'I bow to the divine in you'.",
    },
    "namaskar": {
        "language": "Hindi",
        "native": "नमस्कार",
        "meaning": "Formal Greetings / Salutations",
        "explanation": "Formal Devanagari salutation expressing reverent respect.",
    },
    "dhanyawad": {
        "language": "Hindi",
        "native": "धन्यवाद",
        "meaning": "Thank you",
        "explanation": "Formal Hindi expression of appreciation and gratitude.",
    },
    "dhanyavaad": {
        "language": "Hindi",
        "native": "धन्यवाद",
        "meaning": "Thank you",
        "explanation": "Alternative romanization of Hindi धन्यवाद.",
    },
    "shukriya": {
        "language": "Hindi",
        "native": "शुक्रिया",
        "meaning": "Thank you (everyday / Hindustani)",
        "explanation": "Warm and common colloquial expression of gratitude widely used in Hindi and Urdu.",
    },
    "alvida": {
        "language": "Hindi",
        "native": "अलविदा",
        "meaning": "Goodbye / Farewell",
        "explanation": "Formal farewell conveying poignant or long-term departure.",
    },
    "kaise ho": {
        "language": "Hindi",
        "native": "कैसे हो?",
        "meaning": "How are you? (informal)",
        "explanation": "Common casual Hindi greeting among friends.",
    },
    "aap kaise hain": {
        "language": "Hindi",
        "native": "आप कैसे हैं?",
        "meaning": "How are you? (polite / formal)",
        "explanation": "Polite honorific Hindi greeting inquiry.",
    },

    # ==========================================
    # Arabic (Arabic Script & Romanized Transliteration)
    # ==========================================
    "marhaba": {
        "language": "Arabic",
        "native": "مرحباً",
        "meaning": "Hello / Welcome",
        "explanation": "Universal friendly Arabic greeting used widely across the Arab world.",
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
        "explanation": "Affectionate Arabic term used warmly for friends and loved ones.",
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
        "explanation": "Standard polite Arabic farewell wishing departure in peace and safety.",
    },

    # ==========================================
    # Korean (Hangul & Romanized Transliteration)
    # ==========================================
    "annyeong": {
        "language": "Korean",
        "native": "안녕",
        "meaning": "Hi / Bye (informal)",
        "explanation": "Casual Korean greeting used among peers and close friends.",
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
        "meaning": "Thank you (polite)",
        "explanation": "Polite honorific Korean expression of gratitude.",
    },
    "gamsahamnida": {
        "language": "Korean",
        "native": "감사합니다",
        "meaning": "Thank you (polite)",
        "explanation": "Revised Romanization spelling of Korean 감사합니다.",
    },
    "saranghae": {
        "language": "Korean",
        "native": "사랑해",
        "meaning": "I love you (casual)",
        "explanation": "Expressive Korean declaration of love.",
    },

    # ==========================================
    # Chinese (Hanzi & Romanized Pinyin)
    # ==========================================
    "ni hao": {
        "language": "Chinese",
        "native": "你好",
        "meaning": "Hello / You good",
        "explanation": "Standard Mandarin Chinese greeting used throughout the Sinophone world.",
    },
    "nihao": {
        "language": "Chinese",
        "native": "你好",
        "meaning": "Hello / You good",
        "explanation": "Pinyin single-word representation of 你好.",
    },
    "xie xie": {
        "language": "Chinese",
        "native": "谢谢",
        "meaning": "Thank you",
        "explanation": "Universal Mandarin expression of gratitude.",
    },
    "xiexie": {
        "language": "Chinese",
        "native": "谢谢",
        "meaning": "Thank you",
        "explanation": "Single-token Pinyin spelling of 谢谢.",
    },
    "zai jian": {
        "language": "Chinese",
        "native": "再见",
        "meaning": "Goodbye / See you again",
        "explanation": "Standard Chinese farewell literally meaning 'to see again'.",
    },
    "zaijian": {
        "language": "Chinese",
        "native": "再见",
        "meaning": "Goodbye / See you again",
        "explanation": "Single-token Pinyin spelling of 再见.",
    },

    # ==========================================
    # Turkish
    # ==========================================
    "merhaba": {
        "language": "Turkish",
        "native": "Merhaba",
        "meaning": "Hello",
        "explanation": "Standard Turkish greeting used across Turkey and northern Cyprus.",
    },
    "tesekkurler": {
        "language": "Turkish",
        "native": "Teşekkürler",
        "meaning": "Thank you",
        "explanation": "Everyday Turkish expression of appreciation.",
    },
    "teşekkürler": {
        "language": "Turkish",
        "native": "Teşekkürler",
        "meaning": "Thank you",
        "explanation": "Accented standard Turkish expression of appreciation.",
    },

    # ==========================================
    # Swedish
    # ==========================================
    "hej": {
        "language": "Swedish",
        "native": "Hej",
        "meaning": "Hello / Hi",
        "explanation": "Everyday Swedish greeting used universally in Sweden and Finland.",
    },
    "hejsan": {
        "language": "Swedish",
        "native": "Hejsan",
        "meaning": "Hi there (friendly)",
        "explanation": "Warm and friendly casual Swedish greeting.",
    },
    "tack": {
        "language": "Swedish",
        "native": "Tack",
        "meaning": "Thank you",
        "explanation": "Standard Swedish word expressing gratitude.",
    },
    "tack så mycket": {
        "language": "Swedish",
        "native": "Tack så mycket",
        "meaning": "Thank you very much",
        "explanation": "Emphatic Swedish gratitude phrase.",
    },
    "hej då": {
        "language": "Swedish",
        "native": "Hej då",
        "meaning": "Goodbye",
        "explanation": "Standard Swedish parting farewell.",
    },

    # ==========================================
    # Indonesian
    # ==========================================
    "terima kasih": {
        "language": "Indonesian",
        "native": "Terima kasih",
        "meaning": "Thank you",
        "explanation": "Standard Indonesian expression of gratitude literally meaning 'receive love/affection'.",
    },

    # ==========================================
    # Thai (Romanized)
    # ==========================================
    "sawasdee": {
        "language": "Thai",
        "native": "สวัสดี",
        "meaning": "Hello / Goodbye",
        "explanation": "Traditional Thai greeting and farewell accompanied by the respectful 'wai' gesture.",
    },
    "khop khun": {
        "language": "Thai",
        "native": "ขอบคุณ",
        "meaning": "Thank you",
        "explanation": "Standard Thai phrase for expressing gratitude.",
    },
}


def lookup_romanized(text: str) -> Optional[Dict[str, Any]]:
    """
    Looks up a text snippet in the multi-lingual lexicon.
    Performs:
    1. Exact match on lowercase, punctuation-stripped input.
    2. Substring/word-boundary regex search sorted by phrase length descending,
       ensuring multi-word phrases match before single-word substrings.
    """
    if not text or not text.strip():
        return None

    clean = text.strip().lower()
    # Strip leading and trailing punctuation and whitespace
    clean_stripped = re.sub(r"^[\W_]+|[\W_]+$", "", clean)

    # 1. Exact match
    if clean_stripped in ROMANIZED_LEXICON:
        entry = ROMANIZED_LEXICON[clean_stripped].copy()
        entry["matched_term"] = clean_stripped
        return entry

    # 2. Search multi-word phrases and individual keywords using regex word boundary
    # Sort by length descending so longer phrases match first ('good morning' before 'good')
    for term in sorted(ROMANIZED_LEXICON.keys(), key=len, reverse=True):
        if len(term) < 2:
            continue
        # Using word boundaries
        pattern = r"\b" + re.escape(term) + r"\b"
        if re.search(pattern, clean, re.IGNORECASE):
            entry = ROMANIZED_LEXICON[term].copy()
            entry["matched_term"] = term
            return entry

    return None
