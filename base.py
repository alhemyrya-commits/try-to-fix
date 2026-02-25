# models/base.py - النماذج الأساسية (مصحح كامل)
# جميع البيانات تطابق أنواع القاعدة الجديدة بدقة

from datetime import datetime
from typing import Dict, Optional, Any, List


# ============================================================
# الفئة الأساسية لجميع العناصر
# ============================================================

class BaseElement:
    """الفئة الأساسية لجميع العناصر الإنشائية"""
    
    def __init__(self, name: str, element_type: str):
        """
        إنشاء عنصر أساسي
        
        Args:
            name: اسم العنصر
            element_type: نوع العنصر (Column, Beam, Wall, Material, Section, Story)
        """
        self.name = name
        self.element_type = element_type
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.notes = ""
    
    def __repr__(self) -> str:
        return f"{self.element_type}({self.name})"
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل إلى قاموس"""
        return {
            'name': self.name,
            'element_type': self.element_type,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'notes': self.notes
        }
    
    def update_timestamp(self):
        """تحديث وقت التعديل"""
        self.updated_at = datetime.now()


# ============================================================
# 🔵 نموذج المادة (Material Model)
# ============================================================

class Material(BaseElement):
    """
    نموذج المادة
    
    يطابق جداول:
    - Material_Properties_Concrete_Data
    - Material_Properties_Rebar_Data
    """
    
    def __init__(self, name: str, material_type: str, strength: float):
        """
        إنشاء مادة
        
        Args:
            name: اسم المادة (مثل "C30" أو "S400") - VARCHAR(255)
            material_type: النوع ("Concrete" أو "Rebar") - VARCHAR(255)
            strength: المقاومة الأساسية (Fc أو Fy) - ✅ FLOAT
        """
        super().__init__(name, f"Material_{material_type}")
        self.material_type = material_type
        self.strength = float(strength)  # ✅ تحويل صريح إلى FLOAT
        self.strength_unit = "N/mm²"
        
        # ═══════════════════════════════════════════════════════════════
        # خصائص الخرسانة (إذا كانت Concrete)
        # ═══════════════════════════════════════════════════════════════
        
        self.concrete_properties = {
            'Fc': None,                     # FLOAT - المقاومة الضاغطة
            'LtWtConc': None,               # VARCHAR(255) - خرسانة خفيفة؟
            'IsUserFr': None,               # VARCHAR(255) - تم تحديده من المستخدم؟
            'SSCurveOpt': None,             # VARCHAR(255) - خيار المنحنى
            'SSHysType': None,              # VARCHAR(255) - نوع التخلف
            'SFc': None,                    # FLOAT
            'SCap': None,                   # FLOAT - السعة
            'FinalSlope': None,             # FLOAT - الميل النهائي
            'FAngle': None,                 # INT - زاوية الفشل
            'DAngle': None                  # INT - زاوية الاستنزاف
        }
        
        # ═══════════════════════════════════════════════════════════════
        # خصائص الحديد (إذا كانت Rebar)
        # ═══════════════════════════════════════════════════════════════
        
        self.rebar_properties = {
            'Fy': None,                     # FLOAT - حد الخضوع
            'Fu': None,                     # FLOAT - المقاومة القصوى
            'Fye': None,                    # FLOAT - Fy للمسلحة
            'Fue': None,                    # FLOAT - Fu للمسلحة
            'SSCurveOpt': None,             # VARCHAR(255)
            'SSHysType': None,              # VARCHAR(255)
            'SHard': None,                  # FLOAT
            'SCap': None,                   # FLOAT
            'FinalSlope': None              # FLOAT
        }
        
        # معرفات من قاعدة البيانات
        self.db_id: Optional[int] = None
    
    def set_concrete_properties(self, **kwargs):
        """تعيين خصائص الخرسانة - جميع القيم FLOAT أو VARCHAR"""
        for key, value in kwargs.items():
            if key in self.concrete_properties and value is not None:
                # تحويل FLOAT للقيم الرقمية
                if key in ['Fc', 'SFc', 'SCap', 'FinalSlope']:
                    self.concrete_properties[key] = float(value)
                # INT للزوايا
                elif key in ['FAngle', 'DAngle']:
                    self.concrete_properties[key] = int(value)
                # VARCHAR للنصوص
                else:
                    self.concrete_properties[key] = str(value)
    
    def set_rebar_properties(self, **kwargs):
        """تعيين خصائص الحديد - جميع القيم FLOAT أو VARCHAR"""
        for key, value in kwargs.items():
            if key in self.rebar_properties and value is not None:
                # تحويل FLOAT للقيم الرقمية
                if key in ['Fy', 'Fu', 'Fye', 'Fue', 'SHard', 'SCap', 'FinalSlope']:
                    self.rebar_properties[key] = float(value)
                # VARCHAR للنصوص
                else:
                    self.rebar_properties[key] = str(value)
    
    def __repr__(self) -> str:
        return f"{self.material_type}({self.name}={self.strength} N/mm²)"
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل إلى قاموس"""
        data = super().to_dict()
        data.update({
            'material_type': self.material_type,
            'strength': self.strength,
            'strength_unit': self.strength_unit,
            'concrete_properties': self.concrete_properties.copy(),
            'rebar_properties': self.rebar_properties.copy(),
            'db_id': self.db_id
        })
        return data


