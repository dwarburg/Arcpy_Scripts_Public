# ---------------------------------------------------------------------------------------------------------------------
# SCRIPT TO BE RUN FROM ArcMap 10.5 window as a tool with 4 parameters-------------------------------------------------
# Joins desktop bio data to tree locations from CSV table--------------------------------------------------------------
# Exports 4 feature classes and 1 excel table--------------------------------------------------------------------------
# Python 2.7-----------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

# Import standard modules
import arcpy
import os
import sys

# Import custom module by appending location to sys.path
if r'Q:\SCE\HTRP_DTRP_2016\03_GIS_Data\scripts' not in sys.path:
    sys.path.append(r'Q:\SCE\HTRP_DTRP_2016\03_GIS_Data\scripts')
import DW_FUNCTIONS

# arcpy environment settings
arcpy.env.addOutputsToMap = 0
arcpy.env.overwriteOutput = 1

# Date string for labeling files
Date_STR = DW_FUNCTIONS.Date_String_Label()

# input paramaters with defaults
INPUT_CSV = arcpy.GetParameterAsText(0)

OUTPUT_Excel = arcpy.GetParameterAsText(1)

OUTPUT_GDB = arcpy.GetParameterAsText(2)

OUTPUT_FC_HTMP_Points = os.path.join(OUTPUT_GDB, "HTMP_Bio_Tree_Points_" + Date_STR)
OUTPUT_FC_Wildlife_Merge_OneToMany = os.path.join(OUTPUT_GDB, "HTMP_Bio_Wildlife_" + Date_STR)
OUTPUT_FC_CNDDB_OneToMany = os.path.join(OUTPUT_GDB, "HTMP_Bio_CNDDB_" + Date_STR)
OUTPUT_FC_SCE_Data_OneToMany = os.path.join(OUTPUT_GDB, "HTMP_Bio_SCE_Data_" + Date_STR)

# local variables
Scratch_GDB = r'Q:\SCE\HTRP_DTRP_2016\03_GIS_Data\geodatabases\scratch\Scratch.gdb'
Modeling_GDB = r'Q:\SCE\HTRP_DTRP_2016\03_GIS_Data\geodatabases\DRI_EI01_20161230\DRI_EI01_20161230.gdb\Production_Modeling_Features'
NWI_Wetlands = r'L:\Data\GIS\Wetlands_and_Waters\CA_wetlands\CA_wetlands_clipped.gdb\CA_wetlands_SCE_clip_QUAD_intsct'
EI_Resources = os.path.join(Modeling_GDB, 'EI_Portal_Resources_Poly_EI01_20190313')
SCE_Gov_Lands_20190313 = os.path.join(Modeling_GDB, "SCE_Gov_Lands_20190313")
SCE_Districts = os.path.join(Modeling_GDB, "SCE_Districts_EI01_20160517")
SCE_FIM_OH_Grid_EI01_20160517 = os.path.join(Modeling_GDB, "SCE_FIM_OH_Grid_EI01_20160517")
NHD_Flowline = os.path.join(Modeling_GDB,"NHDFlowline_DRI_EI01_20171212")
Ranger_Districts_CA_Clip = os.path.join(Modeling_GDB,"Ranger_Districts_CA_Clip_WGS_84_EI01_20160525")
DRP_Habitat = os.path.join(Modeling_GDB,"DRP_HTRP_Habitat_EI05_20160516")
Critical_Habitat = r'L:\Data\GIS\USFWS\CriticalHabitat\20191105\crithab_all_layers\CRITHAB_POLY_CA_CLIP.shp'
SCE_Circuits = os.path.join(Modeling_GDB,"SCE_Distribution_Transmission_Lines_EI01_20160525")
Wildlife_Merge = os.path.join(Modeling_GDB, 'USFS_Wildlife_Merge')
InvasivePlantAll = os.path.join(Modeling_GDB, 'USFS_InvasivePlantAll')
TESP_OccurrenceAll =os.path.join(Modeling_GDB, 'USFS_TESP_OccurrenceAll')
SCE_MSUP_USFS_ROADS = os.path.join(Modeling_GDB, 'SCE_MSUP_USFS_ROADS')
cnddb_shp = "L:\\Data\\GIS\\CDFW\\CNDDB\\Shapefiles\\cnddb.shp"
SNF_USFS_Data = os.path.join(Modeling_GDB,"SNF_USFS_Data_Merge_EI02_20191004")
HTMP_Albers = os.path.join(Scratch_GDB, "HTMP_Albers")
downloaded_table = os.path.join(Scratch_GDB, "downloaded_table")
GCS_WGS_1984_SpatRef = arcpy.SpatialReference(4326)
NAD_1983_Albers_SpatRef = arcpy.SpatialReference(102962)
SCE_DATA_Merge = r'Q:\SCE\HTRP_DTRP_2016\03_GIS_Data\geodatabases\SCE_AGOL_Data\SCE_AGOL_Data_Combined.gdb\SCE_ALL_DATA_MERGE'
USGS_QUAD = r'L:\Data\GIS\USGS\Topographic Maps\USGS_24k_Topo_Map_Boundaries.shp'

