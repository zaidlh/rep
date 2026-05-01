#!/usr/bin/env python3
"""
Quran Reel Maker - Web Dashboard (Gradio)
Personal Control Panel
"""

import os
import time
import logging
import requests
from io import BytesIO
from datetime import datetime

import gradio as gr
from pydub import AudioSegment
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, ColorClip, ImageSequenceClip

# ====================== CONFIG ======================
# Base paths
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
VIDEOS_DIR = os.path.join(BASE_DIR, "videos")
VISION_DIR = os.path.join(BASE_DIR, "vision")
TEMP_DIR = os.path.join(BASE_DIR, "temp")
CACHE_DIR = os.path.join(BASE_DIR, "cache")

# Create directories
for directory in [BASE_DIR, VIDEOS_DIR, VISION_DIR, TEMP_DIR, CACHE_DIR]:
    os.makedirs(directory, exist_ok=True)

# Fonts
FONT_ARABIC = os.path.join(FONT_DIR, "Arabic.ttf")
FONT_ENGLISH = os.path.join(FONT_DIR, "English.otf")

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ====================== CONSTANTS ======================
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

NEW_RECITERS = {
    "احمد النفيس": (259, "https://server16.mp3quran.net/nufais/"),
    "وديع اليماني": (219, "https://server6.mp3quran.net/wdee3/"),
    "بندر بليلة": (217, "https://server6.mp3quran.net/balilah/"),
    "ادريس ابكر": (12, "https://server6.mp3quran.net/abkr/"),
    "منصور السالمي": (245, "https://server14.mp3quran.net/mansor/"),
    "رعد الكردي": (221, "https://server6.mp3quran.net/kurdi/"),
}