# ============================================================
# 🟢 نموذج المقطع (Section Model)
# ============================================================

class Section(BaseElement):
    """
    نموذج المقطع
    
    يطابق جداول:
    - Frame_Section_Property_Definitions_Concrete_Rectangular
    - Frame_Section_Property_Definitions_Concrete_Column_Reinforcing
    """
    
    def __init__(self, name: str, material: str, section_type: str = "Rectangular"):
        """
        إنشاء مقطع
        
        Args:
            name: اسم المقطع (مثل "C50x50") - VARCHAR(255) UNIQUE
            material: اسم المادة (مثل "C30") - VARCHAR(255)
            section_type: نوع المقطع (Rectangular, Circular, etc) - VARCHAR(255)
        """
        super().__init__(name, f"Section_{section_type}")
        self.material = material
        self.section_type = section_type
        
        # ═══════════════════════════════════════════════════════════════
        # الخصائص الهندسية - جميعها FLOAT
        # ═══════════════════════════════════════════════════════════════
        
        self.geometric_properties = {
            'Depth': None,                  # FLOAT - الارتفاع
            'Width': None,                  # FLOAT - العرض
            'Area': None,                   # FLOAT - المساحة mm²
            'As2': None,                    # FLOAT - مساحة القص 2
            'As3': None,                    # FLOAT - مساحة القص 3
            'J': None,                      # FLOAT - ثابت الالتواء
            'I22': None,                    # FLOAT - عزم القصور 2
            'I33': None                     # FLOAT - عزم القصور 3
        }
        
        # ═══════════════════════════════════════════════════════════════
        # معاملات الصلابة - جميعها FLOAT
        # ═══════════════════════════════════════════════════════════════
        
        self.stiffness_modifiers = {
            'Area_Modifier': 1.0,           # FLOAT
            'As2_Modifier': 1.0,            # FLOAT
            'As3_Modifier': 1.0,            # FLOAT
            'J_Modifier': 1.0,              # FLOAT
            'I22_Modifier': 1.0,            # FLOAT
            'I33_Modifier': 1.0,            # FLOAT
            'Mass_Modifier': 1.0,           # FLOAT
            'Weight_Modifier': 1.0          # FLOAT
        }
        
        # ═══════════════════════════════════════════════════════════════
        # الخصائص الإضافية
        # ═══════════════════════════════════════════════════════════════
        
        self.additional_properties = {
            'From_File': None,              # VARCHAR(255) - من ملف؟
            'Rigid_Zone': None,             # VARCHAR(255) - منطقة صلبة؟
            'Notional_Size_Type': None,     # VARCHAR(255)
            'Notional_Auto_Factor': None,   # FLOAT
            'Design_Type': None,            # VARCHAR(255)
            'Color': None,                  # VARCHAR(255)
            'GUID': None                    # VARCHAR(255)
        }
        
        # معرفات من قاعدة البيانات
        self.db_id: Optional[int] = None
        self.material_db_id: Optional[int] = None  # MaterialID (FK)
    
    def set_geometric_properties(self, **kwargs):
        """تعيين الخصائص الهندسية - جميعها FLOAT"""
        for key, value in kwargs.items():
            if key in self.geometric_properties and value is not None:
                self.geometric_properties[key] = float(value)
        self.update_timestamp()
    
    def set_stiffness_modifiers(self, **kwargs):
        """تعيين معاملات الصلابة - جميعها FLOAT"""
        for key, value in kwargs.items():
            if key in self.stiffness_modifiers:
                self.stiffness_modifiers[key] = float(value)
        self.update_timestamp()
    
    def set_additional_properties(self, **kwargs):
        """تعيين الخصائص الإضافية"""
        for key, value in kwargs.items():
            if key in self.additional_properties and value is not None:
                # تحويل FLOAT للقيم الرقمية
                if key == 'Notional_Auto_Factor':
                    self.additional_properties[key] = float(value)
                # VARCHAR للنصوص
                else:
                    self.additional_properties[key] = str(value)
        self.update_timestamp()
    
    def __repr__(self) -> str:
        if self.geometric_properties['Depth'] and self.geometric_properties['Width']:
            return f"Section({self.name}={self.geometric_properties['Depth']}x{self.geometric_properties['Width']}mm)"
        return f"Section({self.name})"
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل إلى قاموس"""
        data = super().to_dict()
        data.update({
            'material': self.material,
            'section_type': self.section_type,
            'geometric_properties': self.geometric_properties.copy(),
            'stiffness_modifiers': self.stiffness_modifiers.copy(),
            'additional_properties': self.additional_properties.copy(),
            'db_id': self.db_id,
            'material_db_id': self.material_db_id
        })
        return data


# ============================================================
# 🟡 نموذج الطابق (Story Model)
# ============================================================

class Story(BaseElement):
    """
    نموذج الطابق
    
    يطابق جدول:
    - Story_Definitions
    """
    
    def __init__(self, name: str, height: float):
        """
        إنشاء طابق
        
        Args:
            name: اسم الطابق (مثل "Ground Floor") - VARCHAR(255) UNIQUE
            height: ارتفاع الطابق (FLOAT)
        """
        super().__init__(name, "Story")
        self.height = float(height)  # ✅ FLOAT
        
        # ═══════════════════════════════════════════════════════════════
        # خصائص ETABS
        # ═══════════════════════════════════════════════════════════════
        
        self.tower = None                   # VARCHAR(255)
        self.master_story = None            # VARCHAR(255)
        self.similar_to = None              # VARCHAR(255)
        self.splice_story = None            # VARCHAR(255)
        self.splice_height = None           # FLOAT
        self.color = None                   # VARCHAR(255)
        self.guid = None                    # VARCHAR(255)
        
        # ═══════════════════════════════════════════════════════════════
        # البيانات المرتبطة
        # ═══════════════════════════════════════════════════════════════
        
        self.elements = {
            'columns': [],                  # قائمة الأعمدة
            'beams': [],                    # قائمة العتبات
            'walls': []                     # قائمة الجدران
        }
        
        # معرف من قاعدة البيانات
        self.db_id: Optional[int] = None
    
    def add_column(self, column):
        """إضافة عمود للطابق"""
        if column not in self.elements['columns']:
            self.elements['columns'].append(column)
            self.update_timestamp()
    
    def add_beam(self, beam):
        """إضافة عتبة للطابق"""
        if beam not in self.elements['beams']:
            self.elements['beams'].append(beam)
            self.update_timestamp()
    
    def add_wall(self, wall):
        """إضافة جدار للطابق"""
        if wall not in self.elements['walls']:
            self.elements['walls'].append(wall)
            self.update_timestamp()
    
    def set_etabs_properties(self, tower: str = None, master_story: str = None,
                            similar_to: str = None, splice_story: str = None,
                            splice_height: float = None, color: str = None,
                            guid: str = None):
        """تعيين خصائص ETABS"""
        if tower:
            self.tower = str(tower)
        if master_story:
            self.master_story = str(master_story)
        if similar_to:
            self.similar_to = str(similar_to)
        if splice_story:
            self.splice_story = str(splice_story)
        if splice_height is not None:
            self.splice_height = float(splice_height)  # ✅ FLOAT
        if color:
            self.color = str(color)
        if guid:
            self.guid = str(guid)
        self.update_timestamp()
    
    def get_element_count(self) -> Dict[str, int]:
        """الحصول على عدد العناصر"""
        return {
            'columns': len(self.elements['columns']),
            'beams': len(self.elements['beams']),
            'walls': len(self.elements['walls'])
        }
    
    def __repr__(self) -> str:
        return f"Story({self.name}, h={self.height}mm)"
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل إلى قاموس"""
        data = super().to_dict()
        data.update({
            'height': self.height,
            'tower': self.tower,
            'master_story': self.master_story,
            'similar_to': self.similar_to,
            'splice_story': self.splice_story,
            'splice_height': self.splice_height,
            'color': self.color,
            'guid': self.guid,
            'element_count': self.get_element_count(),
            'db_id': self.db_id
        })
        return data
