import arcpy, os

#inputs
FC_in = arcpy.GetParameterAsText(0)
Unit = arcpy.GetParameterAsText(1)
County = arcpy.GetParameterAsText(2)
GDB = arcpy.GetParameterAsText(3)
CNDDB = r'L:\Data\GIS\CDFW\CNDDB\Shapefiles\cnddb.shp'
CCH_gdb =  r'L:\Data\GIS\CCH\CCH_Records_EI01_20161026.gdb'

#choose CCH feature class based on County
arcpy.env.workspace = CCH_gdb
CCH_list = arcpy.ListFeatureClasses()
for x in CCH_list:
	if County in x.encode() and x <> u'CCH_Kern_CNPS_25YRS_FC_20170516':
		CCH = os.path.join(CCH_gdb, x.encode())
#other way possible using dictionary
#Dict =  {"Orange" : r'L:\Data\GIS\CCH\CCH_Records_EI01_20161026.gdb\CCH_OrangeCo_EI01_20180111', "Tulare" : r'L:\Data\GIS\CCH\CCH_Records_EI01_20161026.gdb\CCH_Records_FC_Tulare_EI01_20180327'}

arcpy.env.workspace = GDB
arcpy.env.overwriteOutput = True

#Buffer
Buffer_FC = os.path.join(GDB,'BUFF_' + Unit.split(' ')[0] + '_' + Unit.split(' ')[1] + '_' + os.path.basename(FC_in))
arcpy.Buffer_analysis(FC_in, Buffer_FC,Unit)

#Clips
CNDDB_FC =os.path.join(GDB, "CNDDB_" + Unit.split(' ')[0] + '_' + Unit.split(' ')[1] + '_' + os.path.basename(FC_in))
arcpy.Clip_analysis(CNDDB, Buffer_FC, CNDDB_FC)
CCH_FC = os.path.join(GDB, "CCH_" + Unit.split(' ')[0] + '_' + Unit.split(' ')[1] + '_' + os.path.basename(FC_in))
arcpy.Clip_analysis(CCH,Buffer_FC,CCH_FC)

#add layers to display
mxd = arcpy.mapping.MapDocument("CURRENT")
dataFrame = arcpy.mapping.ListDataFrames(mxd, "*")[0] 
CNDDBLayer = arcpy.mapping.Layer(CNDDB_FC)
CCHLayer = arcpy.mapping.Layer(CCH_FC)
arcpy.mapping.AddLayer(dataFrame, CNDDBLayer)
arcpy.mapping.AddLayer(dataFrame, CCHLayer)
