# config/input_settings.py - إعدادات الإدخال فقط
# المهمة الوحيدة: ترجمة أسماء الأعمدة من VEDA إلى الجديد
# بدون معلومات الإنشاء أو الربط

# ============================================================
# قاموس ترجمة الأعمدة: VEDA → الجديد
# ============================================================

COLUMN_MAPPING = {
    
    # ═══════════════════════════════════════════════════════
    # 1️⃣ Story_Definitions
    # ═══════════════════════════════════════════════════════
    "Story_Definitions": {
        "Tower": "Tower",
        "Name": "Name",
        "Height": "Height",
        "Master Story": "Master_Story",
        "Similar To": "Similar_To",
        "Splice Story": "Splice_Story",
        "Splice Height": "Splice_Height",
        "Color": "Color",
        "GUID": "GUID",
    },
    
    # ═══════════════════════════════════════════════════════
    # 2️⃣ Material_Properties_Concrete_Data
    # ═══════════════════════════════════════════════════════
    "Material_Properties_Concrete_Data": {
        "Material": "Material",
        "Fc": "Fc",
        "LtWtConc": "LtWtConc",
        "IsUserFr": "IsUserFr",
        "SSCurveOpt": "SSCurveOpt",
        "SSHysType": "SSHysType",
        "SFc": "SFc",
        "SCap": "SCap",
        "FinalSlope": "FinalSlope",
        "FAngle": "FAngle",
        "DAngle": "DAngle",
    },
    
    # ═══════════════════════════════════════════════════════
    # 3️⃣ Material_Properties_Rebar_Data
    # ═══════════════════════════════════════════════════════
    "Material_Properties_Rebar_Data": {
        "Material": "Material",
        "Fy": "Fy",
        "Fu": "Fu",
        "Fye": "Fye",
        "Fue": "Fue",
        "SSCurveOpt": "SSCurveOpt",
        "SSHysType": "SSHysType",
        "SHard": "SHard",
        "SCap": "SCap",
        "FinalSlope": "FinalSlope",
    },
    
    # ═══════════════════════════════════════════════════════
    # 4️⃣ Load_Combination_Definitions
    # ═══════════════════════════════════════════════════════
    "Load_Combination_Definitions": {
        "Name": "Name",
        "Type": "Type",
        "Is Auto": "Is_Auto",
        "Load Name": "Load_Name",
        "SF": "SF",
        "GUID": "GUID",
        "Notes": "Notes",
    },
    
    # ═══════════════════════════════════════════════════════
    # 5️⃣ Objects_and_Elements_Joints
    # ═══════════════════════════════════════════════════════
    "Objects_and_Elements_Joints": {
        "Story": "Story",
        "Element Name": "Element_Name",
        "Object Type": "Object_Type",
        "Object Label": "Object_Label",
        "Object Name": "Object_Name",
        "Global X": "Global_X",
        "Global Y": "Global_Y",
        "Global Z": "Global_Z",
    },
    
    # ═══════════════════════════════════════════════════════
    # 6️⃣ Column_Object_Connectivity
    # ═══════════════════════════════════════════════════════
    "Column_Object_Connectivity": {
        "Unique Name": "Unique_Name",
        "Story": "Story",
        "ColumnBay": "ColumnBay",
        "UniquePtI": "UniquePtI",
        "UniquePtJ": "UniquePtJ",
        "Length": "Length",
        "GUID": "GUID",
    },
    
    # ═══════════════════════════════════════════════════════
    # 7️⃣ Frame_Section_Property_Definitions_Concrete_Column_Reinforcing
    # ═══════════════════════════════════════════════════════
    "Frame_Section_Property_Definitions_Concrete_Column_Reinforcing": {
        "Name": "Name",
        "Longitudinal Bar Material": "Longitudinal_Bar_Material",
        "Tie Bar Material": "Tie_Bar_Material",
        "Reinforcement Configuration": "Reinforcement_Configuration",
        "Is Designed?": "Is_Designed",
        "Clear Cover to Ties": "Clear_Cover_to_Ties",
        "Number Bars 3-Dir": "Number_Bars_3_Dir",
        "Number Bars 2-Dir": "Number_Bars_2_Dir",
        "Longitudinal Bar Size": "Longitudinal_Bar_Size",
        "Corner Bar Size": "Corner_Bar_Size",
        "Tie Bar Size": "Tie_Bar_Size",
        "Tie Bar Spacing": "Tie_Bar_Spacing",
        "Number Ties 3-Dir": "Number_Ties_3_Dir",
        "Number Ties 2-Dir": "Number_Ties_2_Dir",
    },
    
    # ═══════════════════════════════════════════════════════
    # 8️⃣ Frame_Section_Property_Definitions_Concrete_Rectangular
    # ═══════════════════════════════════════════════════════
    "Frame_Section_Property_Definitions_Concrete_Rectangular": {
        "Name": "Name",
        "Material": "Material",
        "From File?": "From_File",
        "Depth": "Depth",
        "Width": "Width",
        "Rigid Zone?": "Rigid_Zone",
        "Notional Size Type": "Notional_Size_Type",
        "Notional Auto Factor": "Notional_Auto_Factor",
        "Design Type": "Design_Type",
        "Area Modifier": "Area_Modifier",
        "As2 Modifier": "As2_Modifier",
        "As3 Modifier": "As3_Modifier",
        "J Modifier": "J_Modifier",
        "I22 Modifier": "I22_Modifier",
        "I33 Modifier": "I33_Modifier",
        "Mass Modifier": "Mass_Modifier",
        "Weight Modifier": "Weight_Modifier",
        "Color": "Color",
        "GUID": "GUID",
        "Notes": "Notes",
    },
    
    # ═══════════════════════════════════════════════════════
    # 9️⃣ Frame_Assignments_Section_Properties
    # ═══════════════════════════════════════════════════════
    "Frame_Assignments_Section_Properties": {
        "Story": "Story",
        "Label": "Label",
        "UniqueName": "UniqueName",
        "Shape": "Shape",
        "Auto Select List": "Auto_Select_List",
        "Section Property": "Section_Property",
    },
    
    # ═══════════════════════════════════════════════════════
    # 🔟 Element_Forces_Columns
    # ═══════════════════════════════════════════════════════
    "Element_Forces_Columns": {
        "Story": "Story",
        "Column": "Column",
        "Unique Name": "Unique_Name",
        "Output Case": "Output_Case",
        "Case Type": "Case_Type",
        "Station": "Station",
        "P": "P",
        "V2": "V2",
        "V3": "V3",
        "T": "T",
        "M2": "M2",
        "M3": "M3",
        "Element": "Element",
        "Elem Station": "Elem_Station",
        "Location": "Location",
    },
}


