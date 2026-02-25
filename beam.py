
"""
===============================================================================
models/beam.py - نموذج العتبة (مصحح كامل)
===============================================================================
"""

from typing import Dict, Optional, Any
from models.base import BaseElement


class Beam(BaseElement):
    """نموذج العتبة"""
    
    def __init__(self, etabs_id: str, story_name: str, section_name: str):
        """
        إنشاء عتبة
        
        المعاملات:
            etabs_id: معرف ETABS (مثل "B1")
            story_name: اسم الطابق
            section_name: اسم المقطع
        """
        super().__init__(etabs_id, "Beam")
        self.etabs_id = etabs_id
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
            'UniquePtI': None,
            'UniquePtJ': None,
            'Length_mm': None,      # ✅ REAL
            'Station_mm': None      # ✅ REAL
        }
        
        # القوى - ✅ جميعها REAL
        self.forces = []
    
    def set_connectivity(self, pt_i: int, pt_j: int, length_mm: float, station_mm: float = None):
        """تعيين بيانات الاتصال - ✅ REAL"""
        self.connectivity['UniquePtI'] = pt_i
        self.connectivity['UniquePtJ'] = pt_j
        self.connectivity['Length_mm'] = float(length_mm)  # ✅ تحويل REAL
        self.connectivity['Station_mm'] = float(station_mm) if station_mm else None  # ✅ تحويل REAL
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
        """الحصول على معلومات العتبة"""
        return {
            'etabs_id': self.etabs_id,
            'story': self.story_name,
            'section': self.section_name,
            'reinforcement': self.reinforcement_type,
            'num_forces': len(self.forces),
            'length_mm': self.connectivity['Length_mm']
        }
    
    def __repr__(self) -> str:
        return f"Beam({self.etabs_id} in {self.story_name})"
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل إلى قاموس"""
        data = super().to_dict()
        data.update({
            'etabs_id': self.etabs_id,
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
    
    def get_max_moment(self) -> Optional[Dict]:
        """الحصول على أقصى عزم"""
        if not self.forces:
            return None
        return max(self.forces, key=lambda x: abs(x['M2_Nmm']))

