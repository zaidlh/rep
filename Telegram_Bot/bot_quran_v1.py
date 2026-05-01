#!/usr/bin/env python3
"""
Quran Reel Maker - Telegram Bot V1
Version: 1.0 (Clean & Recommended)
"""

import os
import time
import logging
import asyncio
import requests
import json
from io import BytesIO
from functools import wraps

# Third-party
import gradio as gr
from pydub import AudioSegment
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

# telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, ConversationHandler, filters

# ====================== CONFIG ======================
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
FONT_DIR = os.path.join(BASE_DIR, "fonts")
VIDEOS_DIR = os.path.join(DATA_DIR, "videos")
VISION_DIR = os.path.join(DATA_DIR, "vision")
TEMP_DIR = os.path.join(DATA_DIR, "temp")
CACHE_DIR = os.path.join(DATA_DIR, "cache")

# Fonts
FONT_ARABIC = os.path.join(FONT_DIR, "Arabic.ttf")
FONT_ENGLISH = os.path.join(FONT_DIR, "English.otf")

# Create directories
for directory in [DATA_DIR, VIDEOS_DIR, VISION_DIR, TEMP_DIR, CACHE_DIR]:
    os.makedirs(directory, exist_ok=True)

# Configure logging
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

STUDIO_FILTER = (
    "highpass=f=60,"
    "equalizer=f=200:width_type=h:width=200:g=3,"
    "equalizer=f=8000:width_type=h:width=1000:g=2,"
    "acompressor=threshold=-21dB:ratio=4:attack=200:release=1000,"
    "extrastereo=m=1.3,"
    "loudnorm=I=-16:TP=-1.5:LRA=11"
)

# Reciters - New (from mp3quran.net)
NEW_RECITERS = {
    "احمد النفيس": (259, "https://server16.mp3quran.net/nufais/Rewayat-Hafs-A-n-Assem/"),
    "وديع اليماني": (219, "https://server6.mp3quran.net/wdee3/"),
    "بندر بليلة": (217, "https://server6.mp3quran.net/balilah/"),
    "ادريس ابكر": (12, "https://server6.mp3quran.net/abkr/"),
    "منصور السالمي": (245, "https://server14.mp3quran.net/mansor/"),
    "رعد الكردي": (221, "https://server6.mp3quran.net/kurdi/"),
    "صلاح ابوالليل": (251, "https://server11.mp3quran.net/salah/"),
    "محمود الشحات": (227, "https://server17.mp3quran.net/hisha/"),
}

# Reciters - Old (from everyayah.com)
OLD_RECITERS = {
    "ابو بكر الشاطري": "Abu_Bakr_Ash-Shaatree_128kbps",
    "ياسر الدسري": "Yasser_Ad-Dussary_128kbps",
    "عبدالرحمن السديس": "Abdurrahmaan_As-Sudais_64kbps",
    "ماهر المعيقلي": "Maher_AlMuaiqly_64kbps",
    "سعود الشريم": "Saood_ash-Shuraym_64kbps",
    "مشاري العفاسي": "Alafasy_64kbps",
    "ناصر القطامي": "Nasser_Alqatami_128kbps",
    "علي Abdul": "Abdul_Basit_128kbps",
    "علي Hassan": "Hassan_Abdul",  # Not confirmed
    "Saad Al-Ghamdi": "Saad_Al-Ghamdi_64kbps",
}

# Themes
THEMES = {
    "ذهبي": {
        "bg": (30, 20, 10),
        "text": (255, 215, 0),
        "translation": (200, 200, 200),
        "banner": (180, 140, 60),
    },
    "ليلي ازرق": {
        "bg": (10, 20, 40),
        "text": (255, 255, 255),
        "translation": (173, 216, 230),
        "banner": (25, 55, 90),
    },
    "اخضر": {
        "bg": (10, 30, 15),
        "text": (255, 255, 255),
        "translation": (144, 238, 144),
        "banner": (20, 60, 30),
    },
    "بنفسجي": {
        "bg": (40, 20, 50),
        "text": (255, 215, 0),
        "translation": (200, 180, 220),
        "banner": (60, 30, 80),
    },
    "ابيض": {
        "bg": (245, 245, 245),
        "text": (30, 30, 30),
        "translation": (80, 80, 80),
        "banner": (200, 200, 200),
    },
    "غروب": {
        "bg": (20, 10, 30),
        "text": (255, 255, 255),
        "translation": (255, 200, 150),
        "banner": (60, 30, 40),
    },
    "ازرق": {
        "bg": (0, 20, 50),
        "text": (255, 255, 255),
        "translation": (135, 206, 250),
        "banner": (0, 50, 100),
    },
    "وردي": {
        "bg": (40, 20, 35),
        "text": (255, 240, 245),
        "translation": (255, 182, 193),
        "banner": (60, 40, 50),
    },
}

