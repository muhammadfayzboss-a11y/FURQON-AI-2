"""
FURQON AI - Telegram Bot
Qur'on oyatlari va Hadislar asosida AI yordamida javob beruvchi bot
"""

import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
)
from config import TELEGRAM_BOT_TOKEN, BOT_NAME, BOT_VERSION, AI_MODEL
from ai_handler import AIHandler
from search_engine import SearchEngine

# Logging sozlamalari
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Global handler'lar
ai_handler = None
search_engine = None


def init_handlers():
    """Handler'larni ishga tushirish"""
    global ai_handler, search_engine
    ai_handler = AIHandler()
    search_engine = SearchEngine()


# ===================== COMMAND HANDLERS =====================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ /start - Botni ishga tushirish """
    user = update.effective_user
    
    welcome_text = f"""
🕌 *Assalomu alaykum, {user.first_name}!*

*Mening ismim FURQON AI* 🤖

Men Qur'on oyatlari va Hadislar asosida savollaringizga javob beraman.

📌 *Nima qila olaman:*
• Islom haqidagi savollaringizga Qur'on va Hadislar asosida javob beraman
• Har qanday diniy mavzuda ma'lumot beraman
• Tasodifiy oyat yoki hadis aytib bera olaman

🔍 *Qanday savol berish mumkin:*
• "Namozning fazilati haqida"
• "Sabr qilish haqida oyatlar"
• "Ota-onaga yaxshilik qilish"
• "Sadaqa haqida hadislar"
• "Tavba qilish haqida"

⬇️ Quyidagi menyudan foydalaning yoki bevosita savol yozing:
"""

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📖 Tasodifiy oyat", callback_data="random_ayat"),
            InlineKeyboardButton("📚 Tasodifiy hadis", callback_data="random_hadith"),
        ],
        [
            InlineKeyboardButton("🕌 Namoz haqida", callback_data="topic_namoz"),
            InlineKeyboardButton("🕋 Ro'za haqida", callback_data="topic_roza"),
        ],
        [
            InlineKeyboardButton("💰 Zakot haqida", callback_data="topic_zakot"),
            InlineKeyboardButton("❤️ Sabr haqida", callback_data="topic_sabr"),
        ],
        [
            InlineKeyboardButton("👨‍👩‍👧 Oila haqida", callback_data="topic_oila"),
            InlineKeyboardButton("📖 Ilm haqida", callback_data="topic_ilm"),
        ],
        [
            InlineKeyboardButton("ℹ️ Yordam", callback_data="help"),
        ],
    ])

    await update.message.reply_text(
        welcome_text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ /help - Yordam """
    help_text = """
🆘 *FURQON AI — Yordam*

📌 *Buyruqlar:*
/start — Botni qayta ishga tushirish
/help — Yordam ko'rsatmalari
/random_ayat — Tasodifiy Qur'on oyati
/random_hadith — Tasodifiy hadis
/topics — Mavzular ro'yxati

📝 *Qanday foydalanish:*
1. Istalgan Islomiy savolingizni yozing
2. Bot AI yordamida savolingizni tushunadi
3. Qur'on oyatlari va Hadislardan mos javoblarni topadi
4. Tushunarli formatda javob qaytaradi

💡 *Maslahatlar:*
• Savolni aniq va tushunarli yozing
• O'zbek tilida yozing
• Bir nechta mavzuni birlashtirib so'rashingiz mumkin

⚠️ *Diqqat:*
Bu bot ma'lumot berish maqsadida yaratilgan. Diniy fatvo uchun mutaxassisga murojaat qiling.
"""

    await update.message.reply_text(help_text, parse_mode="Markdown")


async def random_ayat_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ /random_ayat — Tasodifiy oyat """
    if not search_engine:
        await update.message.reply_text("⚠️ Bot hali tayyor emas. Iltimos kuting.")
        return

    ayat = search_engine.get_random_ayat()
    if ayat:
        text = format_ayat(ayat)
        await update.message.reply_text(text, parse_mode="Markdown")
    else:
        await update.message.reply_text("⚠️ Oyat topilmadi.")


async def random_hadith_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ /random_hadith — Tasodifiy hadis """
    if not search_engine:
        await update.message.reply_text("⚠️ Bot hali tayyor emas. Iltimos kuting.")
        return

    hadith = search_engine.get_random_hadith()
    if hadith:
        text = format_hadith(hadith)
        await update.message.reply_text(text, parse_mode="Markdown")
    else:
        await update.message.reply_text("⚠️ Hadis topilmadi.")


async def topics_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ /topics — Mavzular ro'yxati """
    if not search_engine:
        await update.message.reply_text("⚠️ Bot hali tayyor emas. Iltimos kuting.")
        return

    all_topics = search_engine.get_all_topics()

    text = "📋 *Mavzular ro'yxati*\n\n"
    text += "📖 *Qur'on mavzulari:*\n"
    for topic in all_topics["quran_topics"][:20]:
        text += f"  • {topic}\n"

    text += "\n📚 *Hadis mavzulari:*\n"
    for topic in all_topics["hadith_topics"][:20]:
        text += f"  • {topic}\n"

    text += "\n💡 Istalgan mavzu bo'yicha savol bering!"

    await update.message.reply_text(text, parse_mode="Markdown")


# ===================== MESSAGE HANDLER =====================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Oddiy xabarlarni qayta ishlash """
    if not ai_handler:
        await update.message.reply_text("⚠️ Bot hali tayyor emas. Iltimos kuting.")
        return

    user_message = update.message.text
    user = update.effective_user

    logger.info(f"Savol: {user_message} (from: {user.first_name})")

    # "Biroz kuting" xabari
    processing_msg = await update.message.reply_text(
        "🔍 Savolingizni tahlil qilmoqdaman...\n\n📖 Qur'on va Hadislardan mos javoblar qidirmoqdaman...",
    )

    try:
        # AI bilan javob berish
        answer = await ai_handler.process_question(user_message)

        # Natijani yuborish
        await processing_msg.delete()
        
        # Javobni bo'laklarga bo'lish (agar juda uzun bo'lsa)
        if len(answer) > 4096:
            chunks = [answer[i:i+4096] for i in range(0, len(answer), 4096)]
            for chunk in chunks:
                await update.message.reply_text(chunk, parse_mode="Markdown")
        else:
            await update.message.reply_text(answer, parse_mode="Markdown")

    except Exception as e:
        await processing_msg.delete()
        logger.error(f"Xato: {e}")
        await update.message.reply_text(
            "❌ Kechirasiz, javob berishda xato yuz berdi. Iltimos qaytadan urinib ko'ring.\n\n"
            "Agar muammo davom etsa, /start buyrug'ini yuboring."
        )


# ===================== CALLBACK HANDLER =====================

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Tugma bosishlarni qayta ishlash """
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "random_ayat":
        if search_engine:
            ayat = search_engine.get_random_ayat()
            if ayat:
                await query.edit_message_text(format_ayat(ayat), parse_mode="Markdown")
            else:
                await query.edit_message_text("⚠️ Oyat topilmadi.")

    elif data == "random_hadith":
        if search_engine:
            hadith = search_engine.get_random_hadith()
            if hadith:
                await query.edit_message_text(format_hadith(hadith), parse_mode="Markdown")
            else:
                await query.edit_message_text("⚠️ Hadis topilmadi.")

    elif data == "help":
        help_text = """
🆘 *FURQON AI — Yordam*

📝 Istalgan Islomiy savolingizni yozing va bot javob beradi!

📌 *Buyruqlar:*
/start — Boshlash
/help — Yordam
/random_ayat — Tasodifiy oyat
/random_hadith — Tasodifiy hadis
/topics — Mavzular

⚠️ Diniy fatvo uchun mutaxassisga murojaat qiling.
"""
        await query.edit_message_text(help_text, parse_mode="Markdown")

    elif data.startswith("topic_"):
        topic = data.replace("topic_", "")
        topic_map = {
            "namoz": "Namozning fazilati va ahamiyati haqida",
            "roza": "Ro'za tutishning fazilati va ahloqi haqida",
            "zakot": "Zakot berishning ahamiyati haqida",
            "sabr": "Sabr qilishning fazilati haqida",
            "oila": "Oila va nikoh haqida",
            "ilm": "Ilm o'rganishning fazilati haqida",
        }
        question = topic_map.get(topic, topic)
        
        if ai_handler:
            await query.edit_message_text("🔍 Qidirilmoqda...")
            try:
                answer = await ai_handler.process_question(question)
                if len(answer) > 4096:
                    await query.edit_message_text(answer[:4096], parse_mode="Markdown")
                else:
                    await query.edit_message_text(answer, parse_mode="Markdown")
            except Exception as e:
                await query.edit_message_text(f"❌ Xato: {e}")
        else:
            await query.edit_message_text("⚠️ Bot hali tayyor emas.")


# ===================== FORMAT HELPERS =====================

def format_ayat(ayat: dict) -> str:
    """Oyatni chiroyli formatga keltirish"""
    return f"""
📖 *Qur'on oyati*

🇸🇦 *{ayat['surah_name']} surasi, {ayat['ayat']}-oyat*

{ayat['arabic']}

🇺🇿 *Ma'nosi:*
{ayat['uzbek']}

🏷 Mavzular: {', '.join(ayat.get('topics', []))}

🤖 *FURQON AI*
"""


def format_hadith(hadith: dict) -> str:
    """Hadisni chiroyli formatga keltirish"""
    return f"""
📚 *Hadis*

📖 *{hadith['collection']} to'plami*
👤 Raviy: *{hadith['narrator']}*

{hadith['arabic']}

🇺🇿 *Ma'nosi:*
{hadith['uzbek']}

🏷 Mavzular: {', '.join(hadith.get('topics', []))}

🤖 *FURQON AI*
"""


# ===================== MAIN =====================

def main():
    """Botni ishga tushirish"""
    if not TELEGRAM_BOT_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN topilmadi! .env faylini tekshiring.")
        return

    print(f"""
╔══════════════════════════════════════╗
║     🕌 FURQON AI v{BOT_VERSION}            ║
║                                      ║
║  Qur'on va Hadislar asosida         ║
║  javob beruvchi Telegram Bot         ║
║                                      ║
║  🤖 AI: {AI_MODEL:<24s}║
║  🌐 Til: O'zbek                     ║
╚══════════════════════════════════════╝
    """)

    # Handler'larni ishga tushirish
    init_handlers()
    print("✅ AI va qidiruv tizimi tayyor!")

    # Bot yaratish (timeout va retry bilan)
    from telegram.request import HTTPXRequest
    request = HTTPXRequest(
        connect_timeout=30.0,
        read_timeout=60.0,
        write_timeout=60.0,
        pool_timeout=30.0,
    )
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).request(request).get_updates_request(request).build()

    # Handler'larni qo'shish
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("random_ayat", random_ayat_command))
    app.add_handler(CommandHandler("random_hadith", random_hadith_command))
    app.add_handler(CommandHandler("topics", topics_command))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Botni ishga tushirish
    print("🚀 Bot ishga tushmoqda...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
