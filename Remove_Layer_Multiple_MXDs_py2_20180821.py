import arcpy
import os

layer_name = arcpy.GetParameterAsText(0)
folder = arcpy.GetParameterAsText(1)

if '.lyr' in layer_name:
	TempLyrFile = os.path.join(folder, layer_name)
else:
	TempLyrFile = os.path.join(folder, layer_name +'.lyr')

arcpy.SaveToLayerFile_management(layer_name, TempLyrFile)

for roots, folders, files in os.walk(folder):
	for file in files:
		if file.split('.')[-1] == 'mxd':
			mxd = arcpy.mapping.MapDocument(os.path.join(roots,file))
			for df in arcpy.mapping.ListDataFrames(mxd):
				layers = arcpy.mapping.ListLayers(mxd, "*", df)
				for layer in layers:
  					if layer.name == layer_name:
						RemoveLyr = arcpy.mapping.Layer(TempLyrFile)
    						arcpy.mapping.RemoveLayer(df, RemoveLyr)
			arcpy.RefreshTOC()
			arcpy.RefreshActiveView()
			mxd.save()
			
os.remove(TempLyrFile)