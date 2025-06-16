import argparse
import textwrap


def smogon_to_csv(file_path: str) -> str:
    with open(file_path, "r") as file_pointer:
        lines = file_pointer.readlines()
    # Remove everything but the headers and raw data
    lines = [lines[3]] + lines[5:-1]
    # Clean each line
    lines = list(
        map(
            lambda line: line.removeprefix(" |")
            .removesuffix("| \n")
            .replace("|", ",")
            .replace(" ", ""),
            lines,
        )
    )
    return "\n".join(lines)


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
    out_csv = smogon_to_csv(args.input)
    print(out_csv)


if __name__ == "__main__":
    main()
