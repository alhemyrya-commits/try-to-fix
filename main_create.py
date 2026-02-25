# main_create.py - المرحلة الأولى: إنشاء قاعدة البيانات الفارغة
# المهمة الوحيدة: استدعاء initialize_database() فقط

import sys
from pathlib import Path
import logging
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from database.initializer import initialize_database
from config.settings import NEW_DATABASE_PATH, LOG_DIR


# ============================================================
# إعداد السجل
# ============================================================
def setup_logger():
    """إعداد السجل الرئيسي"""
    log_dir = Path(LOG_DIR)
    log_dir.mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger("main_create")
    logger.setLevel(logging.DEBUG)
    
    # مسح المعالجات السابقة
    logger.handlers.clear()
    
    # معالج الملف
    log_file = log_dir / f"create_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    # معالج الكونسول
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # الصيغة
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


logger = setup_logger()


# ============================================================
# البرنامج الرئيسي
# ============================================================

def main():
    """المرحلة الأولى: إنشاء قاعدة البيانات الفارغة"""
    
    logger.info("\n" + "="*80)
    logger.info("🚀 المرحلة الأولى: إنشاء قاعدة البيانات الفارغة")
    logger.info("="*80)
    
    logger.info(f"\n📁 المسار: {NEW_DATABASE_PATH}")
    logger.info(f"📊 الجداول: 11 جدول")
    
    # استدعاء initializer
    logger.info("\n" + "-"*80)
    logger.info("🔧 بدء الإنشاء...")
    logger.info("-"*80 + "\n")
    
    success = initialize_database(NEW_DATABASE_PATH)
    
    # النتيجة
    logger.info("\n" + "="*80)
    if success:
        logger.info("✅ اكتملت المرحلة الأولى بنجاح!")
        logger.info("\n🎯 الخطوة التالية: main_import.py")
        logger.info("="*80 + "\n")
        return 0
    else:
        logger.error("❌ فشلت المرحلة الأولى!")
        logger.info("="*80 + "\n")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
