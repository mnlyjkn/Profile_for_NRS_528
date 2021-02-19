# Coding Challenge 2
# Problem 2 - list the names that are in both lists and the names that are not in both lists
list_a = ['dog', 'cat', 'rabbit', 'hamster', 'gerbil']
list_b = ['dog', 'hamster', 'snake']
print()
print("The following are in both lists:")
print(list(set(list_b).intersection(list_a)))
print()
print("The following are not in both lists:")
list_c = list((set(list_a) - set(list_b)))
list_c.extend(list(set(list_b) - set(list_a)))
print(list_c)
