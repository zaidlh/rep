# 🕌 Quran Reel Maker

<div align="center">

[![Test](https://github.com/zaidlh/rep/actions/workflows/test.yml/badge.svg)](https://github.com/zaidlh/rep/actions/workflows/test.yml)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![HuggingFace](https://img.shields.io/badge/Deploy-HuggingFace-blue.svg)](https://huggingface.co/spaces)

**Quran Reel Maker** - Generate stunning Quran video reels with Arabic text, translations, and beautiful backgrounds.

[📖 Quick Start](#-quick-start) • [📁 Features](#-features) • [🚀 Deploy](#-deployment) • [🤝 Contribute](CONTRIBUTING.md)

</div>

## 🌟 Features

- **Multiple Reciters** - 16+ reciters (new and old)
- **8 Themes** - Golden, Lilac, Green, Purple, White, Sunset, Blue, Pink
- **Video Qualities** - 720p, 1080p, 4K
- **8 Translation Languages** - English, Urdu, Indonesian, French, Spanish, German, Turkish
- **Backgrounds** - Pexels API integration
- **Professional Audio** - Studio-quality sound processing
- **Telegram Bot** - Interactive bot interface
- **Web Dashboard** - Gradio web interface
- **Docker** - Dockerfile and docker-compose
- **CI/CD** - GitHub Actions testing

## 📁 Project Structure

```
quran-reel-maker/
├── Telegram_Bot/          # Bot versions
├── Web_Dashboard/         # Gradio app
├── Notebooks/            # Google Colab notebooks
│   ├── QuranVideoGenerator_Colab.ipynb
│   ├── QuranBot_Telegram_Colab.ipynb
│   └── Deploy_To_Railway.ipynb
├── Assets/              # Fonts and logos
├── tests/               # Pytest tests
├── render.yaml          # Render.com deployment
├── Dockerfile          # Docker build
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

## 🐳 Docker

```bash
# Build
docker build -t quran-bot .

# Run
docker run -e BOT_TOKEN=your_token quran-bot

# Or use docker-compose
docker-compose up -d
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

### Docker
Use `Dockerfile` or `docker-compose.yml`.

### HuggingFace Spaces
1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Create **New Space**
3. Select **Gradio** or **Docker** SDK
4. Link your GitHub repo
5. Add secrets (`BOT_TOKEN` if needed)
6. Click **Duplicate** to make it private

**Or via CLI:**
```bash
# Install huggingface_hub
pip install huggingface_hub

# Login
huggingface-cli login

# Create space
huggingface-cli space create quran-reel-maker

# Push to space
git clone https://huggingface.co/spaces/yourusername/quran-reel-maker
cp -r Telegram_Bot/* quran-reel-maker/
cd quran-reel-maker && git add . && git commit -m "init" && git push
```

**Hardware:** Free CPU available

## 📜 License

MIT License

## 🧪 Testing on GitHub

### Automatic Tests
Tests run automatically on every push:
1. Go to **Actions** tab
2. Select **Test Quran Reel Maker**
3. View test results

### Local Testing

```bash
# Install test dependencies
pip install -r requirements.txt
sudo apt-get install -y ffmpeg imagemagick

# Run syntax check
python -m py_compile Telegram_Bot/bot_quran_v1.py
python -m py_compile Web_Dashboard/app.py

# Test imports
python -c "from telegram import Update; print('OK')"
```

---
صنع بـ ❤️ للقرآن
