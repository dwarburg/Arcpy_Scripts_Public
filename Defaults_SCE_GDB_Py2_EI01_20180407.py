import arcpy

#geodatabase
arcpy.env.workspace = arcpy.GetParameterAsText(0)

#project name
Proj_name = arcpy.GetParameterAsText(1)

#project type
Proj_type = arcpy.GetParameterAsText(2)

Proj_name_split = Proj_name.split(' ')
Proj_name_abbrev = ''
for word in Proj_name_split:
	Proj_name_abbrev = Proj_name_abbrev + word[0]


FC_List = arcpy.ListFeatureClasses()

for FC in FC_List:

	fields = arcpy.ListFields(FC)
	field_names = []
	defaults = []
	FC_name_split = str(FC).split("_")
	FC_name_abbrev = ""
   	
	for word in FC_name_split: 
		FC_name_abbrev = FC_name_abbrev + word[0:5] + '-' 	

	for field in fields:
		field_names.append(field.name)
		defaults.append(format(field.defaultValue))
		
	with arcpy.da.UpdateCursor(FC, field_names) as UC:
		for row in UC:
			leading_zeros = 4-len(str(row[0]))
			row[2] = Proj_name_abbrev + '-' + FC_name_abbrev + '0' * leading_zeros +str(row[0])
			for i in range(0, len(row)):
				if fields[i].name == 'PROJ_NM':
					row[i] = Proj_name	
				elif fields[i].name == 'PROJ_TYPE' and len(Proj_type) > 1:
					row[i] = Proj_type
				elif row[i] is None and defaults[i] <> 'None':
					row[i] = defaults[i]
			UC.updateRow(row)
   
