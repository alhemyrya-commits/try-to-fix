"""
===============================================================================
database/intermediate_importer.py - نظام الاستيراد الوسيط المحسّن
===============================================================================

المهمة:
1. نسخ خام من VEDA إلى قاعدة وسيطة (بدون تحويل)
2. إنشاء جداول mapping لربط الأعمدة
3. تحويل البيانات من الوسيطة إلى قاعدتك النهائية
"""

import sqlite3
import logging
from typing import Dict, Tuple, List, Optional

logger = logging.getLogger(__name__)


# ============================================================
# الخطوة 1: نسخ خام من VEDA إلى Intermediate DB
# ============================================================

def copy_veda_to_intermediate(veda_path: str, intermediate_path: str) -> bool:
    """نسخ كل الجداول من VEDA إلى قاعدة وسيطة بدون تعديل"""
    try:
        veda_conn = sqlite3.connect(veda_path)
        intermediate_conn = sqlite3.connect(intermediate_path)
        
        logger.info("🔄 المرحلة 1: نسخ VEDA → قاعدة وسيطة")
        
        veda_cursor = veda_conn.cursor()
        veda_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in veda_cursor.fetchall()]
        
        logger.info(f"   وجدت {len(tables)} جدول في VEDA")
        
        for table in tables:
            try:
                veda_cursor.execute(f"PRAGMA table_info({table})")
                columns_info = veda_cursor.fetchall()
                
                if not columns_info:
                    logger.warning(f"   ⚠ {table}: لا توجد أعمدة")
                    continue
                
                # بناء CREATE TABLE
                create_sql = f"CREATE TABLE IF NOT EXISTS \"{table}\" ("
                column_defs = []
                for col in columns_info:
                    col_name = col[1]
                    col_type = col[2] or "TEXT"
                    column_defs.append(f'"{col_name}" {col_type}')
                
                create_sql += ", ".join(column_defs) + ")"
                
                intermediate_cursor = intermediate_conn.cursor()
                intermediate_cursor.execute(create_sql)
                
                # نسخ البيانات
                veda_cursor.execute(f"SELECT * FROM \"{table}\"")
                rows = veda_cursor.fetchall()
                
                if rows:
                    placeholders = ", ".join(["?" for _ in columns_info])
                    col_names = ", ".join([f'"{col[1]}"' for col in columns_info])
                    insert_sql = f"INSERT INTO \"{table}\" ({col_names}) VALUES ({placeholders})"
                    
                    intermediate_cursor.executemany(insert_sql, rows)
                    intermediate_conn.commit()
                    
                    logger.info(f"   ✓ {table}: {len(rows)} صف")
                else:
                    logger.info(f"   ⊘ {table}: فارغ")
            
            except Exception as e:
                logger.error(f"   ✗ خطأ في {table}: {str(e)[:50]}")
                continue
        
        veda_conn.close()
        intermediate_conn.close()
        logger.info(f"   ✓ اكتمل النسخ")
        return True
    
    except Exception as e:
        logger.error(f"❌ خطأ في النسخ: {e}")
        return False


# ============================================================
# الخطوة 2: إنشاء جداول Mapping
# ============================================================