# ---------------------------------------------------------------------------------------------------------------------
# CONVERSION TO GIS FEATURE CLASS--------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

arcpy.TableToTable_conversion(INPUT_CSV, Scratch_GDB,"downloaded_table") 
arcpy.AddMessage("Completed: Covert CSV to Table")

tempEnvironment0 = arcpy.env.workspace
arcpy.env.workspace = Scratch_GDB
#HTMP QUERY NOT NECESARY FOR DRI
#arcpy.MakeQueryTable_management(downloaded_table, "QueryTable", "ADD_VIRTUAL_KEY_FIELD", "", "", SQL_Expression)
#arcpy.AddMessage("Completed: SQL Query")

arcpy.MakeXYEventLayer_management(downloaded_table, "_longitude", "_latitude", "HTMP_XY_Event_Layer", GCS_WGS_1984_SpatRef)
arcpy.AddMessage("Completed: Make XY Point Layer")

arcpy.Project_management("HTMP_XY_Event_Layer", HTMP_Albers , NAD_1983_Albers_SpatRef)
arcpy.AddMessage("Completed: Project to NAD_1983_Albers")

# ---------------------------------------------------------------------------------------------------------------------
# ONE TO ONE JOINS ----------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
arcpy.env.workspace = r'in_memory'#change to in_memory for performance (the Project tool above cannot use in_memory workspace)

#Spatial Join (1) GovLands Intersect
DW_FUNCTIONS.SpatJoin_1to1_Intersect("AGENCY_AREANAME", ["AGENCY_AREANAME"],HTMP_Albers, SCE_Gov_Lands_20190313,"HTMP_GovLands")
arcpy.AddMessage("Completed: Spatial Join (1) GovLands Intersect")

#Spatial Join (2) Ranger Dist Intersect
DW_FUNCTIONS.SpatJoin_1to1_Intersect("Ranger_District", ["Ranger_District"], "HTMP_GovLands", Ranger_Districts_CA_Clip, "HTMP_RangerDist")
arcpy.AddMessage("Completed: Spatial Join (2) Ranger Dist Intersect")

#Spatial Join (3) SCE District Intersect
DW_FUNCTIONS.SpatJoin_1to1_Intersect("SCE_District", ["SCE_District"], "HTMP_RangerDist", SCE_Districts, "HTMP_SCE_District")
arcpy.AddMessage("Completed: Spatial Join (3) SCE District Intersect")

#Spatial Join (4) SCE Map Number Intersect
DW_FUNCTIONS.SpatJoin_1to1_Intersect("SCE_Map_Number", ["SCE_Map_Number"], "HTMP_SCE_District", SCE_FIM_OH_Grid_EI01_20160517, "HTMP_SCE_Map_Grid")
arcpy.AddMessage("Completed: Spatial Join (4) SCE Map Number Intersect")

