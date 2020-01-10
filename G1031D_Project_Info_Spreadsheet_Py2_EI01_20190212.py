# Import arcpy module
import arcpy
import os
import datetime
import getpass

arcpy.env.overwriteOutput = True

now = datetime.datetime.now()
Start_Time = str(now.year) + str(now.month) + str(now.day) +'_'+str(now.hour)+'h' + str(now.minute)+'m' + str(now.second)+'s'

# User Entry Variables:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Project_Location = arcpy.GetParameterAsText(0) 
Geometry_Type = arcpy.GetParameterAsText(1)
GDB = arcpy.GetParameterAsText(2)
tbl_XLS_Output = arcpy.GetParameterAsText(3)

# Constants--------------------------------------------------------------    
EI_Version = "01" #Use two digits
tbl_CSV_Input_1 = r'L:\Data\GIS\Scripts\Useful_Code\Project_Info_Template_Sheet1_DO_NOT_MOVE.csv'
    
#ExportPaths----------------------------------------------------

GDB_folder = os.path.join(GIS_Folder, 'geodatabases')
GDB = arcpy.CreateFileGDB_management (GDB_folder,  EI_Date[:-8] + 'Working_EI01_'+ EI_Date[-8:] +'.gdb')

UTM_11 = arcpy.SpatialReference('NAD 1983 UTM Zone 11N')

Background_Dataset = arcpy.CreateFeatureDataset_management (GDB, 'Background', UTM_11)
Background_Dataset_Path = str(Background_Dataset)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#intersection background data
County = r'L:\Data\GIS\Cal_GIS\1_24000_County.shp'
TownSecRange = r'L:\Data\GIS\USGS\PLSS\PLSS_Sections.lyr'
Quadrangle = r'L:\Data\GIS\Cal_GIS\Quad boundaries\mapgrida\mapgrida_utm.shp'
Cities = r'L:\Data\GIS\Cal_GIS\Incorporated Cities\incorp16_1_shape\incorp16_1.shp'
Ownership = r'L:\Data\GIS\BLM\LandStatus_v10.gdb\LndSurfaceEstate_SMA'
Air_District = r'L:\Data\GIS\Air_Resources_Board\Boundaries\CaAirDistrict.shp'
Air_Basin = r'L:\Data\GIS\Air_Resources_Board\Boundaries\CaAirBasin.shp'
Fire_State = r'L:\Data\GIS\Fire\Statewide\Statewide_FHSZ_All_RAs.lyr'
FMMP_State =  r'L:\Data\GIS\Farmland\Statewide_FMMP_2014.shp'
FEMA_So_Cal =  r'L:\Data\GIS\FEMA\All_So_Cal\S_FLD_HAZ_AR_Merged_20181206.shp'

background = [Cities, County, Quadrangle, TownSecRange, Ownership, Air_District, Air_Basin, Fire_State, FMMP_State, FEMA_So_Cal]
background_strs = ['Cities', 'County', 'Quadrangle', 'TownSecRange', 'Ownership', 'Air_District', 'Air_Basin', 'Fire_State', 'FMMP_State', 'FEMA_So_Cal']

#proximity background data
Scenic_Highway = r'L:\Data\GIS\Caltrans\Elig_and_OffDesignated_Scenic_Hwy\eScenicHwys2014.shp'
Vista_Point = r'L:\Data\GIS\Caltrans\VistaPoints\Vista2015.shp'

proximity = [Scenic_Highway, Vista_Point]
proximity_strs = ['Scenic_Highway', 'Vista_Point']

#conservation CA online data
try:
    Fault_Traces = r'L:\Data\GIS\Geology\ConservationCA_Server\CGS_Earthquake_Hazard_Zones_SHP_Fault_Traces.lyr'
    Fault_Zones = r'L:\Data\GIS\Geology\ConservationCA_Server\CGS_Earthquake_Hazard_Zones_SHP_Fault_Zones.lyr'
    Landslide_Zones = r'L:\Data\GIS\Geology\ConservationCA_Server\CGS_Earthquake_Hazard_Zones_SHP_Landslide_Zones.lyr'
    Liquefaction_Zones = r'L:\Data\GIS\Geology\ConservationCA_Server\CGS_Earthquake_Hazard_Zones_SHP_Liquefaction_Zones.lyr'
    Tsunami = r'L:\Data\GIS\Geology\ConservationCA_Server\CGS.DOC.tsunami_area.lyr'	
except:
    pass

Cons_CA_Server = [Fault_Traces, Fault_Zones, Landslide_Zones, Liquefaction_Zones, Tsunami]
Cons_CA_Server_strs = ['Fault_Traces', 'Fault_Zones', 'Landslide_Zones', 'Liquefaction_Zones', 'Tsunami']
    
#-----------------------------------------------------------------------------------------------------------------------
#Body

if Geometry_Type == "Points":
    #
elif Geometry_Type == "Polygons":
    #
else:
    #

for index, item in enumerate(background):
  arcpy.Intersect_analysis([Project_Location, item] , os.path.join(Background_Dataset_Path, background_strs[index]))

for index, item in enumerate(proximity):
  arcpy.SpatialJoin_analysis(Project_Location, item, os.path.join(Background_Dataset_Path, proximity_strs[index]) "JOIN_ONE_TO_ONE", "KEEP_COMMON","","CLOSEST")