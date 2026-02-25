# database/initializer.py - إنشاء الجداول الفارغة فقط
# المهمة الوحيدة: قراءة schema.py وإنشاء الجداول

import sqlite3
import logging
from pathlib import Path
from datetime import datetime
from database.schema import get_create_tables_sql, get_alter_tables_sql, split_sql_statements


# ============================================================
# إعداد السجلات
# ============================================================

def setup_logger(log_file: str = None):
    """إعداد نظام السجلات"""
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    if log_file is None:
        log_file = log_dir / f"create_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logger = logging.getLogger("DatabaseInitializer")
    logger.setLevel(logging.DEBUG)
    
    # مسح المعالجات السابقة
    logger.handlers.clear()
    
    # معالج الملف
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    # معالج الكونسول
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


logger = setup_logger()


# ============================================================
# فئة إنشاء قاعدة البيانات
# ============================================================

class DatabaseInitializer:
    """فئة متخصصة لإنشاء قاعدة البيانات الجديدة بالجداول الفارغة"""
    
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.conn = None
        self.cursor = None
        self.tables_created = []
        self.tables_failed = []
    
    def ensure_directory(self) -> bool:
        """التأكد من وجود مجلد قاعدة البيانات"""
        try:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            logger.info(f"✅ مجلد قاعدة البيانات: {self.db_path.parent}")
            return True
        except Exception as e:
            logger.error(f"❌ فشل إنشاء المجلد: {e}")
            return False
    
    def connect_database(self) -> bool:
        """الاتصال بقاعدة البيانات"""
        try:
            self.conn = sqlite3.connect(str(self.db_path))
            self.cursor = self.conn.cursor()
            
            # تعطيل المفاتيح الخارجية مؤقتاً (أثناء الإنشاء)
            self.cursor.execute("PRAGMA foreign_keys = OFF")
            self.conn.commit()
            
            logger.info(f"✅ اتصال قاعدة البيانات: {self.db_path}")
            return True
        except Exception as e:
            logger.error(f"❌ فشل الاتصال: {e}")
            return False
    
    def create_tables(self) -> bool:
        """إنشاء جميع الجداول من schema.py"""
        try:
            logger.info("\n" + "="*70)
            logger.info("🏗️  إنشاء الجداول الفارغة...")
            logger.info("="*70)
            
            # الحصول على جميع جمل SQL من CREATE_TABLES_SQL
            create_sql = get_create_tables_sql()
            statements = split_sql_statements(create_sql)
            
            for statement in statements:
                if statement.strip():
                    try:
                        # استخراج اسم الجدول من SQL
                        table_name = self._extract_table_name(statement)
                        
                        self.cursor.execute(statement)
                        self.tables_created.append(table_name)
                        logger.info(f"   ✅ {table_name}")
                    except Exception as e:
                        table_name = self._extract_table_name(statement)
                        self.tables_failed.append((table_name, str(e)))
                        logger.error(f"   ❌ {table_name}: {str(e)[:50]}")
                        return False
            
            self.conn.commit()
            logger.info("="*70)
            logger.info(f"✅ تم إنشاء {len(self.tables_created)} جدول")
            logger.info("="*70)
            
            return True
        
        except Exception as e:
            logger.error(f"❌ خطأ: {e}")
            return False
    
    def _extract_table_name(self, sql_statement: str) -> str:
        """استخراج اسم الجدول من جملة SQL"""
        try:
            # البحث عن CREATE TABLE IF NOT EXISTS `table_name`
            import re
            match = re.search(r'CREATE TABLE IF NOT EXISTS [`"]?(\w+)[`"]?', sql_statement, re.IGNORECASE)
            if match:
                return match.group(1)
            return "Unknown"
        except:
            return "Unknown"
    
    def enable_foreign_keys(self) -> bool:
        """تفعيل المفاتيح الخارجية"""
        try:
            self.cursor.execute("PRAGMA foreign_keys = ON")
            self.conn.commit()
            logger.info("✅ تفعيل المفاتيح الخارجية")
            return True
        except Exception as e:
            logger.error(f"❌ خطأ في تفعيل المفاتيح: {e}")
            return False
    
    def verify_tables(self):
        """التحقق من الجداول المُنشأة"""
        try:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in self.cursor.fetchall()]
            return len(tables), sorted(tables)
        except Exception as e:
            logger.error(f"❌ خطأ في التحقق: {e}")
            return 0, []
    
    def initialize(self) -> bool:
        """تنفيذ الإنشاء الكامل"""
        try:
            if not self.ensure_directory():
                return False
            
            if not self.connect_database():
                return False
            
            if not self.create_tables():
                return False
            
            if not self.enable_foreign_keys():
                return False
            
            # التحقق من النتيجة
            count, tables = self.verify_tables()
            
            logger.info(f"\n✅ اكتملت عملية الإنشاء!")
            logger.info(f"   📁 قاعدة البيانات: {self.db_path}")
            logger.info(f"   📊 الجداول المُنشأة: {count}")
            
            if count > 0:
                logger.debug(f"   الجداول: {', '.join(tables)}")
            
            return True
        
        except Exception as e:
            logger.error(f"❌ خطأ حرج: {e}")
            return False
        finally:
            self.close()
    
    def close(self):
        """إغلاق الاتصال"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
            logger.info("✅ إغلاق الاتصال")
        except Exception as e:
            logger.error(f"❌ خطأ في الإغلاق: {e}")


# ============================================================
# دالة عامة للإنشاء
# ============================================================

def initialize_database(db_path: str) -> bool:
    """
    دالة سريعة لتهيئة قاعدة البيانات الجديدة
    
    Args:
        db_path: مسار قاعدة البيانات الجديدة
    
    Returns:
        bool: True إذا نجح، False إذا فشل
    """
    initializer = DatabaseInitializer(db_path)
    return initializer.initialize()
