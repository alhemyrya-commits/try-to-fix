"""
===============================================================================
database/vedaimporter.py - مستورد VEDA (المرحلة 2️⃣: الإدخال فقط - النسخة النهائية)
===============================================================================

المسؤولية الوحيدة: استيراض البيانات من VEDA إلى قاعدة البيانات الجديدة
- اقرأ من VEDA بـ Name/Material/Label (بدون ID)
- ادخل البيانات في جميع الجداول (11 جدول)
- اترك جميع حقول FK ID = NULL (سيتم ملؤها في link-tables.py)

⚠️ IMPORTANT:
- فقط إدخال البيانات
- اترك FK ID فارغة (NULL)
- بدون ربط جداول
"""

import sqlite3
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime

# ============================================================
# إعداد السجلات
# ============================================================

def setup_logger(log_dir: str = "logs"):
    """إعداد نظام السجلات"""
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger("VedaImporter")
    logger.setLevel(logging.DEBUG)
    
    # معالج الملف
    log_file = log_path / f"veda_import_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
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
# ترتيب الاستيراج الصحيح (11 جدول)
# ============================================================

IMPORT_ORDER = [
    # المرحلة 1: جداول أساسية (بدون تبعيات)
    ("Genralinput", "Genralinput"),
    ("Story_Definitions", "Story_Definitions"),
    ("Material_Properties_Concrete_Data", "Material_Properties_Concrete_Data"),
    ("Load_Combination_Definitions", "Load_Combination_Definitions"),
    
    # المرحلة 2: جداول تعتمد على الأساسية
    ("Material_Properties_Rebar_Data", "Material_Properties_Rebar_Data"),
    ("Frame_Section_Property_Definitions_Concrete_Rectangular", "Frame_Section_Property_Definitions_Concrete_Rectangular"),
    
    # المرحلة 3: جداول متقدمة
    ("Frame_Section_Property_Definitions_Concrete_Column_Reinforcing", "Frame_Section_Property_Definitions_Concrete_Column_Reinforcing"),
    ("Objects_and_Elements_Joints", "Objects_and_Elements_Joints"),
    
    # المرحلة 4: جداول الربط والقوى
    ("Frame_Assignments_Section_Properties", "Frame_Assignments_Section_Properties"),
    ("Column_Object_Connectivity", "Column_Object_Connectivity"),
    ("Element_Forces_Columns", "Element_Forces_Columns"),
]

# ============================================================
# فئة مستورد VEDA
# ============================================================

