# database/linker.py - تنفيذ الروابط (Foreign Keys)
# المهمة الوحيدة: ملء الأعمدة المفقودة وتفعيل الروابط

import sqlite3
import logging
from pathlib import Path
from datetime import datetime
from config.link_settings import ALL_LINKS, DIRECT_LINKS, ID_FILL_LINKS, ID_FILL_COMPLEX_LINKS, STATIC_ID_LINKS, VALIDATION_LINKS
from config.settings import NEW_DATABASE_PATH


# ============================================================
# إعداد السجلات
# ============================================================

def setup_logger(log_file: str = None):
    """إعداد نظام السجلات"""
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    if log_file is None:
        log_file = log_dir / f"link_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logger = logging.getLogger("DatabaseLinker")
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
# فئة الربط
# ============================================================

class DatabaseLinker:
    """فئة متخصصة لربط البيانات بين الجداول"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.link_stats = {}
    
    def connect(self) -> bool:
        """الاتصال بقاعدة البيانات"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            logger.info(f"✅ اتصال قاعدة البيانات: {self.db_path}")
            return True
        except Exception as e:
            logger.error(f"❌ فشل الاتصال: {e}")
            return False
    
    def disable_foreign_keys(self):
        """تعطيل المفاتيح الخارجية مؤقتاً"""
        try:
            self.cursor.execute("PRAGMA foreign_keys = OFF")
            self.conn.commit()
            logger.info("⏸️ تعطيل المفاتيح الخارجية مؤقتاً")
        except Exception as e:
            logger.warning(f"⚠️ خطأ في تعطيل المفاتيح: {e}")
    
    def link_static_id(self, link: dict) -> int:
        """ملء Static ID"""
        try:
            source_table = link["source_table"]
            source_column = link["source_column"]
            static_value = link["static_value"]
            
            query = f"UPDATE `{source_table}` SET `{source_column}` = ? WHERE `{source_column}` IS NULL"
            self.cursor.execute(query, (static_value,))
            self.conn.commit()
            
            count = self.cursor.rowcount
            return count
        except Exception as e:
            logger.debug(f"⚠️ خطأ في Static ID: {str(e)[:50]}")
            return 0
    
    def link_id_fill(self, link: dict) -> int:
        """ملء ID من قيمة نصية"""
        try:
            source_table = link["source_table"]
            source_column = link["source_column"]
            target_table = link["target_table"]
            target_column = link["target_column"]
            lookup_column = link["lookup_column"]
            
            query = f"""
            UPDATE `{source_table}` AS st
            SET `{source_column}` = (
                SELECT `{target_column}`
                FROM `{target_table}`
                WHERE `{lookup_column}` = st.`{lookup_column}`
            )
            WHERE st.`{source_column}` IS NULL
            """
            
            self.cursor.execute(query)
            self.conn.commit()
            
            count = self.cursor.rowcount
            return count
        except Exception as e:
            logger.debug(f"⚠️ خطأ في ID_FILL: {str(e)[:50]}")
            return 0
    
    def link_id_fill_complex(self, link: dict) -> int:
        """ملء ID بشرط مركب"""
        try:
            source_table = link["source_table"]
            source_column = link["source_column"]
            target_table = link["target_table"]
            target_column = link["target_column"]
            source_cols = link["join_on"]["source"]
            target_cols = link["join_on"]["target"]
            
            # بناء شرط الجمع
            join_condition = " AND ".join([
                f"st.`{src}` = t.`{tgt}`"
                for src, tgt in zip(source_cols, target_cols)
            ])
            
            query = f"""
            UPDATE `{source_table}` AS st
            SET `{source_column}` = (
                SELECT t.`{target_column}`
                FROM `{target_table}` AS t
                WHERE {join_condition}
            )
            WHERE st.`{source_column}` IS NULL
            """
            
            self.cursor.execute(query)
            self.conn.commit()
            
            count = self.cursor.rowcount
            return count
        except Exception as e:
            logger.debug(f"⚠️ خطأ في ID_FILL_COMPLEX: {str(e)[:50]}")
            return 0
    
    def execute_link(self, link: dict) -> int:
        """تنفيذ رابط واحد"""
        link_type = link.get("type")
        
        if link_type == "static_id":
            return self.link_static_id(link)
        elif link_type == "id_fill":
            return self.link_id_fill(link)
        elif link_type == "id_fill_complex":
            return self.link_id_fill_complex(link)
        else:
            return 0
    
    def link_all(self) -> bool:
        """تنفيذ جميع الروابط"""
        try:
            if not self.connect():
                return False
            
            self.disable_foreign_keys()
            
            logger.info("\n" + "="*70)
            logger.info("🔗 بدء الربط...")
            logger.info("="*70)
            
            # تصنيف الروابط حسب النوع
            links_by_type = {
                "static_id": STATIC_ID_LINKS,
                "direct": DIRECT_LINKS,
                "id_fill": ID_FILL_LINKS,
                "id_fill_complex": ID_FILL_COMPLEX_LINKS,
                "validation": VALIDATION_LINKS,
            }
            
            total_updated = 0
            
            for link_type, links in links_by_type.items():
                if not links:
                    continue
                
                logger.info(f"\n🔸 {link_type.upper()} Links ({len(links)}):")
                
                for link in links:
                    if link_type == "validation":
                        # لا نفعل شيء للروابط التحقق
                        logger.info(f"   ℹ️ {link['source_column']} ← {link['target_table']}.{link['target_column']}")
                        continue
                    
                    try:
                        count = self.execute_link(link)
                        total_updated += count
                        
                        logger.info(f"   ✅ {link['source_table']}.{link['source_column']} → {count} صف")
                        
                        key = f"{link['source_table']}.{link['source_column']}"
                        self.link_stats[key] = count
                    except Exception as e:
                        logger.error(f"   ❌ خطأ: {str(e)[:50]}")
            
            # تفعيل المفاتيح الخارجية
            logger.info("\n" + "-"*70)
            logger.info("🔐 تفعيل المفاتيح الخارجية...")
            
            try:
                self.cursor.execute("PRAGMA foreign_keys = ON")
                self.conn.commit()
                logger.info("✅ تفعيل المفاتيح الخارجية")
            except Exception as e:
                logger.warning(f"⚠️ خطأ في تفعيل المفاتيح: {e}")
            
            # النتيجة
            logger.info("\n" + "="*70)
            logger.info(f"📊 إجمالي الصفوف المُحدثة: {total_updated}")
            logger.info("="*70 + "\n")
            
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
# دالة عامة للربط
# ============================================================

def link_data(db_path: str) -> bool:
    """
    دالة سريعة لربط البيانات
    
    Args:
        db_path: مسار قاعدة البيانات
    
    Returns:
        bool: True إذا نجح، False إذا فشل
    """
    linker = DatabaseLinker(db_path)
    return linker.link_all()