def create_mapping_tables(intermediate_path: str) -> bool:
    """إنشاء جداول mapping في قاعدة الوسيط"""
    try:
        conn = sqlite3.connect(intermediate_path)
        cursor = conn.cursor()
        
        logger.info("🔄 المرحلة 2: إنشاء جداول Mapping")
        
        # جدول mapping الأعمدة
        cursor.execute("""
            DROP TABLE IF EXISTS column_mapping
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS column_mapping (
                id INTEGER PRIMARY KEY,
                source_table TEXT NOT NULL,
                source_column TEXT NOT NULL,
                target_table TEXT NOT NULL,
                target_column TEXT NOT NULL,
                transformation TEXT,
                notes TEXT
            )
        """)
        
        # جدول mapping القيم
        cursor.execute("""
            DROP TABLE IF EXISTS value_mapping
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS value_mapping (
                id INTEGER PRIMARY KEY,
                source_value TEXT NOT NULL,
                target_table TEXT NOT NULL,
                target_value TEXT NOT NULL,
                mapped_id INTEGER,
                notes TEXT
            )
        """)
        
        # إدراج mappings أساسية
        mappings = [
            # Story
            ('Story_Definitions', 'ID', 'Stories', 'ID', None, 'معرف الطابق'),
            ('Story_Definitions', 'Name', 'Stories', 'Name', None, 'اسم الطابق'),
            ('Story_Definitions', 'Height', 'Stories', 'Height_mm', None, 'ارتفاع'),
            ('Story_Definitions', 'Tower', 'Stories', 'Tower', None, 'البرج'),
            ('Story_Definitions', 'Master_Story', 'Stories', 'Master_Story', None, 'طابق أساسي'),
            
            # Materials Concrete
            ('Material_Concrete', 'ID', 'Materials_Concrete', 'ID', None, 'معرف المادة'),
            ('Material_Concrete', 'Material', 'Materials_Concrete', 'Material', None, 'اسم المادة'),
            ('Material_Concrete', 'Fc', 'Materials_Concrete', 'Fc_N_mm2', None, 'Fc'),
            ('Material_Concrete', 'LtWtConc', 'Materials_Concrete', 'LtWtConc', None, 'خفيفة الوزن'),
            
            # Materials Rebar
            ('Material_Rebar', 'ID', 'Materials_Rebar', 'ID', None, 'معرف المادة'),
            ('Material_Rebar', 'Material', 'Materials_Rebar', 'Material', None, 'اسم المادة'),
            ('Material_Rebar', 'Fy', 'Materials_Rebar', 'Fy_N_mm2', None, 'Fy'),
            ('Material_Rebar', 'Fu', 'Materials_Rebar', 'Fu_N_mm2', None, 'Fu'),
            
            # Load Combinations
            ('Load_Combinations', 'ID', 'Loud_comb', 'id', None, 'معرف الحالة'),
            ('Load_Combinations', 'Name', 'Loud_comb', 'name', None, 'اسم الحالة'),
            ('Load_Combinations', 'Type', 'Loud_comb', 'Tybe', None, 'النوع'),
            ('Load_Combinations', 'Is_Auto', 'Loud_comb', 'Is_Auto', None, 'تلقائي'),
        ]
        
        for mapping in mappings:
            cursor.execute("""
                INSERT INTO column_mapping 
                (source_table, source_column, target_table, target_column, transformation, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, mapping)
        
        conn.commit()
        logger.info(f"   ✓ تم إنشاء {len(mappings)} mapping")
        
        conn.close()
        return True
    
    except Exception as e:
        logger.error(f"❌ خطأ في إنشاء mappings: {e}")
        return False


# ============================================================
# الخطوة 3: تحويل من Intermediate إلى قاعدة النهائية
# ============================================================

def transform_to_final(intermediate_path: str, final_path: str) -> bool:
    """تحويل البيانات من الوسيطة إلى قاعدة النهائية"""
    try:
        intermediate_conn = sqlite3.connect(intermediate_path)
        final_conn = sqlite3.connect(final_path)
        
        logger.info("🔄 المرحلة 3: تحويل → قاعدة النهائية")
        
        intermediate_cursor = intermediate_conn.cursor()
        final_cursor = final_conn.cursor()
        
        # الترتيب الصحيح للاستيراد (بدون تبعيات أولاً)
        import_order = [
            ("Story_Definitions", "Stories"),
            ("Material_Concrete", "Materials_Concrete"),
            ("Material_Rebar", "Materials_Rebar"),
            ("Load_Combinations", "Loud_comb"),
            ("Objects_Joints", "Points"),
            ("Beam_Connectivity", "Beam_Connectivity"),
            ("Column_Connectivity", "Column_Connectivity"),
            ("Wall_Connectivity", "Wall_Connectivity"),
            ("Section_Rectangular", "Sections_Rectangular"),
            ("Beam_Reinforcing", "Beam_Reinforcing_Data"),
            ("Column_Reinforcing", "Column_Reinforcing_Data"),
            ("Wall_Properties", "Wall_Properties"),
            ("Frame_Assignments", "Beams_Data"),
            ("Frame_Assignments", "Columns_Data"),
            ("Area_Assignments_Section", "Walls_Data"),
            ("Forces_Beams", "Element_Force_Beam"),
            ("Forces_Columns", "Element_Force_Column"),
            ("Forces_Piers", "Pier_Force"),
        ]
        
        total_rows = 0
        successful_imports = 0
        
        for source_table, target_table in import_order:
            try:
                # التحقق من وجود الجداول
                intermediate_cursor.execute(
                    f"SELECT name FROM sqlite_master WHERE type='table' AND name='{source_table}'"
                )
                if not intermediate_cursor.fetchone():
                    logger.info(f"   ⊘ {source_table}: غير موجود في VEDA")
                    continue
                
                final_cursor.execute(
                    f"SELECT name FROM sqlite_master WHERE type='table' AND name='{target_table}'"
                )
                if not final_cursor.fetchone():
                    logger.info(f"   ⊘ {target_table}: غير موجود في قاعدة النهائية")
                    continue
                
                # احصل على الـ mappings
                intermediate_cursor.execute("""
                    SELECT source_column, target_column
                    FROM column_mapping
                    WHERE source_table = ? AND target_table = ?
                """, (source_table, target_table))
                
                mappings = intermediate_cursor.fetchall()
                
                if not mappings:
                    logger.info(f"   ⚠ {source_table} → {target_table}: لا توجد mappings")
                    continue
                
                # قراءة البيانات من الوسيط
                source_cols = [m[0] for m in mappings]
                target_cols = [m[1] for m in mappings]
                
                source_col_str = ", ".join([f'"{c}"' for c in source_cols])
                intermediate_cursor.execute(f"SELECT {source_col_str} FROM \"{source_table}\"")
                rows = intermediate_cursor.fetchall()
                
                if not rows:
                    logger.info(f"   ⊘ {source_table} → {target_table}: فارغ")
                    continue
                
                # إدراج في الجدول النهائي
                target_col_str = ", ".join([f'"{c}"' for c in target_cols])
                placeholders = ", ".join(["?" for _ in target_cols])
                insert_sql = f"INSERT INTO \"{target_table}\" ({target_col_str}) VALUES ({placeholders})"
                
                final_cursor.executemany(insert_sql, rows)
                final_conn.commit()
                
                logger.info(f"   ✓ {source_table} → {target_table}: {len(rows)} صف")
                total_rows += len(rows)
                successful_imports += 1
                
            except Exception as e:
                logger.error(f"   ✗ خطأ في {source_table}: {str(e)[:50]}")
                continue
        
        logger.info(f"   ✓ إجمالي: {total_rows} صف محول ({successful_imports} جدول)")
        
        intermediate_conn.close()
        final_conn.close()
        return True
    
    except Exception as e:
        logger.error(f"❌ خطأ في التحويل: {e}")
        return False


# ============================================================
# الدالة الرئيسية
# ============================================================

def run_intermediate_import(veda_path: str, intermediate_path: str, final_path: str) -> bool:
    """تشغيل عملية الاستيراد الوسيطة الكاملة"""
    
    logger.info("\n" + "=" * 70)
    logger.info("🚀 نظام الاستيراد الوسيط (Intermediate DB)")
    logger.info("=" * 70 + "\n")
    
    # المرحلة 1: نسخ خام
    if not copy_veda_to_intermediate(veda_path, intermediate_path):
        logger.error("فشل النسخ الخام")
        return False
    
    logger.info("")
    
    # المرحلة 2: إنشاء mappings
    if not create_mapping_tables(intermediate_path):
        logger.error("فشل إنشاء mappings")
        return False
    
    logger.info("")
    
    # المرحلة 3: تحويل
    if not transform_to_final(intermediate_path, final_path):
        logger.error("فشل التحويل")
        return False
    
    logger.info("\n" + "=" * 70)
    logger.info("✅ اكتملت عملية الاستيراد بنجاح!")
    logger.info("=" * 70 + "\n")
    
    return True