#Spatial Join (5) DRI Habitat 500 ft
DW_FUNCTIONS.SpatJoin_1to1_Within_A_Distance("EI_Habitat_Model", ["EI_Habitat_Model"], "HTMP_SCE_Map_Grid", DRP_Habitat, "HTMP_DRP_Habitat", "500 Feet")
arcpy.AddMessage("Completed: Spatial Join (5) DRI Habitat 500 ft")

#Spatial Join (6) Transmission Lines Closest
DW_FUNCTIONS.SpatJoin_1to1_Closest("SCE_Circuit_Name", '', ["SCE_Circuit_Name"], "HTMP_DRP_Habitat", SCE_Circuits, "HTMP_SCE_Circuits", '')
arcpy.AddMessage("Completed: Spatial Join (6) Transmission Lines Closest")

#Spatial Join (7) Critical Habitat 500 ft
DW_FUNCTIONS.SpatJoin_1to1_Closest("Critical_Habitat", '', ["comname"], "HTMP_SCE_Circuits", Critical_Habitat, "HTMP_CritHabitat", '')
arcpy.AddMessage("Completed: Spatial Join (7) Critical Habitat 500 ft")

#Spatial Join (8) EI Resources 500 ft
DW_FUNCTIONS.SpatJoin_1to1_Within_A_Distance("EI_DATA", ["EI_DATA"], "HTMP_CritHabitat", EI_Resources, "HTMP_EI_Resources", "500 Feet")
arcpy.AddMessage("Completed: Spatial Join (8) EI Resources 500 ft")

#Spatial Join (9) NHD 50ft
DW_FUNCTIONS.SpatJoin_1to1_Closest("NHD_Data", '', ["Resource", "GNIS_Name"], "HTMP_EI_Resources", NHD_Flowline, "HTMP_NHD", '50 Feet')
arcpy.AddMessage("Completed: Spatial Join (9) NHD 50ft")

#Spatial Join (10) NWI 50 ft
#BEGIN:----INTERSECT WITH USGS QUAD THEN USE QUAD QUERY TO LIMIT LARGE NWI DATASET----------
arcpy.SpatialJoin_analysis(HTMP_Albers, USGS_QUAD, "HTMP_QUAD", "JOIN_ONE_TO_ONE", "KEEP_ALL",'',"INTERSECT")
QUADS = []
with arcpy.da.SearchCursor("HTMP_QUAD", "USGS_QD_ID") as SC:
    for row in SC:
        if str(row[0]) not in QUADS:
            QUADS.append(str(row[0]))
QUADS_STR= str(QUADS).replace('[','(').replace(']',')')
SQL_Field = arcpy.AddFieldDelimiters(NWI_Wetlands, "USGS_QD_ID")
QUADS_SQL = """ {0} IN {1} """.format(SQL_Field, QUADS_STR)
arcpy.AddMessage(QUADS_SQL)
arcpy.MakeFeatureLayer_management(NWI_Wetlands, "NWI_Wet_Query", QUADS_SQL)

DW_FUNCTIONS.SpatJoin_1to1_Closest("NWI_Wetland", '', ["WETLAND_TY"], "HTMP_NHD", "NWI_Wet_Query", "HTMP_NWI", '50 Feet')
arcpy.AddMessage("Completed: Spatial Join (10) NWI 50 ft")
#END:----INTERSECT WITH USGS QUAD THEN USE QUAD QUERY TO LIMIT LARGE NWI DATASET----------

#Spatial Join (11) USFS Road Closest
In_Fields = ["Forest","USFS_ROAD_NAME","ROAD_WIDTH","USAGE_STATUS"]
DW_FUNCTIONS.SpatJoin_1to1_Closest("USFS_Road", "Dist_to_ROAD", In_Fields, "HTMP_NHD", SCE_MSUP_USFS_ROADS, "HTMP_USFS_Road", "1 Mile")
arcpy.AddMessage("Completed: Spatial Join (11) USFS Road Closest")

