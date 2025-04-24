"""
Data Structures
Student Project
Project Title:
"""
"""
Do not begin coding.
Instead, fill out the Planning worksheet.
"""

# Imported libraries
import requests
import random



#  API Constants
base_url = "https://pokeapi.co/api/v2/"
pokemon_endpoint = "pokemon/"

#  Welcome message
print("\n🎮 Welcome to the Pokémon Battle Game! 🎮")

#  Get random Pokémon 1 (Player's Pokémon)
pokemon_id = random.randint(1, 898)
response = requests.get(base_url + pokemon_endpoint + str(pokemon_id))

if response.status_code != 200:
    print("Failed to retrieve Pokémon data.")
    exit() # Exit if API request fails

data = response.json()
player_pokemon = {
    "name": data["name"].capitalize(), # Capitalize Pokémon name
    "hp": data["stats"][0]["base_stat"], # Get base HP stat
    "attack": data["stats"][1]["base_stat"], # Get base Attack stat
    "defense": data["stats"][2]["base_stat"] # Get base Defense stat
}

#  Get random Pokémon 2 (Opponent's Pokémon)
pokemon_id = random.randint(1, 898) # Randomly select another Pokémon
response = requests.get(base_url + pokemon_endpoint + str(pokemon_id))

if response.status_code != 200:
    print("Failed to retrieve Pokémon data.")
    exit()

data = response.json()
opponent_pokemon = {
    "name": data["name"].capitalize(),
    "hp": data["stats"][0]["base_stat"],
    "attack": data["stats"][1]["base_stat"],
    "defense": data["stats"][2]["base_stat"]
}

#  Display Pokémon
print("\nYour Pokémon:")
print("🟢 " + player_pokemon["name"] + " - HP: " + str(player_pokemon["hp"]) + ", Attack: " + str(player_pokemon["attack"]))

print("\nOpponent Pokémon:")
print("🔴 " + opponent_pokemon["name"] + " - HP: " + str(opponent_pokemon["hp"]) + ", Attack: " + str(opponent_pokemon["attack"]))

# Battle loop
turn = 0
defending = False  # Track if the player is defending
while True:
    turn += 1
    print("\n Turn " + str(turn))

    # Player's turn: Choose action
    print("\nChoose your action: (Type 'attack' to attack, 'defend' to reduce damage)")
    player_action = input("Your choice: ").lower()

    if player_action == "attack":
        # Calculate damage for player's attack
        player_damage = player_pokemon["attack"]
        random_factor = random.randint(30, 120) 
        player_damage = int(player_damage * random_factor / 100)

        if player_damage < 1:
            player_damage = 1  # Ensure at least 1 damage dealt

        opponent_pokemon["hp"] -= player_damage  # Subtract damage from opponent's HP
        print(player_pokemon["name"] + " attacks " + opponent_pokemon["name"] + " for " + str(player_damage) + " damage! Opponent HP: " + str(opponent_pokemon["hp"]))
        defending = False  # Reset defend status

    elif player_action == "defend":
        print(player_pokemon["name"] + " is defending! Next attack will deal reduced damage.")
        defending = True  # Activate defense mode

    else:
        print("Invalid action! You must choose 'attack' or 'defend'.")
        continue  # Skip opponent's turn if invalid action is chosen

    # Check if opponent's Pokémon has fainted
    if opponent_pokemon["hp"] <= 0:
        print("\n🎉 " + player_pokemon["name"] + " wins the battle! 🎉")
        break

    # Opponent's turn: Automated attack
    opponent_damage = opponent_pokemon["attack"]
    random_factor = random.randint(30, 120)  # Random variation in damage
    opponent_damage = int(opponent_damage * random_factor / 100)

    if opponent_damage < 1:
        opponent_damage = 1  # Ensure at least 1 damage dealt

    if defending:
        opponent_damage = opponent_damage // 2  # Reduce damage if defending
        print("Defense activated! Damage reduced to " + str(opponent_damage))

    player_pokemon["hp"] -= opponent_damage  # Subtract damage from player's HP
    print(opponent_pokemon["name"] + " attacks " + player_pokemon["name"] + " for " + str(opponent_damage) + " damage! Player HP: " + str(player_pokemon["hp"]))

    # Check if player's Pokémon has fainted
    if player_pokemon["hp"] <= 0:
        print("\n💀 " + opponent_pokemon["name"] + " wins the battle! ")
        break

# End of battle message
print("\n Battle Over! Thanks for playing! ")
