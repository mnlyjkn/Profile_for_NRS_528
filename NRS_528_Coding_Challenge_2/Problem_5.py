# Coding Challenge 2
# Problem 5 - input a word and show what its scrabble score would be using the dictionary provided
letter_scores = {
    "aeioulnrst": 1,
    "dg": 2,
    "bcmp": 3,
    "fhvwy": 4,
    "k": 5,
    "jx": 8,
    "qz": 10
}
print("Please enter a word: ")
word = input()
points = 0
for letter in word:
    if letter in "aeioulnrst":
        points = points + letter_scores["aeioulnrst"]
    elif letter in "dg":
        points = points + letter_scores["dg"]
    elif letter in "bcmp":
        points = points + letter_scores["bcmp"]
    elif letter in "fhvwy":
        points = points + letter_scores["fhvwy"]
    elif letter in "k":
        points = points + letter_scores["k"]
    elif letter in "jx":
        points = points + letter_scores["jx"]
    elif letter in "qz":
        points = points + letter_scores["qz"]
print("Your word " + "'" + word + "'" + " scored " + str(points) + " points.")