#Spatial Join (12) Invasive Plant 500 ft
In_Fields = ["SITE_ID_FS", "ACCEPTED_COMMON_NAME"]
DW_FUNCTIONS.SpatJoin_1to1_Within_A_Distance("Invasive_Plant", In_Fields , "HTMP_USFS_Road", InvasivePlantAll, "HTMP_Invasive", "500 Feet")
arcpy.AddMessage("Completed: Spatial Join (12) Invasive Plant 500 ft")

#Spatial Join (13) TESP Occurence 500 ft
In_Fields = ["SITE_ID_FS", "SCIENTIFIC_NAME", "COMMON_NAME", "DATE_COLLECTED"]
DW_FUNCTIONS.SpatJoin_1to1_Within_A_Distance("TESP_Occurence", In_Fields , "HTMP_Invasive", TESP_OccurrenceAll, "HTMP_TESP", "500 Feet")
arcpy.AddMessage("Completed: Spatial Join (13) TESP Occurence 500 ft")

#Spatial Join (14) SNF Data 500 ft
DW_FUNCTIONS.SpatJoin_1to1_Within_A_Distance("SNF_Data",["USFS_Data"] , "HTMP_TESP", SNF_USFS_Data, OUTPUT_FC_HTMP_Points, "500 Feet")
arcpy.AddMessage("Completed: Spatial Join (14) SNF Data 500 ft")

#Delete Unwanted Fields
arcpy.DeleteField_management(OUTPUT_FC_HTMP_Points, ["Join_Count","TARGET_FID","EI_DATA"])
arcpy.AddMessage("Completed: Tree Points OUTPUT")

#Excel OUTPUT
arcpy.TableToExcel_conversion(OUTPUT_FC_HTMP_Points, OUTPUT_Excel, "NAME", "CODE")
arcpy.AddMessage("Completed: Excel OUTPUT")

# ---------------------------------------------------------------------------------------------------------------------
# ONE TO MANY JOINS ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

# -----------------Tree Queries---------------------

# hide unnecessary fields
keep_fields = [u'OBJECTID', u'Shape', u'_record_id', u'_latitude', u'_longitude', u'legacy_fulcrum_id', u'control_number', u'property_type', u'AGENCY_AREANAME']
fields= arcpy.ListFields(OUTPUT_FC_HTMP_Points)
fieldinfo = arcpy.FieldInfo()
for field in fields:
    if field.name in keep_fields:
        fieldinfo.addField(field.name, field.name, "VISIBLE", "")
    else:
        fieldinfo.addField(field.name, field.name, "HIDDEN", "")

# SQL Text
Public_SQL = "\"AGENCY_AREANAME\" <> '[USFS : San Bernardino National Forest]' AND(\"AGENCY_AREANAME\" IS NOT NULL) AND (\"AGENCY_AREANAME\" NOT IN ('Undetermined', '[Undetermined]', 'Private', '[Private]', 'undetermined', '[undetermined]', 'private', '[private]'))"
Private_SQL = "(\"AGENCY_AREANAME\") IS NULL OR (\"AGENCY_AREANAME\" IN ('Undetermined', '[Undetermined]', 'Private', '[Private]', 'undetermined', '[undetermined]', 'private', '[private]'))"
# Process: Make Feature Layer (Public Trees Minus SBNF)
arcpy.MakeFeatureLayer_management(OUTPUT_FC_HTMP_Points, "Public_Query_Layer", Public_SQL, "",fieldinfo)
# Process: Make Feature Layer (Private Trees)
arcpy.MakeFeatureLayer_management(OUTPUT_FC_HTMP_Points, "Private_Query_Layer", Private_SQL,"",fieldinfo)
arcpy.AddMessage("Completed: Tree Queries")

