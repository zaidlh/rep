# 🕌 صانع الريلز القرآني — دليل المشروع الكامل


> ملف مرجعي شامل لإعادة بناء المشروع كاملاً من الصفر في أي وقت.


---

## 📁 هيكل المشروع


```
quran-reel-maker/
│
├── 📓 Notebooks (Google Colab)
│   ├── QuranVideoGenerator_Colab.ipynb   ← واجهة Gradio لتوليد الفيديو
│   ├── QuranBot_Telegram_Colab.ipynb     ← تشغيل بوت تيليجرام من Colab
│   └── Deploy_To_Railway.ipynb           ← رفع المشروع على GitHub + Railway تلقائياً
│
├── 🤖 Telegram Bot
│   ├── bot_quran_v1.py                   ← النسخة الأولى (نظيفة، موصى بها)
│   └── bot_quran_v2.py                   ← النسخة الثانية (قناة تخزين + تقسيم أجزاء)
│
├── 🌐 Web Dashboard (Gradio)
│   ├── app.py                            ← لوحة التحكم الشخصية
│   ├── requirements.txt
│   ├── Procfile
│   ├── nixpacks.toml
│   └── runtime.txt
│
├── 🎨 Assets
│   ├── quran_bot_logo.svg                ← لوغو البوت والقناة
│   └── fonts/
│       ├── Arabic.ttf                    ← خط عربي (حمّله من Drive)
│       └── English.otf                   ← خط إنجليزي
│
└── PROJECT_GUIDE.md                      ← هذا الملف
```


---

## 🔑 المتغيرات المطلوبة


