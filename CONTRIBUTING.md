# Contributing to Quran Reel Maker

Welcome! Thanks for your interest in contributing.

## 🌍 Quick Start

```bash
# Clone the repo
git clone https://github.com/zaidlh/rep.git
cd rep

# Create a branch
git checkout -b feature/my-feature

# Install dependencies
pip install -r requirements.txt

# Test locally
python Telegram_Bot/bot_quran_v1.py
```

## 📋 Ways to Contribute

### 🐛 Report Bugs
- Use GitHub Issues
- Include reproduction steps
- Include error messages

### 💡Suggest Features
- Open a GitHub Issue
- Describe the feature
- Explain why it's useful

### 📝 Code Contributions
1. Fork the repo
2. Create a branch
3. Make your changes
4. Test locally
5. Submit a PR

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Test specific file
python -m pytest tests/test_quran.py

# Syntax check
python -m py_compile Telegram_Bot/bot_quran_v1.py
```

## 📝 Coding Standards

- Use meaningful variable names
- Comment complex logic
- Keep functions small (< 100 lines)
- Use type hints where helpful

## 🌍 Translation

To add a new translation:
1. Find the translation ID from [alquran.cloud](https://api.alquran.cloud)
2. Add to `TRANSLATIONS` dict in bot file

## 🎨 Adding Themes

Add new themes in the `THEMES` dict:
```python
THEMES = {
    "theme_name": {
        "bg": (R, G, B),
        "text": (R, G, B),
        "translation": (R, G, B),
        "banner": (R, G, B),
    },
}
```

## 📤 Pull Request Process

1. Update README.md if needed
2. Ensure tests pass
3. Update the PROJECT_GUIDE.md if adding features
4. Submit PR with clear description

## 📜 License

By contributing, you agree that your code will be under the MIT License.