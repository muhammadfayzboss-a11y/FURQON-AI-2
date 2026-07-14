"""
FURQON AI - Qur'on va Hadislar asosida javob beruvchi Telegram Bot
Konfiguratsiya fayli
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

# Google Gemini API Key (BEPUL! → https://aistudio.google.com/apikey)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Bot sozlamalari
BOT_NAME = "FURQON AI"
BOT_VERSION = "2.0.0"
BOT_LANGUAGE = "uz"

# Ma'lumotlar bazasi yo'llari
QURAN_DATA_PATH = "quran_data/quran_uz.json"
HADITH_DATA_PATH = "hadith_data/hadith_uz.json"

# AI sozlamalari
GEMINI_MODEL = "gemini-2.0-flash"
AI_MAX_TOKENS = 2048
AI_TEMPERATURE = 0.3

# Javob chegaralari
MAX_QURAN_AYATS = 3  # Javobda ko'pi bilan nechta oyat
MAX_HADITHS = 3      # Javobda ko'pi bilan nechta hadis
