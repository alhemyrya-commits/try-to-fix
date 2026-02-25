"""
===============================================================================
read_veda_structure.py - أداة لقراءة هيكل VEDA
===============================================================================

شغّل من المجلد الرئيسي:
python read_veda_structure.py
"""

import sqlite3
from pathlib import Path

# المسار المباشر
VEDA_PATH = r"C:\Users\Huthefh\Desktop\Check\data\project.veda"

def print_table_structure(db_path: str, table_name: str):
    """طباعة هيكل جدول VEDA"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # قراءة البيانات
        cursor.execute(f"SELECT * FROM [{table_name}]")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        
        print(f"\n{'='*100}")
        print(f"جدول: {table_name}")
        print(f"{'='*100}")
        print(f"عدد الصفوف: {len(rows)}")
        print(f"عدد الأعمدة: {len(columns)}")
        print(f"\nأسماء الأعمدة:")
        for i, col in enumerate(columns, 1):
            print(f"  {i:2d}. {col}")
        
        print(f"\nبيانات (أول صفين):")
        for row_idx, row in enumerate(rows[:2], 1):
            print(f"\n  الصف {row_idx}:")
            for col, val in zip(columns, row):
                val_str = str(val)[:50] if val else "None"
                print(f"    {col}: {val_str}")
        
        conn.close()
        return columns
    
    except Exception as e:
        print(f"❌ خطأ في {table_name}: {e}")
        return None

def scan_all_tables(db_path: str):
    """فحص جميع جداول VEDA"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # الحصول على قائمة الجداول
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        print(f"\n{'='*100}")
        print(f"جميع جداول VEDA ({len(tables)} جدول)")
        print(f"{'='*100}")
        
        for table in sorted(tables):
            try:
                cursor.execute(f"SELECT * FROM [{table}]")
                rows = cursor.fetchall()
                col_count = len(cursor.description)
                row_count = len(rows)
                print(f"✓ {table:60s} | صفوف: {row_count:10d} | أعمدة: {col_count}")
            except Exception as e:
                print(f"✗ {table:60s} | خطأ: {e}")
        
        conn.close()
        return sorted(tables)
    
    except Exception as e:
        print(f"❌ خطأ: {e}")
        return []

# ============================================================
# البرنامج الرئيسي
# ============================================================

if __name__ == "__main__":
    print("🔍 أداة فحص هيكل VEDA")
    print(f"مسار VEDA: {VEDA_PATH}\n")
    
    # التحقق من وجود الملف
    if not Path(VEDA_PATH).exists():
        print(f"❌ ملف VEDA غير موجود: {VEDA_PATH}")
        exit(1)
    
    # 1. فحص جميع الجداول
    tables = scan_all_tables(VEDA_PATH)
    
    # 2. طباعة تفاصيل الجداول المهمة
    if tables:
        print("\n\n🔎 تفاصيل الجداول المهمة:\n")
        important = [
            "Material_Properties_Concrete_Data",
            "Material_Properties_Rebar_Data",
            "Story_Definitions",
            "Load_Combination_Definitions",
            "Frame_Section_Property_Definitions_Concrete_Rectangular",
        ]
        
        for table in important:
            if table in tables:
                columns = print_table_structure(VEDA_PATH, table)
                if columns:
                    print(f"\n📋 Template لـ {table}:")
                    print(f'    "{table}": {{')
                    for col in columns:
                        db_col = col.replace(" ", "_").replace("(", "").replace(")", "")
                        print(f'        "{col}": "{db_col}",')
                    print(f'    }},')
    
    print("\n\n✅ اكتمل الفحص!")
