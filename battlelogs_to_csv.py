import argparse
import textwrap
import re
import sys
import os
import chardet

def battlelogs_to_csv(file_path: str, encode):
    with open("./logs/"+file_path, "r", encoding=encode) as file_pointer:
        lines = file_pointer.readlines()

        # Searches for the player info line. This contains both the player name and the elo.
        containing_player_info = [x for x in lines if "|player|p1|" in x][0].split("|")

        player_name = containing_player_info[3]
        player_elo = containing_player_info[-1][:containing_player_info[-1].find("\n")]

        # Searches list of pokemon of the team.
        containing_player_pkmn = [x.split("|")[3].split(",")[0].strip() for x in lines if "|poke|p1|" in x]

        # Searches for the lead pokemon.
        containing_lead_pkmn = [x.split("|")[3].split(",")[0] for x in lines if "|switch|" in x][0]
        
        # Searches for the number of turns

        length = len([x for x in lines if "|turn|" in x])

        # Searches for the winner.
        if len([x for x in lines if "|win|" in x]) == 0:
            outcome ="Tie"
        else:
            winner = [x for x in lines if "|win|" in x][0].split("|")[2]
            if winner == player_name:
                outcome = "Winner"
            else:
                outcome = "Loser"

        # Prints info to file
        print(",".join([player_name,
                        ""+player_elo,containing_player_pkmn[0],
                        containing_player_pkmn[1],
                        containing_player_pkmn[2],
                        containing_player_pkmn[3],
                        containing_player_pkmn[4],
                        containing_player_pkmn[5],
                        containing_lead_pkmn,
                        str(length),
                        outcome]))


def main():
    parser = argparse.ArgumentParser(
        prog="Smogon2CSV",
        description=textwrap.dedent(
            """\
            This is a helper script that transforms Smogon data into .csv format
            which will in turn be converted into a pandas dataframe in
            `phase-1.ipynb`.

            By default, outptut is printed to stdout; use redirection to save it
            in a .csv file.

            Sample usage:
            `python ./smogon-to-csv.py --input ./dataset/raw2016-01-gen1ou-0.txt > ./dataset/2016-01-gen1ou-0.csv`
            """
        ),
    )
    parser.add_argument("-i", "--input", help="Input file")
    args = parser.parse_args()

    for file in os.listdir("./logs"):
        with open("./logs/" + file, "rb") as F:
            encode = chardet.detect(F.read())['encoding']
            battlelogs_to_csv(file, encode)

if __name__ == "__main__":
    main()
