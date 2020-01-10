import arcpy
import os
from datetime import datetime

now = datetime.now()
arcpy.AddMessage(now)

arcpy.env.overwriteOutput = True

#INPUTS---------------------
Update_XLS = arcpy.GetParameterAsText(0) # input excel file
Update_CS = "CS_NUM" # Control sheet number heading string
#TAS = r'Q:\SCE\HTRP_DTRP_2016\03_GIS_Data\geodatabases\DRI_EI01_20161230\DRI_MSUP_TAS_COMPLETE_EI01_20191118.gdb\DRI_TAS_COMPLETE2_EI02_20191120v1'#TESTING
TAS = r'Q:\SCE\HTRP_DTRP_2016\03_GIS_Data\geodatabases\DRI_EI01_20161230\DRI_MSUP_TAS_COMPLETE_EI01_20191118.gdb\DRI_TAS_COMPLETE2_EI02_20191120'#live

#OUTPUTS----------------------
Update_TBL = r'Q:\SCE\HTRP_DTRP_2016\03_GIS_Data\geodatabases\DRI_EI01_20161230\scratch\Scratch.gdb\Update_Table'

#CONVERT TO GIS -------------------------
arcpy.ExcelToTable_conversion(Update_XLS, Update_TBL)

#CREATE DICTIONARY MATRIX FROM TABLE-----------------
matrix = []
i = 0

Update_fields = arcpy.ListFields(Update_TBL)[1:]
Update_names = [str(x.name)for x in Update_fields]

with arcpy.da.SearchCursor(Update_TBL, Update_names) as SC:
    for row in SC:
        dict = {}
        for column, name in enumerate(Update_names):
            dict[name] = row[column]  
        matrix.append(dict)
        i+=1

#CREATE CS NUMBERS LIST FROM MATRIX---------------------
CS_Numbers =[]
for x in range(i):
    CS_Numbers.append(str(matrix[x][Update_CS])) 
    
#UPDATE VALUES IN TAS COMPLETE---------------------------------------
TAS_names = Update_names # CS_NUM first!!!!!!!!!!!!! 
field_count = len(TAS_names)

with arcpy.da.UpdateCursor(TAS, TAS_names) as UC:
    for row in UC:
        dict = {}
        if row[0] in CS_Numbers:
            position = CS_Numbers.index(row[0])
            dict = matrix[position]
            for n in range(1,field_count):
                row[n] = dict[TAS_names[n]]
        UC.updateRow(row)

now2 = datetime.now()
arcpy.AddMessage(now2)