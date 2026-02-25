# database/schema.py - تعريف الجداول الجديدة
# هذا الملف يحتوي على CREATE TABLE و ALTER TABLE فقط
# بدون أي معلومات من VEDA

# قائمة جميع جداول الهيكل الجديد
NEW_TABLES = [
    "Story_Definitions",
    "Objects_and_Elements_Joints",
    "Column_Object_Connectivity",
    "Material_Properties_Concrete_Data",
    "Material_Properties_Rebar_Data",
    "Frame_Section_Property_Definitions_Concrete_Column_Reinforcing",
    "Frame_Section_Property_Definitions_Concrete_Rectangular",
    "Frame_Assignments_Section_Properties",
    "Load_Combination_Definitions",
    "Element_Forces_Columns",
    "Genralinput"
]

# SQL Statements لإنشاء الجداول
CREATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS `Story_Definitions` (
	`ID` INT NOT NULL AUTO_INCREMENT,
	`Tower` VARCHAR(255),
	`Name` VARCHAR(255) NOT NULL UNIQUE,
	`Height` FLOAT,
	`Master_Story` VARCHAR(255),
	`Similar_To` VARCHAR(255),
	`Splice_Story` VARCHAR(255),
	`Splice_Height` FLOAT,
	`Color` VARCHAR(255),
	`GUID` VARCHAR(255),
	`Notes` TEXT,
	PRIMARY KEY(`ID`)
);

CREATE TABLE IF NOT EXISTS `Objects_and_Elements_Joints` (
	`ID` INT NOT NULL AUTO_INCREMENT,
	`Story` VARCHAR(255),
	`Element_Name` INT,
	`Object_Type` VARCHAR(255),
	`Object_Label` VARCHAR(255),
	`Object_Name` FLOAT,
	`Global_X` FLOAT,
	`Global_Y` FLOAT,
	`Global_Z` FLOAT,
	PRIMARY KEY(`ID`)
);

CREATE TABLE IF NOT EXISTS `Column_Object_Connectivity` (
	`Unique_Name` INT UNIQUE,
	`Story` VARCHAR(255),
	`ColumnBay` VARCHAR(255),
	`UniquePtI` INT,
	`UniquePtJ` INT,
	`Length` INT,
	`GUID` VARCHAR(255),
	`ElementID` INT
);

CREATE TABLE IF NOT EXISTS `Material_Properties_Concrete_Data` (
	`ID` INT NOT NULL AUTO_INCREMENT,
	`Material` VARCHAR(255) UNIQUE,
	`Fc` FLOAT,
	`LtWtConc` VARCHAR(255),
	`IsUserFr` VARCHAR(255),
	`SSCurveOpt` VARCHAR(255),
	`SSHysType` VARCHAR(255),
	`SFc` FLOAT,
	`SCap` FLOAT,
	`FinalSlope` FLOAT,
	`FAngle` INT,
	`DAngle` INT,
	PRIMARY KEY(`ID`)
);

CREATE TABLE IF NOT EXISTS `Material_Properties_Rebar_Data` (
	`ID` INT NOT NULL AUTO_INCREMENT,
	`Material` VARCHAR(255) UNIQUE,
	`Fy` FLOAT,
	`Fu` FLOAT,
	`Fye` FLOAT,
	`Fue` FLOAT,
	`SSCurveOpt` VARCHAR(255),
	`SSHysType` VARCHAR(255),
	`SHard` FLOAT,
	`SCap` FLOAT,
	`FinalSlope` FLOAT,
	`GenralID` INT,
	PRIMARY KEY(`ID`)
);

CREATE TABLE IF NOT EXISTS `Frame_Section_Property_Definitions_Concrete_Column_Reinforcing` (
	`ID` INT NOT NULL AUTO_INCREMENT,
	`Name` VARCHAR(255) UNIQUE,
	`Longitudinal_Bar_Material` VARCHAR(255),
	`Tie_Bar_Material` VARCHAR(255),
	`Reinforcement_Configuration` VARCHAR(255),
	`Is_Designed` VARCHAR(255),
	`Clear_Cover_to_Ties` FLOAT,
	`Number_Bars_3_Dir` INT,
	`Number_Bars_2_Dir` INT,
	`Longitudinal_Bar_Size` FLOAT,
	`Corner_Bar_Size` FLOAT,
	`Tie_Bar_Size` FLOAT,
	`Tie_Bar_Spacing` FLOAT,
	`Number_Ties_3_Dir` INT,
	`Number_Ties_2_Dir` INT,
	`LonZgitudinal_Bar_MaterialID` INT,
	`Tie_Bar_MaterialID` INT,
	`NameID` INT,
	PRIMARY KEY(`ID`)
);

