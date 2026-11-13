import random
import json

def save_game(kingdoms, year):
    game_data = {
        "year": year,
        "kingdoms": []
    }

    for kingdom in kingdoms:
            game_data["kingdoms"].append({
                "name": kingdom.name,
                "gold": kingdom.gold,
                "army": kingdom.army,
                "population": kingdom.population
            })   
    with open("savegame.json", "w", encoding="utf-8") as f:
        json.dump(game_data, f, indent=4)
    print("Game saved successfully!")

class Kingdom:
    def __init__(self, name, gold, army, population):
        self.name = name
        self.gold = gold
        self.army = army
        self.population = population

    def advance_year(self):
        taxes = self.population // 10
        upkeep = self.army * 2

        self.gold += taxes - upkeep
        self.population += random.randint(-50, 150)

        if self.gold < 0:
            self.army = max(0, self.army - 50)
            self.gold = 0

    def recruit_soldiers(self):
        cost = 100
        soldiers = 10

        if self.gold >= cost:
            self.gold -= cost
            self.army += soldiers

            print(f"Successfully recruited {soldiers} soldiers!")
            print(f"Remaining gold:{self.gold}")
            print(f"Total army: {self.army}")
        else:
            print(f"Not enough gold to recruit soldiers!")
        

    def report(self):
        print(f"\n{self.name}")
        print(f"Gold: {self.gold}")
        print(f"Army: {self.army}")
        print(f"Population: {self.population}")

def load_game():
    try:
        with open("savegame.json", "r") as file:
            game_data = json.load(file)

        year = game_data["year"]
        kingdoms = []

        for data in game_data["kingdoms"]:
            kingdom = Kingdom(
                data["name"],
                data["gold"],
                data["army"],
                data["population"]
            )

            kingdoms.append(kingdom)

        print("Game loaded successfully!")
        return kingdoms, year

    except FileNotFoundError:
        print("No saved game found!")
        return None

    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        print("Save file is invalid or corrupted!")
        return None  


kingdoms = [
    Kingdom("Ironhold", 5000, 500, 3000),
    Kingdom("Eldoria", 4000, 300, 2500),
    Kingdom("Solmere", 8000, 200, 4000)
]

year = 1000

while True:
    print("\n===== Kingdom Simulator =====")
    print("1. Advance Year")
    print("2. Recruit Soldiers")
    print("3. View Kingdoms")
    print("4. Save Game")
    print("5. Load Game")
    print("6. Exit (or Q)")

    command = input("\nChoose an option:")

    if command == "1":
        year += 1
        print(f"\n===== Year {year} =====")

        for kingdom in kingdoms:
            kingdom.advance_year()
            kingdom.report()
    elif command == "2":
        print("\n===== Select Kingdom =====" )

        for index, kingdom in enumerate(kingdoms, start=1):
            print(f"{index}. {kingdom.name}")

        choice = input("\nChoose a kingdom: ")

        if choice.isdigit() and 1 <= int(choice) <= len(kingdoms):
            selected_kingdom = kingdoms[int(choice)-1]
            selected_kingdom.recruit_soldiers()
        else:
            print("Invalid kingdom selection!")
    elif command == "3":
        print("\n===== Kingdom Overview =====")
        for kingdom in kingdoms:
            kingdom.report()
    elif command == "4":
        save_game(kingdoms, year)
    
    elif command == "5":
            loaded_game = load_game()

            if loaded_game is not None:
                kingdoms, year = loaded_game
    elif command == "6" or command.lower() == "q":
            print("Exiting kingdom simulator...")
            break
    else:
        print("Invalid option! Please choose a valid menu option.")