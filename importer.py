# database/importer.py - إدراج البيانات من VEDA إلى القاعدة الجديدة
# المهمة الوحيدة: نسخ البيانات بدون أي ربط أو Foreign Keys

import sqlite3
import logging
from pathlib import Path
from datetime import datetime
from config.input_settings import COLUMN_MAPPING, COLUMNS_TO_IGNORE, TABLES_TO_IMPORT
from config.settings import VEDA_DATABASE_PATH, NEW_DATABASE_PATH


# ============================================================
# إعداد السجلات
# ============================================================

def setup_logger(log_file: str = None):
    """إعداد نظام السجلات"""
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    if log_file is None:
        log_file = log_dir / f"import_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logger = logging.getLogger("DatabaseImporter")
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
# فئة الإدراج
# ============================================================

class DatabaseImporter:
    """فئة متخصصة لإدراج البيانات من VEDA إلى القاعدة الجديدة"""
    
    def __init__(self, veda_path: str, new_path: str):
        self.veda_path = veda_path
        self.new_path = new_path
        self.veda_conn = None
        self.veda_cursor = None
        self.new_conn = None
        self.new_cursor = None
        self.import_stats = {}
    
    def connect_databases(self) -> bool:
        """الاتصال بقاعدتي البيانات"""
        try:
            # الاتصال بـ VEDA
            self.veda_conn = sqlite3.connect(self.veda_path)
            self.veda_cursor = self.veda_conn.cursor()
            logger.info(f"✅ اتصال VEDA: {self.veda_path}")
            
            # الاتصال بـ القاعدة الجديدة
            self.new_conn = sqlite3.connect(self.new_path)
            self.new_cursor = self.new_conn.cursor()
            
            # تعطيل المفاتيح الخارجية مؤقتاً
            self.new_cursor.execute("PRAGMA foreign_keys = OFF")
            self.new_conn.commit()
            
            logger.info(f"✅ اتصال القاعدة الجديدة: {self.new_path}")
            return True
        
        except Exception as e:
            logger.error(f"❌ فشل الاتصال: {e}")
            return False
    
    def get_veda_columns(self, table_name: str) -> list:
        """الحصول على أسماء الأعمدة الفعلية من VEDA"""
        try:
            self.veda_cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [row[1] for row in self.veda_cursor.fetchall()]
            return columns
        except Exception as e:
            logger.error(f"❌ خطأ في قراءة أعمدة {table_name}: {e}")
            return []
    
    def import_table(self, table_name: str) -> bool:
        """إدراج بيانات جدول واحد"""
        try:
            logger.info(f"\n   📥 إدراج {table_name}...")
            
            # الحصول على الترجمة
            mapping = COLUMN_MAPPING.get(table_name, {})
            if not mapping:
                logger.warning(f"   ⚠️ لا توجد ترجمة لـ {table_name}")
                return False
            
            # الحصول على أعمدة VEDA الفعلية
            veda_columns = self.get_veda_columns(table_name)
            if not veda_columns:
                logger.warning(f"   ⚠️ جدول {table_name} فارغ في VEDA")
                return False
            
            # بناء قائمة الأعمدة المراد نسخها
            columns_to_copy = []
            for veda_col in veda_columns:
                if veda_col in mapping:
                    new_col = mapping[veda_col]
                    # التحقق من عدم تجاهل هذا العمود
                    if not self._should_ignore(table_name, new_col):
                        columns_to_copy.append((veda_col, new_col))
            
            if not columns_to_copy:
                logger.warning(f"   ⚠️ لا توجد أعمدة قابلة للنسخ في {table_name}")
                return False
            
            # قراءة البيانات من VEDA
            veda_cols_str = ", ".join([f'"{col}"' for col, _ in columns_to_copy])
            query_veda = f'SELECT {veda_cols_str} FROM "{table_name}"'
            
            self.veda_cursor.execute(query_veda)
            rows = self.veda_cursor.fetchall()
            
            if not rows:
                logger.info(f"   ℹ️ جدول {table_name} بدون بيانات")
                self.import_stats[table_name] = 0
                return True
            
            # إدراج البيانات في القاعدة الجديدة
            new_cols = [new_col for _, new_col in columns_to_copy]
            new_cols_str = ", ".join([f'`{col}`' for col in new_cols])
            placeholders = ", ".join(["?" for _ in new_cols])
            
            insert_query = f"INSERT INTO `{table_name}` ({new_cols_str}) VALUES ({placeholders})"
            
            inserted_count = 0
            for row in rows:
                try:
                    self.new_cursor.execute(insert_query, row)
                    inserted_count += 1
                except Exception as e:
                    logger.debug(f"   ⚠️ خطأ في إدراج صف: {str(e)[:50]}")
            
            self.new_conn.commit()
            self.import_stats[table_name] = inserted_count
            logger.info(f"   ✅ {inserted_count} صف")
            
            return True
        
        except Exception as e:
            logger.error(f"   ❌ خطأ: {str(e)[:100]}")
            return False
    
    def _should_ignore(self, table_name: str, column_name: str) -> bool:
        """التحقق من أن العمود يجب تجاهله"""
        ignored = COLUMNS_TO_IGNORE.get(table_name, [])
        return column_name in ignored
    
    def import_all(self) -> bool:
        """إدراج جميع الجداول"""
        try:
            if not self.connect_databases():
                return False
            
            logger.info("\n" + "="*70)
            logger.info("📥 بدء إدراج البيانات...")
            logger.info("="*70)
            
            for table_name in TABLES_TO_IMPORT:
                self.import_table(table_name)
            
            # النتيجة
            logger.info("\n" + "="*70)
            logger.info("📊 ملخص الإدراج:")
            logger.info("="*70)
            
            total_inserted = 0
            for table_name, count in self.import_stats.items():
                logger.info(f"   {table_name}: {count} صف")
                total_inserted += count
            
            logger.info("-"*70)
            logger.info(f"إجمالي الصفوف المُدرجة: {total_inserted}")
            logger.info("="*70)
            
            return True
        
        except Exception as e:
            logger.error(f"❌ خطأ حرج: {e}")
            return False
        
        finally:
            self.close()
    
    def close(self):
        """إغلاق الاتصالات"""
        try:
            if self.veda_cursor:
                self.veda_cursor.close()
            if self.veda_conn:
                self.veda_conn.close()
            
            if self.new_cursor:
                self.new_cursor.close()
            if self.new_conn:
                self.new_conn.close()
            
            logger.info("✅ إغلاق الاتصالات")
        except Exception as e:
            logger.error(f"❌ خطأ في الإغلاق: {e}")


# ============================================================
# دالة عامة للإدراج
# ============================================================

def import_data(veda_path: str, new_path: str) -> bool:
    """
    دالة سريعة لإدراج البيانات
    
    Args:
        veda_path: مسار VEDA.db
        new_path: مسار structural_database.db
    
    Returns:
        bool: True إذا نجح، False إذا فشل
    """
    importer = DatabaseImporter(veda_path, new_path)
    return importer.import_all()
