# models/column.py - نموذج العمود (Column Model)
# معدّل بدقة لطابق القاعدة الجديدة

from typing import Dict, List, Optional, Any
from datetime import datetime


class Column:
    """
    نموذج العمود المعدّل للقاعدة الجديدة
    
    يطابق تماماً جداول:
    - Column_Object_Connectivity
    - Frame_Section_Property_Definitions_Concrete_Column_Reinforcing
    - Element_Forces_Columns
    - Objects_and_Elements_Joints
    """
    
    def __init__(self, etabs_id: str, story_name: str, section_name: str):
        """
        إنشاء عمود
        
        Args:
            etabs_id: معرف ETABS (مثل "C1")
            story_name: اسم الطابق (مثل "Ground Floor")
            section_name: اسم المقطع (مثل "C50x50")
        """
        self.etabs_id = etabs_id
        self.story_name = story_name
        self.section_name = section_name
        
        # ═══════════════════════════════════════════════════════════════
        # معرفات من قاعدة البيانات الجديدة (ستُملأ أثناء الربط)
        # ═══════════════════════════════════════════════════════════════
        
        # من Column_Object_Connectivity
        self.unique_name: Optional[int] = None       # INT UNIQUE
        self.element_id: Optional[int] = None        # INT (Foreign Key)
        
        # من Frame_Assignments_Section_Properties
        self.frame_assignment_id: Optional[int] = None  # ID (Foreign Key)
        
        # من Objects_and_Elements_Joints
        self.element_name: Optional[int] = None      # INT
        
        # ═══════════════════════════════════════════════════════════════
        # بيانات الاتصال من Column_Object_Connectivity
        # ═══════════════════════════════════════════════════════════════
        
        self.connectivity = {
            'Unique_Name': None,                    # INT UNIQUE
            'Story': story_name,                    # VARCHAR(255)
            'ColumnBay': None,                      # VARCHAR(255)
            'UniquePtI': None,                      # INT - نقطة البداية
            'UniquePtJ': None,                      # INT - نقطة النهاية
            'Length': None,                         # INT - الطول
            'GUID': None,                           # VARCHAR(255)
            'ElementID': None                       # INT (Foreign Key)
        }
        
        # ═══════════════════════════════════════════════════════════════
        # بيانات التسليح من Frame_Section_Property_Definitions_Concrete_Column_Reinforcing
        # ═══════════════════════════════════════════════════════════════
        
        self.reinforcement = {
            'Name': section_name,                                   # VARCHAR(255) UNIQUE
            'Longitudinal_Bar_Material': None,                      # VARCHAR(255)
            'Tie_Bar_Material': None,                               # VARCHAR(255)
            'Reinforcement_Configuration': None,                    # VARCHAR(255)
            'Is_Designed': None,                                    # VARCHAR(255)
            'Clear_Cover_to_Ties': None,                            # FLOAT
            'Number_Bars_3_Dir': None,                              # INT
            'Number_Bars_2_Dir': None,                              # INT
            'Longitudinal_Bar_Size': None,                          # FLOAT
            'Corner_Bar_Size': None,                                # FLOAT
            'Tie_Bar_Size': None,                                   # FLOAT
            'Tie_Bar_Spacing': None,                                # FLOAT
            'Number_Ties_3_Dir': None,                              # INT
            'Number_Ties_2_Dir': None,                              # INT
            # Foreign Keys (ستُملأ أثناء الربط)
            'LonZgitudinal_Bar_MaterialID': None,                   # INT (FK)
            'Tie_Bar_MaterialID': None,                             # INT (FK)
            'NameID': None                                          # INT (FK)
        }
        
        # ═══════════════════════════════════════════════════════════════
        # قوى العناصر من Element_Forces_Columns
        # ═══════════════════════════════════════════════════════════════
        
        self.forces: List[Dict[str, Any]] = []
        
        # ═══════════════════════════════════════════════════════════════
        # بيانات النقاط من Objects_and_Elements_Joints
        # ═══════════════════════════════════════════════════════════════
        
        self.joints = {
            'start_point': {                        # للنقطة I
                'Element_Name': None,               # INT
                'Story': story_name,                # VARCHAR(255)
                'Object_Type': None,                # VARCHAR(255)
                'Object_Label': None,               # VARCHAR(255)
                'Object_Name': None,                # FLOAT
                'Global_X': None,                   # FLOAT
                'Global_Y': None,                   # FLOAT
                'Global_Z': None                    # FLOAT
            },
            'end_point': {                          # للنقطة J
                'Element_Name': None,               # INT
                'Story': story_name,                # VARCHAR(255)
                'Object_Type': None,                # VARCHAR(255)
                'Object_Label': None,               # VARCHAR(255)
                'Object_Name': None,                # FLOAT
                'Global_X': None,                   # FLOAT
                'Global_Y': None,                   # FLOAT
                'Global_Z': None                    # FLOAT
            }
        }
        
        # ═══════════════════════════════════════════════════════════════
        # البيانات الوصفية
        # ═══════════════════════════════════════════════════════════════
        
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    # ═══════════════════════════════════════════════════════════════════════
    # دوال تعيين البيانات
    # ═══════════════════════════════════════════════════════════════════════
    
    def set_connectivity(self, unique_name: int, column_bay: str,
                        pt_i: int, pt_j: int, length: int, guid: str = None):
        """
        تعيين بيانات الاتصال من Column_Object_Connectivity
        
        Args:
            unique_name: INT UNIQUE - معرف فريد
            column_bay: VARCHAR(255) - اسم الخليج
            pt_i: INT - نقطة البداية
            pt_j: INT - نقطة النهاية
            length: INT - الطول
            guid: VARCHAR(255) - معرف GUID
        """
        self.unique_name = int(unique_name)
        self.connectivity['Unique_Name'] = int(unique_name)
        self.connectivity['ColumnBay'] = column_bay
        self.connectivity['UniquePtI'] = int(pt_i)
        self.connectivity['UniquePtJ'] = int(pt_j)
        self.connectivity['Length'] = int(length)
        if guid:
            self.connectivity['GUID'] = guid
        self.updated_at = datetime.now()
    
    def set_reinforcement(self,
                         long_bar_material: str,
                         tie_bar_material: str,
                         config: str,
                         is_designed: str = None,
                         clear_cover: float = None,
                         num_bars_3dir: int = None,
                         num_bars_2dir: int = None,
                         long_bar_size: float = None,
                         corner_bar_size: float = None,
                         tie_bar_size: float = None,
                         tie_spacing: float = None,
                         num_ties_3dir: int = None,
                         num_ties_2dir: int = None):
        """
        تعيين بيانات التسليح من Frame_Section_Property_Definitions_Concrete_Column_Reinforcing
        
        Args:
            long_bar_material: VARCHAR(255) - مادة التسليح الطولي
            tie_bar_material: VARCHAR(255) - مادة الأسياخ
            config: VARCHAR(255) - تكوين التسليح
            is_designed: VARCHAR(255) - هل تم تصميمه؟
            clear_cover: FLOAT - الغطاء الخرساني
            num_bars_3dir: INT - عدد الأسياخ (اتجاه 3)
            num_bars_2dir: INT - عدد الأسياخ (اتجاه 2)
            long_bar_size: FLOAT - حجم التسليح الطولي
            corner_bar_size: FLOAT - حجم سيخ الزاوية
            tie_bar_size: FLOAT - حجم سيخ الأسياخ
            tie_spacing: FLOAT - مسافة الأسياخ
            num_ties_3dir: INT - عدد الأسياخ (اتجاه 3)
            num_ties_2dir: INT - عدد الأسياخ (اتجاه 2)
        """
        self.reinforcement['Longitudinal_Bar_Material'] = long_bar_material
        self.reinforcement['Tie_Bar_Material'] = tie_bar_material
        self.reinforcement['Reinforcement_Configuration'] = config
        
        if is_designed:
            self.reinforcement['Is_Designed'] = is_designed
        if clear_cover is not None:
            self.reinforcement['Clear_Cover_to_Ties'] = float(clear_cover)
        if num_bars_3dir is not None:
            self.reinforcement['Number_Bars_3_Dir'] = int(num_bars_3dir)
        if num_bars_2dir is not None:
            self.reinforcement['Number_Bars_2_Dir'] = int(num_bars_2dir)
        if long_bar_size is not None:
            self.reinforcement['Longitudinal_Bar_Size'] = float(long_bar_size)
        if corner_bar_size is not None:
            self.reinforcement['Corner_Bar_Size'] = float(corner_bar_size)
        if tie_bar_size is not None:
            self.reinforcement['Tie_Bar_Size'] = float(tie_bar_size)
        if tie_spacing is not None:
            self.reinforcement['Tie_Bar_Spacing'] = float(tie_spacing)
        if num_ties_3dir is not None:
            self.reinforcement['Number_Ties_3_Dir'] = int(num_ties_3dir)
        if num_ties_2dir is not None:
            self.reinforcement['Number_Ties_2_Dir'] = int(num_ties_2dir)
        
        self.updated_at = datetime.now()
    
    def add_force(self,
                 output_case: str,
                 case_type: str,
                 station: float,
                 p: float,
                 v2: float = None,
                 v3: float = None,
                 t: float = None,
                 m2: float = None,
                 m3: float = None,
                 element: int = None,
                 elem_station: float = None,
                 location: float = None):
        """
        إضافة قوة من Element_Forces_Columns
        
        Args:
            output_case: VARCHAR(255) - اسم حالة التحميل
            case_type: VARCHAR(255) - نوع الحالة
            station: FLOAT - محطة القياس
            p: FLOAT - قوة محورية
            v2: FLOAT - قوة قص (اتجاه 2)
            v3: FLOAT - قوة قص (اتجاه 3)
            t: FLOAT - عزم فتل
            m2: FLOAT - عزم انحناء (اتجاه 2)
            m3: FLOAT - عزم انحناء (اتجاه 3)
            element: INT - معرف العنصر
            elem_station: FLOAT - محطة العنصر
            location: FLOAT - الموقع
        """
        force_record = {
            'Story': self.story_name,               # VARCHAR(255)
            'Column': self.etabs_id,                # VARCHAR(255)
            'Unique_Name': self.unique_name,        # INT
            'Output_Case': output_case,             # VARCHAR(255)
            'Case_Type': case_type,                 # VARCHAR(255)
            'Station': float(station),              # FLOAT
            'P': float(p),                          # FLOAT
            'V2': float(v2) if v2 is not None else None,      # FLOAT
            'V3': float(v3) if v3 is not None else None,      # FLOAT
            'T': float(t) if t is not None else None,         # FLOAT
            'M2': float(m2) if m2 is not None else None,      # FLOAT
            'M3': float(m3) if m3 is not None else None,      # FLOAT
            'Element': int(element) if element is not None else None,  # INT
            'Elem_Station': float(elem_station) if elem_station is not None else None,  # FLOAT
            'Location': float(location) if location is not None else None,              # FLOAT
            'ElementID': self.element_id,           # INT (FK)
            'Load_case_id': None                    # INT (FK) - سيُملأ أثناء الربط
        }
        self.forces.append(force_record)
        self.updated_at = datetime.now()
    
    def set_start_joint(self, element_name: int, object_type: str,
                       object_label: str, object_name: float,
                       global_x: float, global_y: float, global_z: float):
        """
        تعيين نقطة البداية من Objects_and_Elements_Joints
        """
        self.joints['start_point'] = {
            'Element_Name': int(element_name),
            'Story': self.story_name,
            'Object_Type': object_type,
            'Object_Label': object_label,
            'Object_Name': float(object_name),
            'Global_X': float(global_x),
            'Global_Y': float(global_y),
            'Global_Z': float(global_z)
        }
        self.element_name = int(element_name)
        self.updated_at = datetime.now()
    
    def set_end_joint(self, element_name: int, object_type: str,
                     object_label: str, object_name: float,
                     global_x: float, global_y: float, global_z: float):
        """
        تعيين نقطة النهاية من Objects_and_Elements_Joints
        """
        self.joints['end_point'] = {
            'Element_Name': int(element_name),
            'Story': self.story_name,
            'Object_Type': object_type,
            'Object_Label': object_label,
            'Object_Name': float(object_name),
            'Global_X': float(global_x),
            'Global_Y': float(global_y),
            'Global_Z': float(global_z)
        }
        self.updated_at = datetime.now()
    
    # ═══════════════════════════════════════════════════════════════════════
    # دوال الحصول على البيانات
    # ═══════════════════════════════════════════════════════════════════════
    
    def get_info(self) -> Dict[str, Any]:
        """الحصول على ملخص معلومات العمود"""
        return {
            'etabs_id': self.etabs_id,
            'story_name': self.story_name,
            'section_name': self.section_name,
            'unique_name': self.unique_name,
            'element_id': self.element_id,
            'reinforcement_config': self.reinforcement['Reinforcement_Configuration'],
            'tie_bar_size': self.reinforcement['Tie_Bar_Size'],
            'clear_cover': self.reinforcement['Clear_Cover_to_Ties'],
            'num_forces': len(self.forces),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل إلى قاموس كامل يطابق قاعدة البيانات"""
        return {
            'etabs_id': self.etabs_id,
            'story_name': self.story_name,
            'section_name': self.section_name,
            'unique_name': self.unique_name,
            'element_id': self.element_id,
            'frame_assignment_id': self.frame_assignment_id,
            'connectivity': self.connectivity.copy(),
            'reinforcement': self.reinforcement.copy(),
            'joints': self.joints.copy(),
            'forces': self.forces.copy(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def get_max_force(self, force_type: str = 'P') -> Optional[Dict]:
        """الحصول على أقصى قوة من نوع معين"""
        if not self.forces:
            return None
        valid_forces = [f for f in self.forces if f.get(force_type) is not None]
        if not valid_forces:
            return None
        return max(valid_forces, key=lambda x: abs(x[force_type]))
    
    def get_max_moment(self) -> Optional[Dict]:
        """الحصول على أقصى عزم"""
        if not self.forces:
            return None
        
        max_moment_force = None
        max_moment_value = 0
        
        for force in self.forces:
            m2 = force.get('M2') or 0
            m3 = force.get('M3') or 0
            total_moment = abs(m2) + abs(m3)
            
            if total_moment > max_moment_value:
                max_moment_value = total_moment
                max_moment_force = force
        
        return max_moment_force
    
    def __repr__(self) -> str:
        return f"Column(ID={self.etabs_id}, Story={self.story_name}, Section={self.section_name})"