# -----------------CNDDB 1 To Many------------------

# All Forests CNDDB SQL Strings
CNDDB_500ft_SQL = "((\"FEDLIST\" <> 'None' ) OR (\"CALLIST\" <> 'None' ) OR \"RPLANTRANK\" NOT IN ( ' ' , '3' , '3.1' , '3.2' , '3.3' , '4.1' , '4.2' , '4.3' ) OR \"CDFWSTATUS\" NOT IN( ' ' , 'WL' ) OR \"OTHRSTATUS\" NOT IN ( ' ' , 'IUCN_LC; NABCI_YWL' , 'IUCN_NT' , 'IUCN_NT; NABCI_YWL' , 'IUCN_VU' , 'NABCI_RWL' , 'NABCI_YWL' )) AND \"DateInt\" > 19500000 AND \"CNAME\" NOT IN ('California Condor', 'Yosemite Toad', 'California Red-Legged Frog', 'Sierra Nevada Yellow-Legged Frog', 'Mountain Yellow-Legged Frog', 'Sierra Nevada Red Fox', 'Sierra Nevada Bighorn Sheep', 'Peninsular Bighorn Sheep')"
CNDDB_03mi_SQL = "\"DateInt\" > 19500000 AND \"CNAME\" IN ('California Condor', 'California Red-Legged Frog', 'Sierra Nevada Yellow-Legged Frog', 'Mountain Yellow-Legged Frog')"
CNDDB_1mi_SQL = "\"DateInt\" > 19500000 AND \"CNAME\" IN ('Yosemite Toad', 'Sierra Nevada Bighorn Sheep', 'Peninsular Bighorn Sheep')"
CNDDB_5mi_SQL = "\"DateInt\" > 19500000 AND \"CNAME\" = 'Sierra Nevada Red Fox'"

# All Forests CNDDB Queries
# Process: Make Feature Layer (All Forests CNDDB 500 ft)
arcpy.MakeFeatureLayer_management(cnddb_shp, "CNDDB_qry_500ft", CNDDB_500ft_SQL, "", "")
# Process: Make Feature Layer (All Forests CNDDB 0.3 mi)
arcpy.MakeFeatureLayer_management(cnddb_shp, "CNDDB_qry_03mi", CNDDB_03mi_SQL, "","")
# Process: Make Feature Layer (All Forests CNDDB 1 mi)
arcpy.MakeFeatureLayer_management(cnddb_shp, "CNDDB_qry_1mi", CNDDB_1mi_SQL, "", "")
# Process: Make Feature Layer (All Forests CNDDB 5 mi)
arcpy.MakeFeatureLayer_management(cnddb_shp, "CNDDB_qry_5mi", CNDDB_5mi_SQL, "", "")
# Private Query
# Process: Make Feature Layer (Private CNDDB 500 ft)
arcpy.MakeFeatureLayer_management(cnddb_shp, "Private_CNDDB_qry_500ft", "((\"FEDLIST\" <> 'None' ) OR (\"CALLIST\" <> 'None' ) OR \"RPLANTRANK\" NOT IN ( ' ' , '3' , '3.1' , '3.2' , '3.3' , '4.1' , '4.2' , '4.3' ) OR \"CDFWSTATUS\" NOT IN( ' ' , 'WL' ) OR \"OTHRSTATUS\" NOT IN ( ' ' , 'IUCN_LC; NABCI_YWL' , 'IUCN_NT' , 'IUCN_NT; NABCI_YWL' , 'IUCN_VU' , 'NABCI_RWL' , 'NABCI_YWL' )) AND \"DateInt\" > 19500000")
arcpy.AddMessage("Completed: CNDDB Queries")

