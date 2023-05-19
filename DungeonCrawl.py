import shelve
import random



with shelve.open("DungeonCrawl") as dungeon:
    dungeon["character"] = character

knight = {"name": name, "class": "Knight", "health": 100, "dexterity": 0, "strength": 0, "defense": 5, "inventory": []}
fighter = {"name": name, "class": "Fighter", "health": 100, "dexterity": 0, "strength": 5, "defense": 0, "inventory": []}
rogue = {"name": name, "class": "Rogue", "health": 100, "dexterity": 5, "strength": 0, "defense": 0, "inventory": []}

def characterCreate(name, _class):
    name = input("What is your name? ")
    print("You can be a Knight(+5 def), Fighter(+5 str), or Rogue (+5 dex)j.")
    _class = input("What class would you like to be? ")
    if _class == "Knight".lower():
        character = shelve.knight(name)
    elif _class == "Fighter".lower():
        character = shelve.fighter(name)
    elif _class == "Rogue".lower():
        character = shelve.rogue(name)
    return character

def characterStats(character):
    print("You will roll 3 dice to determine your stats.")
    dexterity = random.randint(1,20)
    strength = random.randint(1,20)
    defense = random.randint(1,20)
    print("Your dexterity is: ", dexterity)
    print("Your strength is: ", strength)
    print("Your defense is: ", defense)
    reroll = input("Would you like to reroll? ")
    if reroll == "yes".lower():
        dexterity = random.randint(1, 20)
        strength = random.randint(1, 20)
        defense = random.randint(1, 20)
        print("Your dexterity is: ", dexterity)
        print("Your strength is: ", strength)
        print("Your defense is: ", defense)
    elif reroll == "no".lower():
        pass
    character["health"] = 100
    character["dexterity"] = dexterity
    character["strength"] = strength
    character["defense"] = defense
    return character

def characterInventory(character):
    print("You have: ")
    for i in range(len(character["inventory"])):
        print(character["inventory"][i])
    return character

def characterSave(character):
    db["character"] = character
    return character

shelve.close()

if __name__ == "__main__":
    characterCreate()
    characterStats()
    characterSave()