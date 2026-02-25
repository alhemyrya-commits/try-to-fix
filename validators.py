"""
===============================================================================
utils/validators.py - دوال التحقق من صحة البيانات (مصحح شامل)
===============================================================================
"""

from typing import Any, Dict, Tuple, List, Optional
import logging


logger = logging.getLogger(__name__)


# ============================================================
# قواعس التحقق الافتراضية - ✅ مصحح
# ============================================================

DEFAULT_VALIDATION_RULES = {
    'tie_bar_size_mm': {'type': 'float', 'min': 0.1, 'max': 50.0},
    'tie_spacing_mm': {'type': 'float', 'min': 50.0, 'max': 500.0},
    'clear_cover_mm': {'type': 'float', 'min': 10.0, 'max': 100.0},
    'num_ties_3dir': {'type': 'int', 'min': 0, 'max': 100},
    'num_ties_2dir': {'type': 'int', 'min': 0, 'max': 100},
    'height_mm': {'type': 'float', 'min': 100.0, 'max': 10000.0},
}


# ============================================================
# دوال التحقق الأساسية - ✅ مصحح مع معالجة أخطاء شاملة
# ============================================================

def validate_value(value: Any, validation_rule: Optional[Dict] = None) -> Tuple[bool, str]:
    """
    التحقق من صحة القيمة حسب القواعس
    
    Args:
        value: القيمة المراد التحقق منها
        validation_rule: قاعدة التحقق {'min': x, 'max': y, 'type': 'int'}
    
    Returns:
        (صحيح/خاطئ، الرسالة)
    
    مثال:
        >>> validate_value(25.5, {'type': 'float', 'min': 0, 'max': 100})
        (True, '✓ صحيح')
    """
    try:
        # التعامل مع قيمة None
        if value is None:
            return False, "القيمة لا يمكن أن تكون فارغة"
        
        if validation_rule is None:
            validation_rule = {}
        
        # التحقق من النوع وتحويل البيانات - ✅ مع معالجة أخطاء
        value_type = validation_rule.get('type', 'str')
        
        try:
            if value_type == 'int':
                value = int(value)
            elif value_type == 'float':
                value = float(value)
            elif value_type == 'str':
                value = str(value).strip()
            else:
                value = type(value)
        except (ValueError, TypeError) as e:
            return False, f"❌ خطأ في تحويل النوع ({value_type}): {e}"
        
        # التحقق من النطاق - ✅ مع معالجة None
        min_val = validation_rule.get('min')
        max_val = validation_rule.get('max')
        
        if isinstance(value, (int, float)):
            if min_val is not None and value < min_val:
                return False, f"❌ القيمة {value} أقل من الحد الأدنى {min_val}"
            
            if max_val is not None and value > max_val:
                return False, f"❌ القيمة {value} أكبر من الحد الأقصى {max_val}"
        
        logger.debug(f"✓ Validated: {value} ({value_type})")
        return True, "✓ صحيح"
        
    except Exception as e:
        logger.error(f"❌ Unexpected error in validate_value: {e}")
        return False, f"❌ خطأ غير متوقع: {e}"


def validate_column_data(data: Dict, rules: Optional[Dict] = None) -> Tuple[bool, List[str]]:
    """
    التحقق من بيانات العمود كاملة - ✅ مصحح
    
    Args:
        data: قاموس البيانات
        rules: قواعس التحقق (اختياري)
    
    Returns:
        (صحيح/خاطئ، قائمة الأخطاء)
    
    مثال:
        >>> data = {'tie_bar_size_mm': 12, 'tie_spacing_mm': 200}
        >>> validate_column_data(data)
        (True, [])
    """
    if rules is None:
        rules = DEFAULT_VALIDATION_RULES
    
    errors = []
    
    if not isinstance(data, dict):
        return False, ["البيانات يجب أن تكون قاموس (dictionary)"]
    
    try:
        for field, value in data.items():
            if field in rules:
                try:
                    is_valid, message = validate_value(value, rules[field])
                    if not is_valid:
                        errors.append(f"{field}: {message}")
                except Exception as e:
                    logger.error(f"Error validating field {field}: {e}")
                    errors.append(f"{field}: ❌ خطأ في التحقق ({e})")
        
        if errors:
            logger.warning(f"⚠️ Validation errors: {errors}")
            return False, errors
        
        logger.info("✓ All fields validated successfully")
        return True, []
        
    except Exception as e:
        logger.exception(f"❌ Critical error in validate_column_data: {e}")
        return False, [f"❌ خطأ حرج: {e}"]