| المتغير | الوصف | كيف تحصل عليه |
|---------|-------|--------------|
| `BOT_TOKEN` | توكن بوت تيليجرام | من [@BotFather](https://t.me/BotFather) |
| `GITHUB_TOKEN` | Personal Access Token لـ GitHub | github.com → Settings → Developer settings → Tokens |
| `GITHUB_USERNAME` | اسم مستخدمك على GitHub | من صفحتك الشخصية |
| `STORAGE_CHANNEL_ID` | ID قناة تيليجرام للتخزين (اختياري) | انظر القسم أدناه |
| `PEXELS_API_KEY` | مفتاح Pexels للخلفيات (اختياري) | [pexels.com/api](https://www.pexels.com/api/) |


### كيف تحصل على STORAGE_CHANNEL_ID من الهاتف
1. أنشئ قناة خاصة في تيليجرام
2. أضف البوت كـ Admin في القناة
3. افتح [@userinfobot](https://t.me/userinfobot) وأرسل له forward من القناة
4. الرقم الذي يرد به (يبدأ بـ `-100`) هو الـ ID


---


## 📦 المتطلبات


### `requirements.txt`
```
moviepy==1.0.3
pydub==0.25.1
requests==2.31.0
deep-translator==1.11.4
arabic-reshaper
python-bidi
numpy
Pillow==10.1
decorator==4.4.2
proglog==0.1.10
gradio==4.44.0
gdown
python-telegram-bot==20.7
PyGithub
```


### متطلبات النظام
```bash
# Ubuntu / Debian (Railway, Render, Oracle Cloud)
apt-get install -y ffmpeg imagemagick
```


### `nixpacks.toml` (لـ Railway)
```toml
[phases.setup]
nixPkgs = ["ffmpeg", "imagemagick"]
```


### `runtime.txt`
```
python-3.10.12
```


---


## 🎨 الخطوط


الخطوط محفوظة على Google Drive:
- **Folder ID:** `1kSiHCRcznwUd1pU_pNaKdXx_y-hcRuIw`
- **Arabic.ttf** ← الخط العربي الرئيسي
- **English.otf** ← خط الترجمة الإنجليزية


### تحميلها في Colab
```python
import gdown, shutil, os


FOLDER_ID = "1kSiHCRcznwUd1pU_pNaKdXx_y-hcRuIw"
DL_DIR    = "/content/drive_dl"
FONT_DIR  = "/content/app/fonts"   # أو ./fonts للـ web app


os.makedirs(DL_DIR, exist_ok=True)
os.makedirs(FONT_DIR, exist_ok=True)


gdown.download_folder(id=FOLDER_ID, output=DL_DIR, quiet=True, use_cookies=False)


for root, _, files in os.walk(DL_DIR):
    for fname in files:
        if fname.lower().endswith((".ttf", ".otf")):
            shutil.copy2(os.path.join(root, fname), os.path.join(FONT_DIR, fname))
            print(f"✅ {fname}")
```


---


## 🔧 الإعدادات الثابتة في الكود


### مسارات الملفات
```python
import os


# للـ Colab
BASE_DIR    = "/content/app"


# للـ web app / Railway
BASE_DIR    = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


FONT_DIR    = os.path.join(BASE_DIR, "fonts")       # أو ./fonts بجانب app.py
FONT_ARABIC = os.path.join(FONT_DIR, "Arabic.ttf")
FONT_ENGLISH= os.path.join(FONT_DIR, "English.otf")
VIDEOS_DIR  = os.path.join(BASE_DIR, "videos")
VISION_DIR  = os.path.join(BASE_DIR, "vision")      # خلفيات Pexels المحفوظة
TEMP_DIR    = os.path.join(BASE_DIR, "temp")
```


### مفاتيح Pexels المدمجة
```python
PEXELS_KEYS = [
    "AmAgE0J5AuBbsvR6dmG7qQLIc5uYZvDim2Vx250F5QoHNKnGdCofFerx",
    "Fv0qzUGYwbGr6yHsauaXuNKiNR9L7OE7VLr5Wq6SngcLjavmkCEAskb2",
    "1NK8BaBXGsXm4Uxzcesxm0Jxh2yCILOwqqsj4GiM57dXcb7b8bbDYyOu",
    "C9KJNtJET2wAnmD42Gbu0OolTlmhoT02CX7fyst3kKEvnjRRWLiAqQ9t",
]
```


### فلتر الصوت (Studio)
```python
STUDIO_FILTER = (
    "highpass=f=60,"
    "equalizer=f=200:width_type=h:width=200:g=3,"
    "equalizer=f=8000:width_type=h:width=1000:g=2,"
    "acompressor=threshold=-21dB:ratio=4:attack=200:release=1000,"
    "extrastereo=m=1.3,"
    "loudnorm=I=-16:TP=-1.5:LRA=11"
)
```


### القراء
```python
NEW_RECITERS = {
    "احمد النفيس"   : (259, "https://server16.mp3quran.net/nufais/Rewayat-Hafs-A-n-Assem/"),
    "وديع اليماني"  : (219, "https://server6.mp3quran.net/wdee3/"),
    "بندر بليلة"    : (217, "https://server6.mp3quran.net/balilah/"),
    "ادريس أبكر"    : (12,  "https://server6.mp3quran.net/abkr/"),
    "منصور السالمي" : (245, "https://server14.mp3quran.net/mansor/"),
    "رعد الكردي"    : (221, "https://server6.mp3quran.net/kurdi/"),
}
OLD_RECITERS = {
    "أبو بكر الشاطري"  : "Abu_Bakr_Ash-Shaatree_128kbps",
    "ياسر الدوسري"     : "Yasser_Ad-Dussary_128kbps",
    "عبدالرحمن السديس" : "Abdurrahmaan_As-Sudais_64kbps",
    "ماهر المعيقلي"    : "Maher_AlMuaiqly_64kbps",
    "سعود الشريم"      : "Saood_ash-Shuraym_64kbps",
    "مشاري العفاسي"    : "Alafasy_64kbps",
    "ناصر القطامي"     : "Nasser_Alqatami_128kbps",
}
# OLD_RECITERS مصدرها: everyayah.com
# NEW_RECITERS مصدرها: mp3quran.net (مع timing API)
```


### APIs المستخدمة
| الخدمة | الـ URL | الاستخدام |
|---------|---------|-----------|
| AlQuran Cloud | `https://api.alquran.cloud/v1/ayah/{s}:{a}/quran-simple` | النص العربي |
| AlQuran Cloud EN | `http://api.alquran.cloud/v1/ayah/{s}:{a}/en.sahih` | الترجمة الإنجليزية |
| mp3quran Timing | `https://mp3quran.net/api/v3/ayat_timing?surah={s}&read={id}` | توقيت الآيات |
| everyayah | `https://everyayah.com/data/{reciter}/{s:03}{a:03}.mp3` | صوت القراء القدامى |
| Pexels Videos | `https://api.pexels.com/videos/search` | خلفيات الفيديو |


---


## 🎬 منطق توليد الفيديو


```
لكل آية:
  1. تحميل الصوت (mp3quran أو everyayah)
  2. تقليم الصمت من البداية والنهاية
  3. جلب النص العربي من AlQuran Cloud
  4. جلب الترجمة الإنجليزية
  5. رسم النص على صورة RGBA شفافة
  6. دمج الطبقات: خلفية + تعتيم + vignette + نص عربي + ترجمة + بانر + عداد + علامة مائية
  7. تصدير المقطع


بعد كل الآيات:
  8. دمج كل المقاطع بـ concatenate_videoclips
  9. تصدير mp4 مؤقت
  10. تطبيق فلتر الصوت بـ ffmpeg
  11. حفظ الملف النهائي
```


### الجودات المدعومة
| الجودة | الأبعاد | Scale |
|--------|---------|-------|
| 720p | 720×1280 | 0.67 |
| 1080p | 1080×1920 | 1.0 |


---


## 🤖 بوت تيليجرام


### الملفات
| الملف | الوصف |
|-------|-------|
| `bot_quran_v1.py` | النسخة الأولى — نظيفة وبسيطة ✅ |
| `bot_quran_v2.py` | النسخة الثانية — قناة تخزين + حذف تلقائي |


### حالات المحادثة (13 حالة)
```
ST_MAIN → ST_SURAH → ST_AYAH_MODE → ST_AYAH_FROM/TO
       → ST_RECITER → ST_QUALITY → ST_BG_TYPE → ST_BG_TOPIC
       → ST_THEME → ST_EXTRAS → ST_WATERMARK → ST_CONFIRM → [توليد]
```


### تعديل BOT_TOKEN
```python
# في أعلى الملف:
BOT_TOKEN = "ضع_توكنك_هنا"


# أو من متغير البيئة (لـ Railway):
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
```


### تشغيل محلي
```bash
python bot_quran_v1.py
```


---


## 🌐 Web App (Gradio)


### الملف
`app.py` — لوحة تحكم شخصية كاملة


### تشغيل محلي
```bash
pip install -r requirements.txt
python app.py
# افتح: http://localhost:7860
```


### `Procfile` (للنشر)
```
web: python app.py
```


### متغيرات البيئة للـ web app
```
PORT=7860          # منفذ التشغيل (Railway يضبطه تلقائياً)
APP_BASE_DIR=./data  # مجلد البيانات
```


---


## 📓 Notebooks


### 1. `QuranVideoGenerator_Colab.ipynb`
واجهة Gradio كاملة تعمل مباشرة في Colab.


**خلاياه بالترتيب:**
| # | المهمة |
|---|--------|
| 1 | تثبيت المتطلبات (ثم Restart) |
| 2 | تحميل الخطوط من Google Drive |
| 3 | المكتبات + الإعدادات + البيانات |
| 4 | الصوت والنص |
| 5 | الخلفيات + منشئ الفيديو |
| 6 | واجهة Gradio (شغّله وانتظر الرابط) |
| 7 | تحميل الفيديوهات |


---


### 2. `QuranBot_Telegram_Colab.ipynb`
تشغيل بوت تيليجرام من Colab بدون جهاز.


**خلاياه بالترتيب:**
| # | المهمة |
|---|--------|
| 1 | تثبيت المتطلبات |
| 2 | تحميل الخطوط |
| 3 | ضع BOT_TOKEN هنا |
| 4 | كتابة كود البوت تلقائياً |
| 5 | تشغيل البوت + keep-alive |
| 6 | تحميل الفيديوهات |


**keep-alive للـ Colab (يمنع القطع):**
```javascript
// في Console المتصفح (F12)
function keepAlive() {
    let btn = document.querySelector("colab-toolbar-button#connect");
    if (btn) btn.click();
    document.dispatchEvent(new KeyboardEvent("keydown", { keyCode: 32 }));
}
setInterval(keepAlive, 1000 * 55);
```
> ⚠️ الحد الأقصى في Colab المجاني = ~12 ساعة


---


### 3. `Deploy_To_Railway.ipynb`
يرفع كل الملفات على GitHub تلقائياً ثم يعطيك رابط Railway.


**خلاياه:**
| # | المهمة |
|---|--------|
| 1 | تثبيت المتطلبات + PyGithub |
| 2 | تحميل الخطوط |
| 3 | BOT_TOKEN + GITHUB_TOKEN + GITHUB_USERNAME |
| 4 | رفع كل الملفات على GitHub تلقائياً |
| 5 | تعليمات Railway + التوكن جاهز للنسخ |


---


## 🚂 النشر على Railway


### الخطوات
1. ارفع المجلد على GitHub (عبر Notebook أو GitHub Desktop)
2. افتح [railway.app](https://railway.app) وسجّل دخول بـ GitHub
3. **New Project → Deploy from GitHub repo**
4. اختر الـ repo
5. اذهب إلى **Variables** وأضف:


```
BOT_TOKEN          = توكن_البوت
STORAGE_CHANNEL_ID = -1001234567890   (اختياري)
```


6. اضغط **Deploy** ✅


### ملاحظات Railway
- الخطة المجانية: **500 ساعة/شهر** (~21 يوم
- التخزين: **لا يُحفظ** بعد إعادة التشغيل — استخدم قناة تيليجرام للحفظ
- ffmpeg: يُثبَّت تلقائياً عبر `nixpacks.toml`


---


## 🔄 Render.com (بديل مجاني بلا حد ساعات)


### `render.yaml`
```yaml
services:
  - type: worker
    name: quran-bot
    runtime: python
    buildCommand: apt-get install -y ffmpeg imagemagick && pip install -r requirements.txt
    startCommand: python bot_quran_v1.py
    envVars:
      - key: BOT_TOKEN
        sync: false
```


```


## 🏆 Oracle Cloud (مجاني للأبد — الأقوى)


```bash
# بعد إنشاء VM على cloud.oracle.com
sudo apt-get update
sudo apt-get install -y ffmpeg imagemagick python3-pip git


git clone https://github.com/اسمك/quran-bot
cd quran-bot
pip3 install -r requirements.txt


# تشغيل دائم مع systemd
sudo nano /etc/systemd/system/quranbot.service
```


```ini
[Unit]
Description=Quran Bot
After=network.target


[Service]
ExecStart=/usr/bin/python3 /home/ubuntu/quran-bot/bot_quran_v1.py
Restart=always
RestartSec=10
Environment=BOT_TOKEN=توكنك_هنا


[Install]
WantedBy=multi-user.target
```


```bash
sudo systemctl enable quranbot
sudo systemctl start quranbot
sudo systemctl status quranbot
```


---


## 🎨 اللوغو


الملف: `quran_bot_logo.svg`


**تحويله لـ PNG (512×512) من الهاتف:**
1. افتح [cloudconvert.com](https://cloudconvert.com)
2. ارفع `quran_bot_logo.svg`
3. حدد الحجم 512×512
4. حمّل PNG ✅


**ضبطه في تيليجرام:**
- **البوت:** @BotFather → `/mybots` → Edit Bot Photo
- **القناة:** افتح القناة → Edit → صورة القناة


```


## ⚡ مقارنة خيارات الاستضافة


| الخيار | مجاني | يتوقف؟ | RAM | ffmpeg | الأنسب لـ |
|--------|-------|---------|-----|--------|-----------|
| **Railway** | 500h/شهر | لا | 512MB | ✅ | البوت + الويب |
| **Render** | ✅ بلا حد | لا | 512MB | ✅ | البوت |
| **Oracle Cloud** | ✅ للأبد | لا | 24GB | ✅ | كل شيء |
| **Google Cloud** | ✅ للأبد | لا | 0.6GB | ✅ | البوت الخفيف |
| **Colab** | ✅ | بعد 12h | 12GB | ✅ | الاختبار |
| **InfinityFree** | ✅ | لا | — | ❌ | PHP فقط ❌ |


```


## 🔁 الثيمات المتوفرة


| الثيم | الألوان |
|-------|---------|
| ذهبي ✨ | نص ذهبي على خلفية بنية داكنة |
| ليلي أزرق 🌙 | نص أبيض + أزرق على خلفية كحلية |
| أخضر 🌿 | نص أبيض + أخضر فاتح على خلفية خضراء |
| بدونجي 👑 | نص ذهبي + بدونجي على خلفية بدونجية |
| أبيض ⬜ | نص داكن على خلفية فاتحة |
| غروب 🌅 | نص أبيض + ذهبي على تدرج ليلي-برتقالي |


```


## 📝 ملاحظات مهمة


- ❌ **لا موسيقى** — محذوفة من كل الملفات
- ✅ **البسملة** تُحذف تلقائياً من أول آية في السور (عدا الفاتحة والتوبة)
- ✅ **الصوت** يُعالَج بفلتر Studio احترافي
- ✅ **النص العربي** يستخدم arabic-reshaper + bidi لعرض صحيح
- ✅ **الخلفيات** تُحفظ في VISION_DIR لتجنب إعادة التحميل
- ✅ **الصوت** يُحفظ في cache/ لتجنب إعادة التحميل
- ⚠️ **railway** لا يحفظ الملفات بعد restart — استخدم قناة تيليجرام


```


## 🆘 حل المشاكل الشائعة


| المشكلة | الحل |
|---------|------|
| `No module named 'arabic_reshaper'` | `pip install arabic-reshaper python-bidi` |
| `ffmpeg not found` | `apt-get install -y ffmpeg` |
| خط يظهر مربعات | تحقق من مسار `Arabic.ttf` |
| `Pillow ANTIALIAS error` | `pip install "Pillow==10.1"` |
| فيديو بلا صوت | تحقق من `ffmpeg` + `pydub` |
| خطأ Pexels 403 | المفاتيح المدمجة انتهت، أضف مفتاحك الخاص |
| Railway يتوقف بعد restart | الملفات لا تُحفظ — أضف `STORAGE_CHANNEL_ID` |


```


*آخر تحديث: 2026 — المشروع مكتمل وجاهز للنشر*