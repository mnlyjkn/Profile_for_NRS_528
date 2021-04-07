import arcpy

## THIS SI THE POITN OF MY CODE

# workspace
print("Please enter the file path to be used as your workspace")
file_path = "C:\Data\Students_2021\Million\Coding_Challenge_4"    # requires user input to set the file path that will be used in the workspace
arcpy.env.workspace = file_path  # sets the workspace
arcpy.env.scratchWorkspace = file_path  # sets the scratch workspace
print("The workspace is now set to:")
print(file_path)   # informs you that the workspace was set

# tool variables
in_features = 'Watershed_Boundary_Rhode_Island.shp'  # input for the clip tool
clip_features = 'Rhode_Island_state_boundary.shp'    # feature to be used to clip the input
out_feature_class = 'Rhode_Island_Watersheds.shp'    # output data from the clip tool
# cluster_tolerance = '#'  # optional so leaving blank

# tool
arcpy.Clip_analysis(in_features, clip_features, out_feature_class)  # will clip the in_features to the shape of the clip_features
