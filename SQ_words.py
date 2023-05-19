#Josh

import random

word = input("Enter a word: ")
i = 0
times = 0

while i < len(word):
    num = random.randint(65, 122)
    if num in range(91, 96):
        continue
    print(chr(num))
    if chr(num) == word[i]:
        print("You found a letter! It was", chr(num))
        i += 1
    else:
        times += 1
        continue
    if i == len(word):
        print(f"You found the word {word}!")
        break

print("It took you", times, "tries to find the word", word)