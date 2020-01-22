import arcpy
from datetime import datetime

#function that joins a join_fc to target_fc with proper field mapping
def SpatJoin_1to1_Intersect(Out_Field, Join_Fields_list, fc_target, fc_join, out_fc):

    # Create a new fieldmappings object including field maps for all columns in fc_target
    fieldmappings = arcpy.FieldMappings()
    fieldmappings.addTable(fc_target)

    # remove Join_Count and TARGET_FID from field mappings
    list = [x.name for x in fieldmappings.fields]
    if u'Join_Count' in list:
        fieldmappings.removeFieldMap(list.index(u'Join_Count'))
        list.remove(u'Join_Count')
    if u'TARGET_FID' in list:
        fieldmappings.removeFieldMap(list.index(u'TARGET_FID'))

    # Create field map for the new column that gets added by spatial join.
    FieldMap = arcpy.FieldMap()
    # Set input fields from fc_join
    for x in Join_Fields_list:
        FieldMap.addInputField(fc_join, x)
    # Edit output field properties
    field = FieldMap.outputField #get field with current properties
    field.name = Out_Field
    field.aliasName = Out_Field
    FieldMap.outputField = field #overwrite field with editted properties

    # Add field map to field mappings.
    fieldmappings.addFieldMap(FieldMap)

    # Run the Spatial Join tool.
    arcpy.SpatialJoin_analysis(fc_target, fc_join, out_fc,"JOIN_ONE_TO_ONE","KEEP_ALL",fieldmappings,"INTERSECT")


def SpatJoin_1to1_Within_A_Distance(Out_Field, Join_Fields_list, fc_target, fc_join, out_fc, search_distance):

    # Create a new fieldmappings object including field maps for all columns in fc_target
    fieldmappings = arcpy.FieldMappings()
    fieldmappings.addTable(fc_target)

    # remove Join_Count and TARGET_FID from field mappings
    list = [x.name for x in fieldmappings.fields]
    if u'Join_Count' in list:
        fieldmappings.removeFieldMap(list.index(u'Join_Count'))
        list.remove(u'Join_Count')
    if u'TARGET_FID' in list:
        fieldmappings.removeFieldMap(list.index(u'TARGET_FID'))

    # Create field map for the new column that gets added by spatial join.
    FieldMap = arcpy.FieldMap()
    # Set input fields from fc_join
    for x in Join_Fields_list:
        FieldMap.addInputField(fc_join, x)
    # Edit field map properties.
    FieldMap.mergeRule = u'Join'
    FieldMap.joinDelimiter = u' / '
    # Edit output field properties
    field = FieldMap.outputField #get field with current properties
    if field.type == u'String':
        field.length = 3000
    field.name = Out_Field
    field.aliasName = Out_Field
    FieldMap.outputField = field #overwrite field with editted properties

    # Add field map to field mappings.
    fieldmappings.addFieldMap(FieldMap)

    # Run the Spatial Join tool.
    arcpy.SpatialJoin_analysis(fc_target, fc_join, out_fc,"JOIN_ONE_TO_ONE","KEEP_ALL",fieldmappings,"WITHIN_A_DISTANCE", search_distance)

def SpatJoin_1to1_Closest(Out_Field, Dist_Field, Join_Fields_list, fc_target, fc_join, out_fc, search_distance):

    # Create a new fieldmappings object including field maps for all columns in fc_target
    fieldmappings = arcpy.FieldMappings()
    fieldmappings.addTable(fc_target)

    # remove Join_Count and TARGET_FID from field mappings
    list = [x.name for x in fieldmappings.fields]
    if u'Join_Count' in list:
        fieldmappings.removeFieldMap(list.index(u'Join_Count'))
        list.remove(u'Join_Count')
    if u'TARGET_FID' in list:
        fieldmappings.removeFieldMap(list.index(u'TARGET_FID'))

    # Create field map for the new column that gets added by spatial join.
    FieldMap = arcpy.FieldMap()
    # Set input fields from fc_join
    for x in Join_Fields_list:
        FieldMap.addInputField(fc_join, x)
    # Edit output field properties
    field = FieldMap.outputField #get field with current properties
    if field.type == u'String':
        field.length = 3000
    field.name = Out_Field
    field.aliasName = Out_Field
    FieldMap.outputField = field #overwrite field with editted properties

    # Add field map to field mappings.
    fieldmappings.addFieldMap(FieldMap)

    # Run the Spatial Join tool.
    arcpy.SpatialJoin_analysis(fc_target, fc_join, out_fc,"JOIN_ONE_TO_ONE","KEEP_ALL",fieldmappings,"CLOSEST",search_distance,Dist_Field)

#CREATE DATE STRING FOR LABELS------------
def Date_String_Label():
    now = datetime.now()
    year = str(now.date().year)
    month = str(now.date().month)
    if len(month) == 1:
        month = '0' + month
    day = str(now.date().day)
    if len(day) == 1:
        day = '0' + day

    Date_STR = year + month + day
    return Date_STR
   