import arcpy, os, sys
arcpy.env.overwriteOutput = True

#unique value function to be used later
def unique_values(table, field):
   with arcpy.da.SearchCursor(table, [field]) as cursor:
      return sorted({row[0] for row in cursor})
   
#inputs
input_parameter = arcpy.GetParameterAsText(0)
direct = arcpy.GetParameterAsText(2)
coord_sys = arcpy.GetParameter(1)
e_count = 0

#convert kml with standard arcpy tool and list feature classes    
arcpy.conversion.KMLToLayer(input_parameter, direct)    
database = os.path.join(direct, os.path.basename(input_parameter)[:-3] + 'gdb')
raw_dataset = database + '\Placemarks'
arcpy.env.workspace = raw_dataset
GCS_List = arcpy.ListFeatureClasses()

#Create new Datasets
arcpy.CreateFeatureDataset_management(database, "Processing", coord_sys)
arcpy.CreateFeatureDataset_management(database, "Results", coord_sys)
projected_dataset = database + '\Processing'
results_dataset = database + '\Results'

#project into new Coord_System and list new feature classes
for FC in GCS_List:
   arcpy.Project_management(FC, os.path.join(projected_dataset, FC + '_Projected'), coord_sys)
arcpy.env.workspace = projected_dataset
UTM_List = arcpy.ListFeatureClasses()

#add projected FCs to mxd
for FC in UTM_List:
   try:
      mxd = arcpy.mapping.MapDocument('CURRENT')
   except:
      mxd = arcpy.mapping.MapDocument(r'L:\Data\GIS\Scripts\Blank_G0131D_mxd_DO_NOT_MOVE.mxd')
   df = arcpy.mapping.ListDataFrames(mxd)[0]
   processing_layer = arcpy.mapping.Layer(database + '\\' + FC)
   arcpy.mapping.AddLayer(df, processing_layer)

   #split into feature classes for each folder in kmz
   FolderPaths = unique_values(database + '\\' + FC, 'FolderPath')
   for item in FolderPaths:
      sql = "{field} = '{val}'".format(field='FolderPath', val=item)
      arcpy.SelectLayerByAttribute_management(processing_layer, "NEW_SELECTION", sql )
      results_FC = results_dataset + '\\' + item.split("/")[-1].replace(' ', '_').replace('-','_').replace('(','_').replace(')','_').replace('.','_').replace('\n','_')
      if not results_FC[0].isalpha():
         results_FC = 'fc_' + results_FC
      arcpy.CopyFeatures_management(processing_layer, results_FC)
      results_layer = arcpy.mapping.Layer(results_FC)
      arcpy.mapping.AddLayer(df, results_layer)
      
      #convert popupinfo field into a list of field names and values
      with arcpy.da.SearchCursor(results_FC,"PopupInfo") as SC:
         values_2D = []
         for row in SC:
            pop_array = row[0].split("<")
            strings = []
            for item in pop_array:
               if "td>" in item and "/td>" not in item:
                  strings.append(item)
            strings = strings[2:]
            for index, item in enumerate(strings):
               strings[index] = item.replace(u"\u2018", "'").replace(u"\u2019", "'") #replaces un-decipherable unicode characters (left and right quotes)
               strings[index] = strings[index].encode('ascii') #converts unicode string into normal ascii letters
               strings[index] = strings[index].replace('td>', '').replace('\n','_') #replaces tags and line breaks
            names = strings[::2]
            for index, item in enumerate(names):
               names[index] = names[index].replace(' ', '_').replace('-','_').replace('(','_').replace(')','_').replace('.','_')#replaces illegal characters for field names
            values = strings[1::2]
            values_2D.append(values)

      #add fields (all fields are text to simplify)
      #indexing here gets convoluted because any field that already exists needs to be deleted from values_2D list (a matrix)
      #and the fields list, but deleting items in the list while looping through it creates problems
      delete_indexes = []      
      for index, item in enumerate(names):
         try:
            arcpy.AddField_management(results_FC, item, "TEXT", field_length=250)
         except:
            delete_indexes.append(index)
      delete_indexes.reverse() #this is necessary so that columns are deleted right to left, otherwise indexes change with each deletion
      for x in delete_indexes:
         del names[x]
         for row in values_2D:
            del row[x]
   
      #update with correct values       
      with arcpy.da.UpdateCursor(results_FC, names) as UC:
         for row_index, row in enumerate(UC):
            for field_index, item in enumerate(row):
               row[field_index] = values_2D[row_index][field_index]
            UC.updateRow(row)
            
      #delete unnecessary fields
      del_fields = ['AltMode', 'Base', 'Snippet','HasLabel','LabelID','Clamped','Extruded']
      for item in del_fields:
         arcpy.DeleteField_management (results_FC, item)

#remove processing layers
for lyr in arcpy.mapping.ListLayers(mxd, "", df):
   if lyr.name.split('_')[-1] == "Projected":
         arcpy.mapping.RemoveLayer(df, lyr)

#find and remove problematic feature class names by appending to other FC's or renaming
arcpy.env.workspace = results_dataset
for FC in arcpy.ListFeatureClasses():
   Append = False
   Rename = False
   with arcpy.da.SearchCursor(FC, ['Name', 'FolderPath']) as SC:
      row = next(SC)
      Slash_Count = row[0].count('/')
      if Slash_Count <> 0:
         FC_correct_name = results_dataset + '\\' + row[1].split("/")[-1-Slash_Count].replace(' ','_')
         if arcpy.Exists(FC_correct_name):
            Append = True
         else:
            Rename = True
   if Append:
      arcpy.Append_management(FC, FC_correct_name)
      arcpy.Delete_management(FC)
   if Rename:
      arcpy.Rename_management(FC, FC_correct_name)

