# config/link_settings.py - إعدادات الربط (Foreign Keys)
# المهمة الوحيدة: تعريف جميع الروابط بين الجداول

# ============================================================
# 🔵 النوع الأول: روابط DIRECT (قيم نصية مباشرة)
# ============================================================

DIRECT_LINKS = [
    {
        "id": 1,
        "source_table": "Frame_Section_Property_Definitions_Concrete_Column_Reinforcing",
        "source_column": "Longitudinal_Bar_Material",
        "target_table": "Material_Properties_Rebar_Data",
        "target_column": "Material",
        "type": "direct",
    },
    {
        "id": 2,
        "source_table": "Frame_Section_Property_Definitions_Concrete_Column_Reinforcing",
        "source_column": "Tie_Bar_Material",
        "target_table": "Material_Properties_Rebar_Data",
        "target_column": "Material",
        "type": "direct",
    },
    {
        "id": 3,
        "source_table": "Frame_Section_Property_Definitions_Concrete_Rectangular",
        "source_column": "Material",
        "target_table": "Material_Properties_Concrete_Data",
        "target_column": "Material",
        "type": "direct",
    },
    {
        "id": 4,
        "source_table": "Objects_and_Elements_Joints",
        "source_column": "Story",
        "target_table": "Story_Definitions",
        "target_column": "Name",
        "type": "direct",
    },
    {
        "id": 5,
        "source_table": "Column_Object_Connectivity",
        "source_column": "UniquePtI",
        "target_table": "Objects_and_Elements_Joints",
        "target_column": "Element_Name",
        "type": "direct",
    },
    {
        "id": 6,
        "source_table": "Column_Object_Connectivity",
        "source_column": "UniquePtJ",
        "target_table": "Objects_and_Elements_Joints",
        "target_column": "Element_Name",
        "type": "direct",
    },
    {
        "id": 7,
        "source_table": "Frame_Assignments_Section_Properties",
        "source_column": "Section_Property",
        "target_table": "Frame_Section_Property_Definitions_Concrete_Rectangular",
        "target_column": "Name",
        "type": "direct",
    },
    {
        "id": 8,
        "source_table": "Element_Forces_Columns",
        "source_column": "Output_Case",
        "target_table": "Load_Combination_Definitions",
        "target_column": "Name",
        "type": "direct",
    },
    {
        "id": 9,
        "source_table": "Frame_Section_Property_Definitions_Concrete_Column_Reinforcing",
        "source_column": "Name",
        "target_table": "Frame_Section_Property_Definitions_Concrete_Rectangular",
        "target_column": "Name",
        "type": "direct",
    },
]


# ============================================================
# 🟠 النوع الثاني: روابط VALIDATION (للتحقق فقط)
# ============================================================

VALIDATION_LINKS = [
    {
        "id": 10,
        "source_table": "Element_Forces_Columns",
        "source_column": "Story",
        "target_table": "Frame_Assignments_Section_Properties",
        "target_column": "Story",
        "type": "validation",
        "purpose": "تحقق فقط - بدون ملء"
    },
    {
        "id": 11,
        "source_table": "Element_Forces_Columns",
        "source_column": "Unique_Name",
        "target_table": "Frame_Assignments_Section_Properties",
        "target_column": "UniqueName",
        "type": "validation",
        "purpose": "تحقق فقط - بدون ملء"
    },
    {
        "id": 12,
        "source_table": "Column_Object_Connectivity",
        "source_column": "Story",
        "target_table": "Frame_Assignments_Section_Properties",
        "target_column": "Story",
        "type": "validation",
        "purpose": "تحقق فقط - بدون ملء"
    },
    {
        "id": 13,
        "source_table": "Column_Object_Connectivity",
        "source_column": "Unique_Name",
        "target_table": "Frame_Assignments_Section_Properties",
        "target_column": "UniqueName",
        "type": "validation",
        "purpose": "تحقق فقط - بدون ملء"
    },
]


# ============================================================
# 🟢 النوع الثالث: روابط ID_FILL (ملء ID من قيمة نصية)
# ============================================================

