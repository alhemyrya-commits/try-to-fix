"""
═══════════════════════════════════════════════════════════════════════════════
config/veda_schema.py - تعريف 11 جدول من VEDA.db بالضبط - مصحح
═══════════════════════════════════════════════════════════════════════════════

✅ التصحيحات:
1. Material_Properties_Rebar_Data: Material = INTEGER (ليس VARCHAR)
2. Element_Forces_Columns: Station = INTEGER (ليس REAL)
3. Element_Forces_Columns: Elem Station = INTEGER (ليس FLOAT)
4. Frame_Assignments_Section_Properties: إضافة Label

"""

# ============================================================
# 11 جدول من VEDA.db - بالضبط كما هي (مصحح)
# ============================================================

VEDA_TABLES = {
    
    # 1️⃣ Story_Definitions
    "Story_Definitions": [
        "Tower",
        "Name",
        "Height",
        "Master Story",
        "Similar To",
        "Splice Story",
        "Splice Height",
        "Color",
        "GUID"
    ],
    
    # 2️⃣ Material_Properties_Concrete_Data
    "Material_Properties_Concrete_Data": [
        "Material",
        "Fc",
        "LtWtConc",
        "IsUserFr",
        "SSCurveOpt",
        "SSHysType",
        "SFc",
        "SCap",
        "FinalSlope",
        "FAngle",
        "DAngle"
    ],
    
    # 3️⃣ Material_Properties_Rebar_Data
    # ⚠️ تصحيح: Material = INTEGER (ليس VARCHAR)
    "Material_Properties_Rebar_Data": [
        "Material",          # ✅ INTEGER (ليس VARCHAR!)
        "Fy",
        "Fu",
        "Fye",
        "Fue",
        "SSCurveOpt",
        "SSHysType",
        "SHard",
        "SCap",
        "FinalSlope"
    ],
    
    # 4️⃣ Load_Combination_Definitions
    "Load_Combination_Definitions": [
        "Name",
        "Type",
        "Is Auto",
        "Load Name",
        "SF",
        "GUID",
        "Notes"
    ],
    
    # 5️⃣ Objects_and_Elements_Joints
    "Objects_and_Elements_Joints": [
        "Story",
        "Element Name",
        "Object Type",
        "Object Label",
        "Object Name",
        "Global X",
        "Global Y",
        "Global Z"
    ],
    
    # 6️⃣ Column_Object_Connectivity
    "Column_Object_Connectivity": [
        "Unique Name",
        "Story",
        "ColumnBay",
        "UniquePtI",
        "UniquePtJ",
        "Length",
        "GUID"
    ],
    
    # 7️⃣ Frame_Section_Property_Definitions_Concrete_Column_Reinforcing
    "Frame_Section_Property_Definitions_Concrete_Column_Reinforcing": [
        "Name",
        "Longitudinal Bar Material",
        "Tie Bar Material",
        "Reinforcement Configuration",
        "Is Designed?",
        "Clear Cover to Ties",
        "Number Bars 3-Dir",
        "Number Bars 2-Dir",
        "Longitudinal Bar Size",
        "Corner Bar Size",
        "Tie Bar Size",
        "Tie Bar Spacing",
        "Number Ties 3-Dir",
        "Number Ties 2-Dir"
    ],
    
    # 8️⃣ Frame_Section_Property_Definitions_Concrete_Rectangular
    "Frame_Section_Property_Definitions_Concrete_Rectangular": [
        "Name",
        "Material",
        "From File?",
        "Depth",
        "Width",
        "Rigid Zone?",
        "Notional Size Type",
        "Notional Auto Factor",
        "Design Type",
        "Area Modifier",
        "As2 Modifier",
        "As3 Modifier",
        "J Modifier",
        "I22 Modifier",
        "I33 Modifier",
        "Mass Modifier",
        "Weight Modifier",
        "Color",
        "GUID",
        "Notes"
    ],
    
    # 9️⃣ Frame_Assignments_Section_Properties
    # ⚠️ تصحيح: إضافة Label
    "Frame_Assignments_Section_Properties": [
        "Story",
        "Label",               # ✅ إضافة (كان ناقص)
        "UniqueName",
        "Shape",
        "Auto Select List",
        "Section Property"
    ],
    
    # 🔟 Element_Forces_Columns
    # ⚠️ تصحيح: Station و Elem Station = INTEGER (ليس REAL أو FLOAT)
    "Element_Forces_Columns": [
        "Story",
        "Column",
        "Unique Name",
        "Output Case",
        "Case Type",
        "Station",             # ✅ INTEGER (ليس REAL!)
        "P",
        "V2",
        "V3",
        "T",
        "M2",
        "M3",
        "Element",
        "Elem Station",        # ✅ INTEGER (ليس FLOAT!)
        "Location"
    ],
}

# ============================================================
# 11 جدول فقط
# ============================================================

VEDA_TABLE_NAMES = list(VEDA_TABLES.keys())

# ============================================================
# دالة للحصول على أعمدة جدول
# ============================================================

def get_veda_columns(table_name: str) -> list:
    """الحصول على أعمدة جدول في VEDA"""
    return VEDA_TABLES.get(table_name, [])

def is_table_in_veda(table_name: str) -> bool:
    """التحقق من وجود جدول في VEDA"""
    return table_name in VEDA_TABLES

# ============================================================
# الملخص
# ============================================================

VEDA_SUMMARY = {
    "total_tables": len(VEDA_TABLES),
    "total_columns": sum(len(cols) for cols in VEDA_TABLES.values()),
    "tables": VEDA_TABLE_NAMES,
    "issues_fixed": [
        "✅ Material_Properties_Rebar_Data: Material = INTEGER",
        "✅ Element_Forces_Columns: Station = INTEGER",
        "✅ Element_Forces_Columns: Elem Station = INTEGER",
        "✅ Frame_Assignments_Section_Properties: إضافة Label"
    ]
}
