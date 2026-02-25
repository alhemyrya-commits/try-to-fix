"""
===============================================================================
services/query_service.py - خدمات الاستعلام (معدّل للقاعدة الجديدة)
===============================================================================
"""

import sqlite3
from typing import Optional, List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class QueryService:
    """خدمات الاستعلام عن البيانات من القاعدة الجديدة"""
    
    def __init__(self, db_connection: sqlite3.Connection):
        """
        تهيئة خدمة الاستعلام
        
        المعاملات:
            db_connection: الاتصال بقاعدة البيانات
        """
        self.db = db_connection
        self.cursor = db_connection.cursor()
    
    def get_story_by_name(self, story_name: str) -> Optional[Dict[str, Any]]:
        """
        الحصول على بيانات الطابق من Story_Definitions
        
        المعاملات:
            story_name: اسم الطابق
            
        المخرجات:
            قاموس ببيانات الطابق أو None
        """
        try:
            query = """
            SELECT ID, Tower, Name, Height, Master_Story, Color, Notes
            FROM Story_Definitions
            WHERE Name = ?
            """
            
            self.cursor.execute(query, (story_name,))
            result = self.cursor.fetchone()
            
            if result:
                columns = [desc[0] for desc in self.cursor.description]
                return dict(zip(columns, result))
            
            logger.warning(f"لم يتم العثور على الطابق: {story_name}")
            return None
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على بيانات الطابق: {e}")
            return None
    
    def get_all_stories(self) -> List[Dict[str, Any]]:
        """
        الحصول على جميع الطوابق
        
        المخرجات:
            قائمة بجميع الطوابق
        """
        try:
            query = """
            SELECT ID, Tower, Name, Height, Master_Story, Color, Notes
            FROM Story_Definitions
            ORDER BY Height DESC
            """
            
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            
            if results:
                columns = [desc[0] for desc in self.cursor.description]
                return [dict(zip(columns, row)) for row in results]
            
            logger.info("لا توجد طوابق في قاعدة البيانات")
            return []
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على قائمة الطوابق: {e}")
            return []
    
    def get_column_by_name(self, column_name: str, story_name: str) -> Optional[Dict[str, Any]]:
        """
        الحصول على بيانات العمود من Frame_Assignments_Section_Properties
        
        المعاملات:
            column_name: اسم/تسمية العمود
            story_name: اسم الطابق
            
        المخرجات:
            قاموس ببيانات العمود أو None
        """
        try:
            query = """
            SELECT 
                ID,
                Story,
                Label,
                UniqueName,
                Shape,
                Section_Property,
                Section_PropertyID
            FROM Frame_Assignments_Section_Properties
            WHERE Label = ? AND Story = ?
            """
            
            self.cursor.execute(query, (column_name, story_name))
            result = self.cursor.fetchone()
            
            if result:
                columns = [desc[0] for desc in self.cursor.description]
                return dict(zip(columns, result))
            
            logger.warning(f"لم يتم العثور على العمود: {column_name}")
            return None
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على بيانات العمود: {e}")
            return None
    
    def get_column_connectivity(self, column_unique_name: int) -> Optional[Dict[str, Any]]:
        """
        الحصول على بيانات اتصال العمود من Column_Object_Connectivity
        
        المعاملات:
            column_unique_name: الاسم الفريد للعمود
            
        المخرجات:
            قاموس ببيانات الاتصال أو None
        """
        try:
            query = """
            SELECT 
                Unique_Name,
                Story,
                ColumnBay,
                UniquePtI,
                UniquePtJ,
                Length,
                ElementID
            FROM Column_Object_Connectivity
            WHERE Unique_Name = ?
            """
            
            self.cursor.execute(query, (column_unique_name,))
            result = self.cursor.fetchone()
            
            if result:
                columns = [desc[0] for desc in self.cursor.description]
                return dict(zip(columns, result))
            
            logger.warning(f"لم يتم العثور على اتصال العمود: {column_unique_name}")
            return None
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على اتصال العمود: {e}")
            return None
    
    def get_section_property(self, section_name: str) -> Optional[Dict[str, Any]]:
        """
        الحصول على بيانات المقطع من Frame_Section_Property_Definitions_Concrete_Rectangular
        
        المعاملات:
            section_name: اسم المقطع
            
        المخرجات:
            قاموس ببيانات المقطع أو None
        """
        try:
            query = """
            SELECT 
                ID,
                Name,
                Material,
                Depth,
                Width,
                Area_Modifier,
                I22_Modifier,
                I33_Modifier
            FROM Frame_Section_Property_Definitions_Concrete_Rectangular
            WHERE Name = ?
            """
            
            self.cursor.execute(query, (section_name,))
            result = self.cursor.fetchone()
            
            if result:
                columns = [desc[0] for desc in self.cursor.description]
                return dict(zip(columns, result))
            
            logger.warning(f"لم يتم العثور على المقطع: {section_name}")
            return None
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على بيانات المقطع: {e}")
            return None
    
    def get_load_combination(self, load_name: str) -> Optional[Dict[str, Any]]:
        """
        الحصول على بيانات تركيبة الأحمال من Load_Combination_Definitions
        
        المعاملات:
            load_name: اسم تركيبة الأحمال
            
        المخرجات:
            قاموس ببيانات التركيبة أو None
        """
        try:
            query = """
            SELECT 
                ID,
                Name,
                Type,
                Is_Auto,
                Load_Name,
                SF
            FROM Load_Combination_Definitions
            WHERE Name = ?
            """
            
            self.cursor.execute(query, (load_name,))
            result = self.cursor.fetchone()
            
            if result:
                columns = [desc[0] for desc in self.cursor.description]
                return dict(zip(columns, result))
            
            logger.warning(f"لم يتم العثور على تركيبة الأحمال: {load_name}")
            return None
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على تركيبة الأحمال: {e}")
            return None
    
    def search_columns(self, story_name: str, search_term: str = None) -> List[Dict[str, Any]]:
        """
        البحث عن الأعمدة في طابق معين
        
        المعاملات:
            story_name: اسم الطابق
            search_term: مصطلح البحث الاختياري
            
        المخرجات:
            قائمة بالأعمدة المطابقة
        """
        try:
            if search_term:
                query = """
                SELECT 
                    ID,
                    Story,
                    Label,
                    UniqueName,
                    Shape,
                    Section_Property
                FROM Frame_Assignments_Section_Properties
                WHERE Story = ? AND Label LIKE ?
                ORDER BY UniqueName
                """
                self.cursor.execute(query, (story_name, f"%{search_term}%"))
            else:
                query = """
                SELECT 
                    ID,
                    Story,
                    Label,
                    UniqueName,
                    Shape,
                    Section_Property
                FROM Frame_Assignments_Section_Properties
                WHERE Story = ?
                ORDER BY UniqueName
                """
                self.cursor.execute(query, (story_name,))
            
            results = self.cursor.fetchall()
            
            if results:
                columns = [desc[0] for desc in self.cursor.description]
                return [dict(zip(columns, row)) for row in results]
            
            logger.info(f"لا توجد أعمدة مطابقة في الطابق: {story_name}")
            return []
            
        except Exception as e:
            logger.error(f"خطأ في البحث عن الأعمدة: {e}")
            return []
    
    def close(self):
        """إغلاق الاتصال بالقاعدة"""
        if self.cursor:
            self.cursor.close()
        logger.debug("تم إغلاق اتصال QueryService")
