import argparse
import textwrap
import re
import sys
import os
import chardet


def battlelogs_to_csv(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file_pointer:
        lines = file_pointer.readlines()

    player_info = []  # ['', 'player', 'p1', username, elo]
    player_pokemon = []
    pokemon_switches = []
    length = 0
    outcome = "Tie"

    for line in lines:
        if "|player|p1|" in line:
            # Get player info
            player_info += line.split("|")
            player_name = player_info[3]
        elif "|poke|p1|" in line:
            # Get pokemon info
            pokemon = (
                line.removeprefix("|poke|p1|")
                .split("|")[0]
                .split(",")[0]
                .removesuffix("\n")
            )
            player_pokemon.append(pokemon)
        elif "|switch|p1a:" in line:
            # Get pokemon switching info (1st entry == player lead pokemon)
            pokemon = line.removeprefix("|switch|p1a: ").split("|")[1].split(",")[0]
            pokemon_switches.append(pokemon)
        elif "|turn|" in line:
            # Increment turn count
            length += 1
        elif "|win|" in line:
            # Determine if winner
            winner = line.removeprefix("|win|").removesuffix("\n")
            outcome = "Winner" if winner == player_name else "Loser"

    player_elo = player_info[-1].strip("\n")
    lead_pokemon = (
        pokemon_switches[0] if len(pokemon_switches) else "None"
    )  # if lead_pokemon is None, then the battle ended before p1 sent out a Pokemon

    # Prints info to file
    return ",".join(
        [
            os.path.basename(file_path),
            player_name,
            player_elo,
            *player_pokemon,
            lead_pokemon,
            str(length),
            outcome,
        ]
    )


def main():
    out = [
        "BattleTag,Name,Elo,Pokemon1,Pokemon2,Pokemon3,Pokemon4,Pokemon5,Pokemon6,LeadPokemon,BattleLength,Outcome"
    ]
    for file_path in os.listdir("./dataset/showdown/raw"):
        out.append(battlelogs_to_csv("./dataset/showdown/raw/" + file_path))

    with open("./dataset/showdown/showdown.csv", "w", encoding="utf-8") as file_pointer:
        file_pointer.write("\n".join(out))


if __name__ == "__main__":
    main()