# Chat states
(
    ST_MAIN, ST_SURAH, ST_AYAH_MODE, ST_AYAH_FROM, ST_AYAH_TO,
    ST_RECITER, ST_QUALITY, ST_BG_TYPE, ST_BG_TOPIC,
    ST_THEME, ST_EXTRAS, ST_WATERMARK, ST_CONFIRM
) = range(13)

# ====================== HELPERS ======================
def run_async(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))
    return wrapper

def download_file(url: str, path: str = None) -> bytes:
    """Download file from URL"""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    if path:
        with open(path, "wb") as f:
            f.write(response.content)
        return path
    return response.content

def get_arabic_text(text: str) -> str:
    """Reshape Arabic text for proper display"""
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

def get_verse_text(surah: int, ayah: int) -> dict:
    """Get Arabic text and English translation"""
    # Arabic
    ar_response = requests.get(
        f"https://api.alquran.cloud/v1/ayah/{surah}:{ayah}/quran-simple",
        timeout=10
    ).json()
    arabic = ar_response["data"]["text"]
    
    # English
    en_response = requests.get(
        f"http://api.alquran.cloud/v1/ayah/{surah}:{ayah}/en.sahih",
        timeout=10
    ).json()
    english = en_response["data"]["text"]
    
    return {"arabic": arabic, "english": english}

# Translation languages
TRANSLATIONS = {
    "en.sahih": "English (Sahih International)",
    "en.arabice": "English (Arabic)",
    "ur.rahmani": "Urdu (Rahmani)",
    "id.indonesian": "Indonesian (Bahasa)",
    "fr.le_grand": "French (Le Grand)",
    "es.translation": "Spanish",
    "de.buben": "German (Buben)",
    "tr.ozturk": "Turkish (Oz TURK)",
}

def get_translated_text(surah: int, ayah: int, lang: str = "en.sahih") -> str:
    """Get translation in specified language"""
    try:
        response = requests.get(
            f"http://api.alquran.cloud/v1/ayah/{surah}:{ayah}/{lang}",
            timeout=10
        ).json()
        return response.get("data", {}).get("text", "")
    except:
        return ""

def get_verse_timing(surah: int, reciter_id: int) -> list:
    """Get verse timing from mp3quran API"""
    try:
        response = requests.get(
            f"https://mp3quran.net/api/v3/ayat_timing?surah={surah}&read={reciter_id}",
            timeout=10
        ).json()
        return response.get("ayat", [])
    except:
        return []

def get_audio_url(surah: int, reciter_id: int, reciter_name: str = None) -> str:
    """Get audio URL for a verse"""
    if reciter_name and reciter_name in OLD_RECITERS:
        folder = OLD_RECITERS[reciter_name]
        return f"https://everyayah.com/data/{folder}/{surah:03}{1:03}.mp3"
    return f"https://server6.mp3quran.net/{reciter_id:03}/{surah:03}{1:03}.mp3"

def trim_silence(audio_path: str, silence_thresh: int = -40) -> str:
    """Trim silence from audio"""
    try:
        audio = AudioSegment.from_mp3(audio_path)
        audio = audio.strip_silence(silence_thresh=silence_thresh, padding=0)
        audio.export(audio_path, format="mp3")
    except Exception as e:
        logger.warning(f"Error trimming silence: {e}")
    return audio_path

def get_pexels_video(query: str, quality: str = "720p") -> str:
    """Download background video from Pexels"""
    for key in PEXELS_KEYS:
        try:
            headers = {"Authorization": key}
            response = requests.get(
                "https://api.pexels.com/videos/search",
                headers=headers,
                params={"query": query, "per_page": 10},
                timeout=10
            )
            if response.status_code == 200:
                videos = response.json().get("videos", [])
                if videos:
                    video_files = videos[0].get("video_files", [])
                    quality_map = {"720p": "hd", "1080p": "hd"}
                    target = quality_map.get(quality, "hd")
                    for vf in video_files:
                        if vf.get("quality") == target or vf.get("height") in [720, 1080]:
                            url = vf.get("link")
                            if url:
                                # Save to vision dir
                                filename = f"{query}_{int(time.time())}.mp4"
                                filepath = os.path.join(VISION_DIR, filename)
                                download_file(url, filepath)
                                return filepath
        except Exception as e:
            logger.warning(f"Pexels error with key: {e}")
    return None

