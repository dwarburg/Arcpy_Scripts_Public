#Import modules
import arcpy
import os

#input
Points = arcpy.GetParameterAsText(0)
Workspace = arcpy.GetParameterAsText(1)
OutputExcel = arcpy.GetParameterAsText(2)

arcpy.env.workspace = Workspace
arcpy.env.overwriteOutput = True

# Import arcpy module
import arcpy
import os

#Statewide Data
County = arcpy.mapping.Layer(r'L:\Data\GIS\Cal_GIS\1_24000_County.shp')
TownSecRange = arcpy.mapping.Layer(r'L:\Data\GIS\USGS\PLSS\PLSS_Sections.lyr')
Quadrangle = arcpy.mapping.Layer(r'L:\Data\GIS\Cal_GIS\Quad boundaries\mapgrida\mapgrida_utm.shp')
Cities = arcpy.mapping.Layer(r'L:\Data\GIS\Cal_GIS\Incorporated Cities\incorp16_1_shape\incorp16_1.shp')
Ownership = arcpy.mapping.Layer(r'L:\Data\GIS\Cal_GIS\Public lands\All_Agencies\All_public_merge_EI01_20171107.shp')
Air_District = arcpy.mapping.Layer(r'L:\Data\GIS\Air_Resources_Board\Boundaries\CaAirDistrict.shp')
Air_Basin = arcpy.mapping.Layer(r'L:\Data\GIS\Air_Resources_Board\Boundaries\CaAirBasin.shp')
Scenic_Highway = arcpy.mapping.Layer(r'L:\Data\GIS\Caltrans\Elig_and_OffDesignated_Scenic_Hwy\eScenicHwys2014.shp')
Vista_Point = arcpy.mapping.Layer(r'L:\Data\GIS\Caltrans\VistaPoints\Vista2015.shp')
Fire_State = arcpy.mapping.Layer(r'L:\Data\GIS\Fire\Statewide\SRA_FHSZ.lyr')
FMMP_State =  arcpy.mapping.Layer(r'L:\Data\GIS\Farmland\Statewide_FMMP_2014.shp')
FEMA_So_Cal =  arcpy.mapping.Layer(r'L:\Data\GIS\FEMA\All_So_Cal\S_FLD_HAZ_AR_Merged_20181206.shp')
try:
    Fault_Zones = arcpy.mapping.Layer(r'L:\Data\GIS\Geology\ConservationCA_Server\CGS_Earthquake_Hazard_Zones_SHP_Fault_Zones.lyr')
    Landslide_Zones = arcpy.mapping.Layer(r'L:\Data\GIS\Geology\ConservationCA_Server\CGS_Earthquake_Hazard_Zones_SHP_Landslide_Zones.lyr')
    Liquefaction_Zones = arcpy.mapping.Layer(r'L:\Data\GIS\Geology\ConservationCA_Server\CGS_Earthquake_Hazard_Zones_SHP_Liquefaction_Zones.lyr')
    Tsunami = r'L:\Data\GIS\Geology\ConservationCA_Server\CGS.DOC.tsunami_area.lyr'	
except:
    pass


#add layers
mxd = arcpy.mapping.MapDocument('CURRENT')
df = arcpy.mapping.ListDataFrames(mxd)[0]
background = [Cities, County, Quadrangle, TownSecRange, Ownership, Air_District, Air_Basin, Fire_State, Scenic_Highway, Vista_Point, FMMP_State,FEMA_So_Cal]
keep_fields = []
i = 0
fieldmappings = arcpy.FieldMappings()

for index, x in enumerate(background):
    i=i+1
    updateLayer = x
    updateLayer.visible = False
    arcpy.mapping.AddLayer(df, updateLayer, "BOTTOM")
    JoinResult = Workspace + '\SpatialJoin' + str(i)
    fieldmappings.addTable(updateLayer)
    keepers = keep_fields[index] # etc.
    # Remove all output fields you don't want.
    for field in fieldmappings.fields:
        if field.name not in keepers:
            fieldmappings.removeFieldMap(fieldmappings.findFieldMapIndex(field.name))   
    arcpy.SpatialJoin_analysis(Points, updateLayer, JoinResult, "JOIN_ONE_TO_ONE", "KEEP_ALL", fieldmappings, "CLOSEST", "3 Miles", "DISTANCE_M")
    Points = JoinResult

try:
    Conservation_CA_Server = [Fault_Zones, Landslide_Zones, Liquefaction_Zones, Tsunami]
    for y in Conservation_CA_Server:
        i=i+1
        updateLayer = y
        updateLayer.visible = False
        arcpy.mapping.AddLayer(df, updateLayer, "BOTTOM")
        JoinResult = Workspace + '\SpatialJoin' + str(i)
        arcpy.SpatialJoin_analysis(Points, updateLayer, JoinResult, "JOIN_ONE_TO_ONE", "KEEP_ALL", "", "CLOSEST", "3 Miles", "DISTANCE_M")
        Points = JoinResult
except:
    pass

arcpy.TableToExcel_conversion(Points, OutputExcel, True)