CREATE TABLE IF NOT EXISTS `Frame_Section_Property_Definitions_Concrete_Rectangular` (
	`ID` INT NOT NULL AUTO_INCREMENT,
	`Name` VARCHAR(255) UNIQUE,
	`Material` VARCHAR(255),
	`From_File` VARCHAR(255),
	`Depth` FLOAT,
	`Width` FLOAT,
	`Rigid_Zone` VARCHAR(255),
	`Notional_Size_Type` VARCHAR(255),
	`Notional_Auto_Factor` FLOAT,
	`Design_Type` VARCHAR(255),
	`Area_Modifier` FLOAT,
	`As2_Modifier` FLOAT,
	`As3_Modifier` FLOAT,
	`J_Modifier` FLOAT,
	`I22_Modifier` FLOAT,
	`I33_Modifier` FLOAT,
	`Mass_Modifier` FLOAT,
	`Weight_Modifier` FLOAT,
	`Color` VARCHAR(255),
	`GUID` VARCHAR(255),
	`Notes` TEXT,
	`MaterialID` INT,
	PRIMARY KEY(`ID`)
);

CREATE TABLE IF NOT EXISTS `Frame_Assignments_Section_Properties` (
	`ID` INT NOT NULL AUTO_INCREMENT,
	`Story` VARCHAR(255),
	`Label` VARCHAR(255),
	`UniqueName` INT,
	`Shape` VARCHAR(255),
	`Auto_Select_List` VARCHAR(255),
	`Section_Property` VARCHAR(255),
	`Section_PropertyID` INT,
	PRIMARY KEY(`ID`)
);

CREATE TABLE IF NOT EXISTS `Load_Combination_Definitions` (
	`ID` INT NOT NULL AUTO_INCREMENT,
	`Name` VARCHAR(255) UNIQUE,
	`Type` VARCHAR(255),
	`Is_Auto` VARCHAR(255),
	`Load_Name` VARCHAR(255),
	`SF` FLOAT,
	`GUID` VARCHAR(255),
	`Notes` TEXT,
	PRIMARY KEY(`ID`)
);

CREATE TABLE IF NOT EXISTS `Element_Forces_Columns` (
	`ID` INT NOT NULL AUTO_INCREMENT,
	`Story` VARCHAR(255),
	`Column` VARCHAR(255),
	`Unique_Name` INT,
	`Output_Case` VARCHAR(255),
	`Case_Type` VARCHAR(255),
	`Station` FLOAT,
	`P` FLOAT,
	`V2` FLOAT,
	`V3` FLOAT,
	`T` FLOAT,
	`M2` FLOAT,
	`M3` FLOAT,
	`Element` INT,
	`Elem_Station` FLOAT,
	`Location` FLOAT,
	`ElementID` INT,
	`Load_case_id` INT,
	PRIMARY KEY(`ID`)
);