OLD_RECITERS = {
    "ابو بكر الشاطري": "Abu_Bakr_Ash-Shaatree_128kbps",
    "ياسر الدسري": "Yasser_Ad-Dussary_128kbps",
    "عبدالرحمن السديس": "Abdurrahmaan_As_Sudais_64kbps",
    "ماهر المعيقلي": "Maher_AlMuaiqly_64kbps",
    "سعود الشريم": "Saood_ash_Shuraym_64kbps",
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

PEXELS_KEYS = [
    "AmAgE0J5AuBbsvR6dmG7qQLIc5uYZvDim2Vx250F5QoHNKnGdCofFerx",
    "Fv0qzUGYwbGr6yHsauaXuNKiNR9L7OE7VLr5Wq6SngcLjavmkCEAskb2",
    "1NK8BaBXGsXm4Uxzcesxm0Jxh2yCILOwqqsj4GiM57dXcb7b8bbDYyOu",
    "C9KJNtJET2wAnmD42Gbu0OolTlmhoT02CX7fyst3kKEvnjRRWLiAqQ9t",
]

BG_TOPICS = ["nature", "mosque", "islamic", "sky", "clouds", "stars", "desert", "sea", "forest", "mountains"]

# ====================== HELPERS ======================
def get_arabic_text(text: str) -> str:
    """Reshape Arabic text"""
    try:
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
    except Exception as e:
        logger.error(f"Error getting verse text: {e}")
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

def create_text_frame(text_ar: str, text_en: str, theme: dict, width: int = 720, height: int = 1280) -> Image.Image:
    """Create text frame image"""
    img = Image.new("RGBA", (width, height), theme["bg"] + (255,))
    draw = ImageDraw.Draw(img)
    
    # Load fonts
    try:
        font_ar = ImageFont.truetype(FONT_ARABIC, 48)
        font_en = ImageFont.truetype(FONT_ENGLISH, 28)
    except:
        font_ar = font_en = ImageFont.load_default()
    
    # Reshape Arabic
    text_ar = get_arabic_text(text_ar)
    
    # Remove Bismillah from non-Fatiha first verse
    bismillah = "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ"
    if text_ar.startswith(bismillah.rstrip()):
        text_ar = text_ar.replace(bismillah, "", 1)
    
    # Draw Arabic text
    bbox = draw.textbbox((0, 0), text_ar, font=font_ar)
    text_w = bbox[2] - bbox[0]
    x_ar = (width - text_w) // 2
    y_ar = height // 2 - 150
    draw.text((x_ar, y_ar), text_ar, font=font_ar, fill=theme["text"])
    
    # Draw English
    bbox_en = draw.textbbox((0, 0), text_en, font=font_en)
    text_en_w = bbox_en[2] - bbox_en[0]
    x_en = (width - text_en_w) // 2
    y_en = y_ar + (bbox[3] - bbox[1]) + 40
    draw.text((x_en, y_en), text_en, font=font_en, fill=theme["translation"])
    
    # Banner
    banner_h = 60
    draw.rectangle([(0, height - banner_h), (width, height)], fill=theme["banner"])
    
    return img

def create_video(surah: int, from_ayah: int, to_ayah: int, reciter: str, quality: str, theme_name: str, bg_type: str, bg_topic: str) -> str:
    """Create video"""
    # Get reciter ID
    reciter_id = NEW_RECITERS.get(reciter, (259,))[0]
    theme = THEMES.get(theme_name, THEMES["ذهبي"])
    
    dims = {"720p": (720, 1280), "1080p": (1080, 1920)}
    width, height = dims.get(quality, (720, 1280))
    
    output_path = os.path.join(VIDEOS_DIR, f"quran_{surah}_{from_ayah}_{to_ayah}_{int(time.time())}.mp4")
    
    clips = []
    
    for ayah in range(from_ayah, to_ayah + 1):
        # Get text
        text = get_verse_text(surah, ayah)
        if not text["arabic"]:
            continue
        
        # Download audio
        audio_url = get_audio_url(surah, reciter_id)
        audio_path = os.path.join(CACHE_DIR, f"audio_{surah}_{ayah}.mp3")
        if not os.path.exists(audio_path):
            try:
                download_file(audio_url, audio_path)
            except:
                continue
        
        # Create frame
        frame = create_text_frame(text["arabic"], text["english"], theme, width, height)
        frame_path = os.path.join(TEMP_DIR, f"frame_{surah}_{ayah}.png")
        frame.save(frame_path)
        
        # Load audio
        audio = AudioFileClip(audio_path)
        
        # Create video clip
        video = ImageSequenceClip([frame_path], duration=audio.duration)
        video = video.set_audio(audio)
        
        clips.append(video)
    
    if not clips:
        raise ValueError("No verses to process")
    
    # Concatenate
    from moviepy.editor import concatenate_videoclips
    final_video = concatenate_videoclips(clips)
    final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
    
    # Clean temp
    for f in os.listdir(TEMP_DIR):
        try:
            os.remove(os.path.join(TEMP_DIR, f))
        except:
            pass
    
    return output_path

# ====================== GRADIO UI ======================
def create_ui():
    """Create Gradio interface"""
    
    with gr.Blocks(title="صانع الريلز القرآني", theme=gr.themes.Soft()) as app:
        gr.Markdown("# 🌙 صانع الريلز القرآني\n## Quran Reel Maker")
        
        with gr.Row():
            with gr.Column():
                surah = gr.Dropdown(label="السورة", choices=[f"{i+1}. {SURAHS[i]}" for i in range(114)], value="1. الفاتحة")
                from_ayah = gr.Slider(label="من آية", minimum=1, maximum=10, value=1, step=1)
                to_ayah = gr.Slider(label="إلى آية", minimum=1, maximum=10, value=1, step=1)
            
            with gr.Column():
                reciter = gr.Dropdown(label="القارئ", choices=list(NEW_RECITERS.keys()) + list(OLD_RECITERS.keys()), value="احمد النفيس")
                quality = gr.Radio(label="الجودة", choices=["720p", "1080p"], value="720p")
                theme = gr.Dropdown(label="الثيم", choices=list(THEMES.keys()), value="ذهبي")
            
            with gr.Column():
                bg_type = gr.Radio(label="نوع الخلفية", choices=["solid", "pexels"], value="solid")
                bg_topic = gr.Dropdown(label="موضوع الخلفية", choices=BG_TOPICS, value="nature")
        
        generate_btn = gr.Button("🎬 توليد الفيديو", variant="primary")
        
        status = gr.Textbox(label="الحالة", interactive=False)
        output = gr.Video(label="النتيجة")
        
        with gr.Row():
            download_btn = gr.Button("📥 تحميل", variant="secondary")
        
        def generate(surah_name, from_a, to_a, reciter_name, quality_val, theme_name, bg_t, bg_tpc):
            try:
                # Parse surah number
                surah_num = int(surah_name.split(".")[0])
                
                # Validate
                if from_a > to_a:
                    return "❌ خطأ: من آية أكبر من إلى آية", None
                
                yield "⏳ جاري التوليد...", None
                
                # Generate video
                video_path = create_video(
                    surah_num, from_a, to_a,
                    reciter_name, quality_val,
                    theme_name, bg_t, bg_tpc
                )
                
                yield "✅ اكتمل التوليد!", video_path
                
            except Exception as e:
                logger.error(f"Generation error: {e}")
                yield f"❌ خطأ: {str(e)}", None
        
        generate_btn.click(
            generate,
            inputs=[surah, from_ayah, to_ayah, reciter, quality, theme, bg_type, bg_topic],
            outputs=[status, output]
        )
        
        def download_video(video_path):
            if video_path and os.path.exists(video_path):
                return video_path
            return None
        
        download_btn.click(download_video, inputs=[output], outputs=[output])
        
        gr.Markdown("---")
        gr.Markdown("*لا موسيقى | الفيديوهات تُحفظ محلياً*")
    
    return app

# ====================== MAIN ======================
if __name__ == "__main__":
    # Check fonts
    if not os.path.exists(FONT_ARABIC):
        logger.warning(f"Font not found: {FONT_ARABIC}")
        logger.info("Download fonts from: https://drive.google.com/drive/folders/1kSiHCRcznwUd1pU_pNaKdXx_y-hcRuIw")
    
    # Create app
    app = create_ui()
    
    # Get port
    port = int(os.environ.get("PORT", "7860"))
    
    print(f"🌐 Starting Gradio on port {port}...")
    app.launch(server_name="0.0.0.0", server_port=port)