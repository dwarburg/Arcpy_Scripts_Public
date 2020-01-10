# Import arcpy module
import arcpy
import os
import datetime
import getpass
arcpy.env.overwriteOutput = True

now = datetime.datetime.now()
Start_Time = str(now.year) + str(now.month) + str(now.day) +'_'+str(now.hour)+'h' + str(now.minute)+'m' + str(now.second)+'s'

# User Entry Variables:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# conditional variables that can be defined in stand-alone script or in arcmap
try:
  KMZ_Input
  EI_Date
  GIS_Folder
  Geometry_Type
except NameError:
    KMZ_Input = arcpy.GetParameterAsText(0)
    EI_Date = arcpy.GetParameterAsText(1)
    GIS_Folder = arcpy.GetParameterAsText(2)
    Geometry_Type = arcpy.GetParameterAsText(3)
# non-conditional variables that are the same  in stand-alone script and in arcmap    
EI_Version = "01" #Use two digits
KMZ_File_Output_Name = 'project_location'+EI_Version+'_'+EI_Date
KMZ_Output_Folder_Location = r'L:\Data\GIS\Scripts\00-archive\temp_Shapefiles'
if Geometry_Type == "Points":
    Reprojection_Input_File = KMZ_Output_Folder_Location +"\\"+KMZ_File_Output_Name+r'.gdb\Placemarks\Points'
elif Geometry_Type == "Polygons":
    Reprojection_Input_File = KMZ_Output_Folder_Location +"\\"+KMZ_File_Output_Name+r'.gdb\Placemarks\Polygons'
else:
    Reprojection_Input_File = KMZ_Output_Folder_Location +"\\"+KMZ_File_Output_Name+r'.gdb\Placemarks\Polylines'
#ExportPaths

GDB_folder = os.path.join(GIS_Folder, 'geodatabases')
GDB = arcpy.CreateFileGDB_management (GDB_folder,  EI_Date[:-8] + 'Working_EI01_'+ EI_Date[-8:] +'.gdb')

UTM_11 = arcpy.SpatialReference('NAD 1983 UTM Zone 11N')

Boundary_Dataset = arcpy.CreateFeatureDataset_management (GDB, 'Boundaries', UTM_11)
Processing_Dataset = arcpy.CreateFeatureDataset_management (GDB, 'Scratch', UTM_11) 
Bio_Dataset = arcpy.CreateFeatureDataset_management (GDB, 'Bio', UTM_11) 

Boundary_Dataset_Path = str(Boundary_Dataset)
Processing_Dataset_Path = str(Processing_Dataset)
Bio_Dataset_Path = str(Bio_Dataset)

Excel_Table_Path = os.path.join(GIS_Folder, 'tables', 'excel') 
KMZ_Path = os.path.join(GIS_Folder, 'vectors', 'kml') 

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Additional Variables
#Study Area Data
#Note-Point location is UTM after it has been converted from a kml and exported to UTM zone 11 - NEED to figure out this step
#Point_Location = r'Q:\Applied Earthworks\TMDCIR Race Track\02_GIS_Data\vectors\shapefiles\Boundaries\SurveyArea_Boundary_EI01_20170109.shp'
#Point_Location = r'Q:\SCE\On-Call Environmental Services\CWA_048_DetPoles_Blanket\CWA048_024_TD1223685_DP_Private\02_GIS_Data\vectors\shapefiles\Boundaries\PoleLocations_UTM_fromSCE_kmz.shp'
#Line_Location = r'Q:\SCE\On-Call Environmental Services\CWA_048_DetPoles_Blanket\CWA048_006_TD1170213_NDP_Porterville-Woodville\02_GIS_Data\vectors\shapefiles\Boundaries\CWA048_006_Porterville_Woodville_Reconductor_Centerline_UTM_EI01_20170110.shp'
#Polygon_Location = r'Q:\SCE\On-Call Environmental Services\CWA_056_CapitalOnRamp_HuntingtonBeach\02_GIS_Data\geodatabases\CapitalOnRamp_HuntingtonBeach_EI01_20161212.gdb\Boundaries\SurveyArea_Combined_EI01_20161212'


