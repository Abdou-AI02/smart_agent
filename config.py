import os

# إعدادات Ollama
OLLAMA_MODEL = "mistral:latest"
OLLAMA_HOST = "http://localhost:11434"

# مسارات الملفات
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
MEMORY_FILE = os.path.join(DATA_DIR, "agent_memory.json")
USER_CONFIG_FILE = os.path.join(DATA_DIR, "user_config.json")
HELP_FILE = os.path.join(os.path.dirname(__file__), "docs", "help.md")

# التأكد من وجود مجلد البيانات
os.makedirs(DATA_DIR, exist_ok=True)

# إعدادات الذاكرة
MAX_MEMORY_SIZE = 10

# إعدادات اللغات المدعومة
SUPPORTED_LANGUAGES = ["en", "ar"]

# إعدادات OCR
# مسار Tesseract-OCR على Windows
TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# مسار Tesseract-OCR على macOS (قد يختلف)
# TESSERACT_CMD = '/usr/local/bin/tesseract'

# إعدادات الأمان
# مسارات المجلدات التي سيتم فحصها بحثًا عن ملفات مشبوهة
SUSPICIOUS_PATHS = [
    os.path.expanduser('~/Downloads'),
]

# إعدادات إدارة الملفات (جديد)
DEFAULT_SCAN_PATH = os.path.expanduser('~')