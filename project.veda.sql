CREATE TABLE IF NOT EXISTS "Story_Definitions" (
	"ID" INTEGER,
	"Tower" TEXT,
	"Name" TEXT NOT NULL UNIQUE,
	"Height" REAL,
	"Master_Story" TEXT,
	"Similar_To" TEXT,
	"Splice_Story" TEXT,
	"Splice_Height" REAL,
	"Color" TEXT,
	"GUID" TEXT,
	"Notes" TEXT,
	PRIMARY KEY("ID")
);

CREATE TABLE IF NOT EXISTS "Objects_and_Elements_Joints" (
	"ID" INTEGER,
	"Story" TEXT,
	"Element_Name" INTEGER,
	"Object_Type" TEXT,
	"Object_Label" TEXT,
	"Object_Name" REAL,
	"Global_X" REAL,
	"Global_Y" REAL,
	"Global_Z" REAL,
	PRIMARY KEY("ID"),
	FOREIGN KEY ("Story") REFERENCES "Story_Definitions"("Name")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "Column_Object_Connectivity" (
	"Unique_Name" INTEGER UNIQUE,
	"Story" TEXT,
	"ColumnBay" TEXT,
	"UniquePtI" INTEGER,
	"UniquePtJ" INTEGER,
	"Length" INTEGER,
	"GUID" TEXT,
	"ElementID" INTEGER	FOREIGN KEY ("Story") REFERENCES "Frame_Assignments_Section_Properties"("Story")
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY ("Unique_Name") REFERENCES "Frame_Assignments_Section_Properties"("UniqueName")
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY ("UniquePtI") REFERENCES "Objects_and_Elements_Joints"("Element_Name")
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY ("UniquePtJ") REFERENCES "Objects_and_Elements_Joints"("Element_Name")
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY ("ElementID") REFERENCES "Frame_Assignments_Section_Properties"("ID")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "Material_Properties_Concrete_Data" (
	"ID" INTEGER,
	"Material" TEXT UNIQUE,
	"Fc" REAL,
	"LtWtConc" TEXT,
	"IsUserFr" TEXT,
	"SSCurveOpt" TEXT,
	"SSHysType" TEXT,
	"SFc" REAL,
	"SCap" REAL,
	"FinalSlope" REAL,
	"FAngle" INTEGER,
	"DAngle" INTEGER,
	PRIMARY KEY("ID")
);

CREATE TABLE IF NOT EXISTS "Material_Properties_Rebar_Data" (
	"ID" INTEGER,
	"Material" TEXT UNIQUE,
	"Fy" REAL,
	"Fu" REAL,
	"Fye" REAL,
	"Fue" REAL,
	"SSCurveOpt" TEXT,
	"SSHysType" TEXT,
	"SHard" REAL,
	"SCap" REAL,
	"FinalSlope" REAL,
	"GenralID" INTEGER,
	PRIMARY KEY("ID"),
	FOREIGN KEY ("GenralID") REFERENCES "Genralinput"("id")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "Frame_Section_Property_Definitions_Concrete_Column_Reinforcing" (
	"ID" INTEGER,
	"Name" TEXT UNIQUE,
	"Longitudinal_Bar_Material" TEXT,
	"Tie_Bar_Material" TEXT,
	"Reinforcement_Configuration" TEXT,
	"Is_Designed" TEXT,
	"Clear_Cover_to_Ties" REAL,
	"Number_Bars_3_Dir" INTEGER,
	"Number_Bars_2_Dir" INTEGER,
	"Longitudinal_Bar_Size" REAL,
	"Corner_Bar_Size" REAL,
	"Tie_Bar_Size" REAL,
	"Tie_Bar_Spacing" REAL,
	"Number_Ties_3_Dir" INTEGER,
	"Number_Ties_2_Dir" INTEGER,
	"LonZgitudinal_Bar_MaterialID" INTEGER,
	"Tie_Bar_MaterialID" INTEGER,
	"NameID" INTEGER,
	PRIMARY KEY("ID"),
	FOREIGN KEY ("Longitudinal_Bar_Material") REFERENCES "Material_Properties_Rebar_Data"("Material")
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY ("Tie_Bar_Material") REFERENCES "Material_Properties_Rebar_Data"("Material")
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY ("Tie_Bar_MaterialID") REFERENCES "Material_Properties_Rebar_Data"("ID")
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY ("LonZgitudinal_Bar_MaterialID") REFERENCES "Material_Properties_Rebar_Data"("ID")
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY ("NameID") REFERENCES "Frame_Section_Property_Definitions_Concrete_Rectangular"("ID")
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY ("Name") REFERENCES "Frame_Section_Property_Definitions_Concrete_Rectangular"("Name")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "Frame_Section_Property_Definitions_Concrete_Rectangular" (
	"ID" INTEGER,
	"Name" TEXT UNIQUE,
	"Material" TEXT,
	"From_File" TEXT,
	"Depth" REAL,
	"Width" REAL,
	"Rigid_Zone" TEXT,
	"Notional_Size_Type" TEXT,
	"Notional_Auto_Factor" REAL,
	"Design_Type" TEXT,
	"Area_Modifier" REAL,
	"As2_Modifier" REAL,
	"As3_Modifier" REAL,
	"J_Modifier" REAL,
	"I22_Modifier" REAL,
	"I33_Modifier" REAL,
	"Mass_Modifier" REAL,
	"Weight_Modifier" REAL,
	"Color" TEXT,
	"GUID" TEXT,
	"Notes" TEXT,
	"MaterialID" INTEGER,
	PRIMARY KEY("ID"),
	FOREIGN KEY ("Material") REFERENCES "Material_Properties_Concrete_Data"("Material")
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY ("MaterialID") REFERENCES "Material_Properties_Concrete_Data"("ID")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "Frame_Assignments_Section_Properties" (
	"ID" INTEGER,
	"Story" TEXT,
	"Label" TEXT,
	"UniqueName" INTEGER,
	"Shape" TEXT,
	"Auto_Select_List" TEXT,
	"Section_Property" TEXT,
	"Section_PropertyID" INTEGER,
	PRIMARY KEY("ID"),
	FOREIGN KEY ("Section_Property") REFERENCES "Frame_Section_Property_Definitions_Concrete_Rectangular"("Name")
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY ("Section_PropertyID") REFERENCES "Frame_Section_Property_Definitions_Concrete_Rectangular"("ID")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "Load_Combination_Definitions" (
	"ID" INTEGER,
	"Name" TEXT UNIQUE,
	"Type" TEXT,
	"Is_Auto" TEXT,
	"Load_Name" TEXT,
	"SF" REAL,
	"GUID" TEXT,
	"Notes" TEXT,
	PRIMARY KEY("ID")
);

CREATE TABLE IF NOT EXISTS "Element_Forces_Columns" (
	"ID" INTEGER,
	"Story" TEXT,
	"Column" TEXT,
	"Unique_Name" INTEGER,
	"Output_Case" TEXT,
	"Case_Type" TEXT,
	"Station" REAL,
	"P" REAL,
	"V2" REAL,
	"V3" REAL,
	"T" REAL,
	"M2" REAL,
	"M3" REAL,
	"Element" INTEGER,
	"Elem_Station" REAL,
	"Location" REAL,
	"ElementID" INTEGER,
	PRIMARY KEY("ID"),
	FOREIGN KEY ("Story") REFERENCES "Frame_Assignments_Section_Properties"("Story")
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY ("Unique_Name") REFERENCES "Frame_Assignments_Section_Properties"("UniqueName")
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY ("Output_Case") REFERENCES "Load_Combination_Definitions"("Name")
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY ("ElementID") REFERENCES "Frame_Assignments_Section_Properties"("ID")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "Genralinput" (
	"id" INTEGER NOT NULL UNIQUE,
	"Knowledge_Factor" INTEGER,
	"Concrete _Strength_Factor(λ_c)" INTEGER,
	"Steel_Strength_Factor(λ_s)" INTEGER,
	"Performance_Level" TEXT,
	"Safety_Factor(φ)" INTEGER,
	PRIMARY KEY("id")
);
