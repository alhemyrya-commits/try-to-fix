"""
===============================================================================
services/analysis_service.py - خدمات التحليل والمعالجة (معدّل للقاعدة الجديدة)
===============================================================================
"""

import sqlite3
from typing import Optional, Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class AnalysisService:
    """خدمات التحليل والمعالجة للقاعدة الجديدة"""
    
    def __init__(self, db_connection: sqlite3.Connection):
        """
        تهيئة خدمة التحليل
        
        المعاملات:
            db_connection: الاتصال بقاعدة البيانات
        """
        self.db = db_connection
        self.cursor = db_connection.cursor()
    
    def get_column_reinforcement(self, column_name: str, story: str) -> Optional[Dict[str, Any]]:
        """
        الحصول على تفاصيل التسليح للعمود من جدول Frame_Section_Property_Definitions_Concrete_Column_Reinforcing
        
        المعاملات:
            column_name: اسم العمود
            story: اسم الطابق
            
        المخرجات:
            قاموس بتفاصيل التسليح أو None
        """
        try:
            query = """
            SELECT 
                fr.ID,
                fr.Name,
                fr.Longitudinal_Bar_Material,
                fr.Tie_Bar_Material,
                fr.Reinforcement_Configuration,
                fr.Clear_Cover_to_Ties,
                fr.Number_Bars_3_Dir,
                fr.Number_Bars_2_Dir,
                fr.Longitudinal_Bar_Size,
                fr.Tie_Bar_Size,
                fr.Tie_Bar_Spacing
            FROM Frame_Section_Property_Definitions_Concrete_Column_Reinforcing fr
            WHERE fr.Name = ?
            LIMIT 1
            """
            
            self.cursor.execute(query, (column_name,))
            result = self.cursor.fetchone()
            
            if result:
                columns = [desc[0] for desc in self.cursor.description]
                return dict(zip(columns, result))
            
            logger.warning(f"لم يتم العثور على تسليح للعمود: {column_name}")
            return None
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على تسليح العمود: {e}")
            return None
    
    def get_max_forces_for_column(self, column_name: str, story: str) -> Optional[Dict[str, Any]]:
        """
        الحصول على أقصى القوى للعمود من جدول Element_Forces_Columns
        
        المعاملات:
            column_name: اسم العمود
            story: اسم الطابق
            
        المخرجات:
            قاموس بأقصى القوى (P, V2, V3, M2, M3, T) أو None
        """
        try:
            query = """
            SELECT 
                ID,
                Story,
                Column,
                Output_Case,
                Case_Type,
                Station,
                P,
                V2,
                V3,
                T,
                M2,
                M3
            FROM Element_Forces_Columns
            WHERE Column = ? AND Story = ?
            ORDER BY ABS(P) DESC
            LIMIT 1
            """
            
            self.cursor.execute(query, (column_name, story))
            result = self.cursor.fetchone()
            
            if result:
                columns = [desc[0] for desc in self.cursor.description]
                return dict(zip(columns, result))
            
            logger.warning(f"لم يتم العثور على قوى للعمود: {column_name} في الطابق: {story}")
            return None
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على أقصى القوى: {e}")
            return None
    
    def get_all_forces_for_column(self, column_name: str, story: str) -> List[Dict[str, Any]]:
        """
        الحصول على جميع القوى للعمود من جدول Element_Forces_Columns
        
        المعاملات:
            column_name: اسم العمود
            story: اسم الطابق
            
        المخرجات:
            قائمة بجميع سجلات القوى
        """
        try:
            query = """
            SELECT 
                ID,
                Story,
                Column,
                Output_Case,
                Case_Type,
                Station,
                P,
                V2,
                V3,
                T,
                M2,
                M3
            FROM Element_Forces_Columns
            WHERE Column = ? AND Story = ?
            ORDER BY Station
            """
            
            self.cursor.execute(query, (column_name, story))
            results = self.cursor.fetchall()
            
            if results:
                columns = [desc[0] for desc in self.cursor.description]
                return [dict(zip(columns, row)) for row in results]
            
            logger.info(f"لا توجد قوى للعمود: {column_name}")
            return []
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على جميع القوى: {e}")
            return []
    
    def calculate_max_moment(self, column_name: str, story: str) -> Optional[Dict[str, float]]:
        """
        حساب أقصى عزم انحناء للعمود
        
        المعاملات:
            column_name: اسم العمود
            story: اسم الطابق
            
        المخرجات:
            قاموس بأقصى M2, M3 أو None
        """
        try:
            forces = self.get_all_forces_for_column(column_name, story)
            
            if not forces:
                return None
            
            max_m2 = max([abs(f['M2']) for f in forces if f['M2'] is not None], default=0.0)
            max_m3 = max([abs(f['M3']) for f in forces if f['M3'] is not None], default=0.0)
            
            return {
                'max_M2': max_m2,
                'max_M3': max_m3,
                'max_combined': (max_m2**2 + max_m3**2)**0.5
            }
            
        except Exception as e:
            logger.error(f"خطأ في حساب أقصى عزم: {e}")
            return None
    
    def get_story_columns(self, story_name: str) -> List[Dict[str, Any]]:
        """
        الحصول على جميع الأعمدة في طابق معين
        
        المعاملات:
            story_name: اسم الطابق
            
        المخرجات:
            قائمة بجميع الأعمدة في الطابق
        """
        try:
            query = """
            SELECT 
                fa.ID,
                fa.Story,
                fa.Label,
                fa.UniqueName,
                fa.Shape,
                fa.Section_Property
            FROM Frame_Assignments_Section_Properties fa
            WHERE fa.Story = ?
            ORDER BY fa.UniqueName
            """
            
            self.cursor.execute(query, (story_name,))
            results = self.cursor.fetchall()
            
            if results:
                columns = [desc[0] for desc in self.cursor.description]
                return [dict(zip(columns, row)) for row in results]
            
            logger.info(f"لا توجد أعمدة في الطابق: {story_name}")
            return []
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على أعمدة الطابق: {e}")
            return []
    
    def get_material_properties(self, material_type: str, material_name: str) -> Optional[Dict[str, Any]]:
        """
        الحصول على خصائص المواد (خرسانة أو فولاذ)
        
        المعاملات:
            material_type: نوع المادة ('concrete' أو 'rebar')
            material_name: اسم المادة
            
        المخرجات:
            قاموس بخصائص المادة أو None
        """
        try:
            if material_type.lower() == 'concrete':
                query = """
                SELECT ID, Material, Fc, LtWtConc, SSCurveOpt, SSHysType
                FROM Material_Properties_Concrete_Data
                WHERE Material = ?
                """
            elif material_type.lower() == 'rebar':
                query = """
                SELECT ID, Material, Fy, Fu, Fye, Fue, SSCurveOpt, SSHysType
                FROM Material_Properties_Rebar_Data
                WHERE Material = ?
                """
            else:
                logger.error(f"نوع مادة غير معروف: {material_type}")
                return None
            
            self.cursor.execute(query, (material_name,))
            result = self.cursor.fetchone()
            
            if result:
                columns = [desc[0] for desc in self.cursor.description]
                return dict(zip(columns, result))
            
            logger.warning(f"لم يتم العثور على مادة: {material_name}")
            return None
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على خصائص المادة: {e}")
            return None
    
    def close(self):
        """إغلاق الاتصال بالقاعدة"""
        if self.cursor:
            self.cursor.close()
        logger.debug("تم إغلاق اتصال AnalysisService")