# All Forests CNNDB Joins
# Process: Spatial Join CNDDB 500 ft
arcpy.SpatialJoin_analysis("CNDDB_qry_500ft", "Public_Query_Layer", "CNDDB_OneToMany_500ft", "JOIN_ONE_TO_MANY", "KEEP_COMMON", "", "WITHIN_A_DISTANCE", "500 Feet", "")
# Process: Spatial Join CNDDB 0.3 Mile
arcpy.SpatialJoin_analysis("CNDDB_qry_03mi", "Public_Query_Layer", "CNDDB_OneToMany_03mi", "JOIN_ONE_TO_MANY", "KEEP_COMMON", "", "WITHIN_A_DISTANCE", "0.3 Miles", "")
# Process: Spatial Join CNDDB 1 Mile
arcpy.SpatialJoin_analysis("CNDDB_qry_1mi", "Public_Query_Layer", "CNDDB_OneToMany_1mi", "JOIN_ONE_TO_MANY", "KEEP_COMMON", "", "WITHIN_A_DISTANCE", "1 Miles", "")
# Process: Spatial Join CNDDB 5 Mile
arcpy.SpatialJoin_analysis("CNDDB_qry_5mi", "Public_Query_Layer", "CNDDB_OneToMany_5mi", "JOIN_ONE_TO_MANY", "KEEP_COMMON", "", "WITHIN_A_DISTANCE", "5 Miles", "")
# Private Join
# Process: Spatial Join Private CNDDB 500 ft
arcpy.SpatialJoin_analysis("Private_CNDDB_qry_500ft", "Private_Query_Layer", "Private_CNDDB_OneToMany_500ft", "JOIN_ONE_TO_MANY", "KEEP_COMMON", "", "WITHIN_A_DISTANCE", "500 Feet", "")
arcpy.AddMessage("Completed: CNDDB Joins - 1 to Many")


# -----------------USFS Wildlife 1 To Many---------

# All Forests USFS Wildlife Queries
# Process: Make Feature Layer (USFS Wildlife 500ft) 
arcpy.MakeFeatureLayer_management(Wildlife_Merge, "Wildlife_Merge_500ft", "COMMON_NAME NOT IN ('California Condor', 'Yosemite Toad', 'California Red-Legged Frog', 'Sierra Nevada Yellow-Legged Frog', 'Mountain Yellow-Legged Frog', 'Sierra Nevada Red Fox', 'Sierra Nevada Bighorn Sheep', 'Peninsular Bighorn Sheep')", "", "")
# Process: Make Feature Layer (USFS Wildlife 0.3 mi)
arcpy.MakeFeatureLayer_management(Wildlife_Merge, "Wildlife_Merge_03mi", "COMMON_NAME IN ('California Condor', 'California Red-Legged Frog', 'Sierra Nevada Yellow-Legged Frog', 'Mountain Yellow-Legged Frog')", "", "")
# Process: Make Feature Layer (USFS Wildlife 1 mi) 
arcpy.MakeFeatureLayer_management(Wildlife_Merge, "Wildlife_Merge_1mi", "COMMON_NAME IN ('Yosemite Toad', 'Sierra Nevada Bighorn Sheep', 'Peninsular Bighorn Sheep')", "", "")
# Process: Make Feature Layer (USFS Wildlife 5 mi)
arcpy.MakeFeatureLayer_management(Wildlife_Merge, "Wildlife_Merge_5mi", "COMMON_NAME IN ('Sierra Nevada Red Fox')", "", "")
arcpy.AddMessage("Completed: USFS Wildlife Queries")

