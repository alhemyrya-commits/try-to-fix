BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Area_Assignments_Pier_Labels" (
	"Story"	TEXT,
	"Label"	TEXT,
	"UniqueName"	INTEGER,
	"Pier Name"	TEXT
);
CREATE TABLE IF NOT EXISTS "Area_Assignments_Section_Properties" (
	"Story"	TEXT,
	"Label"	TEXT,
	"UniqueName"	INTEGER,
	"Section Property"	TEXT,
	"Property Type"	TEXT
);
CREATE TABLE IF NOT EXISTS "Beam_Object_Connectivity" (
	"Unique Name"	INTEGER,
	"Story"	TEXT,
	"BeamBay"	TEXT,
	"UniquePtI"	INTEGER,
	"UniquePtJ"	INTEGER,
	"Length"	REAL,
	"GUID"	TEXT
);
CREATE TABLE IF NOT EXISTS "Column_Object_Connectivity" (
	"Unique Name"	INTEGER,
	"Story"	TEXT,
	"ColumnBay"	TEXT,
	"UniquePtI"	INTEGER,
	"UniquePtJ"	INTEGER,
	"Length"	INTEGER,
	"GUID"	TEXT
);
CREATE TABLE IF NOT EXISTS "Concrete_Column_Overwrites_ACI_318-19" (
	"Story"	TEXT,
	"Label"	TEXT,
	"Unique Name"	INTEGER,
	"Design Type"	TEXT,
	"Design Section"	TEXT,
	"Frame Type"	TEXT,
	"LLRF"	INTEGER,
	"Unbraced Length Ratio (Major)"	INTEGER,
	"Unbraced Length Ratio (Minor)"	INTEGER,
	"Effective Length Factor (K Major)"	INTEGER,
	"Effective Length Factor (K Minor)"	INTEGER,
	"Moment Coefficient (Cm Major)"	INTEGER,
	"Moment Coefficient (Cm Minor)"	INTEGER,
	"Non Sway Moment Factor (Dns Major)"	INTEGER,
	"Non Sway Moment Factor (Dns Minor)"	INTEGER,
	"Sway Moment Factor (Ds Major)"	INTEGER,
	"Sway Moment Factor (Ds Minor)"	INTEGER,
	"Consider Minimum Eccentricity?"	TEXT
);
CREATE TABLE IF NOT EXISTS "Concrete_Frame_Design_Preferences_ACI_318-19" (
	"Multi-Response Design"	TEXT,
	"# Interaction Curves"	INTEGER,
	"# Interaction Points"	INTEGER,
	"Minimum Eccentricity?"	TEXT,
	"Design for BCCR?"	TEXT,
	"Ignore Beneficial Pu for Beam Design?"	TEXT,
	"Seismic Design Category"	TEXT,
	"Design System Omega0"	INTEGER,
	"Design System Rho"	INTEGER,
	"Design System Sds"	REAL,
	"Phi (Tension)"	REAL,
	"Phi (Compression Tied)"	REAL,
	"Phi (Compression Spiral)"	REAL,
	"Phi (Shear and Torsion)"	REAL,
	"Phi (Shear Seismic)"	REAL,
	"Phi (Shear Joint)"	REAL,
	"Pattern Live Load Factor"	REAL,
	"Utlization Factor Limit"	INTEGER
);
CREATE TABLE IF NOT EXISTS "Element_Forces_Beams" (
	"Story"	TEXT,
	"Beam"	TEXT,
	"Unique Name"	INTEGER,
	"Output Case"	TEXT,
	"Case Type"	TEXT,
	"Station"	REAL,
	"P"	REAL,
	"V2"	REAL,
	"V3"	REAL,
	"T"	REAL,
	"M2"	REAL,
	"M3"	REAL,
	"Element"	TEXT,
	"Elem Station"	REAL,
	"Location"	TEXT
);
CREATE TABLE IF NOT EXISTS "Element_Forces_Columns" (
	"Story"	TEXT,
	"Column"	TEXT,
	"Unique Name"	INTEGER,
	"Output Case"	TEXT,
	"Case Type"	TEXT,
	"Station"	INTEGER,
	"P"	REAL,
	"V2"	REAL,
	"V3"	REAL,
	"T"	REAL,
	"M2"	REAL,
	"M3"	REAL,
	"Element"	INTEGER,
	"Elem Station"	INTEGER,
	"Location"	REAL
);
CREATE TABLE IF NOT EXISTS "Frame_Assignments_Section_Properties" (
	"Story"	TEXT,
	"Label"	TEXT,
	"UniqueName"	INTEGER,
	"Shape"	TEXT,
	"Auto Select List"	TEXT,
	"Section Property"	TEXT
);
CREATE TABLE IF NOT EXISTS "Frame_Section_Property_Definitions_Concrete_Beam_Reinforcing" (
	"Name"	TEXT,
	"Longitudinal Bar Material"	INTEGER,
	"Tie Bar Material"	INTEGER,
	"Top Cover"	INTEGER,
	"Bottom Cover"	INTEGER,
	"Top I-End Area"	INTEGER,
	"Top J-End Area"	INTEGER,
	"Bottom I-End Area"	INTEGER,
	"Bottom J-End Area"	INTEGER
);
CREATE TABLE IF NOT EXISTS "Frame_Section_Property_Definitions_Concrete_Column_Reinforcing" (
	"Name"	TEXT,
	"Longitudinal Bar Material"	INTEGER,
	"Tie Bar Material"	INTEGER,
	"Reinforcement Configuration"	TEXT,
	"Is Designed?"	TEXT,
	"Clear Cover to Ties"	INTEGER,
	"Number Bars 3-Dir"	INTEGER,
	"Number Bars 2-Dir"	INTEGER,
	"Longitudinal Bar Size"	INTEGER,
	"Corner Bar Size"	INTEGER,
	"Tie Bar Size"	INTEGER,
	"Tie Bar Spacing"	INTEGER,
	"Number Ties 3-Dir"	INTEGER,
	"Number Ties 2-Dir"	INTEGER
);
CREATE TABLE IF NOT EXISTS "Frame_Section_Property_Definitions_Concrete_Rectangular" (
	"Name"	TEXT,
	"Material"	TEXT,
	"From File?"	TEXT,
	"Depth"	INTEGER,
	"Width"	INTEGER,
	"Rigid Zone?"	TEXT,
	"Notional Size Type"	TEXT,
	"Notional Auto Factor"	INTEGER,
	"Design Type"	TEXT,
	"Area Modifier"	INTEGER,
	"As2 Modifier"	INTEGER,
	"As3 Modifier"	INTEGER,
	"J Modifier"	REAL,
	"I22 Modifier"	INTEGER,
	"I33 Modifier"	INTEGER,
	"Mass Modifier"	INTEGER,
	"Weight Modifier"	INTEGER,
	"Color"	TEXT,
	"GUID"	TEXT,
	"Notes"	REAL
);
CREATE TABLE IF NOT EXISTS "Load_Combination_Definitions" (
	"Name"	TEXT,
	"Type"	TEXT,
	"Is Auto"	TEXT,
	"Load Name"	TEXT,
	"SF"	REAL,
	"GUID"	TEXT,
	"Notes"	REAL
);
CREATE TABLE IF NOT EXISTS "Material_Properties_Concrete_Data" (
	"Material"	TEXT,
	"Fc"	REAL,
	"LtWtConc"	TEXT,
	"IsUserFr"	TEXT,
	"SSCurveOpt"	TEXT,
	"SSHysType"	TEXT,
	"SFc"	REAL,
	"SCap"	REAL,
	"FinalSlope"	REAL,
	"FAngle"	INTEGER,
	"DAngle"	INTEGER
);
CREATE TABLE IF NOT EXISTS "Material_Properties_Rebar_Data" (
	"Material"	INTEGER,
	"Fy"	REAL,
	"Fu"	REAL,
	"Fye"	REAL,
	"Fue"	REAL,
	"SSCurveOpt"	TEXT,
	"SSHysType"	TEXT,
	"SHard"	REAL,
	"SCap"	REAL,
	"FinalSlope"	REAL
);
CREATE TABLE IF NOT EXISTS "Objects_and_Elements_Joints" (
	"Story"	TEXT,
	"Element Name"	TEXT,
	"Object Type"	TEXT,
	"Object Label"	TEXT,
	"Object Name"	REAL,
	"Global X"	REAL,
	"Global Y"	REAL,
	"Global Z"	INTEGER
);
CREATE TABLE IF NOT EXISTS "Pier_Forces" (
	"Story"	TEXT,
	"Pier"	TEXT,
	"Output Case"	TEXT,
	"Case Type"	TEXT,
	"Location"	TEXT,
	"P"	REAL,
	"V2"	REAL,
	"V3"	REAL,
	"T"	REAL,
	"M2"	REAL,
	"M3"	REAL
);
CREATE TABLE IF NOT EXISTS "Story_Definitions" (
	"Tower"	TEXT,
	"Name"	TEXT,
	"Height"	INTEGER,
	"Master Story"	TEXT,
	"Similar To"	TEXT,
	"Splice Story"	TEXT,
	"Splice Height"	REAL,
	"Color"	TEXT,
	"GUID"	TEXT
);
CREATE TABLE IF NOT EXISTS "Wall_Object_Connectivity" (
	"UniqueName"	INTEGER,
	"Story"	TEXT,
	"WallBay"	TEXT,
	"UniquePt1"	INTEGER,
	"UniquePt2"	INTEGER,
	"UniquePt3"	INTEGER,
	"UniquePt4"	INTEGER,
	"Perimeter"	REAL,
	"Area"	REAL,
	"GUID"	TEXT
);
CREATE TABLE IF NOT EXISTS "Wall_Property_Definitions_Specified" (
	"Name"	TEXT,
	"Modeling Type"	TEXT,
	"Material"	TEXT,
	"Wall Thickness"	INTEGER,
	"Include Auto Rigid Zone?"	TEXT,
	"Notional Size Type"	TEXT,
	"Notional Auto Factor"	INTEGER,
	"f11 Modifier"	REAL,
	"f22 Modifier"	REAL,
	"f12 Modifier"	REAL,
	"m11 Modifier"	REAL,
	"m22 Modifier"	REAL,
	"m12 Modifier"	REAL,
	"v13 Modifier"	INTEGER,
	"v23 Modifier"	INTEGER,
	"Mass Modifier"	INTEGER,
	"Weight Modifier"	INTEGER,
	"Color"	TEXT,
	"GUID"	TEXT,
	"Notes"	REAL
);
COMMIT;
