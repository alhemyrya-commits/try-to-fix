# models/load_combination.py
# نموذج حالات التحميل (Load Combination Model)

from datetime import datetime
from typing import Dict, Optional, Any
from base import BaseElement


class LoadCombination(BaseElement):
    """
    نموذج حالات التحميل
    
    يطابق جدول:
    - Load_Combination_Definitions
    """
    
    def __init__(self, name: str, combo_type: str):
        """
        إنشاء حالة تحميل
        
        Args:
            name: اسم الحالة (مثل "DL+LL+EQX") - VARCHAR(255) UNIQUE
            combo_type: نوع الحالة (Linear Static, Response Spectrum) - VARCHAR(255)
        """
        super().__init__(name, f"LoadCombination_{combo_type}")
        self.combo_type = combo_type
        
        # ═══════════════════════════════════════════════════════════════
        # خصائص حالة التحميل من Load_Combination_Definitions
        # ═══════════════════════════════════════════════════════════════
        
        self.is_auto: Optional[str] = None  # VARCHAR(255) - هل تلقائية؟
        self.guid: Optional[str] = None      # VARCHAR(255)
        
        # ═══════════════════════════════════════════════════════════════
        # مكونات حالة التحميل
        # ═══════════════════════════════════════════════════════════════
        
        self.load_components = []  # قائمة الأحمال والمعاملات
        
        # معرف من قاعدة البيانات
        self.db_id: Optional[int] = None
    
    def add_load_component(self, load_name: str, scale_factor: float):
        """
        إضافة حمل إلى حالة التحميل
        
        Args:
            load_name: اسم الحمل (مثل "Dead", "Live", "EQX")
            scale_factor: معامل التحجيم (مثل 1.0, 0.75)
        """
        component = {
            'Load_Name': str(load_name),
            'Scale_Factor': float(scale_factor)
        }
        self.load_components.append(component)
        self.update_timestamp()
    
    def get_components(self) -> list:
        """الحصول على قائمة الأحمال"""
        return self.load_components.copy()
    
    def __repr__(self) -> str:
        components_str = " + ".join(
            [f"{c['Load_Name']}×{c['Scale_Factor']}" for c in self.load_components]
        )
        return f"LoadCombination({self.name}: {components_str})"
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل إلى قاموس"""
        data = super().to_dict()
        data.update({
            'combo_type': self.combo_type,
            'is_auto': self.is_auto,
            'guid': self.guid,
            'load_components': self.load_components.copy(),
            'num_components': len(self.load_components),
            'db_id': self.db_id
        })
        return data


# ============================================================
# 🔵 نموذج القوة (Force Model)
# ============================================================


class Force:
    """
    نموذج القوة للعمود
    
    يطابق جدول:
    - Element_Forces_Columns
    """
    
    def __init__(self, column_id: int, story: str, output_case: str, case_type: str):
        """
        إنشاء قوة
        
        Args:
            column_id: معرف العمود الفريد (INT)
            story: اسم الطابق (VARCHAR(255))
            output_case: اسم حالة التحميل (VARCHAR(255))
            case_type: نوع الحالة (Linear Static, Response Spectrum) - VARCHAR(255)
        """
        self.column_id = int(column_id)
        self.story = str(story)
        self.output_case = str(output_case)
        self.case_type = str(case_type)
        
        # ═══════════════════════════════════════════════════════════════
        # بيانات القوة من Element_Forces_Columns - جميعها FLOAT
        # ═══════════════════════════════════════════════════════════════
        
        self.station: Optional[float] = None  # FLOAT - محطة القياس
        
        # القوى الأساسية
        self.p: Optional[float] = None  # FLOAT - قوة محورية (N)
        self.v2: Optional[float] = None  # FLOAT - قص في اتجاه 2 (N)
        self.v3: Optional[float] = None  # FLOAT - قص في اتجاه 3 (N)
        self.t: Optional[float] = None  # FLOAT - عزم فتل (N.mm)
        
        # العزوم
        self.m2: Optional[float] = None  # FLOAT - عزم انحناء في اتجاه 2 (N.mm)
        self.m3: Optional[float] = None  # FLOAT - عزم انحناء في اتجاه 3 (N.mm)
        
        # معلومات العنصر
        self.element: Optional[int] = None  # INT - معرف العنصر
        self.elem_station: Optional[float] = None  # FLOAT - محطة العنصر
        self.location: Optional[float] = None  # FLOAT - الموقع
        
        # ═══════════════════════════════════════════════════════════════
        # معرفات من قاعدة البيانات (Foreign Keys)
        # ═══════════════════════════════════════════════════════════════
        
        self.element_id: Optional[int] = None  # INT (FK) - معرف العنصر في الجدول
        self.load_case_id: Optional[int] = None  # INT (FK) - معرف حالة التحميل
        
        # البيانات الوصفية
        self.created_at = datetime.now()
    
    def set_forces(self, p: float = None, v2: float = None, v3: float = None,
                   t: float = None, m2: float = None, m3: float = None,
                   station: float = None):
        """
        تعيين القوى - جميع القيم FLOAT
        
        Args:
            p: قوة محورية
            v2: قص في اتجاه 2
            v3: قص في اتجاه 3
            t: عزم فتل
            m2: عزم في اتجاه 2
            m3: عزم في اتجاه 3
            station: محطة القياس
        """
        if p is not None:
            self.p = float(p)
        if v2 is not None:
            self.v2 = float(v2)
        if v3 is not None:
            self.v3 = float(v3)
        if t is not None:
            self.t = float(t)
        if m2 is not None:
            self.m2 = float(m2)
        if m3 is not None:
            self.m3 = float(m3)
        if station is not None:
            self.station = float(station)
    
    def set_element_info(self, element: int = None, elem_station: float = None,
                        location: float = None):
        """
        تعيين معلومات العنصر - جميع القيم FLOAT أو INT
        """
        if element is not None:
            self.element = int(element)
        if elem_station is not None:
            self.elem_station = float(elem_station)
        if location is not None:
            self.location = float(location)
    
    def get_max_shear(self) -> float:
        """الحصول على أقصى قوة قص"""
        v2_abs = abs(self.v2) if self.v2 else 0
        v3_abs = abs(self.v3) if self.v3 else 0
        return max(v2_abs, v3_abs)
    
    def get_total_moment(self) -> float:
        """الحصول على إجمالي العزم"""
        m2_abs = abs(self.m2) if self.m2 else 0
        m3_abs = abs(self.m3) if self.m3 else 0
        return (m2_abs ** 2 + m3_abs ** 2) ** 0.5  # جذر المربعات
    
    def __repr__(self) -> str:
        return f"Force(Case={self.output_case}, P={self.p}, V2={self.v2}, V3={self.v3})"
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل إلى قاموس"""
        return {
            'column_id': self.column_id,
            'story': self.story,
            'output_case': self.output_case,
            'case_type': self.case_type,
            'station': self.station,
            'forces': {
                'p': self.p,
                'v2': self.v2,
                'v3': self.v3,
                't': self.t,
                'm2': self.m2,
                'm3': self.m3
            },
            'element_info': {
                'element': self.element,
                'elem_station': self.elem_station,
                'location': self.location
            },
            'max_shear': self.get_max_shear(),
            'total_moment': self.get_total_moment(),
            'created_at': self.created_at.isoformat()
        }