def create_video_frame(
    text_ar: str,
    text_en: str,
    bg_color: tuple,
    text_color: tuple,
    trans_color: tuple,
    banner_color: tuple,
    duration: float,
    width: int = 720,
    height: int = 1280,
    font_size: int = 48,
    font_en_size: int = 28,
) -> Image.Image:
    """Create a single video frame with text"""
    img = Image.new("RGBA", (width, height), bg_color + (255,))
    draw = ImageDraw.Draw(img)
    
    # Load fonts
    try:
        font_ar = ImageFont.truetype(FONT_ARABIC, font_size)
        font_en = ImageFont.truetype(FONT_ENGLISH, font_en_size)
    except:
        font_ar = font_en = ImageFont.load_default()
    
    # Get Arabic text (reshaped)
    text_ar = get_arabic_text(text_ar)
    
    # Calculate positions
    # Remove Bismillah from first verse
    if text_ar.startswith("بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ"):
        if text_ar.startswith("بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ"):
            text_ar = text_ar.replace("بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ", "", 1)
    
    # Draw Arabic text (centered)
    bbox = draw.textbbox((0, 0), text_ar, font=font_ar)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x_ar = (width - text_w) // 2
    y_ar = height // 2 - 150
    draw.text((x_ar, y_ar), text_ar, font=font_ar, fill=text_color)
    
    # Draw English translation
    bbox_en = draw.textbbox((0, 0), text_en, font=font_en)
    text_en_w = bbox_en[2] - bbox_en[0]
    x_en = (width - text_en_w) // 2
    y_en = y_ar + text_h + 40
    draw.text((x_en, y_en), text_en, font=font_en, fill=trans_color)
    
    # Draw banner
    banner_h = 60
    draw.rectangle(
        [(0, height - banner_h), (width, height)],
        fill=banner_color
    )
    
    # Add vignette effect
    for i in range(50):
        alpha = int(255 * (1 - i / 50))
        overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        overlay.paste((0, 0, 0, alpha), (0, i))
        overlay.paste((0, 0, 0, alpha), (0, height - i - 1))
        overlay.paste((0, 0, 0, alpha), (0, 0, i, height))
        overlay.paste((0, 0, 0, alpha), (width - i, 0, width, height))
        img = Image.alpha_composite(img, overlay)
    
    return img

def create_verse_video(
    surah: int,
    ayah: int,
    text_ar: str,
    text_en: str,
    audio_path: str,
    theme: dict,
    bg_video_path: str = None,
    quality: str = "720p",
    watermark: str = None,
) -> str:
    """Create video for a single verse"""
    from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, ColorClip
    import moviepy.config as config
    
    # Set temp directory
    config.get_logger().setLevel(30)  # Suppress moviepy warnings
    
    # Dimensions
    dims = {"720p": (720, 1280), "1080p": (1080, 1920), "4K": (2160, 3840)}
    width, height = dims.get(quality, (720, 1280))
    
    # Create frame
    frame = create_video_frame(
        text_ar, text_en,
        theme["bg"], theme["text"], theme["translation"], theme["banner"],
        duration=5, width=width, height=height
    )
    
    frame_path = os.path.join(TEMP_DIR, f"frame_{surah}_{ayah}.png")
    frame.save(frame_path)
    
    # Load background video or create static background
    if bg_video_path and os.path.exists(bg_video_path):
        bg_clip = VideoFileClip(bg_video_path).resize((width, height))
        bg_clip = bg_clip.subclip(0, 5)
    else:
        bg_clip = ColorClip(size=(width, height), color=theme["bg"], duration=5)
    
    # Load audio
    audio = AudioFileClip(audio_path)
    
    # Create text clip from frame
    video = ImageSequenceClip([frame], duration=audio.duration)
    
    # Composite
    final = CompositeVideoClip([bg_clip, video])
    final = final.set_audio(audio)
    
    # Export
    output_path = os.path.join(TEMP_DIR, f"verse_{surah}_{ayah}.mp4")
    final.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
    
    return output_path

