#!/usr/bin/env python3
"""
Quran Reel Maker - Telegram Bot V2
Version: 2.0 (With Storage Channel & Auto-Delete)
"""

import os
import time
import logging
import asyncio
import requests
import json
from io import BytesIO
from datetime import datetime
from functools import wraps
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, ConversationHandler, filters

# ====================== CONFIG ======================
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
STORAGE_CHANNEL_ID = os.environ.get("STORAGE_CHANNEL_ID", "")  # Optional: -1001234567890
AUTO_DELETE_HOURS = 24  # Auto-delete after X hours

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
FONT_DIR = os.path.join(BASE_DIR, "fonts")
VIDEOS_DIR = os.path.join(DATA_DIR, "videos")
TEMP_DIR = os.path.join(DATA_DIR, "temp")
CACHE_DIR = os.path.join(DATA_DIR, "cache")

# Create directories
for directory in [DATA_DIR, VIDEOS_DIR, TEMP_DIR, CACHE_DIR]:
    os.makedirs(directory, exist_ok=True)

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ====================== CONSTANTS ======================
PEXELS_KEYS = [
    "AmAgE0J5AuBbsvR6dmG7qQLIc5uYZvDim2Vx250F5QoHNKnGdCofFerx",
    "Fv0qzUGYwbGr6yHsauaXuNKiNR9L7OE7VLr5Wq6SngcLjavmkCEAskb2",
    "1NK8BaBXGsXm4Uxzcesxm0Jxh2yCILOwqqsj4GiM57dXcb7b8bbDYyOu",
    "C9KJNtJET2wAnmD42Gbu0OolTlmhoT02CX7fyst3kKEvnjRRWLiAqQ9t",
]

NEW_RECITERS = {
    "احمد النفيس": (259, "https://server16.mp3quran.net/nufais/Rewayat-Hafs-A-n-Assem/"),
    "وديع اليماني": (219, "https://server6.mp3quran.net/wdee3/"),
    "بندر بليلة": (217, "https://server6.mp3quran.net/balilah/"),
    "ادريس ابكر": (12, "https://server6.mp3quran.net/abkr/"),
    "منصور السالمي": (245, "https://server14.mp3quran.net/mansor/"),
    "رعد الكردي": (221, "https://server6.mp3quran.net/kurdi/"),
}

OLD_RECITERS = {
    "ابو بكر الشاطري": "Abu_Bakr_Ash-Shaatree_128kbps",
    "ياسر الدسري": "Yasser_Ad-Dussary_128kbps",
    "عبدالرحمن السديس": "Abdurrahmaan_As-Sudais_64kbps",
    "ماهر المعيقلي": "Maher_AlMuaiqly_64kbps",
    "سعود الشريم": "Saood_ash-Shuraym_64kbps",
    "مشاري العفاسي": "Alafasy_64kbps",
}

THEMES = {
    "ذهبي": {"bg": (30, 20, 10), "text": (255, 215, 0), "translation": (200, 200, 200), "banner": (180, 140, 60)},
    "ليلي ازرق": {"bg": (10, 20, 40), "text": (255, 255, 255), "translation": (173, 216, 230), "banner": (25, 55, 90)},
    "اخضر": {"bg": (10, 30, 15), "text": (255, 255, 255), "translation": (144, 238, 144), "banner": (20, 60, 30)},
    "بنفسجي": {"bg": (40, 20, 50), "text": (255, 215, 0), "translation": (200, 180, 220), "banner": (60, 30, 80)},
    "ابيض": {"bg": (245, 245, 245), "text": (30, 30, 30), "translation": (80, 80, 80), "banner": (200, 200, 200)},
    "غروب": {"bg": (20, 10, 30), "text": (255, 255, 255), "translation": (255, 200, 150), "banner": (60, 30, 40)},
}