CREATE TABLE IF NOT EXISTS `Genralinput` (
	`id` INT NOT NULL AUTO_INCREMENT UNIQUE,
	`Knowledge_Factor` INT,
	`Concrete_Strength_Factor_Lambda_c` FLOAT DEFAULT 1.5,
	`Steel_Strength_Factor_Lambda_s` FLOAT DEFAULT 1.25,
	`Performance_Level` VARCHAR(255),
	`Safety_Factor_Phi` FLOAT DEFAULT 1,
	PRIMARY KEY(`id`)
);
"""

# SQL Statements لإضافة Foreign Keys
ALTER_TABLES_SQL = """
ALTER TABLE `Frame_Section_Property_Definitions_Concrete_Column_Reinforcing`
ADD FOREIGN KEY(`Longitudinal_Bar_Material`) REFERENCES `Material_Properties_Rebar_Data`(`Material`)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE `Frame_Section_Property_Definitions_Concrete_Column_Reinforcing`
ADD FOREIGN KEY(`Tie_Bar_Material`) REFERENCES `Material_Properties_Rebar_Data`(`Material`)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE `Frame_Section_Property_Definitions_Concrete_Rectangular`
ADD FOREIGN KEY(`Material`) REFERENCES `Material_Properties_Concrete_Data`(`Material`)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE `Objects_and_Elements_Joints`
ADD FOREIGN KEY(`Story`) REFERENCES `Story_Definitions`(`Name`)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE `Element_Forces_Columns`
ADD FOREIGN KEY(`Story`) REFERENCES `Frame_Assignments_Section_Properties`(`Story`)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE `Element_Forces_Columns`
ADD FOREIGN KEY(`Unique_Name`) REFERENCES `Frame_Assignments_Section_Properties`(`UniqueName`)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE `Column_Object_Connectivity`
ADD FOREIGN KEY(`Story`) REFERENCES `Frame_Assignments_Section_Properties`(`Story`)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE `Column_Object_Connectivity`
ADD FOREIGN KEY(`Unique_Name`) REFERENCES `Frame_Assignments_Section_Properties`(`UniqueName`)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE `Column_Object_Connectivity`
ADD FOREIGN KEY(`UniquePtI`) REFERENCES `Objects_and_Elements_Joints`(`Element_Name`)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE `Column_Object_Connectivity`
ADD FOREIGN KEY(`UniquePtJ`) REFERENCES `Objects_and_Elements_Joints`(`Element_Name`)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE `Frame_Assignments_Section_Properties`
ADD FOREIGN KEY(`Section_Property`) REFERENCES `Frame_Section_Property_Definitions_Concrete_Rectangular`(`Name`)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE `Element_Forces_Columns`
ADD FOREIGN KEY(`Output_Case`) REFERENCES `Load_Combination_Definitions`(`Name`)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE `Frame_Section_Property_Definitions_Concrete_Column_Reinforcing`
ADD FOREIGN KEY(`Tie_Bar_MaterialID`) REFERENCES `Material_Properties_Rebar_Data`(`ID`)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE `Frame_Section_Property_Definitions_Concrete_Column_Reinforcing`
ADD FOREIGN KEY(`LonZgitudinal_Bar_MaterialID`) REFERENCES `Material_Properties_Rebar_Data`(`ID`)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE `Frame_Section_Property_Definitions_Concrete_Column_Reinforcing`
ADD FOREIGN KEY(`NameID`) REFERENCES `Frame_Section_Property_Definitions_Concrete_Rectangular`(`ID`)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE `Frame_Section_Property_Definitions_Concrete_Column_Reinforcing`
ADD FOREIGN KEY(`Name`) REFERENCES `Frame_Section_Property_Definitions_Concrete_Rectangular`(`Name`)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE `Frame_Assignments_Section_Properties`
ADD FOREIGN KEY(`Section_PropertyID`) REFERENCES `Frame_Section_Property_Definitions_Concrete_Rectangular`(`ID`)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE `Frame_Section_Property_Definitions_Concrete_Rectangular`
ADD FOREIGN KEY(`MaterialID`) REFERENCES `Material_Properties_Concrete_Data`(`ID`)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE `Element_Forces_Columns`
ADD FOREIGN KEY(`ElementID`) REFERENCES `Frame_Assignments_Section_Properties`(`ID`)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE `Column_Object_Connectivity`
ADD FOREIGN KEY(`ElementID`) REFERENCES `Frame_Assignments_Section_Properties`(`ID`)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE `Material_Properties_Rebar_Data`
ADD FOREIGN KEY(`GenralID`) REFERENCES `Genralinput`(`id`)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE `Element_Forces_Columns`
ADD FOREIGN KEY(`Load_case_id`) REFERENCES `Load_Combination_Definitions`(`ID`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
"""


def get_create_tables_sql():
    """الحصول على SQL لإنشاء جميع الجداول"""
    return CREATE_TABLES_SQL


def get_alter_tables_sql():
    """الحصول على SQL لإضافة Foreign Keys"""
    return ALTER_TABLES_SQL


def get_all_new_tables():
    """الحصول على قائمة جميع جداول الهيكل الجديد"""
    return NEW_TABLES


def split_sql_statements(sql_string):
    """تقسيم SQL statements إلى قائمة من الجمل المنفصلة"""
    statements = []
    current_statement = ""
    
    for line in sql_string.split('\n'):
        line = line.strip()
        if not line or line.startswith('--'):
            continue
        
        current_statement += " " + line
        
        if line.endswith(';'):
            statements.append(current_statement.strip())
            current_statement = ""
    
    return [stmt for stmt in statements if stmt]
