import os
import zipfile
import arcpy
import itertools

#geodatabase
if arcpy.GetParameterAsText(0) and arcpy.GetParameterAsText(0) <> "#":
	path = arcpy.GetParameterAsText(0)
	parent_folder = os.path.dirname(path)
	name = os.path.basename(path)
	if '.gdb' in name:
		name = name[:-4]
	contents = os.walk(path)
	i = 0

#shapefile	
elif '.shp' in arcpy.GetParameterAsText(1):
	path = arcpy.GetParameterAsText(1)
	parent_folder = os.path.dirname(path)
	name = os.path.basename(path[:-4])
	contents = os.walk(parent_folder)
	i = 1

zf = zipfile.ZipFile(parent_folder + '\\' + name + '.zip', 'w', zipfile.ZIP_DEFLATED)

for root, folders, files in contents:
        # Include all subfolders, including empty ones.
    for folder_name in folders:
        absolute_path = os.path.join(root, folder_name)
        relative_path = absolute_path.replace(parent_folder + '\\',
                                              '')
        if i == 0 or name in absolute_path:
        		zf.write(absolute_path, relative_path)
				
    for file_name in files:
        absolute_path = os.path.join(root, file_name)
        relative_path = absolute_path.replace(parent_folder + '\\',
        										  '')
		#extra stuff in if statement prevents redundant writing of zipfile within itself for shapefiles
		#because for shapefiles os.walk goes through the parent folder where zf has been created
        if i == 0 and '.zip' not in absolute_path or name in absolute_path and '.zip' not in absolute_path:
        		zf.write(absolute_path, relative_path)                                      
		
zf.close()
	
