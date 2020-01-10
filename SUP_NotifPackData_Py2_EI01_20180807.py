import os
import arcpy
import numpy

#Inputs 
EXCEL_folder  = arcpy.GetParameterAsText(0) # input folder containing excel tables for each forest
Date = arcpy.GetParameter(1) #date string
GDB_folder= arcpy.GetParameterAsText(2) 

#MXD_template =  arcpy.mapping.MapDocument(arcpy.GetParameter(3))
#MXD_folder = arcpy.GetParameter(4) 

#---------------------------------------------------------------------------------------------------------------

#variables

Scale = 4200
SR = arcpy.SpatialReference(4326) #GCS WGS spatial reference (decimal degrees)
SUP_list = ['ANF','CNF','HTNF','INF','LPNF','NPS','SBNF','SNF','SQNF']

Excels = []
Forests =[]
GDBs = []
DB_tables = []
RDs = []

#--------------------------------------------------------------------------------------------------------------------

for roots, folders, files in os.walk(EXCEL_folder):
	for file in files:
		if 'xls' in file.split('.')[-1]:
			Excel = os.path.join(EXCEL_folder, file)
			Excels.append(Excel)
			if '_SCE' in file:
				Forest = file.split('_SCE')[0]
			else:
				Forest = file.split('SCE')[0]
			Forests.append(Forest)
			GDB_result = arcpy.CreateFileGDB_management(GDB_folder, Forest + '_SCETrees_' + Date)
			GDB = str(GDB_result)
			GDBs.append(GDB)
			DB_table = arcpy.ExcelToTable_conversion(Excel,os.path.join(GDB, Forest+'_SCE_TREES_TABLE_' + Date))
			DB_tables.append(DB_table)
			XY_event = arcpy.MakeXYEventLayer_management(DB_table,"X","Y", os.path.join(Forest +'_SCE_TREES_TEMP_' + Date), SR)
			Point_FC = arcpy.CopyFeatures_management(XY_event, os.path.join(GDB, Forest +'_SCE_TREES_BIOLOGY_' + Date))
			#list ranger districts
			#with arcpy.da.SearchCursor(Point_FC,['RANGER_DIST']) as cursor:
					#RDs = sorted({row[0].encode('ascii', 'ignore') for row in cursor})
			#query ranger districts
			
			#make mapbook if necessary
			
			#save mxd for each district
			
#for i in range(len(Excels)):
	#DB_table = arcpy.ExcelToTable_conversion(Excels[i],os.path.join(GDBs[i],Forests[i]+'_SCE_TREES_BIOLOGY_' + Date))
	#DB_tables.append(DB_table)