#Background Data
County = r'L:\Data\GIS\Cal_GIS\1_24000_County.shp'
TownSecRange = r'L:\Data\GIS\Cal_GIS\plsa\plsa_utm.shp'
Quadrangle = r'L:\Data\GIS\Cal_GIS\Quad boundaries\mapgrida\mapgrida_utm.shp'
City = r'L:\Data\GIS\Cal_GIS\Incorporated Cities\incorp16_1_shape\incorp16_1.shp'
BLM_LandFile = r'L:\Data\GIS\BLM\LandStatus_v10.gdb\LndSurfaceEstate_SMA'
CPAD_LandFile = r'L:\Data\GIS\California Protected Areas\CPAD_2016a\CPAD_2016a\CPAD_2016a_SuperUnits.shp'
USFS_LandFile = r'L:\Data\GIS\USFS\S_USA.Ownership_P.gdb\Ownership_P'
HTRP_LandOwner = r'L:\SCE\HTRP_DTRP_2016\03_GIS_Data\geodatabases\HTRP_DTRP_TAS\DRP_HTRP_TAS_EI01_20160517.gdb\Model_Features\Land_Ownership_EI01_20160429'

#Bio Data
CritHabPoly = r'L:\Data\GIS\USFWS\CriticalHabitat\20160825\CRITHAB_POLY.shp'
CritHabLine = r'L:\Data\GIS\USFWS\CriticalHabitat\20160825\CRITHAB_LINE.shp'
CNDDB = r'L:\Data\GIS\CDFW\CNDDB\Shapefiles\cnddb.shp'
NWI_wet = r'L:\Data\GIS\Wetlands_and_Waters\NWI\CA_wetlands.gdb\CA_Wetlands'
NWI_rip = r'L:\Data\GIS\Wetlands_and_Waters\NWI\CA_wetlands.gdb\CA_Riparian' 
NHD = r'L:\Data\GIS\Wetlands_and_Waters\NHD\NHD_H_06_GDB\NHD_H_06_GDB.gdb\Hydrography\NHDFlowline'#need field calculator script for what flowline codes mean
#LandPlanningAreas = r'L:\Data\GIS\BLM\LndUsePlans_v10.gdb\lupa\lupa_exist_poly' #BLM
LandPlanningAreas = r'L:\Data\GIS\CDFW\HCP_NCCPs\ds760_CDFW_HCP_NCCPs.shp' #NCCP_HCPs
#CCH = Need to download all and ensure all records in each County
#CalVeg = r'L:\Data\GIS\Riverside_County\Riverside_County_MSHCP\CWData.gdb\Vegetation' #Riverside county
#CalVeg = r'L:\Data\GIS\Cal_GIS\CALveg\ExistingVegSouthCoast2002_2010_v2.gdb\ExistingVegSouthCoast2002_2010_v2'
#CalVeg = r'L:\Data\GIS\Cal_GIS\CALveg\CentralValley_1998_2007_v1_UTM\CentralValley_1998_2007_v1_UTM.shp' #Central Valley Region
#CalVeg = r'L:\Data\GIS\Desert Renewable Energy Conservation Plan\ds735.gdb\ds735' # DRECP
#CoastalZone = r'L:\Data\GIS\Coastal Zone\Coastal_Zone_Layer_fromSCE_20170103.gdb\Placemarks\Polygons'
ACEC = r'L:\Data\GIS\BLM\Acec_v10.gdb\Acec\acec_desig_poly'
CFWO_Spp = r'G:\Data\GIS\USFWS\Species Occurrence Data\Carlsbad_FWO\Species_Occurrence_Polys.shp'

#Exports
#KMZ_to_GDB_Export


Point_UTM_Export = Boundary_Dataset_Path+r'\project_location'+EI_Version+'_'+EI_Date
#Boundaries Feature Dataset
#Point_UTM_Export = Boundary_Dataset_Path+r'\Pole_Locations_EI'+EI_Version+'_'+EI_Date
#Buffer_100ft = Point_UTM_Export
Buffer_100ft = Boundary_Dataset_Path+r'\StudyArea_100ft_BUFF_EI'+EI_Version+'_'+EI_Date
Buffer_3Mile = Boundary_Dataset_Path+r'\StudyArea_3mi_BUFF_EI'+EI_Version+'_'+EI_Date

