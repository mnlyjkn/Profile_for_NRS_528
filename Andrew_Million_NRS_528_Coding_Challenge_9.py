# Purpose of coding challenge 9
# 1.	Count how many sites have photos, and how many do not (2 numbers), print the results.
# 2.	Count how many unique species there are in the dataset, print the result.
# 3.	Generate two shapefiles, one with photos and the other without.

import arcpy

print("Please enter your file path to set the work space environment")
file_path = input()
arcpy.env.workspace = file_path
arcpy.env.scratchWorkspace = file_path
print("The workspace is now set to: " + "'" + file_path + "'")
arcpy.env.overwriteOutput = True

input = "RI_Forest_Health_Works_Project%3A_Points_All_Invasives.shp"

expression_1 = arcpy.AddFieldDelimiters(input, "photo") + " = 'y'"
expression_2 = arcpy.AddFieldDelimiters(input, "photo") + " = ''"

ycounter = 0
sites_with_photos = []
nophotocounter = 0
no_photo_sites = []
with arcpy.da.SearchCursor(input, '*') as cursor:
    for row in cursor:
        # print(row)    # double checks to make sure all fields are printed
        if 'y' in row[18]:
            sites_with_photos.append(row)
            ycounter += 1
        else:
            no_photo_sites.append(row)
            nophotocounter += 1
    arcpy.Select_analysis(input, "sites_with_photos_of_invasive_species.shp", expression_1)  # creates a shapefile using the input and the query expression_1
    print("Created shapefile of sites with photos of invasive species.")
    arcpy.Select_analysis(input, "no_photos_of_invasive_species.shp", expression_2)  # creates a shapefile using the input and the query expression_2
    print("Created shapefile of sites with no photos of invasive species.")
print("There are " + str(ycounter) + " sites that have photos of invasive species.")
print("There are " + str(nophotocounter) + " sites that do not have photos of invasive species.")

# print(len(sites_with_photos))     # double checks to make sure the list length matches the counter
# print(len(no_photo_sites))        # double checks to make sure the list length matches the counter

specieslist = []
with arcpy.da.SearchCursor(input, 'species') as cursor:
    for row in cursor:
        if row not in specieslist:
            specieslist.append(row)
print("There are " + str(len(specieslist)) + " unique species in the dataset")
# print(str(set(specieslist)))  # will provide each unique output