def validate_section_name(name: Any) -> Tuple[bool, str]:
    """
    التحقق من صحة اسم المقطع - ✅ مصحح مع معالجة أخطاء
    
    Args:
        name: اسم المقطع
    
    Returns:
        (صحيح/خاطئ، الرسالة)
    
    مثال:
        >>> validate_section_name("C50x50")
        (True, '✓ صحيح')
        >>> validate_section_name("")
        (False, '❌ اسم المقطع لا يمكن أن يكون فارغاً')
    """
    try:
        # التحقق من النوع
        if name is None:
            return False, "❌ اسم المقطع لا يمكن أن يكون فارغاً"
        
        if not isinstance(name, str):
            try:
                name = str(name)
            except Exception:
                return False, "❌ اسم المقطع يجب أن يكون نصاً"
        
        # تنظيف البيانات
        name = name.strip()
        
        # التحقق من عدم الفراغ
        if len(name) == 0:
            return False, "❌ اسم المقطع لا يمكن أن يكون فارغاً"
        
        # التحقق من الطول
        if len(name) > 100:
            return False, f"❌ اسم المقطع طويل جداً ({len(name)}/100 حرف)"
        
        # التحقق من الأحرف الصحيحة
        valid_chars = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-.')
        if not all(c in valid_chars for c in name):
            return False, f"❌ اسم المقطع يحتوي على أحرف غير صالحة"
        
        logger.debug(f"✓ Valid section name: {name}")
        return True, "✓ صحيح"
        
    except Exception as e:
        logger.error(f"❌ Error validating section name: {e}")
        return False, f"❌ خطأ في التحقق: {e}"


def validate_reinforcement_data(data: Dict, rules: Optional[Dict] = None) -> Tuple[bool, List[str]]:
    """
    التحقق من بيانات التسليح كاملة - ✅ مصحح مع معالجة أخطاء شاملة
    
    Args:
        data: قاموس بيانات التسليح
        rules: قواعس التحقق (اختياري)
    
    Returns:
        (صحيح/خاطئ، قائمة الأخطاء)
    
    مثال:
        >>> data = {
        ...     'section_name': 'C50x50',
        ...     'tie_bar_size_mm': 12,
        ...     'tie_spacing_mm': 200,
        ...     'clear_cover_mm': 40
        ... }
        >>> validate_reinforcement_data(data)
        (True, [])
    """
    if rules is None:
        rules = DEFAULT_VALIDATION_RULES
    
    errors = []
    
    if not isinstance(data, dict):
        return False, ["بيانات التسليح يجب أن تكون قاموس (dictionary)"]
    
    try:
        # فحص الحقول المطلوبة - ✅ مصحح
        required_fields = ['section_name', 'tie_bar_size_mm', 'tie_spacing_mm']
        
        for field in required_fields:
            if field not in data:
                errors.append(f"❌ الحقل المطلوب '{field}' غير موجود")
            elif data[field] is None or (isinstance(data[field], str) and len(data[field].strip()) == 0):
                errors.append(f"❌ الحقل '{field}' فارغ")
        
        # فحص اسم المقطع بشكل خاص
        if 'section_name' in data and data['section_name'] is not None:
            is_valid, msg = validate_section_name(data['section_name'])
            if not is_valid:
                errors.append(msg)
        
        # فحص القيم العددية - ✅ مصحح مع معالجة أخطاء
        numeric_fields = {
            'tie_bar_size_mm': {'type': 'float', 'min': 0.1, 'max': 50.0},
            'tie_spacing_mm': {'type': 'float', 'min': 50.0, 'max': 500.0},
            'clear_cover_mm': {'type': 'float', 'min': 10.0, 'max': 100.0},
            'num_ties_3dir': {'type': 'int', 'min': 0, 'max': 100},
            'num_ties_2dir': {'type': 'int', 'min': 0, 'max': 100},
        }
        
        for field, rule in numeric_fields.items():
            if field in data and data[field] is not None:
                try:
                    value = float(data[field]) if rule['type'] == 'float' else int(data[field])
                    
                    # فحص القيمة الموجبة
                    if value < 0:
                        errors.append(f"❌ {field} يجب أن تكون موجبة (القيمة: {value})")
                    
                    # فحص النطاق
                    is_valid, msg = validate_value(value, rule)
                    if not is_valid:
                        errors.append(f"❌ {field}: {msg}")
                
                except (ValueError, TypeError) as e:
                    errors.append(f"❌ {field} يجب أن تكون قيمة عددية (خطأ: {e})")
        
        if errors:
            logger.warning(f"⚠️ Reinforcement validation errors: {errors}")
            return False, errors
        
        logger.info("✓ Reinforcement data validated successfully")
        return True, []
        
    except Exception as e:
        logger.exception(f"❌ Critical error in validate_reinforcement_data: {e}")
        return False, [f"❌ خطأ حرج: {e}"]