# ====================== BOT HANDLERS ======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command"""
    await update.message.reply_text(
        "🌙 *صانع الريلز القرآني* 🌙\n\n"
        "مرحباً! سأقوم بتوليد فيديو احترافي للآيات القرآنية.\n\n"
        "اختر_mode:\n"
        "• /generate - بدء التوليد\n"
        "• /cancel - الغاء\n"
        "• /help - المساعدة",
        parse_mode="Markdown"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command"""
    await update.message.reply_text(
        "📖 *مساعدة* 📖\n\n"
        "1️⃣ ارسل /generate للبدء\n"
        "2️⃣ اختر السورة\n"
        "3️⃣ اختر范围的 الآيات\n"
        "4️⃣ اختر القارئ\n"
        "5️⃣ اختر الجودة والثيم\n"
        "6️⃣ انتظر التوليد\n\n"
        "_ملاحظة: لا موسيقى في الفيديو_",
        parse_mode="Markdown"
    )

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel conversation"""
    await update.message.reply_text("❌ تم الالغاء")
    return ConversationHandler.END

async def generate_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start generation conversation"""
    await update.message.reply_text(
        "🎬 *بدء التوليد* 🎬\n\n"
        "اختر السورة (1-114):",
        parse_mode="Markdown"
    )
    return ST_SURAH

def get_surah_keyboard():
    """Get surah selection keyboard"""
    keyboard = []
    rows = [
        ["الفاتحة", "البقرة", "آل عمران", "النساء", "المائدة"],
        ["الانعام", "الاعراف", "الانفال", "التوبة", "يونس"],
        ["هود", "يوسف", "الرعد", "ابراهيم", "الحجر"],
        ["النحل", "الاسراء", "الكهف", "مريم", "طه"],
        ["الانبياء", "الحج", "المؤمنون", "النور", "الفرقان"],
        ["الشعراء", "النمل", "القصص", "العنكبوت", "الروم"],
        ["لقمان", "السجدة", " الاحزاب", "سبا", "فاطر"],
        [" يس", "الصافات", "ص", "الزمر", "غافر"],
        ["فصلت", "الشورى", "الزخرف", "الدخان", "الجاثية"],
        ["الاحقاف", "محمد", "الفتح", "الحجرات", "ق"],
        ["الذاريات", "الطور", "النجم", "القمر", "الرحمن"],
        ["الواقعة", "الحديد", "المجادلة", "الحشر", "الممتحنة"],
        ["الصف", "الجمعة", "المنافقون", "التغابن", "الطلاق"],
        ["التحريم", "الملك"],
    ]
    for row in rows:
        keyboard.append([InlineKeyboardButton(s, callback_data=f"surah:{s}") for s in row])
    return InlineKeyboardMarkup(keyboard)

def get_reciter_keyboard():
    """Get reciter selection keyboard"""
    keyboard = []
    # New reciters
    new_list = list(NEW_RECITERS.keys())[:6]
    for r in new_list:
        keyboard.append([InlineKeyboardButton(r, callback_data=f"reciter:{r}")])
    # Old reciters
    for r in list(OLD_RECITERS.keys())[:3]:
        keyboard.append([InlineKeyboardButton(r, callback_data=f"reciter:{r}")])
    return InlineKeyboardMarkup(keyboard)

def get_quality_keyboard():
    """Get quality selection keyboard"""
    keyboard = [
        [InlineKeyboardButton("720p", callback_data="quality:720p")],
        [InlineKeyboardButton("1080p", callback_data="quality:1080p")],
        [InlineKeyboardButton("4K", callback_data="quality:4K")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_theme_keyboard():
    """Get theme selection keyboard"""
    keyboard = [
        [InlineKeyboardButton("ذهبي ✨", callback_data="theme:ذهبي")],
        [InlineKeyboardButton("ليلي ازرق 🌙", callback_data="theme:ليلي ازرق")],
        [InlineKeyboardButton("اخضر 🌿", callback_data="theme:اخضر")],
        [InlineKeyboardButton("بنفسجي 👑", callback_data="theme:بنفسجي")],
    ]
    return InlineKeyboardMarkup(keyboard)

async def surah_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle surah selection"""
    text = update.message.text
    if text.isdigit():
        surah = int(text)
        if 1 <= surah <= 114:
            context.user_data["surah"] = surah
            await update.message.reply_text(
                f"✅ تم اختيار السورة {surah}\n\n"
                "اختر_range الآيات:",
                reply_markup=get_ayah_range_keyboard(surah)
            )
            return ST_AYAH_MODE
    await update.message.reply_text("رجاء ادخل رقماً صحيحاً (1-114)")
    return ST_SURAH

def get_ayah_range_keyboard(surah: int):
    """Get ayah range keyboard"""
    keyboard = [
        [InlineKeyboardButton("آية واحدة", callback_data="range:1")],
        [InlineKeyboardButton("الآيات 1-5", callback_data="range:5")],
        [InlineKeyboardButton("الآيات 1-10", callback_data="range:10")],
        [InlineKeyboardButton("كل السورة", callback_data="range:all")],
    ]
    return InlineKeyboardMarkup(keyboard)

# ====================== MAIN ======================
def main():
    """Run the bot"""
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("cancel", cancel))
    
    # Conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("generate", generate_start)],
        states={
            ST_SURAH: [MessageHandler(filters.TEXT & ~filters.COMMAND, surah_selection)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler)
    
    # Start polling
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()