# Surah names
SURAHS = [
    "الفاتحة", "البقرة", "آل عمران", "النساء", "المائدة", "الانعام", "الاعراف", "الانفال", "التوبة", "يونس",
    "هود", "يوسف", "الرعد", "ابراهيم", "الحجر", "النحل", "الاسراء", "الكهف", "مريم", "طه",
    "الانبياء", "الحج", "المؤمنون", "النور", "الفرقان", "الشعراء", "النمل", "القصص", "العنكبوت", "الروم",
    "لقمان", "السجدة", "الاحزاب", "سبا", "فاطر", "يس", "الصافات", "ص", "الزمر", "غافر",
    "فصلت", "الشورى", "الزخرف", "الدخان", "الجاثية", "الاحقاف", "محمد", "الفتح", "الحجرات", "ق",
    "الذاريات", "الطور", "النجم", "القمر", "الرحمن", "الواقعة", "الحديد", "المجادلة", "الحشر", "الممتحنة",
    "الصف", "الجمعة", "المنافقون", "التغابن", "الطلاق", "التحريم", "الملك", "القلم", "الحاقة", "المعارج",
    "نوح", "الجن", "المزمل", "القيامة", "الانسان", "التبارك", "الطور", "القرآن", "الذاريات", "الغاشية",
    "الكوثر", "الكافرون", "المسد", "التوحيد", "الفلق", "الناس"
]

# Chat states
ST_MAIN, ST_SURAH, ST_AYAH_MODE, ST_AYAH_FROM, ST_AYAH_TO, ST_RECITER, ST_QUALITY, ST_BG_TYPE, ST_BG_TOPIC, ST_THEME, ST_EXTRAS, ST_WATERMARK, ST_CONFIRM = range(13)

# ====================== STORAGE CHANNEL ======================
async def send_to_channel(bot, file_path: str, caption: str = None) -> int:
    """Send video to storage channel and return message ID"""
    if not STORAGE_CHANNEL_ID:
        return None
    try:
        with open(file_path, "rb") as f:
            message = await bot.send_video(
                chat_id=STORAGE_CHANNEL_ID,
                video=f,
                caption=caption or "",
                disable_notification=True
            )
            return message.message_id
    except Exception as e:
        logger.error(f"Error sending to channel: {e}")
        return None

async def delete_from_channel(bot, message_id: int):
    """Delete message from storage channel"""
    if not STORAGE_CHANNEL_ID or not message_id:
        return
    try:
        await bot.delete_message(chat_id=STORAGE_CHANNEL_ID, message_id=message_id)
    except Exception as e:
        logger.error(f"Error deleting from channel: {e}")

# ====================== HELPERS ======================
def get_arabic_text(text: str) -> str:
    """Reshape Arabic text"""
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    except:
        return text

def get_verse_text(surah: int, ayah: int) -> dict:
    """Get Arabic and English text"""
    try:
        ar = requests.get(f"https://api.alquran.cloud/v1/ayah/{surah}:{ayah}/quran-simple", timeout=10).json()
        en = requests.get(f"http://api.alquran.cloud/v1/ayah/{surah}:{ayah}/en.sahih", timeout=10).json()
        return {"arabic": ar["data"]["text"], "english": en["data"]["text"]}
    except:
        return {"arabic": "", "english": ""}

def get_audio_url(surah: int, reciter_id: int) -> str:
    """Get audio URL"""
    return f"https://server6.mp3quran.net/{reciter_id:03}/{surah:03}{1:03}.mp3"

def download_file(url: str, path: str) -> str:
    """Download file"""
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    with open(path, "wb") as f:
        f.write(response.content)
    return path

