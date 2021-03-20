# NRS 528 Coding Challenge 6
# Creating NDVI indexes of images in one for loop.  The loop needs to go through each folder, find the correct files,
# and create the NDVI with a custom name for each month.

import os, arcpy
from arcpy.sa import *

print("Enter the workspace (up to the folder that contains the folders to be worked with):")  # where the workspace will be
workspace = input()
# example :workspace = r"C:\Python\Coding_Challenge_6\Step_3_data_lfs"
# the data will be in individual folders in folder Step_3_data_lfs

# Create list of workspace files
listMonths = os.listdir(workspace)
print(listMonths)

for month in listMonths:
    arcpy.env.workspace = workspace + "\\" + str(month)  # will change which folder is being worked with as it loops for the workspace
    listRasters = arcpy.ListRasters("*", "TIF")  # finds all of the appropriate files
    # Remove all but B4.tif and B5.tif files from the list, replace ****** with the correct string.
    B4Raster = [x for x in listRasters if "B4" in x]  # find the correct file, and puts it into a list
    print(B4Raster)
    Red = workspace + "\\" + str(month) + "\\" + str(B4Raster[0])  # turns the element into a string
    print(Red)
    B5Raster = [x for x in listRasters if "B5" in x]  # find the correct file
    print(B5Raster)
    NIR = workspace + "\\" + str(month) + "\\" + str(B5Raster[0])  # turns the element into a string
    print(NIR)
    print()  # space between loop iteration print outs

    output_raster = (Raster(NIR) - Raster(Red)) / (Raster(NIR) + Raster(Red))  # equation to calculate the NDVI
    output_raster.save(workspace + "\\" + str(month) + "\\" + str(month) + "_NDVI.tif")  # Saves the NDVI output
