import arcpy
import os
from datetime import datetime
arcpy.env.overwriteOutput = True

#CREATE DATE STRING FOR LABELS
now = datetime.now()
year = str(now.date().year)
month = str(now.date().month)
if len(month) == 1:
    month = '0' + month
day = str(now.date().day)
if len(day) == 1:
    day = '0' + day

Date_STR = year + month + day

#INPUTS---------------------
Append_XLS = arcpy.GetParameterAsText(0) # input excel file
Append_CS = "CS_NUM" # Control sheet number heading string
#TAS = r'Q:\SCE\HTRP_DTRP_2016\03_GIS_Data\geodatabases\DRI_EI01_20161230\DRI_MSUP_TAS_COMPLETE_EI01_20191118.gdb\DRI_TAS_COMPLETE2_EI02_20191120v1'#TESTING
TAS = r'Q:\SCE\HTRP_DTRP_2016\03_GIS_Data\geodatabases\DRI_EI01_20161230\DRI_MSUP_TAS_COMPLETE_EI01_20191118.gdb\DRI_TAS_COMPLETE2_EI02_20191120'#live

#OUTPUTS----------------------
Append_TBL = r'Q:\SCE\HTRP_DTRP_2016\03_GIS_Data\geodatabases\DRI_EI01_20161230\DRI_MSUP_TAS_APPENDS_EI01_20200109.gdb\DRI_MSUP_TAS_Append_TBL_' + Date_STR
Append_FC = r'Q:\SCE\HTRP_DTRP_2016\03_GIS_Data\geodatabases\DRI_EI01_20161230\DRI_MSUP_TAS_APPENDS_EI01_20200109.gdb\DRI_MSUP_TAS_Append_ALL_' + Date_STR
Append_FC2 = r'Q:\SCE\HTRP_DTRP_2016\03_GIS_Data\geodatabases\DRI_EI01_20161230\DRI_MSUP_TAS_APPENDS_EI01_20200109.gdb\DRI_MSUP_TAS_Append_DUPL_REMOVED_' + Date_STR
Duplicates_FC = r'Q:\SCE\HTRP_DTRP_2016\03_GIS_Data\geodatabases\DRI_EI01_20161230\DRI_MSUP_TAS_APPENDS_EI01_20200109.gdb\DRI_MSUP_TAS_Duplicates_' + Date_STR

#CONVERT TO GIS -------------------------
#Arcpy Task 1
arcpy.ExcelToTable_conversion(Append_XLS, Append_TBL)

#DISPLAY XY DATA-----------------------------------------
SR = arcpy.SpatialReference('WGS 1984')
#Arcpy Task 2
arcpy.MakeXYEventLayer_management(Append_TBL, "X", "Y", "XY_Layer", SR)

#PROJECT INTO NAD 1983 2011 CA TEALE ALBERS (METERS)-------------------------
SR2 = arcpy.SpatialReference(102962)
#Arcpy Task 3
arcpy.Project_management("XY_Layer", Append_FC, SR2)

#EXPORT FC OF DUPLICATES------------
CS_List = []
with arcpy.da.SearchCursor(Append_TBL, ["CS_NUM"]) as SC:
    for row in SC:
        CS_List.append(str(row[0]))
CS_STR = str(CS_List).replace('[','(').replace(']',')')
SQL = "CS_NUM IN " + CS_STR
#Arcpy Task 4
arcpy.Select_analysis(TAS, Duplicates_FC, SQL)

#EXPORT FC OF NON-DUPLICATES---------------------------------------
CS_Dupl = []
with arcpy.da.SearchCursor(Duplicates_FC, ["CS_NUM"]) as SC:
    for row in SC:
        CS_Dupl.append(str(row[0]))
Dupl_Count = len(CS_Dupl)
message1 = str(Dupl_Count) + " Duplicates Found"
arcpy.AddMessage(message1)
if Dupl_Count <> 0:
    CS_Dupl_STR = str(CS_Dupl).replace('[','(').replace(']',')')
    SQL2 = "CS_NUM NOT IN " + CS_Dupl_STR
    #Arcpy Task 5
    arcpy.Select_analysis(Append_FC, Append_FC2, SQL2)
else:
    #Arcpy Task 5
    arcpy.CopyFeatures_management(Append_FC, Append_FC2)

#APPEND TO TAS COMPLETE----------------------------------------------
#Arcpy Task 6
arcpy.Append_management(Append_FC2, TAS, "NO_TEST")

#END MESSAGE-------------------------------------
now2 = datetime.now()
message2 = str((now2-now)/len(CS_List)) + " Seconds Per Tree"
arcpy.AddMessage(message2)