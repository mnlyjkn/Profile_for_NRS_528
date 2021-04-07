# NRS 528 midterm assignment
# This script will find all of the sections of rivers within Southern Kingstown, RI that are within 50 meters of a road.
# It will take a RI municipalities shapefile and select Southern Kingstown.
# The it will clip out the roads and rivers within Southern Kingstown.
# A 50 meter buffer will be applied to the Kingstown roads and use that to clip the river sections within the buffer.

import arcpy

# environment
arcpy.env.overwriteOutput = True
print("Enter the workspace file path:")
workspace = "C:\Data\Students_2021\Million\Midterm\data"
arcpy.env.workspace = workspace
print("The workspace has been set")

# inputs
roads = "Roads.shp"
rivers = "Rivers.shp"
towns = "Towns.shp"

# tools/procedure
print("The Southern Kingstown municipality will now be selected from the towns shapefile.")
towns_output = "Kingstown.shp"
selection_equation = "NAME LIKE '%SOUTH KINGSTOWN%'"
arcpy.Select_analysis(towns, towns_output, selection_equation)  # Selects a feature and makes a shapefile

print("Now clipping the roads in Kingstown.")
Kingstown_roads_output = "Kingstown_Roads.shp"
arcpy.Clip_analysis(roads, towns_output, Kingstown_roads_output) # uses one feature to clip another

print("Now clipping the rivers in Kingstown.")
Kingstown_rivers_output = "Kingstown_Rivers.shp"
arcpy.Clip_analysis(rivers, towns_output, Kingstown_rivers_output) # uses one feature to clip another

print("Buffer being applied to the Kingstown roads.")
Roads_buffer_output = "Roads_Buffer.shp"
buffer_distance = "50 meter"
line_side = "FULL"
line_end_type = "ROUND"
dissolve_option = "ALL"
dissolve_field = "#"
method = "PLANAR"
arcpy.Buffer_analysis(Kingstown_roads_output, Roads_buffer_output, buffer_distance, line_side, line_end_type, dissolve_option, dissolve_field, method)  # creates a buffer around a feature

print("Now clipping the rivers within the roads buffer.")
Rivers_near_roads_output = "Kingstown_rivers_near_roads.shp"
arcpy.Clip_analysis(Kingstown_rivers_output, Roads_buffer_output, Rivers_near_roads_output)  # uses one feature to clip another

print("Will now delete intermediate files except for Kingstown.shp and Kingstown_Rivers.shp")

if arcpy.Exists(Kingstown_roads_output):
    arcpy.Delete_management(Kingstown_roads_output)

if arcpy.Exists(Roads_buffer_output):
    arcpy.Delete_management(Roads_buffer_output)
print("Deleted intermediate files")
