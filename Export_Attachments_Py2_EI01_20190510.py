import arcpy
from arcpy import da
import os

inTable = arcpy.GetParameterAsText(0)
fileLocation = arcpy.GetParameterAsText(1)
name_field = arcpy.GetParameterAsText(2) 

with da.SearchCursor(inTable, ['DATA', name_field, 'ATTACHMENTID']) as cursor:
    for item in cursor:
        attachment = item[0]
        filename = item[1]
        open(fileLocation + os.sep + filename, 'wb').write(attachment.tobytes())
        del item
        del filename
        del attachment