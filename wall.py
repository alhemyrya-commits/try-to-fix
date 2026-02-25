
"""
===============================================================================
models/wall.py - نموذج الجدار (مصحح كامل)
===============================================================================
"""

from typing import Dict, Optional, Any
from models.base import BaseElement


class Wall(BaseElement):
    """نموذج الجدار"""
    
    def __init__(self, pier_name: str, story_name: str, section_name: str):
        """
        إنشاء جدار
        
        المعاملات:
            pier_name: اسم الجدار (Pier)
            story_name: اسم الطابق
            section_name: اسم خصائص الجدار
        """
        super().__init__(pier_name, "Wall")
        self.pier_name = pier_name
        self.story_name = story_name
        self.section_name = section_name
        
        # معرفات
        self.unique_name: Optional[int] = None
        self.internal_id: Optional[int] = None
        
        # خصائص التسليح
        self.reinforcement_type: Optional[str] = None
        self.rho_percent: Optional[float] = None
        
        # البيانات الهندسية - ✅ REAL
        self.connectivity = {
            'UniquePt1': None,
            'UniquePt2': None,
            'UniquePt3': None,
            'UniquePt4': None,
            'Perimeter_mm': None,   # ✅ REAL
            'Area_mm2': None,       # ✅ REAL
            'Station_mm': None      # ✅ REAL
        }
        
        # القوى - ✅ جميعها REAL
        self.forces = []
    
    def set_connectivity(self, pt1: int, pt2: int, pt3: int, pt4: int,
                        perimeter_mm: float = None, area_mm2: float = None,
                        station_mm: float = None):
        """تعيين بيانات الاتصال (4 نقاط) - ✅ REAL"""
        self.connectivity['UniquePt1'] = pt1
        self.connectivity['UniquePt2'] = pt2
        self.connectivity['UniquePt3'] = pt3
        self.connectivity['UniquePt4'] = pt4
        self.connectivity['Perimeter_mm'] = float(perimeter_mm) if perimeter_mm else None  # ✅ REAL
        self.connectivity['Area_mm2'] = float(area_mm2) if area_mm2 else None  # ✅ REAL
        self.connectivity['Station_mm'] = float(station_mm) if station_mm else None  # ✅ REAL
        self.update_timestamp()
    
    def add_force(self, output_case: str, station_mm: float,
                 p_n: float, v2_n: float, v3_n: float,
                 t_nmm: float, m2_nmm: float, m3_nmm: float):
        """إضافة قوة - ✅ جميع القيم REAL"""
        force_data = {
            'output_case': output_case,
            'station_mm': float(station_mm),     # ✅ REAL
            'P_N': float(p_n),                   # ✅ REAL
            'V2_N': float(v2_n),                 # ✅ REAL
            'V3_N': float(v3_n),                 # ✅ REAL
            'T_Nmm': float(t_nmm),               # ✅ REAL
            'M2_Nmm': float(m2_nmm),             # ✅ REAL
            'M3_Nmm': float(m3_nmm)              # ✅ REAL
        }
        self.forces.append(force_data)
        self.update_timestamp()
    
    def get_info(self) -> Dict[str, Any]:
        """الحصول على معلومات الجدار"""
        return {
            'pier_name': self.pier_name,
            'story': self.story_name,
            'section': self.section_name,
            'reinforcement': self.reinforcement_type,
            'num_forces': len(self.forces),
            'area_mm2': self.connectivity['Area_mm2'],
            'perimeter_mm': self.connectivity['Perimeter_mm']
        }
    
    def __repr__(self) -> str:
        return f"Wall({self.pier_name} in {self.story_name})"
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل إلى قاموس"""
        data = super().to_dict()
        data.update({
            'pier_name': self.pier_name,
            'story_name': self.story_name,
            'section_name': self.section_name,
            'unique_name': self.unique_name,
            'internal_id': self.internal_id,
            'reinforcement_type': self.reinforcement_type,
            'rho_percent': self.rho_percent,
            'connectivity': self.connectivity,
            'num_forces': len(self.forces)
        })
        return data
    
    def get_max_shear(self) -> Optional[Dict]:
        """الحصول على أقصى قص"""
        if not self.forces:
            return None
        return max(self.forces, key=lambda x: abs(x['V2_N']))
    
    def get_max_axial_force(self) -> Optional[Dict]:
        """الحصول على أقصى قوة محورية"""
        if not self.forces:
            return None
        return max(self.forces, key=lambda x: abs(x['P_N']))
