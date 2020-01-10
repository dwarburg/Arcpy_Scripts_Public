import os
import arcpy
import datetime
import re

#starting variables
WORK_table = arcpy.GetParameterAsText(0)
TAS_complete =  r'Q:\SCE\HTRP_DTRP_2016\03_GIS_Data\geodatabases\DRI_EI01_20161230\DRI_EI01_20161230.gdb\DRI_TAS_Complete\DRI_TAS_Complete_EI02_20170208'
TAS_MSUP = r'Q:\SCE\HTRP_DTRP_2016\03_GIS_Data\geodatabases\DRI_EI01_20161230\DRI_MSUP_TAS_COMPLETE_EI01_20191118.gdb\DRI_TAS_COMPLETE2_EI02_20191120'
CS_field = arcpy.GetParameterAsText(1)
OUTPUT_folder = arcpy.GetParameterAsText(2)
workday = datetime.datetime.now() + datetime.timedelta(days=1)
OUTPUT_excel = OUTPUT_folder + "\WorkPlan_Check_" + workday.strftime("%Y%m%d") + ".xls"
OUTPUT_excel_MSUP = OUTPUT_folder + "\WorkPlan_Check_MSUP_" + workday.strftime("%Y%m%d") + ".xls"
Schema_table = r'Q:\SCE\HTRP_DTRP_2016\03_GIS_Data\geodatabases\WorkPlan_Checks\WorkPlan_Checks_EI01_20180621.gdb\WorkPlan_Check_Blank_Schema_EI03_20180705'
keep_list = [u'OBJECTID', u'Shape', u'Notes', u'Date', u'Crew', u'Ranger_District', u'CS_GRID', u'Arch_Monitor', u'TREE_SPC', u'Address', u'X', u'Y', u'CS_NUM', u'Owner_Status', u'SCE_District', u'SCE_Circuit_Name', u'CNDDB', u'Critical_Habitat', u'USFS_Data', u'SMZ', u'Riparian_Vegetation', u'Wetland_Waters', u'Monitor_Needed', u'Comments', u'Surveyor', u'Survey_Date', u'Notes_1', u'QAQC_Date', u'USFS_Approved', u'SUP_NUM', 'CS_Prime']
keep_list_MSUP = ['CS_NUM', 'HTMP_CN', 'GRID', 'ADDRESS', 'MSUP_NUM', 'OWNERSHIP', 'SCE_DISTRICT', 'CIRCUIT', 'TREE_DBH', 'TREE_HEIGHT', 'TREE_SPS', 'ACCESS', 'Y', 'X', 'UTS_BIO_MONITOR', 'UTS_BIO_COMMENTS', 'UTS_WATER_MONITOR', 'UTS_WATER_COMMENTS', 'BIO_REVIEW', 'BIO_RPM', 'WATER_REVIEW', 'WATER_RPM', 'ASSIGNMENT_WEEK', 'M_BIO_Y_N', 'M_WW_Y_N', 'M_ARCH_Y_N', 'USFS_NOTES', 'CS_PRIME', 'MSUP_NonMSUP_Approval', 'NOTES']
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)[0]

#set  workspace
cwd =r'Q:\SCE\HTRP_DTRP_2016\03_GIS_Data\geodatabases\WorkPlan_Checks\WorkPlan_Checks_EI01_20180621.gdb'
arcpy.env.workspace = cwd
arcpy.env.overwriteOutput = True
arcpy.env.qualifiedFieldNames = False

#convert excel table and add integer field of CS number
tbl_name =   'To_Check_' + workday.strftime("%Y%m%d")
db_tbl_path =  cwd + '\\' + tbl_name
arcpy.ExcelToTable_conversion(WORK_table, db_tbl_path )
arcpy.AddField_management(db_tbl_path,'CS_int',"LONG")
with arcpy.da.UpdateCursor(db_tbl_path,[CS_field, 'CS_int']) as UC:
	for row in UC:
		if row[0] is str:
			row[1] = int(filter(lambda x: x in '0123456789', row[0]))
		else:
			row[1] = int(row[0])
		UC.updateRow(row)

#create table view of database table and hide unneeded fields
Check_Table_View = arcpy.mapping.TableView(db_tbl_path)
fieldInfo = ""  
fieldList = arcpy.ListFields(db_tbl_path)
for field in fieldList:  
    if field.name in ['CS_int', "Crew", "Date"] :  
        fieldInfo = fieldInfo + field.name + " " + field.name + " VISIBLE;"  
    else:  
        fieldInfo = fieldInfo + field.name + " " + field.name + " HIDDEN;"  
arcpy.MakeTableView_management(db_tbl_path, tbl_name, "", "", fieldInfo)

#create layer of TAS complete and hide unneeded fields
TASlayerName = "TAS_Complete_Layer"
fieldInfo2= ""  
fieldList = arcpy.ListFields(TAS_complete)
for field in fieldList:  
    if field.name in keep_list: 
        fieldInfo2 = fieldInfo2 + field.name + " " + field.name + " VISIBLE;"  
    else:  
        fieldInfo2 = fieldInfo2 + field.name + " " + field.name + " HIDDEN;"  
arcpy.MakeFeatureLayer_management(TAS_complete, TASlayerName, "", "", fieldInfo2)

#create layer of TAS MSUP and hide unneeded fields
TASlayerName_MSUP = "TAS_MSUP_Layer"
fieldInfo3= ""  
fieldList = arcpy.ListFields(TAS_MSUP)
for field in fieldList:  
    if field.name in keep_list_MSUP: 
        fieldInfo3 = fieldInfo3 + field.name + " " + field.name + " VISIBLE;"  
    else:  
        fieldInfo3 = fieldInfo3 + field.name + " " + field.name + " HIDDEN;"  
arcpy.MakeFeatureLayer_management(TAS_MSUP, TASlayerName_MSUP, "", "", fieldInfo3)

#join
arcpy.AddJoin_management(TASlayerName, 'CS_Prime', Check_Table_View, 'CS_int','KEEP_COMMON')
arcpy.AddJoin_management(TASlayerName_MSUP, 'CS_PRIME', Check_Table_View, 'CS_int','KEEP_COMMON')

#copy to scratch FC
joined_table = cwd + '\joined_TAS_table_' + workday.strftime("%Y%m%d")
joined_table_MSUP = cwd + '\joined_TAS_table_MSUP' + workday.strftime("%Y%m%d")
arcpy.CopyFeatures_management (TASlayerName, joined_table)
arcpy.CopyFeatures_management (TASlayerName_MSUP, joined_table_MSUP)

#create TAS complete table based on blank schema with fields in correct order, create Ref Number field and then delete extra fields
WorkPlan_table = cwd + '\WorkPlan_' + workday.strftime("%Y%m%d")
arcpy.Merge_management([Schema_table, joined_table], WorkPlan_table)
fieldList = arcpy.ListFields(WorkPlan_table)
with arcpy.da.UpdateCursor(WorkPlan_table,['CS_Prime', 'Ref_Num']) as UC:
	for row in UC:
		row[1] =row[0]
		UC.updateRow(row)
for field in fieldList:
	if fieldList.index(field) > 30:
		arcpy.DeleteField_management(WorkPlan_table, field.name)

#export to excel
arcpy.TableToExcel_conversion(WorkPlan_table, OUTPUT_excel)
arcpy.TableToExcel_conversion(joined_table_MSUP, OUTPUT_excel_MSUP)