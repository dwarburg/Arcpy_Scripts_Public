import os
import arcpy
import numpy

#Inputs 
InFc  = arcpy.GetParameterAsText(0) # input horizontal mapbook feature class in UTM or state plane
Scale = arcpy.GetParameter(1) #mapbook scale
OutFc = arcpy.GetParameterAsText(3) # output feature class
OutSR = arcpy.GetParameter(4) # spatial reference of coordinates to be displayed (GCS_WGS default)

#--------------------------------------------------------------------------------------------------------------------
 # Spatial reference of input feature class
SR = arcpy.Describe(InFc).spatialReference

# change in native coordinates to shift point away from corner of frame
Inches = arcpy.GetParameter(2)
Delta = Inches * Scale/(39.37*SR.metersPerUnit) #1 map inch in meters * meters_per_SR_unit
	
# Create NumPy array from input feature class
input_array = arcpy.da.FeatureClassToNumPyArray(InFc,["SHAPE@XY"], spatial_reference=SR, explode_to_points=True)
#NumPy arrays cannot have elements deleted so we must create a new array with the values we want to keep
n = len(input_array)
#create list of indexes not including odd last element that contains file details
keep_elements = range(n-1)
#delete every fifth element starting at index = 4 (which is the 5th because 1st is 0) to get rid of duplicate starting points
del keep_elements[4::5]
#Skip every 2nd point to get just bottom left and top right
keep_elements = keep_elements[::2]
#add back in the last element that contains file details
keep_elements.append(n-1)
array = input_array[keep_elements]


#shift points in from corners within numpy array(abandoned in favor of UpdateCursor
#multipliers = numpy.empty((n-1))
#multipliers[::2] = Delta
#multipliers[1::2] = -1*Delta


# Check array and Exit if no features found
if array.size == 0:
    arcpy.AddError(InFc + " has no features.")

# Create a new points feature class
else:
	arcpy.da.NumPyArrayToFeatureClass(array, OutFc, ['SHAPE@XY'], SR)
	#shift points in from corners
	with arcpy.da.UpdateCursor(OutFc, ["SHAPE@XY"]) as cursor:
		i = 0
		for row in cursor:
			if i%2 == 0:
				row[0] = (row[0][0] + Delta, row[0][1] + Delta)
			else:
				row[0] = (row[0][0] - Delta, row[0][1] - Delta)
			i = i + 1
        		cursor.updateRow(row)
	#add coordinate fields to display
	arcpy.AddGeometryAttributes_management(OutFc,"POINT_X_Y_Z_M",'','',OutSR)
	#add to layout
	mxd = arcpy.mapping.MapDocument("CURRENT")
	df = arcpy.mapping.ListDataFrames(mxd)[0]
	addLayer = arcpy.mapping.Layer(OutFc)
	arcpy.mapping.AddLayer(df, addLayer, "TOP")