ID_FILL_LINKS = [
    {
        "id": 14,
        "source_table": "Frame_Section_Property_Definitions_Concrete_Column_Reinforcing",
        "source_column": "Tie_Bar_MaterialID",
        "target_table": "Material_Properties_Rebar_Data",
        "target_column": "ID",
        "lookup_column": "Tie_Bar_Material",
        "type": "id_fill",
        "priority": 2,  # بعد الربط المباشر
    },
    {
        "id": 15,
        "source_table": "Frame_Section_Property_Definitions_Concrete_Column_Reinforcing",
        "source_column": "LonZgitudinal_Bar_MaterialID",
        "target_table": "Material_Properties_Rebar_Data",
        "target_column": "ID",
        "lookup_column": "Longitudinal_Bar_Material",
        "type": "id_fill",
        "priority": 2,
    },
    {
        "id": 16,
        "source_table": "Frame_Section_Property_Definitions_Concrete_Column_Reinforcing",
        "source_column": "NameID",
        "target_table": "Frame_Section_Property_Definitions_Concrete_Rectangular",
        "target_column": "ID",
        "lookup_column": "Name",
        "type": "id_fill",
        "priority": 2,
    },
    {
        "id": 17,
        "source_table": "Frame_Assignments_Section_Properties",
        "source_column": "Section_PropertyID",
        "target_table": "Frame_Section_Property_Definitions_Concrete_Rectangular",
        "target_column": "ID",
        "lookup_column": "Section_Property",
        "type": "id_fill",
        "priority": 2,
    },
    {
        "id": 18,
        "source_table": "Frame_Section_Property_Definitions_Concrete_Rectangular",
        "source_column": "MaterialID",
        "target_table": "Material_Properties_Concrete_Data",
        "target_column": "ID",
        "lookup_column": "Material",
        "type": "id_fill",
        "priority": 2,
    },
    {
        "id": 19,
        "source_table": "Element_Forces_Columns",
        "source_column": "Load_case_id",
        "target_table": "Load_Combination_Definitions",
        "target_column": "ID",
        "lookup_column": "Output_Case",
        "type": "id_fill",
        "priority": 2,
    },
]


# ============================================================
# 🟣 النوع الرابع: روابط ID_FILL_COMPLEX (شرط مركب)
# ============================================================

ID_FILL_COMPLEX_LINKS = [
    {
        "id": 20,
        "source_table": "Element_Forces_Columns",
        "source_column": "ElementID",
        "target_table": "Frame_Assignments_Section_Properties",
        "target_column": "ID",
        "lookup_columns": ["Unique_Name", "Story"],
        "join_on": {
            "source": ["Unique_Name", "Story"],
            "target": ["UniqueName", "Story"],
        },
        "type": "id_fill_complex",
        "priority": 3,
    },
    {
        "id": 21,
        "source_table": "Column_Object_Connectivity",
        "source_column": "ElementID",
        "target_table": "Frame_Assignments_Section_Properties",
        "target_column": "ID",
        "lookup_columns": ["Unique_Name", "Story"],
        "join_on": {
            "source": ["Unique_Name", "Story"],
            "target": ["UniqueName", "Story"],
        },
        "type": "id_fill_complex",
        "priority": 3,
    },
]


# ============================================================
# ⚪ النوع الخامس: روابط STATIC_ID
# ============================================================

STATIC_ID_LINKS = [
    {
        "id": 22,
        "source_table": "Material_Properties_Rebar_Data",
        "source_column": "GenralID",
        "target_table": "Genralinput",
        "target_column": "id",
        "static_value": 1,
        "type": "static_id",
        "priority": 1,
        "note": "عادة هناك صف واحد فقط في Genralinput"
    },
]


# ============================================================
# جميع الروابط (مرتبة حسب الأولوية)
# ============================================================

ALL_LINKS = sorted(
    STATIC_ID_LINKS + DIRECT_LINKS + ID_FILL_LINKS + ID_FILL_COMPLEX_LINKS + VALIDATION_LINKS,
    key=lambda x: x.get("priority", 1)
)


# ============================================================
# دوال مساعدة
# ============================================================

def get_links_by_type(link_type: str) -> list:
    """الحصول على الروابط حسب النوع"""
    type_map = {
        "direct": DIRECT_LINKS,
        "validation": VALIDATION_LINKS,
        "id_fill": ID_FILL_LINKS,
        "id_fill_complex": ID_FILL_COMPLEX_LINKS,
        "static_id": STATIC_ID_LINKS,
    }
    return type_map.get(link_type, [])


def get_links_by_source_table(table_name: str) -> list:
    """الحصول على جميع الروابط من جدول معين"""
    return [link for link in ALL_LINKS if link["source_table"] == table_name]


def get_links_by_target_table(table_name: str) -> list:
    """الحصول على جميع الروابط إلى جدول معين"""
    return [link for link in ALL_LINKS if link["target_table"] == table_name]


def get_ordered_tables_for_linking() -> list:
    """الحصول على ترتيب الجداول للربط (حسب الأولويات)"""
    tables_order = []
    processed = set()
    
    for link in ALL_LINKS:
        source = link["source_table"]
        target = link["target_table"]
        
        if target not in processed:
            tables_order.append(target)
            processed.add(target)
        
        if source not in processed:
            tables_order.append(source)
            processed.add(source)
    
    return tables_order


# ============================================================
# الملخص
# ============================================================

LINK_SUMMARY = {
    "total_links": len(ALL_LINKS),
    "direct_links": len(DIRECT_LINKS),
    "validation_links": len(VALIDATION_LINKS),
    "id_fill_links": len(ID_FILL_LINKS),
    "id_fill_complex_links": len(ID_FILL_COMPLEX_LINKS),
    "static_id_links": len(STATIC_ID_LINKS),
    "tables_involved": len(set(
        link["source_table"] for link in ALL_LINKS
    )),
}
