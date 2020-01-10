import arcpy
import os

excel_cut = arcpy.GetParameterAsText(0)

tbl_TAS_Complete =r'Q:\SCE\HTRP_DTRP_2016\03_GIS_Data\geodatabases\DRI_EI01_20161230\DRI_EI01_20161230.gdb\DRI_TAS_Complete\DRI_TAS_Complete_EI02_20170208'
fields = arcpy.ListFields(tbl_TAS_Complete)

GDB_output =  arcpy.GetParameterAsText(1)

tbl_cut = os.path.join(GDB_output, 'CutTrees'+Date_str)

arcpy.ExcelToTable_conversion(excel_cut, tbl_cut)

date_str = arcpy.GetParameterAsText(2)

str_Primary_field = arcpy.ListFields(tbl_cut)[1].name

tbl_Output_FC = os.path.join(GDB_output,'UnmatchedTrees'+date_str)

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
			(if n in CS_str_list) or (if n in CS_int_list):
				OID_list.append(row[0])

if len(OID_list) ==0:
	quit()

sql = "{} IN ({})".format("OBJECTID", ", ".join([str(y) for y in OID_list]))

arcpy.Select_analysis(tbl_TAS_Complete, tbl_Output_FC, sql )
				
				
	
	

	