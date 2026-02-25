# main_import.py - المرحلة الثانية: إدراج البيانات من VEDA
# المهمة الوحيدة: استدعاء import_data() فقط

import sys
from pathlib import Path
import logging
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from database.importer import import_data
from config.settings import VEDA_DATABASE_PATH, NEW_DATABASE_PATH, LOG_DIR


# ============================================================
# إعداد السجل
# ============================================================

def setup_logger():
    """إعداد السجل الرئيسي"""
    log_dir = Path(LOG_DIR)
    log_dir.mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger("main_import")
    logger.setLevel(logging.DEBUG)
    
    # مسح المعالجات السابقة
    logger.handlers.clear()
    
    # معالج الملف
    log_file = log_dir / f"import_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
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
    """المرحلة الثانية: إدراج البيانات من VEDA"""
    
    logger.info("\n" + "="*80)
    logger.info("🚀 المرحلة الثانية: إدراج البيانات من VEDA")
    logger.info("="*80)
    
    logger.info(f"\n📂 المصدر: {VEDA_DATABASE_PATH}")
    logger.info(f"📁 الهدف: {NEW_DATABASE_PATH}")
    
    # التحقق من وجود VEDA
    if not Path(VEDA_DATABASE_PATH).exists():
        logger.error(f"❌ لم يتم العثور على {VEDA_DATABASE_PATH}")
        return 1
    
    # التحقق من وجود القاعدة الجديدة
    if not Path(NEW_DATABASE_PATH).exists():
        logger.error(f"❌ لم يتم العثور على {NEW_DATABASE_PATH}")
        logger.error("💡 الحل: شغّل main_create.py أولاً")
        return 1
    
    # استدعاء المُدرِج
    logger.info("\n" + "-"*80)
    logger.info("🔄 بدء الإدراج...")
    logger.info("-"*80 + "\n")
    
    success = import_data(VEDA_DATABASE_PATH, NEW_DATABASE_PATH)
    
    # النتيجة
    logger.info("\n" + "="*80)
    if success:
        logger.info("✅ اكتملت المرحلة الثانية بنجاح!")
        logger.info("\n🎯 الخطوة التالية:")
        logger.info("   python main_link.py")
        logger.info("="*80 + "\n")
        return 0
    else:
        logger.error("❌ فشلت المرحلة الثانية!")
        logger.info("="*80 + "\n")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
