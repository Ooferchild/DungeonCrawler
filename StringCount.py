#Josh

vowels = 0
spaces = 0
words = 0

sentence = input("Enter a sentence: ")

for i in sentence:
    if i in "aeiouAEIOU":
        vowels += 1
    elif i == " ":
        spaces += 1
    else:
        words += 1
print("Vowels: ", vowels)
print("Spaces: ", spaces)
print("Words: ", words)
seperate = sentence.replace(" ", "")
print(seperate)