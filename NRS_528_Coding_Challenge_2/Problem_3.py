# Coding Challenge 2
# Problem 3 - print out and count how many times each word appears
string = 'hi dee hi how are you mr dee'
counts = dict()
words = string.split()
for word in words:
    if word in counts:
        counts[word] += 1
    else:
        counts[word] = 1
print(counts)

# Excellent, well done