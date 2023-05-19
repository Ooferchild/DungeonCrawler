#Josh
import random

heads, tail = 0
head, tail = 0

total = 0

for i in range(50):
    flip = random.randint(0,1)
    if flip == 0:
        heads += 1
        head += 1
        tails = 0
        total += 2
        print(f"Flip {i+1}: Heads ({heads})")
    else:
        tails += 1
        tail += 1
        heads = 0
        total -= 2
        print(f"Flip {i+1}: Tails ({tails})")

    #if 5 in a row
    if heads == 5:
        print("TOO MANY IN A ROW")
        break
    elif tails == 5:
        print("TOO MANY IN A ROW")
        break

winner = lambda total: "Heads wins!!" if total > 0 else "Tails wins!!"

print(f"The total is {total}\n{winner(total)}")
print(f"Max Heads in a row: {head}")
print(f"Max Tails in a row: {tail}")
print(f"Point differential: {abs(total)}")