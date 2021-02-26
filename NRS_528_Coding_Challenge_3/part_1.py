# create directories with subdirectories (folders inside of folders)
# then delete tree

import os
import shutil

main = "Part_1_Directory"  # creating the main directory to store these files
os.mkdir(main)

os.mkdir(os.path.join(main, "draft_code"))  # one method of creating files within other files
os.mkdir(os.path.join(main, "draft_code/pending"))  # can use "/"
os.mkdir(os.path.join(main, "draft_code", "complete"))  # or ","

os.mkdir("Part_1_Directory/includes")  # can just type out the entire path
# not including the path from C:/ will create the file in the current folder location

layouts = "Part_1_Directory/layouts"  # using a for loop to create folder with a list
os.mkdir(layouts)
sub_folder = ["default", "post"]
for folder in sub_folder:
    os.mkdir(os.path.join(layouts, folder))
os.mkdir("Part_1_Directory/layouts/post/posted")

os.mkdir("Part_1_Directory/site")
print(os.listdir("Part_1_Directory"))
print(os.listdir("Part_1_Directory/layouts"))  # checking to make sure for loop worked

shutil.rmtree(main)  # deleting entire tree by using shutil.  rmdir won't work if directory has contents in it
