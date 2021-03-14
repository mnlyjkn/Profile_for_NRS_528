
#####
# Step 3 - Python Script from Tools
#####

# NOTE THAT THIS TASK IS ALSO YOUR CODING CHALLENGE THIS WEEK, I DO NOT EXPECT US TO COMPLETE THIS IN CLASS.

# Task 1 - Use what you have learned to process the Landsat files provided, this time, you know you are
# interested in the NVDI index which will use Bands 4 (red, aka vis) and 5 (near-infrared, aka nir) from the
# Landsat 8 imagery. Data provided are monthly (a couple are missing due to cloud coverage) during the
# year 2015 for the State of RI.

# Before you start, here is a suggested workflow:

# 1) Extract the Step_3_data.zip file into a known location.
# 2) For each month provided, you want to calculate the NVDI, using the equation: nvdi = (nir - vis) / (nir + vis)
# https://en.wikipedia.org/wiki/Normalized_difference_vegetation_index. Consider using the Raster Calculator Tool
# in ArcMap and using "Copy as Python Snippet" for the first calculation.

# The only rule is, you should run your script once, and generate the NVDI for ALL MONTHS provided. As part of your
# code submission, you should also provide a visualization document (e.g. an ArcMap layout), showing the patterns for
# an area of RI that you find interesting.

import os, arcpy

# print("Enter the workspace (up to the folder that contains the folders to be worked with):")  # where the workspace will be
# workspace = input()

workspace = r"C:\Users\Million\Desktop\URI Classes\Spring 2021\NRS 528\PythonScriptsAndLectures\Coding_challenges\Coding_Challenge_6\Step_3_data_lfs"

# Create list of workspace files
listMonths = os.listdir(workspace)
print(listMonths)

for month in listMonths:
    arcpy.env.workspace = workspace + "\\" + str(month)  # will change which file is being worked with as it loops for the workspace
    listRasters = arcpy.ListRasters("*", "TIF")
    # print(listRasters)
    # Remove all but B4.tif and B5.tif files from the list, replace ****** with the correct string.
    B4Raster = [x for x in listRasters if "B4" in x]
    print(B4Raster)
    Red = workspace + "\\" + str(month) + "\\" + str(B4Raster[0])
    print(Red)
    B5Raster = [x for x in listRasters if "B5" in x]
    print(B5Raster)
    NIR = workspace + "\\" + str(month) + "\\" + str(B5Raster[0])
    print(NIR)
    print()  # space between loop iteration print outs

    output_raster = arcpy.sa.RasterCalculator((NIR - Red) / (NIR + Red))
    output_raster.save(workspace + "\\" + str(month) + "\\" + str(month) + "_NDVI.tif")

    # output_raster = arcpy.sa.RasterCalculator(( "" - " ") / ( "" + " "))
