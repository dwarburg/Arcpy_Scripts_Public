import os
import arcpy

ws = arcpy.GetParameterAsText(0)

arcpy.env.workspace = ws 

mxd_list = arcpy.ListFiles("*.mxd")

for mxd in mxd_list:
    
    current_mxd = arcpy.mapping.MapDocument(os.path.join(ws, mxd))
    pdf_name = mxd[:-4] + ".pdf"
    arcpy.mapping.ExportToPDF(current_mxd, pdf_name)
 
del mxd_list	
