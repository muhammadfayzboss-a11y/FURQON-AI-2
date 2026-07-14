"""
FURQON AI - Qur'on va Hadislar asosida javob beruvchi Telegram Bot
Konfiguratsiya fayli
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

# OpenRouter API Key ( https://openrouter.ai )
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

# Bot sozlamalari
BOT_NAME = "FURQON AI"
BOT_VERSION = "2.1.0"
BOT_LANGUAGE = "uz"

# Ma'lumotlar bazasi yo'llari
QURAN_DATA_PATH = "quran_data/quran_uz.json"
HADITH_DATA_PATH = "hadith_data/hadith_uz.json"

# AI sozlamalari — OpenRouter orqali Gemini 2.0 Flash (BEPUL!)
AI_BASE_URL = "https://openrouter.ai/api/v1"
AI_MODEL = "google/gemini-2.0-flash-exp:free"  # Bepul model
AI_MAX_TOKENS = 2048
AI_TEMPERATURE = 0.3

# Javob chegaralari
MAX_QURAN_AYATS = 3  # Javobda ko'pi bilan nechta oyat
MAX_HADITHS = 3      # Javobda ko'pi bilan nechta hadis
