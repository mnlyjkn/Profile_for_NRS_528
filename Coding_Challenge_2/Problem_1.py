# 1. List values
# Using this list:
#
# [1, 2, 3, 6, 8, 12, 20, 32, 46, 85]
# Make a new list that has all the elements less than 5 from this list in it and print out this new list.
# Write this in one line of Python.

List_1 = [1, 2, 3, 6, 8, 12, 20, 32, 46, 85]

for i in List_1:
    #do something.
    pass



# Write this in one line of Python.
List_2 = [i for i in List_1 if i < 5]; print(List_2)


# I find it good practice to copy out the entire challenge. You see that you ably meet the
# "one line challenge", but not the for loop part.