#Processing
#Clips
CritHabPoly_3mi_Clip = Processing_Dataset_Path+r'\CritHabPoly_3mi_CLIP_EI'+EI_Version+'_'+EI_Date
CritHabLine_3mi_Clip = Processing_Dataset_Path+r'\CritHabLine_3mi_CLIP_EI'+EI_Version+'_'+EI_Date
CNDDB_3mi_Clip = Processing_Dataset_Path+r'\CNDDB_3mi_CLIP_EI'+EI_Version+'_'+EI_Date
NWI_wet_3mi_Clip = Processing_Dataset_Path+r'\NWI_wet_3mi_CLIP_EI'+EI_Version+'_'+EI_Date
NWI_rip_3mi_Clip = Processing_Dataset_Path+r'\NWI_rip_3mi_CLIP_EI'+EI_Version+'_'+EI_Date
NHD_3mi_Clip = Processing_Dataset_Path+r'\NHD_3mi_CLIP_EI'+EI_Version+'_'+EI_Date
LandPlanningAreas_3mi_Clip = Processing_Dataset_Path+r'\LandPlanningAreas_3mi_CLIP_EI'+EI_Version+'_'+EI_Date
#CalVeg_3mi_Clip = Processing_Dataset_Path+r'\CalVeg_3mi_CLIP_EI'+EI_Version+'_'+EI_Date
#CalVeg_100ft_Intersect = Processing_Dataset_Path+r'\CalVeg_100ft_INTERSECT_EI'+EI_Version+'_'+EI_Date
CFWO_Spp_3mi_Clip = Processing_Dataset_Path+r'\CFWO_Spp_3mi_CLIP_EI'+EI_Version+'_'+EI_Date

#Bio Feature Dataset
CritHabPoly_SpatialJoin = Bio_Dataset_Path+r'\CritHabPoly_in_3mi_100ft_Buff_JOIN_EI'+EI_Version+'_'+EI_Date
CritHabLine_SpatialJoin = Bio_Dataset_Path+r'\CritHabLine_in_3mi_100ft_Buff_JOIN_EI'+EI_Version+'_'+EI_Date
CNDDB_SpatialJoin = Bio_Dataset_Path+r'\CNDDB_in_3mi_100ft_Buff_JOIN_EI'+EI_Version+'_'+EI_Date
NWI_wet_SpatialJoin = Bio_Dataset_Path+r'\NWI_wet_in_3mi_100ft_Buff_JOIN_EI'+EI_Version+'_'+EI_Date
NWI_rip_SpatialJoin = Bio_Dataset_Path+r'\NWI_rip_in_3mi_100ft_Buff_JOIN_EI'+EI_Version+'_'+EI_Date
NHD_SpatialJoin = Bio_Dataset_Path+r'\NHD_in_3mi_100ft_Buff_JOIN_EI'+EI_Version+'_'+EI_Date
LandPlanningAreas_SpatialJoin = Bio_Dataset_Path+r'\LandPlanningAreas_in_3mi_100ft_Buff_JOIN_EI'+EI_Version+'_'+EI_Date
#CalVeg_SpatialJoin = Bio_Dataset_Path+r'\CalVeg_in_3mi_100ft_Buff_JOIN_EI'+EI_Version+'_'+EI_Date
CFWO_Spp_SpatialJoin = Bio_Dataset_Path+r'\CFWO_Spp_in_3mi_100ft_Buff_JOIN_EI'+EI_Version+'_'+EI_Date

#Excel Tables
CritHabPoly_Excel = Excel_Table_Path+r'\CritHabPoly_in_3mi_BUFF_EI'+EI_Version+'_'+EI_Date+".xls"
CritHabLine_Excel = Excel_Table_Path+r'\CritHabLine_in_3mi_BUFF_EI'+EI_Version+'_'+EI_Date+".xls"
CNDDB_Excel = Excel_Table_Path+r'\CNDDB_in_3mi_BUFF_EI'+EI_Version+'_'+EI_Date+".xls"
NWI_wet_Excel = Excel_Table_Path+r'\NWI_wet_in_3mi_BUFF_EI'+EI_Version+'_'+EI_Date+".xls"
NWI_rip_Excel = Excel_Table_Path+r'\NWI_rip_in_3mi_BUFF_EI'+EI_Version+'_'+EI_Date+".xls"
NHD_Excel = Excel_Table_Path+r'\NHD_in_3mi_BUFF_EI'+EI_Version+'_'+EI_Date+".xls"
LandPlanningAreas_Excel = Excel_Table_Path+r'\LandPlanningAreas_in_3mi_BUFF_EI'+EI_Version+'_'+EI_Date+".xls"
#CalVeg_Excel = Excel_Table_Path+r'\CalVeg_in_100ft_BUFF_EI'+EI_Version+'_'+EI_Date+".xls"
CFWO_Spp_Excel = Excel_Table_Path+r'\CFWO_Spp_in_3mi_BUFF_EI'+EI_Version+'_'+EI_Date+".xls"

