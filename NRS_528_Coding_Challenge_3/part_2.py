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
