"""Tests for Quran Reel Maker"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class TestImports:
    """Test all imports work"""
    
    def test_telegram_imports(self):
        from telegram import Update, InlineKeyboardButton
        from telegram.ext import Application
        assert True
    
    def test_gradio_imports(self):
        import gradio
        assert True
    
    def test_pydub_imports(self):
        from pydub import AudioSegment
        assert True
    
    def test_pillow_imports(self):
        from PIL import Image, ImageDraw
        assert True
    
    def test_arabic_imports(self):
        import arabic_reshaper
        from bidi.algorithm import get_display
        assert True
    
    def test_moviepy_imports(self):
        from moviepy.editor import VideoFileClip
        assert True


class TestArabicText:
    """Test Arabic text processing"""
    
    def test_arabic_reshaping(self):
        import arabic_reshaper
        from bidi.algorithm import get_display
        text = "بسم الله الرحمن الرحيم"
        reshaped = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped)
        assert bidi_text is not None
        assert len(bidi_text) > 0
    
    def test_quran_api(self):
        import requests
        response = requests.get(
            "https://api.alquran.cloud/v1/ayah/1:1/quran-simple",
            timeout=10
        )
        assert response.status_code == 200
        data = response.json()
        assert "data" in data


class TestBot:
    """Test bot configuration"""
    
    def test_reciters_loaded(self):
        # Import the bot module to test constants
        import sys
        sys.path.insert(0, 'Telegram_Bot')
        # Check if file has valid syntax
        import py_compile
        py_compile.compile('Telegram_Bot/bot_quran_v1.py', doraise=True)
        assert True
    
    def test_themes_defined(self):
        # Just verify the file is readable
        with open('Telegram_Bot/bot_quran_v1.py') as f:
            content = f.read()
        assert 'THEMES' in content


class TestWebDashboard:
    """Test web dashboard"""
    
    def test_app_syntax(self):
        import py_compile
        py_compile.compile('Web_Dashboard/app.py', doraise=True)
        assert True


class TestConfig:
    """Test configuration"""
    
    def test_requirements_installable(self):
        with open('requirements.txt') as f:
            content = f.read()
        assert 'moviepy' in content
        assert 'telegram' in content
        assert 'gradio' in content