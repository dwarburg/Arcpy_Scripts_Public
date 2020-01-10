import os
import arcpy

ws = arcpy.GetParameterAsText(0)

arcpy.env.workspace = ws 

mxd_list = arcpy.ListFiles("*.mxd")

ddp_list = []
single_list = []

for mxd in mxd_list:
    current_mxd = arcpy.mapping.MapDocument(os.path.join(ws, mxd))
    if current_mxd.isDDPEnabled:
        ddp_list.append(mxd)
    else:
        single_list.append(mxd)

for mxd in single_list:
    current_mxd = arcpy.mapping.MapDocument(os.path.join(ws, mxd))
    pdf_name = mxd[:-4] + ".pdf"    
    arcpy.mapping.ExportToPDF(current_mxd, pdf_name)

for mxd in ddp_list:
    current_mxd = arcpy.mapping.MapDocument(os.path.join(ws, mxd))
    pdf_name = mxd[:-4] + ".pdf"    
    ddp = current_mxd.dataDrivenPages 
    ddp.exportToPDF(pdf_name, "ALL")
    
del mxd_list	
