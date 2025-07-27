import argparse
import textwrap
import re
import sys
import os
from pprint import pprint


def battlelogs_to_csv(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file_pointer:
        lines = file_pointer.readlines()

    lines = map(lambda line: line.removesuffix("\n"), lines)
    lines = filter(lambda line: line != "|", lines)

    # Tokenize the lines
    # (Split them into lists of tokens and ensure these lists and tokens are not empty)
    tokenized_data = filter(
        lambda token_list: token_list,
        map(lambda line: list(filter(lambda token: token, line.split("|"))), lines),
    )

    """
    At this stage, a log like
    ```
    |j|☆firelit nights
    |player|p1|firelit nights|26|1541
    ```
    will be stored in tokenized_data as
    [
        ['j','☆firelit nights'],
        ['player','p1','firelit nights','26','1541']
    ]
    """

    """
    Generate a battle dict.
    We turn each entry [item_x, ...] into {item_x: [[...]]}
    and any succeeding entry [item_x, ...2] will add onto its corresponding list
    (i.e. {item_x: [[...], [...]]} )
    """
    battle = {}
    for item in tokenized_data:
        if item[0] not in battle.keys():
            battle.update({item[0]: []})
        battle[item[0]] += [item[1:]]

    """
    We now clean up the battle dictionary a little bit
    """
    CAPTURED_KEYS = [
        "player",
        "poke",
        "win",
        "switch",
        "raw",
        "turn",
        "move",
    ]
    [battle.pop(key) for key in battle.keys() - CAPTURED_KEYS]

    battle["tag"] = (
        file_path.split("/")[-1].removeprefix("gen5ou-").removesuffix(".log")
    )
    battle["turncount"] = battle.pop("turn")[-1][0] if "turn" in battle.keys() else "0"

    # Filter only player 1's name and pokemon
    is_p1 = lambda entry: entry[0] == "p1"
    battle["player"] = list(filter(is_p1, battle["player"]))[0][1]
    battle["poke"] = list(
        map(lambda entry: entry[1].split(",")[0], filter(is_p1, battle["poke"]))
    )

    """
    Extract lead Pokemon by getting the first switch in.
    If None, the battle ended prematurely.
    """
    if "switch" in battle.keys():
        battle["lead"] = battle.pop("switch")[0][1].split(",")[0]
    else:
        battle["lead"] = "None"

    # Determine if the player won
    if "win" in battle.keys():
        battle["outcome"] = (
            "win" if battle.pop("win")[0][0] == battle["player"] else "lose"
        )
    else:
        battle["outcome"] = "tie"

    # Extract elo from `raw`
    battle["raw"] = list(filter(lambda entry: "rating" in entry[0], battle["raw"]))
    battle["elo"] = battle.pop("raw")[0][0].split("rating: ")[1].split()[0]

    # Extract moves
    try:
        battle["move"] = set(
            map(
                lambda move_entry: (move_entry[0].removeprefix("p1a: "), move_entry[1]),
                filter(lambda move_entry: "p1a: " in move_entry[0], battle["move"]),
            )
        )

        # battle["move"] is a set of tuples (Pokemon, Move)
        # We turn this into a list since we want the end product to be a dataframe
        moves = [[] for _ in range(6)]
        for poke_target, move in battle["move"]:
            # We manually search instead of using `index` because Landorus-Therian is reported as Landorus
            for index, poke_name in enumerate(battle["poke"]):
                if poke_target in poke_name:
                    moves[index].append(move)
                    break

        for entry in moves:
            while len(entry) < 4:
                entry.append("None")
            try:
                assert len(entry) == 4
            except AssertionError:
                print(len(entry), battle["tag"], battle["moves"])

    except KeyError:
        # No moves, player probably disconnected
        moves = [["None"] * 4] * 6

    moves = ",".join([",".join(entry) for entry in moves])

    # Weather
    RAIN = 0
    SAND = 1
    weather = ["0", "0"]
    if "Politoed" in battle["poke"] and any(
        ("Tentacruel" in battle["poke"], "Thundurus-Therian" in battle["poke"])
    ):
        weather[SAND] = "1"

    if "Tyranitar" in battle["poke"] and any(
        ("Alakazam" in battle["poke"], "Landorus-Therian" in battle["poke"])
    ):
        weather[RAIN] = "1"

    # Finally, we return a line of csv
    retval = ",".join(
        [
            battle["tag"],
            battle["player"],
            battle["elo"],
            *battle["poke"],
            battle["lead"],
            battle["turncount"],
            battle["outcome"],
        ]
        + [moves]
        + weather
    )
    return retval


def main():
    headers = [
        "Tag",
        "Player",
        "Elo",
        *[f"Pokemon {i}" for i in range(1, 7)],  # Pokemon 1, 2, 3, ..., 6
        "LeadPokemon",
        "TurnCount",
        "Result",
        *[
            f"Pokemon {i} Move {j}" for i in range(1, 7) for j in range(1, 5)
        ],  # Pokemon I Move J
        *[f"Weather-{weather_type}" for weather_type in ["Rain", "Sand"]],
    ]
    print(headers)
    out = [",".join(headers)]
    file_paths = os.listdir("./dataset/showdown/raw")
    file_count = len(file_paths)
    for i, file_path in enumerate(file_paths):
        out.append(battlelogs_to_csv("./dataset/showdown/raw/" + file_path))
        if i % 1000 == 0:
            print(f"Processed {i}/{file_count} files")

    with open("./dataset/showdown/showdown.csv", "w", encoding="utf-8") as file_pointer:
        file_pointer.write("\n".join(out))


if __name__ == "__main__":
    main()
