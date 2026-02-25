# database/connection.py
# الاتصال بقاعدة البيانات وجلب البيانات كـ Objects
# Database Connection & Data Retrieval - النسخة النهائية المكتملة


import sqlite3
from typing import Optional, List, Dict, Any
from pathlib import Path


from models.base import BaseElement, Material, Section, Story
from models.column import Column
from models.load_and_force import LoadCombination, Force, LoadCaseGroup



class DatabaseConnection:
    """
    فئة الاتصال بقاعدة البيانات
    
    تقوم بـ:
    1. الاتصال بقاعدة البيانات
    2. جلب البيانات من جميع الجداول
    3. تحويل البيانات إلى Objects
    
    الجداول المدعومة (11/11):
    ✅ Story_Definitions
    ✅ Objects_and_Elements_Joints
    ✅ Column_Object_Connectivity
    ✅ Material_Properties_Concrete_Data
    ✅ Material_Properties_Rebar_Data
    ✅ Frame_Section_Property_Definitions_Concrete_Column_Reinforcing
    ✅ Frame_Section_Property_Definitions_Concrete_Rectangular
    ✅ Frame_Assignments_Section_Properties
    ✅ Load_Combination_Definitions
    ✅ Element_Forces_Columns
    ✅ Genralinput
    """
    
    def __init__(self, db_path: str):
        """
        تهيئة الاتصال
        
        Args:
            db_path: مسار ملف قاعدة البيانات
        """
        self.db_path = str(db_path)
        self.connection = None
        self.cursor = None
    
    def connect(self) -> bool:
        """
        الاتصال بقاعدة البيانات
        
        Returns:
            True إذا نجح الاتصال
        """
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # للوصول بالأسماء
            self.cursor = self.connection.cursor()
            return True
        except Exception as e:
            print(f"❌ فشل الاتصال: {e}")
            return False
    
    def disconnect(self):
        """قطع الاتصال"""
        if self.connection:
            self.connection.close()
    
    # ════════════════════════════════════════════════════════════════
    # جلب المواد
    # ════════════════════════════════════════════════════════════════
    
    def get_concrete_material(self, material_id: int) -> Optional[Material]:
        """
        جلب مادة خرسانة من قاعدة البيانات
        
        Args:
            material_id: معرف المادة
            
        Returns:
            كائن Material أو None
        """
        try:
            self.cursor.execute("""
                SELECT ID, Material, Fc, LtWtConc, IsUserFr, SSCurveOpt,
                       SSHysType, SFc, SCap, FinalSlope, FAngle, DAngle
                FROM Material_Properties_Concrete_Data
                WHERE ID = ?
            """, (material_id,))
            
            row = self.cursor.fetchone()
            if not row:
                return None
            
            # إنشاء كائن Material
            concrete = Material(
                name=row['Material'],
                material_type='Concrete',
                strength=float(row['Fc'])
            )
            concrete.db_id = row['ID']
            
            # تعيين خصائص الخرسانة
            concrete.set_concrete_properties(
                Fc=row['Fc'],
                LtWtConc=row['LtWtConc'],
                IsUserFr=row['IsUserFr'],
                SSCurveOpt=row['SSCurveOpt'],
                SSHysType=row['SSHysType'],
                SFc=row['SFc'],
                SCap=row['SCap'],
                FinalSlope=row['FinalSlope'],
                FAngle=row['FAngle'],
                DAngle=row['DAngle']
            )
            
            return concrete
        except Exception as e:
            print(f"❌ خطأ في جلب الخرسانة: {e}")
            return None
    
    def get_rebar_material(self, material_id: int) -> Optional[Material]:
        """
        جلب مادة حديد من قاعدة البيانات
        
        Args:
            material_id: معرف المادة
            
        Returns:
            كائن Material أو None
        """
        try:
            self.cursor.execute("""
                SELECT ID, Material, Fy, Fu, Fye, Fue, SSCurveOpt,
                       SSHysType, SHard, SCap, FinalSlope
                FROM Material_Properties_Rebar_Data
                WHERE ID = ?
            """, (material_id,))
            
            row = self.cursor.fetchone()
            if not row:
                return None
            
            # إنشاء كائن Material
            rebar = Material(
                name=row['Material'],
                material_type='Rebar',
                strength=float(row['Fy'])
            )
            rebar.db_id = row['ID']
            
            # تعيين خصائص الحديد
            rebar.set_rebar_properties(
                Fy=row['Fy'],
                Fu=row['Fu'],
                Fye=row['Fye'],
                Fue=row['Fue'],
                SSCurveOpt=row['SSCurveOpt'],
                SSHysType=row['SSHysType'],
                SHard=row['SHard'],
                SCap=row['SCap'],
                FinalSlope=row['FinalSlope']
            )
            
            return rebar
        except Exception as e:
            print(f"❌ خطأ في جلب الحديد: {e}")
            return None
    
    def get_concrete_lower_bound(self, material_id: int) -> Optional[float]:
        """
        جلب f'c,LE (Lower Bound compressive strength)
        
        إذا لم تكن موجودة، نستخدم f'c العادية
        
        حسب ASCE 41-17: f'c,LE = f'c (بدون تخفيض في معظم الحالات)
        
        Args:
            material_id: معرف المادة
            
        Returns:
            f'c,LE (MPa) أو None
        """
        try:
            # جرّب جلب Lower Bound أولاً (إذا كانت موجودة في جدول منفصل)
            self.cursor.execute("""
            SELECT Fc_LB
            FROM Material_Properties_Concrete_LowerBound
            WHERE ID = ?
            """, (material_id,))
            
            lb_row = self.cursor.fetchone()
            if lb_row and lb_row[0]:
                return float(lb_row[0])
            
            # إذا لم توجد، استخدم f'c العادية (حسب ASCE 41-17)
            self.cursor.execute("""
            SELECT Fc
            FROM Material_Properties_Concrete_Data
            WHERE ID = ?
            """, (material_id,))
            
            normal_row = self.cursor.fetchone()
            if normal_row:
                return float(normal_row[0])
                
        except Exception as e:
            print(f"❌ خطأ في جلب Lower Bound Concrete: {e}")
        
        return None
    
    def get_rebar_lower_bound(self, material_id: int) -> Optional[float]:
        """
        جلب fy,LE (Lower Bound yield strength)
        
        إذا لم تكن موجودة، نستخدم fy العادي
        
        حسب ASCE 41-17: fy,LE = fy (بدون تخفيض في معظم الحالات)
        
        Args:
            material_id: معرف المادة
            
        Returns:
            fy,LE (MPa) أو None
        """
        try:
            # جرّب جلب Lower Bound أولاً (إذا كانت موجودة في جدول منفصل)
            self.cursor.execute("""
            SELECT Fy_LB
            FROM Material_Properties_Rebar_LowerBound
            WHERE ID = ?
            """, (material_id,))
            
            lb_row = self.cursor.fetchone()
            if lb_row and lb_row[0]:
                return float(lb_row[0])
            
            # إذا لم توجد، استخدم fy العادي (حسب ASCE 41-17)
            self.cursor.execute("""
            SELECT Fy
            FROM Material_Properties_Rebar_Data
            WHERE ID = ?
            """, (material_id,))
            
            normal_row = self.cursor.fetchone()
            if normal_row:
                return float(normal_row[0])
                
        except Exception as e:
            print(f"❌ خطأ في جلب Lower Bound Rebar: {e}")
        
        return None
    
    # ════════════════════════════════════════════════════════════════
    # جلب المقاطع
    # ════════════════════════════════════════════════════════════════
    
    def get_section(self, section_id: int) -> Optional[Section]:
        """
        جلب مقطع من قاعدة البيانات
        
        Args:
            section_id: معرف المقطع
            
        Returns:
            كائن Section أو None
        """
        try:
            self.cursor.execute("""
                SELECT ID, Name, Material, Depth, Width, Area,
                       Rigid_Zone, Notional_Size_Type, Notional_Auto_Factor,
                       Design_Type, From_File, Color, GUID,
                       Area_Modifier, As2_Modifier, As3_Modifier, J_Modifier,
                       I22_Modifier, I33_Modifier, Mass_Modifier, Weight_Modifier,
                       MaterialID
                FROM Frame_Section_Property_Definitions_Concrete_Rectangular
                WHERE ID = ?
            """, (section_id,))
            
            row = self.cursor.fetchone()
            if not row:
                return None
            
            # إنشاء كائن Section
            section = Section(
                name=row['Name'],
                material=row['Material'],
                section_type='Rectangular'
            )
            section.db_id = row['ID']
            section.material_db_id = row['MaterialID']
            
            # تعيين الخصائص الهندسية
            section.set_geometric_properties(
                Depth=row['Depth'],
                Width=row['Width'],
                Area=row['Area']
            )
            
            # تعيين معاملات الصلابة
            section.set_stiffness_modifiers(
                Area_Modifier=row['Area_Modifier'],
                As2_Modifier=row['As2_Modifier'],
                As3_Modifier=row['As3_Modifier'],
                J_Modifier=row['J_Modifier'],
                I22_Modifier=row['I22_Modifier'],
                I33_Modifier=row['I33_Modifier'],
                Mass_Modifier=row['Mass_Modifier'],
                Weight_Modifier=row['Weight_Modifier']
            )
            
            # تعيين الخصائص الإضافية
            section.set_additional_properties(
                From_File=row['From_File'],
                Rigid_Zone=row['Rigid_Zone'],
                Notional_Size_Type=row['Notional_Size_Type'],
                Notional_Auto_Factor=row['Notional_Auto_Factor'],
                Design_Type=row['Design_Type'],
                Color=row['Color'],
                GUID=row['GUID']
            )
            
            return section
        except Exception as e:
            print(f"❌ خطأ في جلب المقطع: {e}")
            return None
    
    # ════════════════════════════════════════════════════════════════
    # جلب الطوابق
    # ════════════════════════════════════════════════════════════════
    
    def get_story(self, story_id: int) -> Optional[Story]:
        """
        جلب طابق من قاعدة البيانات
        
        Args:
            story_id: معرف الطابق
            
        Returns:
            كائن Story أو None
        """
        try:
            self.cursor.execute("""
                SELECT ID, Tower, Name, Height, Master_Story, Similar_To,
                       Splice_Story, Splice_Height, Color, GUID
                FROM Story_Definitions
                WHERE ID = ?
            """, (story_id,))
            
            row = self.cursor.fetchone()
            if not row:
                return None
            
            # إنشاء كائن Story
            story = Story(
                name=row['Name'],
                height=float(row['Height'])
            )
            story.db_id = row['ID']
            
            # تعيين خصائص ETABS
            story.set_etabs_properties(
                tower=row['Tower'],
                master_story=row['Master_Story'],
                similar_to=row['Similar_To'],
                splice_story=row['Splice_Story'],
                splice_height=row['Splice_Height'],
                color=row['Color'],
                guid=row['GUID']
            )
            
            return story
        except Exception as e:
            print(f"❌ خطأ في جلب الطابق: {e}")
            return None
    
    # ════════════════════════════════════════════════════════════════
    # جلب الأعمدة (الجزء الأساسي)
    # ════════════════════════════════════════════════════════════════
    
    def get_column(self, column_id: int, story_name: str = None) -> Optional[Column]:
        """
        جلب عمود من قاعدة البيانات مع جميع بيانات القص الخام
        
        Args:
            column_id: معرف العمود (Unique_Name)
            story_name: اسم الطابق (اختياري)
            
        Returns:
            كائن Column كامل مع جميع البيانات الخام
        """
        try:
            # جلب بيانات الاتصال
            self.cursor.execute("""
                SELECT Unique_Name, Story, ColumnBay, UniquePtI, UniquePtJ,
                       Length, GUID, ElementID
                FROM Column_Object_Connectivity
                WHERE Unique_Name = ?
            """, (column_id,))
            
            connectivity_row = self.cursor.fetchone()
            if not connectivity_row:
                return None
            
            # إنشاء كائن Column
            column = Column(
                etabs_id=f"C{column_id}",
                story_name=connectivity_row['Story'],
                section_name="Unknown"
            )
            
            # تعيين بيانات الاتصال
            column.set_connectivity(
                unique_name=connectivity_row['Unique_Name'],
                column_bay=connectivity_row['ColumnBay'],
                pt_i=connectivity_row['UniquePtI'],
                pt_j=connectivity_row['UniquePtJ'],
                length=connectivity_row['Length'],
                guid=connectivity_row['GUID']
            )
            column.element_id = connectivity_row['ElementID']
            
            # جلب جميع البيانات الإضافية
            self._load_column_dimensions(column)
            self._load_column_reinforcement(column)
            self._load_column_joints(column)
            self._load_column_forces(column)
            
            return column
        except Exception as e:
            print(f"❌ خطأ في جلب العمود: {e}")
            return None
    
    def _load_column_dimensions(self, column: Column):
        """
        تحميل الأبعاد الهندسية (Height, Width) من جدول المقاطع
        
        Args:
            column: كائن العمود المراد تحميل الأبعاد إليه
        """
        try:
            # جلب معرف المقطع من Frame_Assignments
            self.cursor.execute("""
            SELECT SectionName
            FROM Frame_Assignments_Section_Properties
            WHERE ElementID = ?
            LIMIT 1
            """, (column.element_id,))
            
            section_row = self.cursor.fetchone()
            if not section_row:
                return
            
            section_name = section_row[0]
            
            # ثم جلب الأبعاد من جدول المقاطع
            self.cursor.execute("""
            SELECT Depth, Width, Area
            FROM Frame_Section_Property_Definitions_Concrete_Rectangular
            WHERE Name = ?
            """, (section_name,))
            
            dim_row = self.cursor.fetchone()
            if dim_row:
                height = float(dim_row['Depth'])
                width = float(dim_row['Width'])
                area = float(dim_row['Area'])
                
                column.reinforcement['Height'] = height
                column.reinforcement['Width'] = width
                column.reinforcement['Area'] = area
                column.section_name = section_name
        except Exception as e:
            print(f"⚠️ تحذير: خطأ في جلب الأبعاد: {e}")
    
    def _load_column_reinforcement(self, column: Column):
        """
        تحميل بيانات التسليح الكاملة للعمود مع Foreign Keys
        
        Args:
            column: كائن العمود المراد تحميل التسليح إليه
        """
        try:
            self.cursor.execute("""
            SELECT 
                ID,
                Name,
                Longitudinal_Bar_Material,
                Tie_Bar_Material,
                Clear_Cover_to_Ties,
                Number_Bars_3_Dir,
                Number_Bars_2_Dir,
                Longitudinal_Bar_Size,
                Tie_Bar_Size,
                Tie_Bar_Spacing,
                Number_Ties_3_Dir,
                Number_Ties_2_Dir,
                Reinforcement_Configuration,
                LonZgitudinal_Bar_MaterialID,
                Tie_Bar_MaterialID,
                NameID
            FROM Frame_Section_Property_Definitions_Concrete_Column_Reinforcing
            WHERE Name = ?
            """, (column.section_name,))
            
            row = self.cursor.fetchone()
            if row:
                column.reinforcement['ID'] = row['ID']
                column.reinforcement['Longitudinal_Bar_Material'] = row['Longitudinal_Bar_Material']
                column.reinforcement['Tie_Bar_Material'] = row['Tie_Bar_Material']
                column.reinforcement['Clear_Cover_to_Ties'] = float(row['Clear_Cover_to_Ties']) if row['Clear_Cover_to_Ties'] else 40
                column.reinforcement['Number_Bars_3_Dir'] = int(row['Number_Bars_3_Dir']) if row['Number_Bars_3_Dir'] else 0
                column.reinforcement['Number_Bars_2_Dir'] = int(row['Number_Bars_2_Dir']) if row['Number_Bars_2_Dir'] else 0
                column.reinforcement['Longitudinal_Bar_Size'] = float(row['Longitudinal_Bar_Size']) if row['Longitudinal_Bar_Size'] else 16
                column.reinforcement['Tie_Bar_Size'] = float(row['Tie_Bar_Size']) if row['Tie_Bar_Size'] else 8
                column.reinforcement['Tie_Bar_Spacing'] = float(row['Tie_Bar_Spacing']) if row['Tie_Bar_Spacing'] else 150
                column.reinforcement['Number_Ties_3_Dir'] = int(row['Number_Ties_3_Dir']) if row['Number_Ties_3_Dir'] else 2
                column.reinforcement['Number_Ties_2_Dir'] = int(row['Number_Ties_2_Dir']) if row['Number_Ties_2_Dir'] else 2
                
                # ✅ إضافة Foreign Keys:
                column.reinforcement['LonZgitudinal_Bar_MaterialID'] = row['LonZgitudinal_Bar_MaterialID']
                column.reinforcement['Tie_Bar_MaterialID'] = row['Tie_Bar_MaterialID']
                column.reinforcement['NameID'] = row['NameID']
                
        except Exception as e:
            print(f"⚠️ تحذير: خطأ في جلب التسليح: {e}")
    
    def _load_column_joints(self, column: Column):
        """
        تحميل بيانات النقاط (Joints) والإحداثيات للعمود
        
        Args:
            column: كائن العمود المراد تحميل النقاط إليه
        """
        try:
            # جلب بيانات النقطة الأولى
            if column.unique_pt_i:
                self.cursor.execute("""
                SELECT Joint_ID, Unique_Name, X_Coord, Y_Coord, Z_Coord, 
                       Global_X, Global_Y, Global_Z
                FROM Objects_and_Elements_Joints
                WHERE Unique_Name = ?
                LIMIT 1
                """, (column.unique_pt_i,))
                
                joint_i = self.cursor.fetchone()
                if joint_i:
                    column.set_start_joint({
                        'joint_id': joint_i['Joint_ID'],
                        'name': joint_i['Unique_Name'],
                        'x': float(joint_i['X_Coord']),
                        'y': float(joint_i['Y_Coord']),
                        'z': float(joint_i['Z_Coord']),
                        'global_x': float(joint_i['Global_X']),
                        'global_y': float(joint_i['Global_Y']),
                        'global_z': float(joint_i['Global_Z'])
                    })
            
            # جلب بيانات النقطة الثانية
            if column.unique_pt_j:
                self.cursor.execute("""
                SELECT Joint_ID, Unique_Name, X_Coord, Y_Coord, Z_Coord,
                       Global_X, Global_Y, Global_Z
                FROM Objects_and_Elements_Joints
                WHERE Unique_Name = ?
                LIMIT 1
                """, (column.unique_pt_j,))
                
                joint_j = self.cursor.fetchone()
                if joint_j:
                    column.set_end_joint({
                        'joint_id': joint_j['Joint_ID'],
                        'name': joint_j['Unique_Name'],
                        'x': float(joint_j['X_Coord']),
                        'y': float(joint_j['Y_Coord']),
                        'z': float(joint_j['Z_Coord']),
                        'global_x': float(joint_j['Global_X']),
                        'global_y': float(joint_j['Global_Y']),
                        'global_z': float(joint_j['Global_Z'])
                    })
        except Exception as e:
            print(f"⚠️ تحذير: خطأ في جلب النقاط: {e}")
    
    def _load_column_forces(self, column: Column):
        """
        تحميل جميع القوى للعمود
        
        Args:
            column: كائن العمود المراد تحميل القوى إليه
        """
        try:
            self.cursor.execute("""
                SELECT Story, Column, Unique_Name, Output_Case, Case_Type,
                       Station, P, V2, V3, T, M2, M3, Element,
                       Elem_Station, Location, ElementID, Load_case_id
                FROM Element_Forces_Columns
                WHERE Unique_Name = ?
                ORDER BY Output_Case
            """, (column.unique_name,))
            
            rows = self.cursor.fetchall()
            for row in rows:
                column.add_force(
                    output_case=row['Output_Case'],
                    case_type=row['Case_Type'],
                    station=row['Station'],
                    p=row['P'],
                    v2=row['V2'],
                    v3=row['V3'],
                    t=row['T'],
                    m2=row['M2'],
                    m3=row['M3'],
                    element=row['Element'],
                    elem_station=row['Elem_Station'],
                    location=row['Location']
                )
        except Exception as e:
            print(f"⚠️ تحذير: خطأ في جلب القوى: {e}")
    
    # ════════════════════════════════════════════════════════════════
    # جلب معلومات التعيين (NEW)
    # ════════════════════════════════════════════════════════════════
    
    def get_frame_assignment(self, element_id: int) -> Optional[Dict]:
        """جلب معلومات تعيين المقطع للعنصر (NEW)"""
        try:
            self.cursor.execute("""
            SELECT ID, Story, Label, UniqueName, Shape, 
                   Auto_Select_List, Section_Property, Section_PropertyID
            FROM Frame_Assignments_Section_Properties
            WHERE ID = ?
            """, (element_id,))
            
            row = self.cursor.fetchone()
            if row:
                return {
                    'id': row['ID'],
                    'story': row['Story'],
                    'label': row['Label'],
                    'unique_name': row['UniqueName'],
                    'shape': row['Shape'],
                    'auto_select_list': row['Auto_Select_List'],
                    'section_property': row['Section_Property'],
                    'section_property_id': row['Section_PropertyID']
                }
        except Exception as e:
            print(f"❌ خطأ في جلب التعيين: {e}")
        
        return None

    def get_frame_assignments_by_story(self, story_name: str) -> List[Dict]:
        """جلب جميع التعيينات في طابق معين (NEW)"""
        try:
            self.cursor.execute("""
            SELECT ID, Story, Label, UniqueName, Shape, 
                   Auto_Select_List, Section_Property, Section_PropertyID
            FROM Frame_Assignments_Section_Properties
            WHERE Story = ?
            ORDER BY Label
            """, (story_name,))
            
            rows = self.cursor.fetchall()
            results = []
            for row in rows:
                results.append({
                    'id': row['ID'],
                    'story': row['Story'],
                    'label': row['Label'],
                    'unique_name': row['UniqueName'],
                    'shape': row['Shape'],
                    'auto_select_list': row['Auto_Select_List'],
                    'section_property': row['Section_Property'],
                    'section_property_id': row['Section_PropertyID']
                })
            
            return results
        except Exception as e:
            print(f"❌ خطأ في جلب التعيينات: {e}")
        
        return []
    
    # ════════════════════════════════════════════════════════════════
    # جلب حالات التحميل مع التحسينات
    # ════════════════════════════════════════════════════════════════
    
    def get_load_combinations(self) -> LoadCaseGroup:
        """
        جلب جميع حالات التحميل
        
        Returns:
            كائن LoadCaseGroup يحتوي على جميع الحالات
        """
        try:
            load_cases = LoadCaseGroup()
            
            self.cursor.execute("""
                SELECT ID, Name, Type, Is_Auto, GUID
                FROM Load_Combination_Definitions
                ORDER BY Name
            """)
            
            rows = self.cursor.fetchall()
            for row in rows:
                load_case = LoadCombination(
                    name=row['Name'],
                    combo_type=row['Type']
                )
                load_case.db_id = row['ID']
                load_case.is_auto = row['Is_Auto']
                load_case.guid = row['GUID']
                
                load_cases.add_load_case(load_case)
            
            return load_cases
        except Exception as e:
            print(f"⚠️ خطأ في جلب حالات التحميل: {e}")
            return LoadCaseGroup()
    
    def get_load_combination_with_components(self, combo_id: int) -> Optional[Dict]:
        """جلب حالة التحميل مع مكونات التحميل (NEW)"""
        try:
            self.cursor.execute("""
            SELECT ID, Name, Type, Is_Auto, GUID, Load_Name, SF
            FROM Load_Combination_Definitions
            WHERE ID = ?
            """, (combo_id,))
            
            row = self.cursor.fetchone()
            if row:
                return {
                    'id': row['ID'],
                    'name': row['Name'],
                    'type': row['Type'],
                    'is_auto': row['Is_Auto'],
                    'guid': row['GUID'],
                    'load_name': row['Load_Name'],
                    'scale_factor': float(row['SF']) if row['SF'] else 1.0
                }
        except Exception as e:
            print(f"❌ خطأ في جلب مكونات التحميل: {e}")
        
        return None

    def get_load_combinations_extended(self) -> List[Dict]:
        """جلب حالات التحميل مع جميع المكونات (NEW)"""
        try:
            self.cursor.execute("""
            SELECT ID, Name, Type, Is_Auto, GUID, Load_Name, SF
            FROM Load_Combination_Definitions
            ORDER BY Name
            """)
            
            rows = self.cursor.fetchall()
            results = []
            for row in rows:
                results.append({
                    'id': row['ID'],
                    'name': row['Name'],
                    'type': row['Type'],
                    'is_auto': row['Is_Auto'],
                    'guid': row['GUID'],
                    'load_name': row['Load_Name'],
                    'scale_factor': float(row['SF']) if row['SF'] else 1.0
                })
            
            return results
        except Exception as e:
            print(f"❌ خطأ في جلب حالات التحميل: {e}")
        
        return []
    
    # ════════════════════════════════════════════════════════════════
    # جلب البيانات العامة من Genralinput (NEW)
    # ════════════════════════════════════════════════════════════════
    
    def get_general_input(self, input_id: int = 1) -> Optional[Dict]:
        """
        جلب البيانات العامة والمعاملات من Genralinput (NEW)
        
        Args:
            input_id: معرف السجل (عادة 1)
            
        Returns:
            قاموس بالبيانات العامة
        """
        try:
            self.cursor.execute("""
            SELECT id, Knowledge_Factor, 
                   Concrete_Strength_Factor_Lambda_c,
                   Steel_Strength_Factor_Lambda_s,
                   Performance_Level,
                   Safety_Factor_Phi
            FROM Genralinput
            WHERE id = ?
            """, (input_id,))
            
            row = self.cursor.fetchone()
            if row:
                return {
                    'id': row['id'],
                    'knowledge_factor': float(row['Knowledge_Factor']) if row['Knowledge_Factor'] else 1,
                    'lambda_c': float(row['Concrete_Strength_Factor_Lambda_c']),
                    'lambda_s': float(row['Steel_Strength_Factor_Lambda_s']),
                    'performance_level': row['Performance_Level'],
                    'phi': float(row['Safety_Factor_Phi'])
                }
        except Exception as e:
            print(f"❌ خطأ في جلب البيانات العامة: {e}")
        
        return None

    def get_all_general_inputs(self) -> List[Dict]:
        """جلب جميع سجلات البيانات العامة (NEW)"""
        try:
            self.cursor.execute("""
            SELECT id, Knowledge_Factor, 
                   Concrete_Strength_Factor_Lambda_c,
                   Steel_Strength_Factor_Lambda_s,
                   Performance_Level,
                   Safety_Factor_Phi
            FROM Genralinput
            ORDER BY id
            """)
            
            rows = self.cursor.fetchall()
            results = []
            for row in rows:
                results.append({
                    'id': row['id'],
                    'knowledge_factor': float(row['Knowledge_Factor']) if row['Knowledge_Factor'] else 1,
                    'lambda_c': float(row['Concrete_Strength_Factor_Lambda_c']),
                    'lambda_s': float(row['Steel_Strength_Factor_Lambda_s']),
                    'performance_level': row['Performance_Level'],
                    'phi': float(row['Safety_Factor_Phi'])
                })
            
            return results
        except Exception as e:
            print(f"❌ خطأ في جلب البيانات العامة: {e}")
        
        return []
    
    # ════════════════════════════════════════════════════════════════
    # دوال المساعدة
    # ════════════════════════════════════════════════════════════════
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Any]:
        """
        تنفيذ استعلام مخصص
        
        Args:
            query: نص الاستعلام
            params: المعاملات
            
        Returns:
            قائمة النتائج
        """
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"❌ خطأ في الاستعلام: {e}")
            return []
    
    def execute_update(self, query: str, params: tuple = ()):
        """
        تنفيذ عملية تحديث (INSERT, UPDATE, DELETE)
        
        Args:
            query: نص الاستعلام
            params: المعاملات
            
        Returns:
            True إذا نجح، False في حالة الفشل
        """
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            return True
        except Exception as e:
            print(f"❌ خطأ في التحديث: {e}")
            self.connection.rollback()
            return False
    
    def __enter__(self):
        """دعم Context Manager"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """دعم Context Manager"""
        self.disconnect()
