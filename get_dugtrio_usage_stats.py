import requests
import os

gen5ou_stats_url = (
    lambda year, month: f"https://www.smogon.com/stats/{year}-{month:0>2}/gen5ou-0.txt"
)
save_path = lambda year, month: f"dataset/smogon/raw/{year}-{month:0>2}-gen5ou-0.txt"
csv_out = "Date,Rank,Pokemon,Usage%,Raw,Raw%,Real,Real%\n"

for year in range(2014, 2022):
    for month in range(1, 13):
        # Start at 2014-11
        if year == 2014 and month < 11:
            continue
        
        print(year, month)

        # If no .txt file then download it
        if save_path(year, month).split("/")[-1] not in os.listdir(
            "dataset/smogon/raw"
        ):
            url = gen5ou_stats_url(year, month)
            response = requests.get(url)
            with open(save_path(year, month), "w") as file_pointer:
                file_pointer.write(response.text)

        # Get Dugtrio specifically
        with open(save_path(year, month), "r") as file_pointer:
            lines = file_pointer.readlines()

        try:
            dugtrio_line: str = list(filter(lambda line: "Dugtrio" in line, lines))[0]
            row = list(filter(lambda entry: entry, dugtrio_line.removesuffix("\n").replace(" ", "").split("|")))
            csv_out += f"{year}-{month:0>2},{','.join(row)}\n"
        except IndexError:
            # No Dugtrio
            csv_out += f"{year}-{month:0>2},0,Dugtrio,0%,0,0%,0,0%\n"

print(csv_out)

with open("dataset/smogon/dugtrio.csv", 'w') as file_pointer:
    file_pointer.write(csv_out)