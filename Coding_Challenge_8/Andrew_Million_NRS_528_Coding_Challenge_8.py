# Turn previous class code work into a function
# Chose to use Lecture 5 Step 3

import arcpy

def heatmap(inputFile,outputFile, overwrite):   # function to create a heatmap from a cvs file

    arcpy.env.overwriteOutput = overwrite   # overwrites the results if the overwrite input is True

    # csv to a shapefile
    in_Table = inputFile
    x_coords = "lon"
    y_coords = "lat"
    z_coords = ""
    out_Layer = "Cepphus_grylle"
    saved_Layer = r"Cepphus_grylle_output.shp"
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

    # Generate a fishnet
    arcpy.env.outputCoordinateSystem = spRef
    outFeatureClass = "Fishnet.shp"
    originCoordinate = (str(x_min) + " " + str(y_min))
    yAxisCoordinate = (str(x_min) + " " + str(y_max))
    cellSizeWidth = "0.25"
    cellSizeHeight = "0.25"
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

    # Spatial Join the fishnet to the observed points
    target_features = outFeatureClass
    join_features = saved_Layer
    out_feature_class = outputFile
    join_operation = "JOIN_ONE_TO_ONE"
    join_type = "KEEP_ALL"
    field_mapping = ""
    match_option = "INTERSECT"
    search_radius = ""
    distance_field_name = ""

    arcpy.SpatialJoin_analysis(target_features, join_features, out_feature_class,
                               join_operation, join_type, field_mapping, match_option,
                               search_radius, distance_field_name)

    # Check if heatmap is created, then delete the intermediate files

    if arcpy.Exists(out_feature_class):
        print("Created Heatmap, will now delete intermediate files")
        arcpy.Delete_management(target_features)
        arcpy.Delete_management(join_features)
        print("Deleted intermediate files")

    print("View results in ArcMap. Be sure to change symbology to properly represent the heat map.")
    return

print("Please enter your file path to set the work space environment\n")
file_path = input()
arcpy.env.workspace = file_path
arcpy.env.scratchWorkspace = file_path
print("The workspace is now set to: " + "'" + file_path + "'")
# arcpy.env.workspace = r"C:\Users\Million\Desktop\URI Classes\Spring 2021\NRS 528\PythonScriptsAndLectures\Coding_challenges\Coding_Challenge_8\Coding_Challenge_8_Data"

inputFile = "Cepphus_grylle.csv"  # can change to an input() for user input
outputFile = "HeatMap_Cepphus_grylle.shp"  # can change to an input() for user input
overwrite = True  # can change to an input() for user input

heatmap(inputFile, outputFile,overwrite)   # calls function
