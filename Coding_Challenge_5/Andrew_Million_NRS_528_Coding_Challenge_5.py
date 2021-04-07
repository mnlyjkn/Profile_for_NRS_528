# Coding Challenge 5 for class NRS 528 - working with multiple tools and joining data in arcpy
# setup - import and environments
import arcpy
import csv
import os
arcpy.env.overwriteOutput = True

file_path = "C:\Data\Students_2021\Million\Coding_Challenge_5"
arcpy.env.workspace = file_path
arcpy.env.scratchWorkspace = file_path
print("The workspace is now set to: " + "'" + file_path + "'")

species_list = []

with open("species_data.csv") as species_coordinates:
    next(species_coordinates)
    for row in csv.reader(species_coordinates):
        if row[0] not in species_list:
            species_list.append(row[0])
species_coordinates.close()

print(species_list)
species_1 = species_list[0]
species_2 = species_list[1]
print(species_1)
print(species_2)
header = "scientificName"
print(header)

with open("species_data.csv") as species_coordinates:
    for row in csv.reader(species_coordinates):
        if row[0] == header:
            file_1 = open(species_1 + ".csv", "a")
            file_1.write(",".join(row))
            file_1.write("\n")
            file_2 = open(species_2 + ".csv", "a")
            file_2.write(",".join(row))
            file_2.write("\n")
        if row[0] == species_1:
            file_1 = open(species_1 + ".csv", "a")
            file_1.write(",".join(row))
            file_1.write("\n")
        if row[0] == species_2:
            file_2 = open(species_2 + ".csv", "a")
            file_2.write(",".join(row))
            file_2.write("\n")
species_coordinates.close()
print("Species files created for heatmap creation")

# FOR LOOP
for species in species_list:

    # species heatmap generation
    print("First heatmap")
    # Convert to shapefiles
    in_Table = species + ".csv"
    x_coords = "lon"
    y_coords = "lat"
    z_coords = ""
    out_Layer = ""
    saved_Layer = species + ".shp"
    spRef = arcpy.SpatialReference(4326)
    print("Spatial reference created")
    lyr = arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef, z_coords)

    arcpy.CopyFeatures_management(lyr, saved_Layer)
    if arcpy.Exists(saved_Layer):
        print("Created file successfully!")

    # Extact the Extent
    desc = arcpy.Describe(saved_Layer)
    print(desc.extent)
    y_min = desc.extent.YMin
    y_max = desc.extent.YMax
    x_min = desc.extent.XMin
    x_max = desc.extent.XMax
    print("Coordinate extents obtained")

    cellsize = abs(((y_max + y_min)/2)/10)
    if cellsize <= 1:
        cellsize = 1
    print("The y cell size is: " + str(cellsize))

    # Generate fishnet/grid
    arcpy.env.outputCoordinateSystem = spRef
    outFeatureClass = species + " Fishnet.shp"
    originCoordinate = (str(x_min) + " " + str(y_min))
    yAxisCoordinate = (str(x_min) + " " + str(y_max))
    cellSizeWidth = cellsize
    cellSizeHeight = cellsize
    numRows = ""
    numColumns = ""
    oppositeCorner = (str(x_max) + " " + str(y_max))
    labels = "NO_LABELS"
    templateExtent = "#"
    geometryType = "POLYGON"

    arcpy.CreateFishnet_management(outFeatureClass, originCoordinate, yAxisCoordinate,
                                   cellSizeWidth, cellSizeHeight, numRows, numColumns,
                                   oppositeCorner, labels, templateExtent, geometryType)
    print("Fishnet created")

    # Create heatmap
    target_features = species + " Fishnet.shp"
    join_features = saved_Layer
    out_feature_class = species + " HeatMap.shp"
    join_operation = "JOIN_ONE_TO_ONE"
    join_type = "KEEP_ALL"
    field_mapping = ""
    match_option = "INTERSECT"
    search_radius = ""
    distance_field_name = ""

    arcpy.SpatialJoin_analysis(target_features, join_features, out_feature_class,
                               join_operation, join_type, field_mapping, match_option,
                               search_radius, distance_field_name)

    # delete intermediate files, leaving only the heatmap
    if arcpy.Exists(out_feature_class):
        print("Created Heatmap, will now delete intermediate files")
        arcpy.Delete_management(target_features)
        arcpy.Delete_management(join_features)
        print("Deleted intermediate shapefiles")
species_coordinates.close()

file_1.close()
file_2.close()

print("Now removing remaining intermediate files")
for species in species_list:
    os.remove(species + ".csv")

print("All intermediate files have been deleted")
