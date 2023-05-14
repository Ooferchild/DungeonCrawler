import shelve
import random

def loot_table():
    items = [
        ("potion", 0.5),
        ("gold", 0.3),
        ("scroll", 0.1),
        ("wood sword", 0.05),
        ("iron sword", 0.025),
        ("leather armor", 0.05),
        ("iron armor", 0.025),
        ("enchanted scroll", 0.025)
    ]
    return random.choices(items, [weight for _, weight, _ in items])[0]


def characterCreate():
    name = input("What is your name? ")
    print("You can be a Knight(+5 def), Fighter(+5 str), or Rogue (+5 dex).")
    Class = input("What class would you like to be? ")
    if Class.lower() == "knight":
        character = {"name": name, "class": "Knight", "health": 100, "dexterity": 0, "strength": 0, "defense": 5, "inventory": []}
    elif Class.lower() == "fighter":
        character = {"name": name, "class": "Fighter", "health": 100, "dexterity": 0, "strength": 5, "defense": 0, "inventory": []}
    elif Class.lower() == "rogue":
        character = {"name": name, "class": "Rogue", "health": 100, "dexterity": 5, "strength": 0, "defense": 0, "inventory": []}
    else:
        print("Invalid class")
        return None
    return character

def characterStats(character):
    print("You will roll 3 dice to determine your stats.")
    dexterity = random.randint(1,20)
    strength = random.randint(1,20)
    defense = random.randint(1,20)
    print("Your dexterity is:", dexterity)
    print("Your strength is:", strength)
    print("Your defense is:", defense)
    reroll = input("Would you like to reroll? ")
    if reroll.lower() == "yes":
        dexterity = random.randint(1,20)
        strength = random.randint(1,20)
        defense = random.randint(1,20)
        print("Your dexterity is:", dexterity)
        print("Your strength is:", strength)
        print("Your defense is:", defense)
    elif reroll.lower() != "no":
        print("Invalid input")
    character["dexterity"] = dexterity
    character["strength"] = strength
    character["defense"] = defense
    return character

def characterInventory(character):
    print("You have:")
    for item in character["inventory"]:
        if item == "leather armor":
            print("- Leather Armor (Defense + 5)")
        elif item == "iron armor":
            print("- Iron Armor (Defense + 10)")
        elif item == "wood sword":
            print("- Wood Sword (Strength + 5)")
        elif item == "iron sword":
            print("- Iron Sword (Strength + 10)")
        elif item == "scroll":
            print("- Scroll (Dexterity + 5)")
        elif item == "enchanted scroll":
            print("- Enchanted Scroll (Dexterity + 10)")
        else:
            print("- " + item)

    choice = input("Enter an item name to use it, or press Enter to exit: ")
    if choice in character["inventory"]:
        if choice == "leather armor":
            character["defense"] += 5
            print("You put on the Leather Armor. Your Defense is now", character["defense"])
        elif choice == "iron armor":
            character["defense"] += 10
            print("You put on the Iron Armor. Your Defense is now", character["defense"])
        elif choice == "wood sword":
            character["strength"] += 5
            print("You equip the Wood Sword. Your Strength is now", character["strength"])
        elif choice == "iron sword":
            character["strength"] += 10
            print("You equip the Iron Sword. Your Strength is now", character["strength"])
        elif choice == "scroll":
            character["dexterity"] += 5
            print("You read the Scroll. Your Dexterity is now", character["dexterity"])
        elif choice == "enchanted scroll":
            character["dexterity"] += 10
            print("You read the Enchanted Scroll. Your Dexterity is now", character["dexterity"])
        elif choice == "potion":
            character["health"] += 10
            print("You drink the Potion. Your health is now", character["health"])
            if character["health"] > 100:
                character["health"] = 100
        else:
            print("You cannot use that item.")
    else:
        print("You do not have that item.")


def characterSave(character):
    db = shelve.open("DungeonCrawl")
    db["character"] = character
    db.close()
    print("Character saved")

def dungeon():
    turns = 0
    
    events = [
        ("You find a treasure chest!", 0.3),
        ("You encounter a monster!", 0.5),
        ("You stumble upon a hidden passage.", 0.2)
    ]
    
    while True:
        turns += 1
        
        event = random.choices(events, [weight for _, weight in events])[0]
        
        print(event[0])
        
        if "treasure chest" in event[0]:
            chest()
        elif "monster" in event[0]:
            battle()
        elif "hidden passage" in event[0]:
            # Generate a random puzzle or secret room
            pass
        
        choice = input("What do you want to do? (continue, inventory, quit) ")
        if choice.lower() != "continue" and choice.lower() != "inventory":
            break
        elif choice.lower() == "inventory":
            characterInventory(character)
            continue