# ============================================================
# 🟢 نموذج حالات التحميل المتعددة (LoadCases Group)
# ============================================================


class LoadCaseGroup:
    """
    مجموعة حالات التحميل
    
    تجميع جميع حالات التحميل لسهولة الوصول
    """
    
    def __init__(self):
        """إنشاء مجموعة فارغة"""
        self.load_cases: Dict[str, LoadCombination] = {}
    
    def add_load_case(self, load_case: LoadCombination):
        """
        إضافة حالة تحميل
        
        Args:
            load_case: كائن LoadCombination
        """
        self.load_cases[load_case.name] = load_case
    
    def get_load_case(self, name: str) -> Optional[LoadCombination]:
        """الحصول على حالة تحميل بالاسم"""
        return self.load_cases.get(name)
    
    def get_all_load_cases(self) -> list:
        """الحصول على جميع حالات التحميل"""
        return list(self.load_cases.values())
    
    def get_seismic_cases(self) -> list:
        """الحصول على حالات التحميل الزلزالية فقط"""
        seismic = []
        for case in self.load_cases.values():
            if 'EQ' in case.name or 'Seismic' in case.combo_type:
                seismic.append(case)
        return seismic
    
    def get_static_cases(self) -> list:
        """الحصول على الحالات الثابتة فقط"""
        static = []
        for case in self.load_cases.values():
            if 'Linear Static' in case.combo_type:
                static.append(case)
        return static
    
    def __repr__(self) -> str:
        return f"LoadCaseGroup({len(self.load_cases)} cases)"
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل إلى قاموس"""
        return {
            'total_cases': len(self.load_cases),
            'seismic_cases': len(self.get_seismic_cases()),
            'static_cases': len(self.get_static_cases()),
            'load_cases': {
                name: case.to_dict()
                for name, case in self.load_cases.items()
            }
        }