#KMZ Files
CritHabPoly_KML = KMZ_Path+r'\CritHabPoly_in_3mi_BUFF_EI'+EI_Version+'_'+EI_Date+".kmz"
CritHabLine_KML = KMZ_Path+r'\CritHabLine_in_3mi_BUFF_EI'+EI_Version+'_'+EI_Date+".kmz"
CNDDB_KML = KMZ_Path+r'\CNDDB_in_3mi_BUFF_EI'+EI_Version+'_'+EI_Date+".kmz"
NWI_wet_KML = KMZ_Path+r'\NWI_wet_in_3mi_BUFF_EI'+EI_Version+'_'+EI_Date+".kmz"
NWI_rip_KML = KMZ_Path+r'\NWI_rip_in_3mi_BUFF_EI'+EI_Version+'_'+EI_Date+".kmz"
NHD_KML = KMZ_Path+r'\NHD_in_3mi_BUFF_EI'+EI_Version+'_'+EI_Date+".kmz"
LandPlanningAreas_KML = KMZ_Path+r'\LandPlanningAreas_in_3mi_BUFF_EI'+EI_Version+'_'+EI_Date+".kmz"
#CalVeg_KML = KMZ_Path+r'\CalVeg_in_100ft_BUFF_EI'+EI_Version+'_'+EI_Date+".kmz"
StudyArea_100ft_BUFF_KML = KMZ_Path+r'\StudyArea_100ft_BUFF_EI'+EI_Version+'_'+EI_Date+".kmz"
StudyArea_3mi_BUFF_KML = KMZ_Path+r'\StudyArea_3mi_BUFF_EI'+EI_Version+'_'+EI_Date+".kmz"
CFWO_Spp_KML = KMZ_Path+r'\CFWO_Spp_in_3mi_BUFF_EI'+EI_Version+'_'+EI_Date+".kmz"

###-----Processing--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Set Environment
#arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("NAD_1983_UTM_Zone_11N")
#arcpy.env.geographicTransformations = "NAD_1983_To_WGS_1984_1"
arcpy.env.outputCoordinateSystem = "PROJCS['NAD_1983_UTM_Zone_11N',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-117.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]"
arcpy.env.geographicTransformations = "NAD_1983_To_WGS_1984_1"

#KMZ Import
arcpy.KMLToLayer_conversion(KMZ_Input, KMZ_Output_Folder_Location, KMZ_File_Output_Name)
#KMZ_to_FeatureClass



