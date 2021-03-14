import sys
argument_1 = sys.argv[1]
argument_2 = sys.argv[2]
argument_3 = sys.argv[3]
argument_4 = sys.argv[4]
argument_5 = sys.argv[5]
list = [argument_1, argument_2, argument_3, argument_4, argument_5]
print("These are the arguments you inputted")
print(list)
list_sorted = []
list_sorted = sorted(list, key=len)
print("The argument list is now sorted by length:")
print(list_sorted)

#add in some comments to better present your work. I had to correct the file name
# in the bat, as it was looking for a different python file to the one you provided