class VedaImporter:
    """استيراج البيانات من VEDA إلى قاعدة البيانات الجديدة"""
    
    def __init__(self, veda_path: str, db_path: str):
        self.veda_path = veda_path
        self.db_path = db_path
        self.veda_conn = None
        self.db_conn = None
        self.stats = {
            'tables_processed': 0,
            'total_inserted': 0,
            'total_errors': 0,
            'table_details': {}
        }
    
    def connect(self) -> bool:
        """الاتصال بقاعدتي البيانات"""
        try:
            # التحقق من وجود ملف VEDA
            if not Path(self.veda_path).exists():
                logger.error(f"❌ ملف VEDA غير موجود: {self.veda_path}")
                return False
            
            # الاتصال بـ VEDA (للقراءة فقط)
            self.veda_conn = sqlite3.connect(f"file:{self.veda_path}?mode=ro", uri=True)
            self.veda_conn.row_factory = sqlite3.Row
            logger.info(f"✅ تم الاتصال بـ VEDA: {self.veda_path}")
            
            # الاتصال بقاعدة البيانات المستهدفة
            if not Path(self.db_path).exists():
                logger.error(f"❌ قاعدة البيانات غير موجودة: {self.db_path}")
                return False
            
            self.db_conn = sqlite3.connect(self.db_path)
            self.db_conn.row_factory = sqlite3.Row
            self.db_conn.execute("PRAGMA foreign_keys = OFF")  # تعطيل FK مؤقتاً
            logger.info(f"✅ تم الاتصال بقاعدة البيانات: {self.db_path}")
            
            return True
        
        except Exception as e:
            logger.error(f"❌ خطأ في الاتصال: {e}")
            return False
    
    def get_veda_columns(self, table_name: str) -> List[str]:
        """الحصول على أسماء أعمدة جدول VEDA"""
        try:
            cursor = self.veda_conn.cursor()
            cursor.execute(f"PRAGMA table_info([{table_name}])")
            columns = [row[1] for row in cursor.fetchall()]
            return columns
        except Exception as e:
            logger.warning(f"⚠️ خطأ في قراءة أعمدة {table_name}: {e}")
            return []
    
    def get_db_columns(self, table_name: str) -> List[str]:
        """الحصول على أسماء أعمدة جدول DB"""
        try:
            cursor = self.db_conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [row[1] for row in cursor.fetchall()]
            return columns
        except Exception as e:
            logger.warning(f"⚠️ خطأ في قراءة أعمدة {table_name}: {e}")
            return []
    
    def map_columns(self, veda_columns: List[str], db_columns: List[str]) -> Dict[str, str]:
        """ربط أعمدة VEDA مع أعمدة DB"""
        mapping = {}
        
        for db_col in db_columns:
            # تخطي ID
            if db_col in ['ID', 'id']:
                continue
            
            # ابحث عن تطابق مباشر
            if db_col in veda_columns:
                mapping[db_col] = db_col
            else:
                # ابحث عن تطابق بحثي
                for veda_col in veda_columns:
                    if veda_col.lower() == db_col.lower():
                        mapping[db_col] = veda_col
                        break
        
        return mapping
    
    def import_single_table(self, veda_table: str, db_table: str) -> Tuple[int, int]:
        """استيراج جدول واحد"""
        
        inserted = 0
        errors = 0
        
        try:
            logger.info(f"\n📥 استيراج {veda_table} → {db_table}")
            
            # قراءة من VEDA
            veda_cursor = self.veda_conn.cursor()
            veda_cursor.execute(f"SELECT * FROM [{veda_table}]")
            veda_rows = veda_cursor.fetchall()
            veda_columns = [desc[0] for desc in veda_cursor.description]
            
            if not veda_rows:
                logger.info(f"   ⓘ لا توجد بيانات في VEDA")
                return 0, 0
            
            logger.info(f"   📖 عدد الصفوف: {len(veda_rows)}")
            
            # الحصول على أعمدة DB
            db_columns = self.get_db_columns(db_table)
            
            # ربط الأعمدة
            column_mapping = self.map_columns(veda_columns, db_columns)
            
            if not column_mapping:
                logger.warning(f"   ⚠️ لم يتم العثور على أعمدة متطابقة")
                return 0, len(veda_rows)
            
            logger.debug(f"   🔗 أعمدة مربوطة: {len(column_mapping)}")
            
            # معالجة كل صف
            db_cursor = self.db_conn.cursor()
            
            for row_idx, veda_row in enumerate(veda_rows, 1):
                try:
                    # تحويل الصف إلى قاموس
                    row_dict = dict(veda_row)
                    
                    # إنشاء قاموس الإدراج
                    insert_dict = {}
                    
                    for db_col, veda_col in column_mapping.items():
                        value = row_dict.get(veda_col)
                        insert_dict[db_col] = value
                    
                    if not insert_dict:
                        errors += 1
                        logger.debug(f"   صف {row_idx}: لا توجد بيانات")
                        continue
                    
                    # بناء جملة INSERT
                    columns_str = ", ".join(f'"{col}"' for col in insert_dict.keys())
                    placeholders = ", ".join(["?"] * len(insert_dict))
                    values = tuple(insert_dict.values())
                    
                    insert_query = f"INSERT INTO {db_table} ({columns_str}) VALUES ({placeholders})"
                    
                    # إدراج الصف
                    db_cursor.execute(insert_query, values)
                    inserted += 1
                    
                except Exception as e:
                    errors += 1
                    logger.debug(f"   صف {row_idx}: {str(e)[:60]}")
            
            # التأكيد
            self.db_conn.commit()
            logger.info(f"   ✅ تم إدراج: {inserted} صف | ❌ أخطاء: {errors}")
            
            return inserted, errors
        
        except Exception as e:
            logger.error(f"   ❌ خطأ في الاستيراج: {e}")
            self.db_conn.rollback()
            return 0, 1
    
    def print_summary(self):
        """طباعة ملخص الاستيراج"""
        logger.info("\n" + "="*70)
        logger.info("📋 ملخص الاستيراج")
        logger.info("="*70)
        
        logger.info(f"\n✅ إجمالي المُدرجات: {self.stats['total_inserted']}")
        logger.info(f"❌ إجمالي الأخطاء: {self.stats['total_errors']}")
        
        logger.info("\n📊 تفاصيل الجداول:")
        for table, details in self.stats['table_details'].items():
            inserted = details['inserted']
            errors = details['errors']
            status = "✅" if errors == 0 else "⚠️"
            logger.info(f"   {status} {table:<50} | ✓: {inserted:<5} | ✗: {errors:<5}")
        
        logger.info("\n" + "="*70)
    
    def run(self) -> bool:
        """تنفيذ الاستيراج الكامل"""
        try:
            logger.info("\n" + "="*70)
            logger.info("🚀 بدء استيراج البيانات من VEDA")
            logger.info("="*70)
            
            # الاتصال
            if not self.connect():
                return False
            
            # استيراج الجداول بالترتيب
            for veda_table, db_table in IMPORT_ORDER:
                try:
                    inserted, errors = self.import_single_table(veda_table, db_table)
                    self.stats['tables_processed'] += 1
                    self.stats['total_inserted'] += inserted
                    self.stats['total_errors'] += errors
                    self.stats['table_details'][db_table] = {
                        'inserted': inserted,
                        'errors': errors
                    }
                except Exception as e:
                    logger.error(f"❌ خطأ في {db_table}: {e}")
                    self.stats['total_errors'] += 1
            
            # ملخص النتائج
            self.print_summary()
            
            # تفعيل المفاتيح الخارجية مرة أخرى
            self.db_conn.execute("PRAGMA foreign_keys = ON")
            
            logger.info("\n✅ اكتمل الاستيراج!")
            return True
        
        except Exception as e:
            logger.error(f"❌ خطأ حرج: {e}")
            return False
        finally:
            self.cleanup()
    
    def cleanup(self):
        """إغلاق الاتصالات"""
        try:
            if self.veda_conn:
                self.veda_conn.close()
            if self.db_conn:
                self.db_conn.close()
            logger.info("🔚 تم إغلاق الاتصالات")
        except Exception as e:
            logger.error(f"❌ خطأ في الإغلاق: {e}")

# ============================================================
# نقطة الدخول
# ============================================================

if __name__ == "__main__":
    from config.settings import DATABASE_PATH, VEDA_PATH
    
    logger.info("\n" + "="*70)
    logger.info("🔧 برنامج استيراج البيانات من VEDA")
    logger.info("="*70)
    
    importer = VedaImporter(VEDA_PATH, DATABASE_PATH)
    success = importer.run()
    
    if success:
        logger.info("\n✅ اكتمل الاستيراج بنجاح!")
        logger.info("⏭️  الخطوة القادمة: تشغيل link-tables.py")
    else:
        logger.error("\n❌ فشل الاستيراج!")