Reprojection_Output_Coords = "PROJCS['NAD_1983_UTM_Zone_11N',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-117.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]"
Reprojection_Transformation = "NAD_1983_To_WGS_1984_1"
arcpy.Project_management(Reprojection_Input_File, Point_UTM_Export, Reprojection_Output_Coords, Reprojection_Transformation)
arcpy.AddField_management(Point_UTM_Export, "PoleName", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.CalculateField_management(Point_UTM_Export, "PoleName", "!Name!", "PYTHON_9.3", "")
Drop_Fields = ["Name", "FolderPath", "SymbolID", "AltMode", "Base", "Snippet", "PopupInfo", "HasLabel", "LabelID"] 
arcpy.DeleteField_management(Point_UTM_Export, Drop_Fields)

# Process: Copy Features - copies features from shapefile to GDB boundary feature dataset
#arcpy.CopyFeatures_management(Point_Location, Point_UTM_Export, "", "0", "0", "0")
#print "Features copied to GDB"

# Process: Buffer
arcpy.Buffer_analysis(Point_UTM_Export, Buffer_100ft, "100 Feet", "FULL", "ROUND", "NONE", "", "PLANAR")
arcpy.Buffer_analysis(Buffer_100ft, Buffer_3Mile, "3 Miles", "FULL", "ROUND", "ALL", "", "PLANAR")

# Process: Clip
#arcpy.Intersect_analysis([CalVeg, Buffer_100ft], CalVeg_100ft_Intersect, "")
#print "Cal Veg Intersect completed"
arcpy.Clip_analysis(CritHabPoly, Buffer_3Mile, CritHabPoly_3mi_Clip, "")
arcpy.Clip_analysis(CritHabLine, Buffer_3Mile, CritHabLine_3mi_Clip, "")
arcpy.Clip_analysis(CNDDB, Buffer_3Mile, CNDDB_3mi_Clip, "")
arcpy.Clip_analysis(NWI_wet, Buffer_3Mile, NWI_wet_3mi_Clip, "")
arcpy.Clip_analysis(NWI_rip, Buffer_3Mile, NWI_rip_3mi_Clip, "")
arcpy.Clip_analysis(NHD, Buffer_3Mile, NHD_3mi_Clip, "")
arcpy.Clip_analysis(LandPlanningAreas, Buffer_3Mile, LandPlanningAreas_3mi_Clip, "")

#arcpy.Clip_analysis(CalVeg, Buffer_3Mile, CalVeg_3mi_Clip, "")
#print "Cal Veg Clip completed"
arcpy.Clip_analysis(CFWO_Spp, Buffer_3Mile, CFWO_Spp_3mi_Clip, "")

# Process: Spatial Join
try:
	arcpy.SpatialJoin_analysis(CritHabPoly_3mi_Clip, Buffer_100ft, CritHabPoly_SpatialJoin, "JOIN_ONE_TO_MANY", "#", "#", "CLOSEST", "3 miles", "Dist_m")
except:
	pass
try:
	arcpy.SpatialJoin_analysis(CritHabLine_3mi_Clip, Buffer_100ft, CritHabLine_SpatialJoin, "JOIN_ONE_TO_MANY", "#", "#", "CLOSEST", "3 miles", "Dist_m")
except:
	pass
arcpy.SpatialJoin_analysis(CNDDB_3mi_Clip, Buffer_100ft, CNDDB_SpatialJoin, "JOIN_ONE_TO_MANY", "", "", "CLOSEST", "3 miles", "Dist_m")
arcpy.SpatialJoin_analysis(NWI_wet_3mi_Clip, Buffer_100ft, NWI_wet_SpatialJoin, "JOIN_ONE_TO_MANY", "#", "#", "CLOSEST", "3 miles", "Dist_m")
arcpy.SpatialJoin_analysis(NWI_rip_3mi_Clip, Buffer_100ft, NWI_rip_SpatialJoin, "JOIN_ONE_TO_MANY", "#", "#", "CLOSEST", "3 miles", "Dist_m")
arcpy.SpatialJoin_analysis(NHD_3mi_Clip, Buffer_100ft, NHD_SpatialJoin, "JOIN_ONE_TO_MANY", "#", "#", "CLOSEST", "3 miles", "Dist_m")
arcpy.SpatialJoin_analysis(LandPlanningAreas_3mi_Clip, Buffer_100ft, LandPlanningAreas_SpatialJoin, "JOIN_ONE_TO_MANY", "#", "#", "CLOSEST", "3 miles", "Dist_m")
#arcpy.SpatialJoin_analysis(CalVeg_3mi_Clip, Buffer_100ft, CalVeg_SpatialJoin, "JOIN_ONE_TO_MANY", "#", "#", "CLOSEST", "3 miles", "Dist_m")
arcpy.SpatialJoin_analysis(CFWO_Spp_3mi_Clip, Buffer_100ft, CFWO_Spp_SpatialJoin, "JOIN_ONE_TO_MANY", "#", "#", "CLOSEST", "3 miles", "Dist_m")

#Process: Add and Calculate Fields - distance field to miles and feet
#CritHabPoly
try:
	arcpy.AddField_management(CritHabPoly_SpatialJoin, "Dist_ft", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(CritHabPoly_SpatialJoin, "Dist_mi", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
	arcpy.CalculateField_management(CritHabPoly_SpatialJoin, "Dist_ft", "!Dist_m!*3.28084", "PYTHON_9.3", "")
	arcpy.CalculateField_management(CritHabPoly_SpatialJoin, "Dist_mi", "!Dist_ft!/5280", "PYTHON_9.3", "")
except:
	pass
#CritHabLine
try:
	arcpy.AddField_management(CritHabLine_SpatialJoin, "Dist_ft", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(CritHabLine_SpatialJoin, "Dist_mi", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
	arcpy.CalculateField_management(CritHabLine_SpatialJoin, "Dist_ft", "!Dist_m!*3.28084", "PYTHON_9.3", "")
	arcpy.CalculateField_management(CritHabLine_SpatialJoin, "Dist_mi", "!Dist_ft!/5280", "PYTHON_9.3", "")
except:
	pass
#CNDDB
arcpy.AddField_management(CNDDB_SpatialJoin, "Dist_ft", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(CNDDB_SpatialJoin, "Dist_mi", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.CalculateField_management(CNDDB_SpatialJoin, "Dist_ft", "!Dist_m!*3.28084", "PYTHON_9.3", "")
arcpy.CalculateField_management(CNDDB_SpatialJoin, "Dist_mi", "!Dist_ft!/5280", "PYTHON_9.3", "")
#NWI Wetland
arcpy.AddField_management(NWI_wet_SpatialJoin, "Dist_ft", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(NWI_wet_SpatialJoin, "Dist_mi", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.CalculateField_management(NWI_wet_SpatialJoin, "Dist_ft", "!Dist_m!*3.28084", "PYTHON_9.3", "")
arcpy.CalculateField_management(NWI_wet_SpatialJoin, "Dist_mi", "!Dist_ft!/5280", "PYTHON_9.3", "")
#NWI Riparian
arcpy.AddField_management(NWI_rip_SpatialJoin, "Dist_ft", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(NWI_rip_SpatialJoin, "Dist_mi", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.CalculateField_management(NWI_rip_SpatialJoin, "Dist_ft", "!Dist_m!*3.28084", "PYTHON_9.3", "")
arcpy.CalculateField_management(NWI_rip_SpatialJoin, "Dist_mi", "!Dist_ft!/5280", "PYTHON_9.3", "")
#NHD
arcpy.AddField_management(NHD_SpatialJoin, "Dist_ft", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(NHD_SpatialJoin, "Dist_mi", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.CalculateField_management(NHD_SpatialJoin, "Dist_ft", "!Dist_m!*3.28084", "PYTHON_9.3", "")
arcpy.CalculateField_management(NHD_SpatialJoin, "Dist_mi", "!Dist_ft!/5280", "PYTHON_9.3", "")
#Land Planning Areas
try:
	arcpy.AddField_management(LandPlanningAreas_SpatialJoin, "Dist_ft", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(LandPlanningAreas_SpatialJoin, "Dist_mi", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
	arcpy.CalculateField_management(LandPlanningAreas_SpatialJoin, "Dist_ft", "!Dist_m!*3.28084", "PYTHON_9.3", "")
	arcpy.CalculateField_management(LandPlanningAreas_SpatialJoin, "Dist_mi", "!Dist_ft!/5280", "PYTHON_9.3", "")
except:
	pass
#CalVeg
try:
	arcpy.AddField_management(CalVeg_SpatialJoin, "Dist_ft", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(CalVeg_SpatialJoin, "Dist_mi", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
	arcpy.CalculateField_management(CalVeg_SpatialJoin, "Dist_ft", "!Dist_m!*3.28084", "PYTHON_9.3", "")
	arcpy.CalculateField_management(CalVeg_SpatialJoin, "Dist_mi", "!Dist_ft!/5280", "PYTHON_9.3", "")
except:
	pass
#CFWO Species
arcpy.AddField_management(CFWO_Spp_SpatialJoin, "Dist_ft", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(CFWO_Spp_SpatialJoin, "Dist_mi", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(CFWO_Spp_SpatialJoin, "OccDateDes", "TEXT", "", "", "255", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.CalculateField_management(CFWO_Spp_SpatialJoin, "Dist_ft", "!Dist_m!*3.28084", "PYTHON_9.3", "")
arcpy.CalculateField_management(CFWO_Spp_SpatialJoin, "Dist_mi", "!Dist_ft!/5280", "PYTHON_9.3", "")

now = datetime.datetime.now()
Start_Time4 = str(now.year) + str(now.month) + str(now.day) +'_'+str(now.hour)+'h' + str(now.minute)+'m' + str(now.second)+'s'

#Process: Export to Excel
try:
	arcpy.TableToExcel_conversion(CritHabPoly_SpatialJoin, CritHabPoly_Excel)
	arcpy.TableToExcel_conversion(CritHabLine_SpatialJoin, CritHabLine_Excel)
except:
	pass
arcpy.TableToExcel_conversion(CNDDB_SpatialJoin, CNDDB_Excel)
arcpy.TableToExcel_conversion(NWI_wet_SpatialJoin, NWI_wet_Excel)
arcpy.TableToExcel_conversion(NWI_rip_SpatialJoin, NWI_rip_Excel)
arcpy.TableToExcel_conversion(NHD_SpatialJoin, NHD_Excel)
try:
	arcpy.TableToExcel_conversion(LandPlanningAreas_SpatialJoin, LandPlanningAreas_Excel)
except:
	pass
#arcpy.TableToExcel_conversion(CalVeg_100ft_Intersect, CalVeg_Excel)
arcpy.TableToExcel_conversion(CFWO_Spp_SpatialJoin, CFWO_Spp_Excel)

#Process - CNDDB symbolize and label prior to kmz output
#Adds layer (feature class) to mxd
try:
  mxd = arcpy.mapping.MapDocument("CURRENT")
  ArcMap = True
  
except:
  mxd = arcpy.mapping.MapDocument(r'L:\Data\GIS\Scripts\Blank_G0131D_mxd_DO_NOT_MOVE.mxd')
  ArcMap = False
  
df = arcpy.mapping.ListDataFrames(mxd)[0]
updateLayer = arcpy.mapping.Layer(CNDDB_SpatialJoin)
sourceLayer = arcpy.mapping.Layer(r'L:\Data\GIS\Scripts\Layer_Files_for_KMZ_Symbology\CNDDB_CName_All_Example.lyr')
arcpy.mapping.UpdateLayer(df, updateLayer, sourceLayer, True)

#if updateLayer.symbologyType == "UNIQUE_VALUES":
	#updateLayer.symbology.valueField = "CNAME"
		#updateLayer.symbology.addAllValues()

updateLayer.showLabels = True
updateLayer.labelClasses[0].expression = "[CNAME]"
arcpy.mapping.AddLayer(df, updateLayer, "BOTTOM")

newLayer = arcpy.mapping.Layer(Buffer_100ft)
arcpy.ApplySymbologyFromLayer_management(newLayer, r'L:\Data\GIS\Scripts\Layer_Files_for_KMZ_Symbology\StudyArea_Boundary_100ft_Buff.lyr')
arcpy.mapping.AddLayer(df, newLayer, "BOTTOM")

#mxd.save()

#Process: Export to KML
tempLayer = os.path.join(GIS_Folder, 'tempLayer.lyr')
try:
	arcpy.MakeFeatureLayer_management(CritHabPoly_SpatialJoin, tempLayer)
	arcpy.LayerToKML_conversion(tempLayer, CritHabPoly_KML)
	arcpy.MakeFeatureLayer_management(CritHabLine_SpatialJoin, tempLayer)
	arcpy.LayerToKML_conversion(tempLayer, CritHabLine_KML)
except:
	pass
	
#if using custom CNDDB layer:
arcpy.MakeFeatureLayer_management(updateLayer, tempLayer)
arcpy.LayerToKML_conversion(updateLayer, CNDDB_KML)

#arcpy.MakeFeatureLayer_management(CNDDB_SpatialJoin, tempLayer)
#arcpy.LayerToKML_conversion(tempLayer, CNDDB_KML)

arcpy.MakeFeatureLayer_management(NWI_wet_SpatialJoin, tempLayer)
arcpy.LayerToKML_conversion(tempLayer, NWI_wet_KML)

arcpy.MakeFeatureLayer_management(NWI_rip_SpatialJoin, tempLayer)
arcpy.LayerToKML_conversion(tempLayer, NWI_rip_KML)

arcpy.MakeFeatureLayer_management(NHD_SpatialJoin, tempLayer)
arcpy.LayerToKML_conversion(tempLayer, NHD_KML)

arcpy.MakeFeatureLayer_management(LandPlanningAreas_SpatialJoin, tempLayer)
arcpy.LayerToKML_conversion(tempLayer, LandPlanningAreas_KML)

#arcpy.MakeFeatureLayer_management(CalVeg_100ft_Intersect, tempLayer)
#arcpy.LayerToKML_conversion(tempLayer, CalVeg_KML)

arcpy.MakeFeatureLayer_management(Buffer_100ft, tempLayer)
arcpy.LayerToKML_conversion(newLayer, StudyArea_100ft_BUFF_KML)

arcpy.MakeFeatureLayer_management(Buffer_3Mile, tempLayer)
arcpy.LayerToKML_conversion(tempLayer, StudyArea_3mi_BUFF_KML)

arcpy.MakeFeatureLayer_management(CFWO_Spp_SpatialJoin, tempLayer)
arcpy.LayerToKML_conversion(tempLayer, CFWO_Spp_KML)




  