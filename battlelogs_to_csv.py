import argparse
import textwrap
import re
import sys
import os


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
    CAPTURED_KEYS = ["player", "poke", "win", "switch", "raw", "turn"]
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

    # Finally, we return a line of csv
    return ",".join(
        [
            battle["tag"],
            battle["player"],
            battle["elo"],
            *battle["poke"],
            battle["lead"],
            battle["turncount"],
            battle["outcome"],
        ]
    )


def main():
    headers = [
        "Tag",
        "Player",
        "Elo",
        *[f"Pokemon {i}" for i in range(1, 7)], # Pokemon 1, 2, 3, ..., 6
        "LeadPokemon",
        "TurnCount",
        "Result",
    ]
    out = [",".join(headers)]
    file_paths = os.listdir("./dataset/showdown/raw")
    file_count = len(file_paths)
    for i, file_path in enumerate(file_paths):
        print(f"Processed {i+1}/{file_count} files")
        out.append(battlelogs_to_csv("./dataset/showdown/raw/" + file_path))

    with open("./dataset/showdown/showdown.csv", "w", encoding="utf-8") as file_pointer:
        file_pointer.write("\n".join(out))


if __name__ == "__main__":
    main()
