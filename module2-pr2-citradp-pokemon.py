# 2) Gunakan Pokemon API
# Pokemon Stats
# Masukkan Nama Pokemon: 
# Outputnya: 
# Nama: Pikachu
# HP: ...
# Attack: ...
# Defense: .....
# Ability Name: ..... (Bulbasaur Ability ada 2)
# 1, ....
# 2, ....
# Speed: 
# Type: 

import requests

# Pokemon URL
base_pokemon_url = 'https://pokeapi.co/api/v2/pokemon/'

def getPokemon(nama, base_url):
    data = requests.get(base_url + nama)
    data = data.json()
    poke_data = {
        "Name": '',
        "HP": int,
        "Attack": int,
        "Defense": int,
        "Abilities": [],
        "Speed": int,
        "Type": []
    }

    if data == {"detail":"Not found."}:
        print("Invalid Pokemon Name.")
    else:
        poke_data["Name"] = data["name"].title()
        for i in data["stats"]:
            if i["stat"]["name"] == "hp":
                poke_data["HP"] = i["base_stat"]
            if i["stat"]["name"] == "attack":
                poke_data["Attack"] = i["base_stat"]
            if i["stat"]["name"] == "defense":
                poke_data["Defense"] = i["base_stat"]
            if i["stat"]["name"] == "speed":
                poke_data["Speed"] = i["base_stat"]

        for j in data["abilities"]:
            poke_data["Abilities"].append(j["ability"]["name"])

        for k in data["types"]:
            poke_data["Type"].append(k["type"]["name"])
            
        print("Nama:", poke_data["Name"])
        print("HP:", poke_data["HP"])
        print("Attack:", poke_data["Attack"])
        print("Defense:", poke_data["Defense"])
        print("Ability Name:")
        for idx, i in enumerate(poke_data["Abilities"], start=1):
            print(f"{idx}. {i.title()}")
        print("Speed:", poke_data["Speed"])
        if len(poke_data["Type"]) > 1:
            print("Type: ")
        for idx, i in enumerate(poke_data["Type"]):
            if len(poke_data["Type"]) == 1:
                print(f"Type: {i.title()}")
            else:
                print(f"{idx+1}. {i.title()}")


def pokemon(base_url):
    namapokemon = input("Masukkan nama pokemon: ")
    getPokemon(namapokemon, base_url)

pokemon(base_pokemon_url)