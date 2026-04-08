# config/settings.py
from pathlib import Path

# __file__ = مسیر این فایل (config/settings.py)
# .parent = پوشه config/
# .parent.parent = ریشه پروژه (spam_detection/)
BASE_DIR = Path(__file__).parent.parent

MODEL_PATH = BASE_DIR / "models" / "spam_model.pkl"
