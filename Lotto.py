#Josh
import random
winning = []
def getRepeating(list):
    for i in range(len(list)):
        for j in range(len(list)):
            if list[i] == list[j] and i != j:
                return True
    return False
for i in range(5):
    winning.append(random.randint(1,70))
while getRepeating(winning):
    winning = []
    for i in range(5):
        winning.append(random.randint(1,70))
winning.sort()
print("The winning numbers are: ", end="\n")
print(winning)