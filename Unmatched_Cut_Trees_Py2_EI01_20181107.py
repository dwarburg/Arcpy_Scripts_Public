import arcpy
import os

tbl_Unmatched = arcpy.GetParameterAsText(0)

tbl_TAS_Complete =r'Q:\SCE\HTRP_DTRP_2016\03_GIS_Data\geodatabases\DRI_EI01_20161230\DRI_EI01_20161230.gdb\DRI_TAS_Complete\DRI_TAS_Complete_EI02_20170208'
fields = arcpy.ListFields(tbl_TAS_Complete)

str_Primary_field = arcpy.GetParameterAsText(1)

tbl_Output_FC = arcpy.GetParameterAsText(2)

CS_str_list = []
CS_int_list = []

with arcpy.da.SearchCursor(tbl_Unmatched, [str_Primary_field]) as SC:
	for row in SC:
		CS_str_list.append(str(row[0]))
		try:
			CS_int_list.append(int(row[0]))
		except:
			pass

OID_list = []

#fields = arcpy.ListFields(tbl_TAS_Complete)
field_names = ['OBJECTID','CS_NUM','CS_PRIME','Notes','Address']
#for x in fields:
	#if x.type in [u'String', u'Integer']:
		#field_names.append(x.name)

with arcpy.da.SearchCursor(tbl_TAS_Complete, field_names) as SC:
	for row in SC:
		for n in row[1:]:
			if n in CS_str_list or n in CS_int_list:
				OID_list.append(row[0])
				
Tree_Count = len(OID_list)
if  Tree_Count == 0:
	arcpy.AddMessage('NO TREES FOUND')
else:
	sql = "{} IN ({})".format("OBJECTID", ", ".join([str(y) for y in OID_list]))
	arcpy.Select_analysis(tbl_TAS_Complete, tbl_Output_FC, sql )
	arcpy.AddMessage(Tree_Count + ' TREES FOUND')				
				
	
	

	