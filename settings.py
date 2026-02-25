# config/settings.py - إعدادات الإنشاء فقط
# المهمة الوحيدة: المسارات والإعدادات الأساسية للإنشاء
# لا تتدخل في الإدخال أو الربط

from pathlib import Path
from datetime import datetime


# ============================================================
# المسارات الأساسية
# ============================================================

PROJECT_ROOT = Path(__file__).parent.parent
DB_DIR = PROJECT_ROOT / "databases"
DB_DIR.mkdir(parents=True, exist_ok=True)

# قاعدة البيانات الجديدة (المراد إنشاؤها)
NEW_DATABASE_PATH = str(DB_DIR / "structural_database.db")

# قاعدة VEDA القديمة (مصدر البيانات - للقراءة فقط في المهام الأخرى)
VEDA_DATABASE_PATH = str(DB_DIR / "project.veda")

LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# إعدادات الإنشاء فقط
# ============================================================

# عدد الجداول المراد إنشاؤها
TOTAL_NEW_TABLES = 11

# اسم قاعدة البيانات الجديدة
NEW_DATABASE_NAME = "structural_database.db"

# حذف قاعدة البيانات القديمة عند الإنشاء؟ (اختياري)
# False = الحفاظ على البيانات القديمة إن وجدت
RECREATE_DATABASE = False


# ============================================================
# السجلات (logs)
# ============================================================

LOGS = {
    "create": str(LOG_DIR / "create_{}.log".format(datetime.now().strftime("%Y%m%d_%H%M%S"))),
}


# ============================================================
# معلومات قاعدة البيانات الجديدة (للإنشاء)
# ============================================================

NEW_DATABASE_INFO = {
    "name": NEW_DATABASE_NAME,
    "path": NEW_DATABASE_PATH,
    "total_tables": TOTAL_NEW_TABLES,
    "type": "SQLite",
    "encoding": "utf-8"
}


# ============================================================
# للتحقق من الإنشاء
# ============================================================

def get_new_database_path():
    """الحصول على مسار قاعدة البيانات الجديدة"""
    return NEW_DATABASE_PATH


def get_log_path():
    """الحصول على مسار ملف السجل"""
    return LOGS["create"]


def is_database_exists():
    """التحقق من وجود قاعدة البيانات الجديدة"""
    return Path(NEW_DATABASE_PATH).exists()
