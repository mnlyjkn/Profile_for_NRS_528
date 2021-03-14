# create directories with subdirectories (folders inside of folders)
# then delete tree

import os
import shutil

main = "C:\Part_1_Directory"  # creating the main directory to store these files
os.mkdir(main)

os.mkdir(os.path.join(main, "draft_code"))  # one method of creating files within other files
os.mkdir(os.path.join(main, "draft_code/pending"))  # can use "/"
os.mkdir(os.path.join(main, "draft_code", "complete"))  # or ","

os.mkdir(os.path.join(main, "includes"))  # can just type out the entire path
# not including the path from C:/ will create the file in the current folder location

layouts = os.path.join(main, "layouts")  # using a for loop to create folder with a list
os.mkdir(layouts)
sub_folder = ["default", "post"]
for folder in sub_folder:
    os.mkdir(os.path.join(main, layouts, folder))
os.mkdir(os.path.join(main, "layouts", "post", "posted"))

os.mkdir(os.path.join(main, "site"))
print(os.listdir(main))
print(os.listdir(os.path.join(main, "layouts"))) # checking to make sure for loop worked

shutil.rmtree(main)  # deleting entire tree by using shutil.  rmdir won't work if directory has contents in it

# Do not use main as a variable name, its a reserved word. I'd also use a
# full file path: C:\Part_1_directory for example. Also, use os.path.join to
# better handle subdirs.