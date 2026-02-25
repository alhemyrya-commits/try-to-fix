"""
===============================================================================
utils/logger.py - إعداد مسجل الأحداث الاحترافي (مصحح شامل)
===============================================================================
"""

import logging
import logging.handlers
from pathlib import Path
from datetime import datetime
from typing import Optional


# ============================================================
# ثوابت Logger - ✅ مصحح
# ============================================================

LOG_DIR_NAME = "logs"
LOG_FILE_PREFIX = "app"
MAX_LOG_SIZE = 10 * 1024 * 1024  # 10 MB
BACKUP_COUNT = 5  # احتفظ بـ 5 نسخ احتياطية


# ============================================================
# مسجل مخصص - ✅ جديد
# ============================================================

class StructuralLogger:
    """مسجل أحداث مخصص للمشروع الهندسي"""
    
    _instances = {}  # تخزين النسخ المفردة (Singleton)
    
    def __new__(cls, name: str = __name__):
        """Singleton pattern"""
        if name not in cls._instances:
            cls._instances[name] = super().__new__(cls)
        return cls._instances[name]
    
    def __init__(self, name: str = __name__):
        """تهيئة المسجل"""
        self.logger_name = name
        self.logger = None
    
    def setup(self, log_dir: Optional[Path] = None, level: int = logging.INFO) -> logging.Logger:
        """إعداد المسجل بشكل احترافي"""
        try:
            # تحديد مسار المجلد
            if log_dir is None:
                # محاولة الوصول للمجلد الأب
                try:
                    log_dir = Path(__file__).parent.parent / LOG_DIR_NAME
                except Exception:
                    log_dir = Path(".") / LOG_DIR_NAME
            
            # إنشاء مجلد السجلات
            try:
                log_dir.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                print(f"⚠️ Warning: Could not create log directory: {e}")
                log_dir = Path(".") / LOG_DIR_NAME
                log_dir.mkdir(parents=True, exist_ok=True)
            
            # إنشاء أو الحصول على المسجل
            self.logger = logging.getLogger(self.logger_name)
            self.logger.setLevel(logging.DEBUG)  # مستوى عميق للملف
            
            # تنظيف المعالجات القديمة
            if self.logger.handlers:
                for handler in self.logger.handlers[:]:
                    self.logger.removeHandler(handler)
            
            # تنسيق مشترك - ✅ مصحح
            detailed_formatter = logging.Formatter(
                '[%(asctime)s] %(levelname)-8s [%(name)s:%(funcName)s:%(lineno)d] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            
            simple_formatter = logging.Formatter(
                '[%(asctime)s] %(levelname)-8s %(message)s',
                datefmt='%H:%M:%S'
            )
            
            # معالج الملف مع التدوير - ✅ جديد (RotatingFileHandler)
            try:
                log_file = log_dir / f"{LOG_FILE_PREFIX}_{datetime.now().strftime('%Y%m%d')}.log"
                
                file_handler = logging.handlers.RotatingFileHandler(
                    log_file,
                    maxBytes=MAX_LOG_SIZE,
                    backupCount=BACKUP_COUNT,
                    encoding='utf-8'
                )
                file_handler.setLevel(logging.DEBUG)
                file_handler.setFormatter(detailed_formatter)
                self.logger.addHandler(file_handler)
            except Exception as e:
                print(f"⚠️ Warning: Could not setup file handler: {e}")
            
            # معالج الشاشة - ✅ مصحح
            try:
                console_handler = logging.StreamHandler()
                console_handler.setLevel(level)
                console_handler.setFormatter(simple_formatter)
                self.logger.addHandler(console_handler)
            except Exception as e:
                print(f"⚠️ Warning: Could not setup console handler: {e}")
            
            # تجنب الانتشار المزدوج
            self.logger.propagate = False
            
            self.logger.info(f"✓ Logger initialized successfully")
            return self.logger
        
        except Exception as e:
            print(f"❌ Critical error setting up logger: {e}")
            # إرجاع logger افتراضي في حالة الفشل
            basic_logger = logging.getLogger(self.logger_name)
            basic_logger.setLevel(logging.INFO)
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s %(message)s'))
            basic_logger.addHandler(console_handler)
            return basic_logger


# ============================================================
# دالة الإعداد الرئيسية - ✅ مصحح
# ============================================================

def setup_logger(
    name: str = __name__,
    log_dir: Optional[Path] = None,
    level: int = logging.INFO
) -> logging.Logger:
    """
    إعداد مسجل الأحداث بشكل احترافي
    
    Args:
        name: اسم المسجل
        log_dir: مجلد السجلات (اختياري)
        level: مستوى logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Logger instance
    
    مثال:
        >>> logger = setup_logger(__name__)
        >>> logger.info("تم بدء البرنامج")
        >>> logger = setup_logger("database", log_dir=Path("./logs/db"))
    """
    try:
        # استخدام Singleton pattern
        struct_logger = StructuralLogger(name)
        return struct_logger.setup(log_dir=log_dir, level=level)
    
    except Exception as e:
        print(f"❌ Error in setup_logger: {e}")
        # إرجاع logger افتراضي
        basic_logger = logging.getLogger(name)
        basic_logger.setLevel(logging.INFO)
        return basic_logger


# ============================================================
# دوال مساعدة - ✅ جديدة
# ============================================================

def get_logger(name: str = __name__) -> logging.Logger:
    """
    الحصول على مسجل موجود بدون إعادة تهيئة
    
    Args:
        name: اسم المسجل
    
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


def set_log_level(logger: logging.Logger, level: int) -> None:
    """
    تغيير مستوى logging للمسجل
    
    Args:
        logger: المسجل
        level: المستوى الجديد
    """
    try:
        logger.setLevel(level)
        for handler in logger.handlers:
            handler.setLevel(level)
        logger.info(f"✓ Log level changed to {logging.getLevelName(level)}")
    except Exception as e:
        print(f"Error changing log level: {e}")


def log_exception(logger: logging.Logger, message: str = "") -> None:
    """
    تسجيل استثناء مع المعلومات الكاملة
    
    Args:
        logger: المسجل
        message: رسالة إضافية
    """
    try:
        if message:
            logger.error(f"Exception: {message}", exc_info=True)
        else:
            logger.error("An exception occurred", exc_info=True)
    except Exception as e:
        print(f"Error logging exception: {e}")


# ============================================================
# Logger مخصص لأجزاء مختلفة - ✅ جديد
# ============================================================

def get_database_logger() -> logging.Logger:
    """الحصول على logger لقاعدة البيانات"""
    return setup_logger("database")


def get_importer_logger() -> logging.Logger:
    """الحصول على logger للاستيراد"""
    return setup_logger("importer")


def get_validation_logger() -> logging.Logger:
    """الحصول على logger للتحقق من البيانات"""
    return setup_logger("validation")


def get_models_logger() -> logging.Logger:
    """الحصول على logger للنماذج"""
    return setup_logger("models")


# ============================================================
# معالج مخصص لرسائل الأخطاء - ✅ جديد
# ============================================================

class ErrorFilter(logging.Filter):
    """مصفاة مخصصة لرسائل الأخطاء"""
    
    def filter(self, record: logging.LogRecord) -> bool:
        """تصفية السجلات"""
        if record.levelno >= logging.ERROR:
            # إضافة معلومات إضافية للأخطاء
            record.status = "❌"
        elif record.levelno >= logging.WARNING:
            record.status = "⚠️"
        else:
            record.status = "✓"
        return True


# ============================================================
# مثال على الاستخدام - ✅ جديد
# ============================================================

if __name__ == "__main__":
    # إعداد logger رئيسي
    main_logger = setup_logger("main", level=logging.DEBUG)
    
    # اختبار المستويات المختلفة
    main_logger.debug("هذه رسالة debug")
    main_logger.info("✓ تم بدء البرنامج")
    main_logger.warning("⚠️ تحذير: قد تكون هناك مشكلة")
    main_logger.error("❌ حدث خطأ ما")
    
    # إعداد loggers متعددة
    db_logger = get_database_logger()
    db_logger.info("✓ تم الاتصال بقاعدة البيانات")
    
    import_logger = get_importer_logger()
    import_logger.info("✓ بدء الاستيراد من Excel")
    
    # تغيير مستوى logging
    set_log_level(main_logger, logging.WARNING)
    
    main_logger.info("هذه الرسالة لن تظهر (مستوى WARNING)")
    main_logger.warning("هذه الرسالة ستظهر (مستوى WARNING)")
