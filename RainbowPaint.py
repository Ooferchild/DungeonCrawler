#Josh

colors = ["red", "green","purple"]
prices =  [21.95, 19.95, 17.75]
amt = [0,0,0]
total = 0

while True:
    color = input("What color do you want? ")
    if color == "quit":
        break
    if color in colors:
        index = colors.index(color)
        print("Each gallon of " + color + " costs $" + str(prices[index]))
        many = int(input("How many gallons do you want? "))
        if many > 0:
            print("That will be $" + str(prices[index] * many))
            amt[index] += many
            total += prices[index] * many
            print("So far you have bought " + str(amt[0]) + " gallons of " + colors[0] + " and " + str(amt[1]) + " gallons of " + colors[1])
        elif many < 0:
            print("You subtracted " + str(many) + " gallons of " + color + " from your total.")
            amt[index] += many
            total += prices[index] * many
            print("So far you have bought " + str(amt[0]) + " gallons of " + colors[0] + " and " + str(amt[1]) + " gallons of " + colors[1])
    else:
        print("Sorry, we don't have that color.")
        continue

    answer = input("Do you want to buy another? ")
    if answer == "no":
        print("Your total is $" + str(total))
        print("You bought " + str(amt[0]) + " gallons of " + colors[0] + " and " + str(amt[1]) + " gallons of " + colors[1])
        break
    elif answer == "yes":
        print("So far you have bought " + str(amt[0]) + " gallons of " + colors[0] + " and " + str(amt[1]) + " gallons of " + colors[1])
        continue