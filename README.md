# 🕌 FURQON AI — Qur'on va Hadislar Asosida Javob Beruvchi Bot

![FURQON AI](https://img.shields.io/badge/FURQON-AI-green?style=for-the-badge&logo=telegram)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![Gemini](https://img.shields.io/badge/Google-Gemini-orange?style=flat-square&logo=google)
![Bepul](https://img.shields.io/badge/Narx-BEPUL-success?style=flat-square)

## 📖 Loyiha haqida

**FURQON AI** — bu Telegram bot bo'lib, foydalanuvchining savolini AI yordamida tushunib, Qur'on oyatlari va Hadislar asosida javob beradi.

### ✅ Xususiyatlari

- 🤖 **AI tushunish** — Google Gemini yordamida savolning ma'nosini tahlil qiladi
- 📖 **Qur'on oyatlari** — 90+ oyatlar bazasi (o'zbek va arabcha)
- 📚 **Hadislar** — 30+ hadislar bazasi (Buxoriy, Muslim, Tirmiziy, va boshqalar)
- 🔍 **Aqlli qidiruv** — Mavzu, kalit so'z va matn bo'yicha qidirish
- 🎲 **Tasodifiy oyat/hadis** — Har kungi ilhom olish
- 📱 **Telegram interfeys** — Qulay tugmalar va menyular
- 💰 **100% BEPUL** — Google Gemini bepul ishlaydi!

## 🚀 O'rnatish

### 1. Repository'ni klonlash

```bash
git clone https://github.com/muhammadfayzboss-a11y/FURQON-AI-2.git
cd FURQON-AI-2
```

### 2. Virtual muhit yaratish

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

### 3. Kutubxonalarni o'rnatish

```bash
pip install -r requirements.txt
```

### 4. .env faylini sozlash

```bash
cp .env.example .env
```

`.env` faylini oching va quyidagilarni to'ldiring:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
GEMINI_API_KEY=your_gemini_api_key
```

#### Tokenlarni olish (BEPUL!):

1. **Telegram Bot Token**: [@BotFather](https://t.me/BotFather) ga murojaat qiling
2. **Google Gemini API Key**: [aistudio.google.com/apikey](https://aistudio.google.com/apikey) dan bepul oling

### 5. Botni ishga tushirish

```bash
python bot.py
```

## 🐳 Docker orqali

```bash
# Docker image yaratish
docker build -t furqon-ai .

# Ishga tushirish
docker run -d --name furqon-ai \
  -e TELEGRAM_BOT_TOKEN=your_token \
  -e GEMINI_API_KEY=your_key \
  furqon-ai
```

## 📂 Loyiha strukturasi

```
FURQON-AI-2/
├── bot.py                  # Asosiy Telegram bot
├── ai_handler.py           # AI bilan ishlash (Google Gemini)
├── search_engine.py        # Qidiruv tizimi
├── config.py               # Konfiguratsiya
├── quran_data/
│   └── quran_uz.json       # Qur'on oyatlari ma'lumotlar bazasi
├── hadith_data/
│   └── hadith_uz.json      # Hadislar ma'lumotlar bazasi
├── requirements.txt        # Python kutubxonalari
├── Dockerfile              # Docker konfiguratsiyasi
├── .env.example            # Muhit o'zgaruvchilari namunasi
├── .gitignore
└── README.md
```

## 🎯 Foydalanish

### Buyruqlar:

| Buyruq | Tavsif |
|--------|--------|
| `/start` | Botni ishga tushirish |
| `/help` | Yordam |
| `/random_ayat` | Tasodifiy Qur'on oyati |
| `/random_hadith` | Tasodifiy hadis |
| `/topics` | Mavzular ro'yxati |

### Savol misollari:

- "Namozning fazilati haqida"
- "Sabr qilish haqida oyatlar"
- "Ota-onaga yaxshilik qilish"
- "Sadaqa haqida hadislar"
- "Tavba qilish haqida"
- "Ilm o'rganish haqida"
- "Jannat haqida"

## ⚙️ Ishlash printsipi

1. **Savol qabul qilinadi** → Foydalanuvchi savol yozadi
2. **AI tahlil** → Google Gemini savolni tushunib, mavzularni aniqlaydi
3. **Qidiruv** → Mavzular bo'yicha Qur'on va Hadislardan mos javoblar topiladi
4. **AI javob** → Topilgan oyatlar va hadislar asosida AI tushunarli javob yaratadi
5. **Natija** → Formatlangan javob foydalanuvchiga yuboriladi

## 💰 Narx: BEPUL!

- **Google Gemini API** — kuniga 1500+ so'rov bepul ✅
- **Telegram Bot API** — butunlay bepul ✅
- **Hosting** — Render/Railway free tier ishlatish mumkin ✅

## ⚠️ Muhim eslatma

Bu bot **ma'lumot berish** maqsadida yaratilgan. **Diniy fatvo** uchun mahalliy masjid imomi yoki diniy idoraga murojaat qiling.

## 📄 Litsenziya

MIT License

---

🤖 **FURQON AI** — Qur'on va Hadislar bilim manbai
