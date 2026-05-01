# 🕌 Quran Reel Maker

<div align="center">

[![Test](https://github.com/zaidlh/rep/actions/workflows/test.yml/badge.svg)](https://github.com/zaidlh/rep/actions/workflows/test.yml)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![HuggingFace](https://img.shields.io/badge/Deploy-HuggingFace-blue.svg)](https://huggingface.co/spaces)

**Quran Reel Maker** — Create stunning video reels from Quran verses with Arabic text, translations, and beautiful backgrounds.

[📖 About](#about) • [🚀 Quick Start](#quick-start) • [📁 Features](#features) • [🚀 Deploy](#deployment) • [🤝 Contribute](CONTRIBUTING.md)

</div>

---

## 📖 About

**Quran Reel Maker** is a powerful tool for creating professional Quran video reels. Generate beautiful videos with Arabic text, multiple translations, and professional audio from renowned reciters.

### Key Features
- 🎬 Beautiful video frames with Arabic text and translations
- 🔊 Professional audio from 16+ reciters
- 🎨 8 stunning themes
- 🌍 8 translation languages
- 📱 Telegram bot + Web Dashboard
- 🐳 Docker support
- ☁️ Deploy to Railway, Render, HuggingFace

---

## 🚀 Quick Start

### Local
```bash
# Install
pip install -r requirements.txt

# Telegram Bot
python Telegram_Bot/bot_quran_v1.py

# Web Dashboard
python Web_Dashboard/app.py
```

### Google Colab (No installation needed)

1. Upload `Notebooks/QuranVideoGenerator_Colab.ipynb` to [colab.research.google.com](https://colab.research.google.com)
2. Run each cell sequentially
3. Click the Gradio link to generate videos

**Or use directly from GitHub:**
```python
# In Colab, run this to load from GitHub:
!git clone https://github.com/zaidlh/rep.git
%cd rep/Notebooks
```

---

### Colab Notebooks

| Notebook | Description |
|----------|-------------|
| `QuranVideoGenerator_Colab.ipynb` | Full video generator with Gradio UI |
| `QuranBot_Telegram_Colab.ipynb` | Run Telegram bot from Colab |
| `Deploy_To_Railway.ipynb` | Deployment guide |

**⚠️ Note:** Colab disconnects after ~12 hours (free tier). Use keep-alive script in browser console:
```javascript
setInterval(() => {
  document.querySelector("colab-toolbar-button#connect")?.click();
}, 60000);
```

---

## 📁 Features

- **Multiple Reciters** - 16+ reciters (new and old)
- **8 Themes** - Golden, Lilac, Green, Purple, White, Sunset, Blue, Pink
- **Video Qualities** - 720p, 1080p, 4K
- **Translation Languages** - English, Urdu, Indonesian, French, Spanish, German, Turkish
- **Backgrounds** - Pexels API integration
- **Professional Audio** - Studio-quality sound processing
- **Telegram Bot** - Interactive bot interface
- **Web Dashboard** - Gradio web interface
- **Docker** - Dockerfile and docker-compose
- **CI/CD** - GitHub Actions testing

---

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

---

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

---

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

---

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

---

## 🐳 Docker

```bash
# Build
docker build -t quran-bot .

# Run
docker run -e BOT_TOKEN=your_token quran-bot

# Or use docker-compose
docker-compose up -d
```

---

## 🚀 Deployment

### 1. HuggingFace Spaces (Recommended - Free)

**Option A: Web UI**
1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click **Create New Space**
3. Select **Gradio** as SDK
4. Choose **Space Hardware**: CPU (free)
5. Under **Repository**, select GitHub repo (`zaidlh/rep`)
6. Under **Branch**, select `quran-reel-maker-v1`
7. Add secrets if needed:
   - `BOT_TOKEN` = your Telegram bot token
8. Click **Create Space**

**Option B: Clone & Push**
```bash
# Install HF CLI
pip install huggingface_hub

# Login
huggingface-cli login

# Clone your repo
git clone https://huggingface.co/spaces/yourusername/quran-reel-maker

# Copy Web Dashboard files
cp -r Web_Dashboard/* quran-reel-maker/
cp requirements.txt quran-reel-maker/
cp huggingface.yaml quran-reel-maker/space.py  # if using Gradio

# Push
cd quran-reel-maker
git add .
git commit -m "initial"
git push
```

**Hardware:** Free CPU available

---

### 2. Railway
1. Go to [railway.app](https://railway.app)
2. Connect GitHub → Select repo
3. Add `BOT_TOKEN` variable
4. Deploy

---

### 3. Render (Free)
1. Go to [render.com](https://render.com)
2. Connect GitHub → Select repo
3. Use `render.yaml`
4. Add `BOT_TOKEN`
5. Deploy

---

### 4. Docker (Any cloud)
```bash
# Build
docker build -t quran-bot .

# Run
docker run -e BOT_TOKEN=your_token quran-bot

# Or use docker-compose
docker-compose up -d
```

---

## 📜 License

MIT License

---

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

# Run syntax check
python -m py_compile Telegram_Bot/bot_quran_v1.py
python -m py_compile Web_Dashboard/app.py

# Test imports
python -c "from telegram import Update; print('OK')"
```

---

صنع بـ ❤️ للقرآن