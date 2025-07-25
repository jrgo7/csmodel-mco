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
    CAPTURED_KEYS = ["poke"]
    [battle.pop(key) for key in battle.keys() - CAPTURED_KEYS]

    battle["tag"] = (
        file_path.split("/")[-1].removeprefix("gen5ou-").removesuffix(".log")
    )

    battle["poke"] = list(
        map(lambda entry: entry[1].split(",")[0], battle["poke"])
    )

    # Finally, we return a line of csv

    retval = ",".join(
        [
            battle["tag"],
            *battle["poke"],
        ]
    ) 
    return retval


def main():
    print("hello")
    headers = [
        "Tag",
        *[f"Player {i} Pokemon {j}" for i in (1, 2) for j in range(1, 7)],  # Pokemon 1, 2, 3, ..., 6
    ]
    print(headers)
    out = [",".join(headers)]
    file_paths = os.listdir("./dataset/showdown/raw")
    file_count = len(file_paths)
    for i, file_path in enumerate(file_paths):
        out.append(battlelogs_to_csv("./dataset/showdown/raw/" + file_path))
        if i % 1000 == 0:
            print(f"Processed {i}/{file_count} files")

    with open("./dataset/showdown/showdown_2players.csv", "w", encoding="utf-8") as file_pointer:
        file_pointer.write("\n".join(out))


if __name__ == "__main__":
    main()