# All Forests USFS Wildlife Joins
# Process: Spatial Join Wildllfie Sites 500ft
arcpy.SpatialJoin_analysis("Wildlife_Merge_500ft", "Public_Query_Layer", "Wildlife_Merge_500ft_OneToMany", "JOIN_ONE_TO_MANY", "KEEP_COMMON", "", "WITHIN_A_DISTANCE", "500 Feet", "")
# Process: Spatial Join USFS Wildlife 0.3 mile
arcpy.SpatialJoin_analysis("Wildlife_Merge_03mi", "Public_Query_Layer", "Wildlife_Merge_03mi_OneToMany", "JOIN_ONE_TO_MANY", "KEEP_COMMON", "", "WITHIN_A_DISTANCE", "0.3 Miles", "")
# Process: Spatial Join USFS Wildlife 1 mile
arcpy.SpatialJoin_analysis("Wildlife_Merge_1mi", "Public_Query_Layer", "Wildlife_Merge_1mi_OneToMany", "JOIN_ONE_TO_MANY", "KEEP_COMMON", "", "WITHIN_A_DISTANCE", "1 Miles", "")
# Process: Spatial Join USFS Wildlife 5 mile
arcpy.SpatialJoin_analysis("Wildlife_Merge_5mi", "Public_Query_Layer", "Wildlife_Merge_5mi_OneToMany", "JOIN_ONE_TO_MANY", "KEEP_COMMON", "", "WITHIN_A_DISTANCE", "5 Miles", "")
# Process: Private Spatial Join USFS Wildlife 500ft
arcpy.SpatialJoin_analysis(Wildlife_Merge, "Private_Query_Layer", "Wildlife_Merge_500ft_OneToMany_Private", "JOIN_ONE_TO_MANY", "KEEP_COMMON", "", "WITHIN_A_DISTANCE", "500 Feet", "")
arcpy.AddMessage("Completed: USFS Wildlife Joins - 1 to Many ")

# ANF USFS Wildlife Queries
# Process: Make Feature Layer (USFS Wildlife 0.3 mi) (3)
arcpy.MakeFeatureLayer_management(Wildlife_Merge, "CASP_PAC_Layer_ANF", "SITE_NAME LIKE '%Spotted Owl PAC%'")
# Process: Make Feature Layer (4)
arcpy.MakeFeatureLayer_management(OUTPUT_FC_HTMP_Points, "Angeles_Query_Layer", "AGENCY_AREANAME = '[USFS : Angeles National Forest]'")
arcpy.AddMessage("Completed: ANF CASPO Query")
# ANF USFS Wildlife Join
# Process: Spatial Join USFS Wildlife 0.3 mile (3)
arcpy.SpatialJoin_analysis("CASP_PAC_Layer_ANF", "Angeles_Query_Layer", "CASPO_ANF_03mi_OneToMany", "JOIN_ONE_TO_MANY", "KEEP_COMMON", "", "WITHIN_A_DISTANCE", "0.3 Miles", "")
arcpy.AddMessage("Completed: ANF CASPO Join - 1 to Many")

# -----------------SCE AGOL DATA 1 To Many------------------

# All Forests SCE Queries
# Process: Make Feature Layer (SCE 50ft)
arcpy.MakeFeatureLayer_management(SCE_DATA_Merge, "SCE_50ft", "Layer IN( 'JD__Jurisdictional_Polygons' , 'JD__Wetlands' )")
# Process: Make Feature Layer (SCE 500ft)
arcpy.MakeFeatureLayer_management(SCE_DATA_Merge, "SCE_500ft", "SP_STAT_SP = 'Yes' AND SPP_NM_CM NOT IN ('California Condor', 'Yosemite Toad', 'California Red-Legged Frog', 'Sierra Nevada Yellow-Legged Frog', 'Mountain Yellow-Legged Frog', 'Sierra Nevada Red Fox', 'Sierra Nevada Bighorn Sheep', 'Peninsular Bighorn Sheep')")
# Process: Make Feature Layer (SCE 0.3 mi)
arcpy.MakeFeatureLayer_management(SCE_DATA_Merge, "SCE_03mi", "SPP_NM_CM IN ('California Condor', 'California Red-Legged Frog', 'Sierra Nevada Yellow-Legged Frog', 'Mountain Yellow-Legged Frog')")
# Process: Make Feature Layer (SCE 1 mi)
arcpy.MakeFeatureLayer_management(SCE_DATA_Merge, "SCE_1mi", "SPP_NM_CM IN ('Yosemite Toad', 'Sierra Nevada Bighorn Sheep', 'Peninsular Bighorn Sheep')")
# Process: Make Feature Layer (SCE 5 mi)
arcpy.MakeFeatureLayer_management(SCE_DATA_Merge, "SCE_5mi", "SPP_NM_CM IN ('Sierra Nevada Red Fox')")
arcpy.AddMessage("Completed: SCE Queries")