def validate_float_range(value: Any, min_val: float = None, max_val: float = None) -> Tuple[bool, str]:
    """
    التحقق من نطاق قيمة عددية - ✅ دالة مساعدة جديدة
    
    Args:
        value: القيمة
        min_val: الحد الأدنى (اختياري)
        max_val: الحد الأقصى (اختياري)
    
    Returns:
        (صحيح/خاطئ، الرسالة)
    """
    try:
        try:
            value = float(value)
        except (ValueError, TypeError):
            return False, f"❌ يجب أن تكون قيمة عددية"
        
        if min_val is not None and value < min_val:
            return False, f"❌ القيمة {value} أقل من {min_val}"
        
        if max_val is not None and value > max_val:
            return False, f"❌ القيمة {value} أكبر من {max_val}"
        
        return True, "✓ صحيح"
        
    except Exception as e:
        logger.error(f"Error in validate_float_range: {e}")
        return False, f"❌ خطأ: {e}"


def validate_integer_range(value: Any, min_val: int = None, max_val: int = None) -> Tuple[bool, str]:
    """
    التحقق من نطاق عدد صحيح - ✅ دالة مساعدة جديدة
    
    Args:
        value: القيمة
        min_val: الحد الأدنى (اختياري)
        max_val: الحد الأقصى (اختياري)
    
    Returns:
        (صحيح/خاطئ، الرسالة)
    """
    try:
        try:
            value = int(value)
        except (ValueError, TypeError):
            return False, f"❌ يجب أن يكون عداً صحيحاً"
        
        if min_val is not None and value < min_val:
            return False, f"❌ القيمة {value} أقل من {min_val}"
        
        if max_val is not None and value > max_val:
            return False, f"❌ القيمة {value} أكبر من {max_val}"
        
        return True, "✓ صحيح"
        
    except Exception as e:
        logger.error(f"Error in validate_integer_range: {e}")
        return False, f"❌ خطأ: {e}"


def batch_validate(data_list: List[Dict], validator_func=None) -> Tuple[List[Dict], List[Tuple[int, List[str]]]]:
    """
    التحقق من قائمة بيانات - ✅ دالة جديدة
    
    Args:
        data_list: قائمة البيانات
        validator_func: دالة التحقق (اختياري)
    
    Returns:
        (قائمة البيانات الصحيحة، قائمة الأخطاء)
    """
    if validator_func is None:
        validator_func = validate_reinforcement_data
    
    valid_data = []
    errors = []
    
    try:
        for idx, data in enumerate(data_list):
            is_valid, error_list = validator_func(data)
            if is_valid:
                valid_data.append(data)
            else:
                errors.append((idx, error_list))
        
        logger.info(f"✓ Batch validation: {len(valid_data)} valid, {len(errors)} errors")
        return valid_data, errors
        
    except Exception as e:
        logger.exception(f"Error in batch_validate: {e}")
        return [], [(i, [f"❌ خطأ: {e}"]) for i in range(len(data_list))]
