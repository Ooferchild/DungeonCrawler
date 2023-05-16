import os
import random
import shelve

from azure.cosmos import CosmosClient
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for

# Initialize the Cosmos DB client
load_dotenv()
app = Flask(__name__)


def get_cosmos_client():
    connection_string = os.getenv('PRIMARY_CONNECTION_STRING')
    return CosmosClient.from_connection_string(f"{connection_string}")

database = 'DungeonCrawler'
container = 'Character'


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
    char_class = input("What class would you like to be? ")
    
    character = {
        "name": name,
        "class": char_class,
        "health": 100,
        "dexterity": 0,
        "strength": 0,
        "defense": 0,
        "inventory": []
    }
    
    if char_class.lower() == "knight":
        character["defense"] = 5
    elif char_class.lower() == "fighter":
        character["strength"] = 5
    elif char_class.lower() == "rogue":
        character["dexterity"] = 5
    else:
        print("Invalid class")
        return None
    
    client = get_cosmos_client()
    container = client.get_database_client(database).get_container_client(container)
    container.create_item(body=character)
    
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
        elif choice == "":
            return
        else:
            print("You cannot use that item.")
        
        # Update character document in the database
        client = get_cosmos_client()
        container = client.get_database_client(database).get_container_client(container)
        container.upsert_item(body=character)
    else:
        print("You do not have that item.")


def characterSave(character):
    client = get_cosmos_client()
    container = client.get_database_client(database).get_container_client(container)
    container.upsert_item(body=character)
    print("Character saved")


def dungeon(character):
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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create", methods=["POST"])
def create():
    name = request.form["name"]
    character_class = request.form["class"]
    character = characterCreate()
    
    # Return some response indicating success or failure
    return render_template("character.html", character=character)

@app.route("/dungeon", methods=["POST"])
def dungeon_route():
    character = characterCreate()
    dungeon(character)

if __name__ == "__main__":
    app.run(debug=True)