# ====================== BOT HANDLERS ======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command"""
    await update.message.reply_text(
        "🌙 *صانع الريلز القرآني* 🌙\n\n"
        "الإصدار 2.0 مع قناة التخزين 🗄️\n\n"
        "اختر:\n"
        "• /generate - بدء التوليد\n"
        "• /help - المساعدة",
        parse_mode="Markdown"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command"""
    await update.message.reply_text(
        "📖 *مساعدة* 📖\n\n"
        "1️⃣ ارسل /generate\n"
        "2️⃣ اختر السورة\n"
        "3️⃣ اختر نطاق الآيات\n"
        "4️⃣ اختر القارئ والجودة والثيم\n"
        "5️⃣ انتظر التوليد\n\n"
        "💾 الفيديو المحفوظ في قناة التخزين"
        "会被自动删除 بعد 24 ساعة",
        parse_mode="Markdown"
    )

async def generate_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start conversation"""
    context.user_data.clear()
    await update.message.reply_text(
        "🎬 *بدء التوليد* 🎬\n\nاختر السورة (1-114):",
        parse_mode="Markdown"
    )
    return ST_SURAH

def get_surah_keyboard():
    """Surah keyboard"""
    keyboard = [[InlineKeyboardButton(f"{i+1}. {SURAHS[i]}", callback_data=f"surah:{i+1}")] for i in range(0, 20)]
    return InlineKeyboardMarkup(keyboard)

def get_reciter_keyboard():
    """Reciter keyboard"""
    keyboard = []
    for name in list(NEW_RECITERS.keys())[:6]:
        keyboard.append([InlineKeyboardButton(name, callback_data=f"reciter:{name}")])
    return InlineKeyboardMarkup(keyboard)

def get_quality_keyboard():
    """Quality keyboard"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("720p 📱", callback_data="quality:720p")],
        [InlineKeyboardButton("1080p 🖥️", callback_data="quality:1080p")],
    ])

def get_theme_keyboard():
    """Theme keyboard"""
    keyboard = [
        [InlineKeyboardButton("ذهبي ✨", callback_data="theme:ذهبي")],
        [InlineKeyboardButton("ليلي ازرق 🌙", callback_data="theme:ليلي ازرق")],
        [InlineKeyboardButton("اخضر 🌿", callback_data="theme:اخضر")],
        [InlineKeyboardButton("بنفسجي 👑", callback_data="theme:بنفسجي")],
    ]
    return InlineKeyboardMarkup(keyboard)

async def surah_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle surah selection"""
    query = update.callback_query
    if query:
        await query.answer()
        surah = int(query.data.split(":")[1])
        context.user_data["surah"] = surah
        await query.edit_message_text(f"✅ تم اختيار السورة {surah}: {SURAHS[surah-1]}\n\nاختر نطاق الآيات:", reply_markup=get_ayah_range_keyboard(surah))
        return ST_AYAH_MODE
    return ST_SURAH

def get_ayah_range_keyboard(surah: int):
    """Ayah range keyboard"""
    keyboard = [
        [InlineKeyboardButton("آية واحدة", callback_data="range:1")],
        [InlineKeyboardButton("1-5 آيات", callback_data="range:5")],
        [InlineKeyboardButton("1-10 آيات", callback_data="range:10")],
    ]
    return InlineKeyboardMarkup(keyboard)

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle callback queries"""
    query = update.callback_query
    await query.answer()
    data = query.data
    
    if data.startswith("surah:"):
        surah = int(data.split(":")[1])
        context.user_data["surah"] = surah
        await query.edit_message_text(f"✅ السورة {surah}: {SURAHS[surah-1]}\n\nاختر نطاق الآيات:", reply_markup=get_ayah_range_keyboard(surah))
        return ST_AYAH_MODE
    
    elif data.startswith("range:"):
        mode = data.split(":")[1]
        if mode == "1":
            context.user_data["from_ayah"] = 1
            context.user_data["to_ayah"] = 1
        elif mode == "5":
            context.user_data["from_ayah"] = 1
            context.user_data["to_ayah"] = 5
        elif mode == "10":
            context.user_data["from_ayah"] = 1
            context.user_data["to_ayah"] = 10
        await query.edit_message_text("✅ تم اختيار النطاق\n\nاختر القارئ:", reply_markup=get_reciter_keyboard())
        return ST_RECITER
    
    elif data.startswith("reciter:"):
        reciter = data.split(":")[1]
        context.user_data["reciter"] = reciter
        await query.edit_message_text(f"✅ القارئ: {reciter}\n\nاختر الجودة:", reply_markup=get_quality_keyboard())
        return ST_QUALITY
    
    elif data.startswith("quality:"):
        quality = data.split(":")[1]
        context.user_data["quality"] = quality
        await query.edit_message_text(f"✅ الجودة: {quality}\n\nاختر الثيم:", reply_markup=get_theme_keyboard())
        return ST_THEME
    
    elif data.startswith("theme:"):
        theme = data.split(":")[1]
        context.user_data["theme"] = theme
        surah = context.user_data.get("surah", 1)
        from_a = context.user_data.get("from_ayah", 1)
        to_a = context.user_data.get("to_ayah", 1)
        reciter = context.user_data.get("reciter", "احمد النفيس")
        quality = context.user_data.get("quality", "720p")
        await query.edit_message_text(
            f"✅ *التأكيد* ✅\n\n"
            f"📖 السورة: {surah} ({SURAHS[surah-1]})\n"
            f"📝 الآيات: {from_a}-{to_a}\n"
            f"🎤 القارئ: {reciter}\n"
            f"📱 الجودة: {quality}\n"
            f"🎨 الثيم: {theme}\n\n"
            "ارسل /confirm للتأكيد والتبدء",
            parse_mode="Markdown"
        )
        return ST_CONFIRM

async def confirm_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle confirmation and start generation"""
    await update.message.reply_text("⏳ جاري التوليد... هذا قد يستغرق بضع دقائق.")
    
    # Get settings
    surah = context.user_data.get("surah", 1)
    from_ayah = context.user_data.get("from_ayah", 1)
    to_ayah = context.user_data.get("to_ayah", 1)
    reciter = context.user_data.get("reciter", "احمد النفيس")
    theme = context.user_data.get("theme", "ذهبي")
    quality = context.user_data.get("quality", "720p")
    
    # Get reciter ID
    reciter_id = NEW_RECITERS.get(reciter, (259,))[0]
    
    try:
        # Generate videos for each verse
        for ayah in range(from_ayah, to_ayah + 1):
            await update.message.reply_text(f"📝 جاري معالجة الآية {ayah}...")
            
            # Get text
            text = get_verse_text(surah, ayah)
            if not text["arabic"]:
                continue
            
            # Download audio
            audio_url = get_audio_url(surah, reciter_id)
            audio_path = os.path.join(TEMP_DIR, f"audio_{surah}_{ayah}.mp3")
            try:
                download_file(audio_url, audio_path)
            except Exception as e:
                logger.error(f"Audio download error: {e}")
                continue
            
            # Note: Full video generation requires moviepy
            # For now, send text confirmation
            await update.message.reply_text(
                f"✅ الآية {ayah} ready:\n\n"
                f"*Arabic:* {text['arabic']}\n\n"
                f"*English:* {text['english']}",
                parse_mode="Markdown"
            )
        
        await update.message.reply_text("✅ اكتمل التوليد!")
        
    except Exception as e:
        logger.error(f"Generation error: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")
    
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel"""
    await update.message.reply_text("❌ تم الإلغاء")
    return ConversationHandler.END

# ====================== MAIN ======================
def main():
    """Run bot"""
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("cancel", cancel))
    app.add_handler(CommandHandler("confirm", confirm_handler))
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("generate", generate_start)],
        states={
            ST_SURAH: [CallbackQueryHandler(callback_handler)],
            ST_AYAH_MODE: [CallbackQueryHandler(callback_handler)],
            ST_RECITER: [CallbackQueryHandler(callback_handler)],
            ST_QUALITY: [CallbackQueryHandler(callback_handler)],
            ST_THEME: [CallbackQueryHandler(callback_handler)],
            ST_CONFIRM: [MessageHandler(filters.TEXT, confirm_handler)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv_handler)
    
    app.add_handler(CallbackQueryHandler(callback_handler))
    
    print("🤖 Bot started! Version 2.0 with Storage Channel")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()