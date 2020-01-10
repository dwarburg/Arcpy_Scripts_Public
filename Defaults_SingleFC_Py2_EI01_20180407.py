import arcpy

FC = arcpy.GetParameterAsText(0)

defaults = []
field_names = []
fields = arcpy.ListFields(FC)

for field in fields:
  defaults.append(format(field.defaultValue))
  field_names.append(field.name)

with arcpy.da.UpdateCursor(FC, field_names) as UC:
  for row in UC:
     for i in range(0, len(row)):
        if row[i] is None and defaults[i] <> 'None':
           row[i] = defaults[i]

     UC.updateRow(row)

