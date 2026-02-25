# main_link.py - المرحلة الثالثة: ربط البيانات (Foreign Keys)
# المهمة الوحيدة: استدعاء link_data() فقط

import sys
from pathlib import Path
import logging
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from database.linker import link_data
from config.settings import NEW_DATABASE_PATH, LOG_DIR


# ============================================================
# إعداد السجل
# ============================================================

def setup_logger():
    """إعداد السجل الرئيسي"""
    log_dir = Path(LOG_DIR)
    log_dir.mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger("main_link")
    logger.setLevel(logging.DEBUG)
    
    # مسح المعالجات السابقة
    logger.handlers.clear()
    
    # معالج الملف
    log_file = log_dir / f"link_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
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
    """المرحلة الثالثة: ربط البيانات"""
    
    logger.info("\n" + "="*80)
    logger.info("🚀 المرحلة الثالثة: ربط البيانات (Foreign Keys)")
    logger.info("="*80)
    
    logger.info(f"\n📁 قاعدة البيانات: {NEW_DATABASE_PATH}")
    
    # التحقق من وجود القاعدة
    if not Path(NEW_DATABASE_PATH).exists():
        logger.error(f"❌ لم يتم العثور على {NEW_DATABASE_PATH}")
        logger.error("💡 الحل: شغّل main_create.py و main_import.py أولاً")
        return 1
    
    # استدعاء المرابط
    logger.info("\n" + "-"*80)
    logger.info("🔗 بدء الربط...")
    logger.info("-"*80 + "\n")
    
    success = link_data(NEW_DATABASE_PATH)
    
    # النتيجة
    logger.info("\n" + "="*80)
    if success:
        logger.info("✅ اكتملت المرحلة الثالثة بنجاح!")
        logger.info("\n🎉 انتهت جميع المراحل!")
        logger.info("\n📊 ملخص العملية:")
        logger.info("   1️⃣ المرحلة الأولى: إنشاء القاعدة الجديدة ✅")
        logger.info("   2️⃣ المرحلة الثانية: إدراج البيانات من VEDA ✅")
        logger.info("   3️⃣ المرحلة الثالثة: ربط البيانات ✅")
        logger.info("="*80 + "\n")
        return 0
    else:
        logger.error("❌ فشلت المرحلة الثالثة!")
        logger.info("="*80 + "\n")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