# All Forests SCE Joins
# Process: Spatial Join SCE 50 ft
arcpy.SpatialJoin_analysis("SCE_50ft", "Public_Query_Layer", "SCE_50ft_OneToMany", "JOIN_ONE_TO_MANY", "KEEP_COMMON", "", "WITHIN_A_DISTANCE", "50 Feet", "")
# Process: Spatial Join SCE 500 ft
arcpy.SpatialJoin_analysis("SCE_500ft", "Public_Query_Layer", "SCE_500ft_OneToMany", "JOIN_ONE_TO_MANY", "KEEP_COMMON", "", "WITHIN_A_DISTANCE", "500 Feet", "")
# Process: Spatial Join SCE 03mile
arcpy.SpatialJoin_analysis("SCE_03mi", "Public_Query_Layer", "SCE_03mi_OneToMany", "JOIN_ONE_TO_MANY", "KEEP_COMMON", "", "WITHIN_A_DISTANCE", "0.3 Miles", "")
# Process: Spatial Join SCE 1 mile
arcpy.SpatialJoin_analysis("SCE_1mi", "Public_Query_Layer", "SCE_1mi_OneToMany", "JOIN_ONE_TO_MANY", "KEEP_COMMON", "", "WITHIN_A_DISTANCE", "1 Miles", "")
# Process: Spatial Join SCE 5 mile
arcpy.SpatialJoin_analysis("SCE_5mi", "Public_Query_Layer", "SCE_5mi_OneToMany", "JOIN_ONE_TO_MANY", "KEEP_COMMON", "", "WITHIN_A_DISTANCE", "5 Miles", "")
# Process: Private Spatial Join SCE 500ft
arcpy.SpatialJoin_analysis(SCE_DATA_Merge, "Private_Query_Layer", "SCE_500ft_OneToMany_Private", "JOIN_ONE_TO_MANY", "KEEP_COMMON", "", "WITHIN_A_DISTANCE", "500 Feet", "")
arcpy.AddMessage("Completed: SCE Joins - 1 to Many")


# -----------------Final Merged Outputs------------------
# CNDDB Merge
arcpy.Merge_management(["CNDDB_OneToMany_500ft", "CNDDB_OneToMany_03mi", "CNDDB_OneToMany_1mi", "CNDDB_OneToMany_5mi", "Private_CNDDB_OneToMany_500ft"], OUTPUT_FC_CNDDB_OneToMany)
arcpy.AddMessage("Completed: CNDDB OUTPUT")
# USFS Wildlife Merge
arcpy.Merge_management(["Wildlife_Merge_500ft_OneToMany_Private", "Wildlife_Merge_500ft_OneToMany", "Wildlife_Merge_03mi_OneToMany", "Wildlife_Merge_1mi_OneToMany","Wildlife_Merge_5mi_OneToMany","CASPO_ANF_03mi_OneToMany"], OUTPUT_FC_Wildlife_Merge_OneToMany)
arcpy.AddMessage("Completed: USFS Wildlife OUTPUT")
# SCE Merge
arcpy.Merge_management(["SCE_500ft_OneToMany_Private", "SCE_50ft_OneToMany", "SCE_500ft_OneToMany", "SCE_03mi_OneToMany", "SCE_1mi_OneToMany", "SCE_5mi_OneToMany"], OUTPUT_FC_SCE_Data_OneToMany)
arcpy.AddMessage("Completed: SCE Data OUTPUT")