# ============================================================
# الأعمدة المراد تجاهلها (لا توجد في VEDA)
# ============================================================

COLUMNS_TO_IGNORE = {
    "Story_Definitions": ["Notes"],
    
    "Material_Properties_Rebar_Data": ["GenralID"],
    
    "Frame_Section_Property_Definitions_Concrete_Column_Reinforcing": [
        "LonZgitudinal_Bar_MaterialID",
        "Tie_Bar_MaterialID",
        "NameID",
    ],
    
    "Frame_Section_Property_Definitions_Concrete_Rectangular": [
        "MaterialID"
    ],
    
    "Frame_Assignments_Section_Properties": [
        "Section_PropertyID"
    ],
    
    "Column_Object_Connectivity": [
        "ElementID"
    ],
    
    "Element_Forces_Columns": [
        "ElementID",
        "Load_case_id",
    ],
}


# ============================================================
# الجداول المراد نسخ البيانات منها (11 جدول فقط)
# ============================================================

TABLES_TO_IMPORT = list(COLUMN_MAPPING.keys())

TOTAL_TABLES_TO_IMPORT = len(TABLES_TO_IMPORT)


# ============================================================
# دوال مساعدة
# ============================================================

def get_column_mapping(table_name: str) -> dict:
    """الحصول على ترجمة أعمدة جدول معين"""
    return COLUMN_MAPPING.get(table_name, {})


def get_veda_column_name(table_name: str, new_column_name: str) -> str:
    """الحصول على اسم العمود في VEDA من اسمه في الجديد"""
    mapping = get_column_mapping(table_name)
    for veda_col, new_col in mapping.items():
        if new_col == new_column_name:
            return veda_col
    return None


def get_new_column_name(table_name: str, veda_column_name: str) -> str:
    """الحصول على اسم العمود في الجديد من اسمه في VEDA"""
    mapping = get_column_mapping(table_name)
    return mapping.get(veda_column_name, None)


def should_import_column(table_name: str, column_name: str) -> bool:
    """التحقق من أن العمود يجب نسخه (ليس في قائمة التجاهل)"""
    ignored = COLUMNS_TO_IGNORE.get(table_name, [])
    return column_name not in ignored


def get_columns_to_import(table_name: str) -> list:
    """الحصول على قائمة الأعمدة المراد نسخها من جدول معين"""
    mapping = get_column_mapping(table_name)
    veda_columns = list(mapping.keys())
    return [col for col in veda_columns if should_import_column(table_name, mapping[col])]


# ============================================================
# الملخص
# ============================================================

IMPORT_SUMMARY = {
    "total_tables": TOTAL_TABLES_TO_IMPORT,
    "total_mappings": sum(len(cols) for cols in COLUMN_MAPPING.values()),
    "total_ignored": sum(len(cols) for cols in COLUMNS_TO_IGNORE.values()),
    "tables": TABLES_TO_IMPORT,
}
