# 🕌 Quran Reel Maker

[![Test](https://github.com/zaidlh/rep/actions/workflows/test.yml/badge.svg)](https://github.com/zaidlh/rep/actions/workflows/test.yml)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

صانع الفيديوهات القرآنية -.Generate stunning Quran video reels with Arabic text, English translations, and beautiful backgrounds.

## 🌟 Features

- **Multiple Reciters** - 16+ reciters (new and old)
- **8 Themes** - Golden, Lilac, Green, Purple, White, Sunset, Blue, Pink
- **Video Qualities** - 720p and 1080p
- **Backgrounds** - Pexels API integration
- **Professional Audio** - Studio-quality sound processing
- **Telegram Bot** - Interactive bot interface
- **Web Dashboard** - Gradio web interface

## 📁 Project Structure

```
quran-reel-maker/
├── Telegram_Bot/          # Bot versions
├── Web_Dashboard/         # Gradio app
├── Notebooks/            # Colab notebooks
├── Assets/              # Fonts and logos
└── requirements.txt
```

## 🚀 Quick Start

### Telegram Bot
```bash
pip install -r requirements.txt
python Telegram_Bot/bot_quran_v1.py
```

### Web Dashboard
```bash
pip install -r requirements.txt
python Web_Dashboard/app.py
```

## 🎨 Themes

| Theme | Colors |
|-------|--------|
| Golden ✨ | Gold text on dark brown |
| Lilac 🌙 | White + blue on lavender |
| Green 🌿 | White + light green on green |
| Purple 👑 | Gold + purple on purple |
| White ⬜ | Dark text on light background |
| Sunset 🌅 | White + gold on blue-orange gradient |
| Blue 💙 | White + sky blue on dark blue |
| Pink 💗 | White + pink on dark pink |

## 🎤 Reciters

### New Reciters (mp3quran.net)
- أحمد النفيس
- وديد اليماني
- بندر بليلة
- إدريس أبكر
- منصور السالمي
- رعد الكردي
- صلاح أبوالليل
- محمود الشحات

### Old Reciters (everyayah.com)
- أبو بكر الشاطري
- ياسر الدوسري
- عبد الرحمن السديس
- ماهر المعيقلي
- سعود الشريم
- مشاري العفاسي
- ناصر القطامي
- علي عبدالباسط
- سعد الغامدي

## 📦 Requirements

```
moviepy==1.0.3
pydub==0.25.1
requests==2.31.0
deep-translator==1.11.4
arabic-reshaper
python-bidi
numpy
Pillow==10.1
gradio==4.44.0
gdown
python-telegram-bot==20.7
```

## 🔧 Deployment

### Railway
1. Connect GitHub repo
2. Add `BOT_TOKEN` variable
3. Deploy

### Render
Use `render.yaml` for free hosting.

## 📜 License

MIT License

## 🧪 Testing on GitHub

### Automatic Tests
Tests run automatically on every push:
1. Go to **Actions** tab
2. Select **Test Quran Reel Maker**
3. Click **Run workflow**

### Manual Test
Comment on any issue/PR:
```
/test
```

### Local Testing
```bash
# Install test dependencies
pip install -r requirements.txt
sudo apt-get install -y ffmpeg imagemagick

# Run tests
python -m pytest tests/
# Or run manually
python -c "from telegram import Update; print('OK')"
```

---
صنع بـ ❤️ للقرآن
