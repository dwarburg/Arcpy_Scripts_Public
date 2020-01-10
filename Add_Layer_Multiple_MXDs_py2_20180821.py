import arcpy
import os

Lyr = arcpy.GetParameterAsText(0)
folder = arcpy.GetParameterAsText(1)

if '.lyr' in Lyr:
	TempLyrFile = os.path.join(folder, Lyr)
else:
	TempLyrFile = os.path.join(folder, Lyr+'.lyr')

arcpy.SaveToLayerFile_management(Lyr, TempLyrFile)

for roots, folders, files in os.walk(folder):
	for file in files:
		if file.split('.')[-1] == 'mxd':
			mxd = arcpy.mapping.MapDocument(os.path.join(roots,file))
			for df in arcpy.mapping.ListDataFrames(mxd):
				addLayer = arcpy.mapping.Layer(TempLyrFile)
				arcpy.mapping.AddLayer(df, addLayer)
			arcpy.RefreshTOC()
			arcpy.RefreshActiveView()
			mxd.save()
			
os.remove(TempLyrFile)