def chest():    
    item = loot_table()
    
    print("You found a", item, "in the chest!")
    
    with shelve.open("DungeonCrawl") as db:
        if "inventory" not in db:
            character["inventory"] = []
        
        character["inventory"].append(item)
    
    return item

def puzzle():
    print("You come across a door with a strange inscription on it.")
    print("The inscription reads:")
    loot = [
        ("potion", 0.5),
        ("gold", 0.3),
        ("scroll", 0.2)
    ]
    
    # Choose a random puzzle
    puzzles = [
        ("What has to be broken before you can use it?", "An egg"),
        ("I am not alive, but I grow; I don't have lungs, but I need air; I don't have a mouth, but water kills me. What am I?", "Fire"),
        ("I have cities, but no houses. I have mountains, but no trees. I have water, but no fish. What am I?", "Map")
    ]
    puzzle, answer = random.choice(puzzles)
    
    while True:
        guess = input(puzzle + " ")
        if guess.lower() == answer.lower():
            print("Congratulations, you solved the puzzle!")
            item = random.choices(loot, [weight for _, weight in loot])[0][0]
            print("You open the door and find a", item, "!")
            with shelve.open("DungeonCrawl") as db:
                if "inventory" not in db:
                    character["inventory"] = []
                
                character["inventory"].append(item)
            return
        else:
            print("Incorrect, try again.")


def battle():
    damage = 0
    monsters = [
        ("goblin", 0.5),
        ("skeleton", 0.3),
        ("troll", 0.2)
    ]

    monster = random.choices(monsters, [weight for _, weight in monsters])[0]
    
    print("You encounter a", monster[0] + "!")
    
    with shelve.open("DungeonCrawl") as db:
        character = db["character"]
    
    turn = 1
    
    # Initialize monster health
    monster_health = 100
    
    while True:
        print("\nTurn", turn)
        attack_value = random.randint(1, character["strength"])
        print("Your health:", character["health"])
        print("The", monster[0], "health:", monster_health)
        
        choice = input("What do you want to do? (attack, defend, inventory, run) ")
        
        if choice.lower() == "attack":
            # Calculate damage done to the monster
            damage = attack_value
            monster_health -= damage
            print("You attack for", damage, "damage!")
        elif choice.lower() == "defend":
            defense_value = random.randint(1, character["defense"])
            print("You defend for", defense_value, "damage!")
        elif choice.lower() == "run":
            run_value = random.randint(1, character["dexterity"])
            if run_value > 10:
                print("You successfully run away!")
                return
            else:
                print("You failed to run away!")
        elif choice.lower() == "inventory":
            characterInventory(character)
            continue
        else:
            print("Invalid input")
            continue
        
        monster_attack_value = random.randint(1, 10)
        print("The", monster[0], "attacks for", monster_attack_value, "damage!")
        
        player_damage = monster_attack_value - defense_value if choice.lower() == "defend" else monster_attack_value
        
        character["health"] -= player_damage
        if character["health"] < 0:
            character["health"] = 0
        
        
        print("You take", player_damage, "damage!")
        print("The", monster[0], "takes", damage, "damage!")
        item = loot_table()
        if character["health"] == 0:
            print("You died!")
            quit()
        elif monster_health <= 0:
            print("You win!")
            with shelve.open("DungeonCrawl") as db:
                if "inventory" not in db:
                    character["inventory"] = []
                
                character["inventory"].append(item)
            print("You found a", item, "on the monster!")
            return
        
        # Increment turn counter
        turn += 1


while True:
    print("Welcome to Dungeon Crawler!")
    print("1. Create Character")
    print("2. Load Character")
    print("3. Exit")
    choice = input("What would you like to do? ")
    if choice == "1":
        character = characterCreate()
        if character is not None:
            character = characterStats(character)
            characterInventory(character)
            characterSave(character)
            dungeon()
            break
    elif choice == "2":
        db = shelve.open("DungeonCrawl")
        character = db["character"]
        db.close()
        dungeon()
        break
    elif choice == "3":
        print("Thank you for playing!")
        break
    else:
        print("Invalid input")

