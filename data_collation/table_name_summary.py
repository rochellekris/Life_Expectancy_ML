import os


"""
This script creates a text file, [named_life_tables_data/summary.txt], which
summarizes the contents of [named_life_tables_data] by listing the names
of all files on a single page. File names are sorted by table number.

NOTE: this script should not be used until [named_life_table_extraction.py] has
already been run.
"""


def key_func(s):
    # Key function - yes I know this is a stupid way to process roman numerals
    s_key = s.split()[1]
    if s_key.isnumeric():
        return int(s_key)
    elif s_key == "I":
        return 91
    elif s_key == "II":
        return 92
    elif s_key == "III":
        return 93
    elif s_key == "IV":
        return 94
    elif s_key == "V":
        return 95
    elif s_key == "VI":
        return 96
    elif s_key == "VII":
        return 97
    elif s_key == "VIII":
        return 98
    elif s_key == "IX":
        return 99


# Verify that data directory has been created
if not os.path.isdir("named_life_tables_data"):
    print("Directory [named_life_tables_data] does not exist - please run "
          + "[named_life_table_extraction.py] first.")
    exit(1)

# Delete summary file if it exists
if os.path.exists("named_life_tables_data/summary.txt"):
    os.remove("named_life_tables_data/summary.txt")

# Get structure of life tables
years = os.listdir("named_life_tables_data")
named_file_dict = {year: [os.path.join("named_life_tables_data", year, f) for f in os.listdir(
    os.path.join("named_life_tables_data", year))] for year in years}

# Write file names in summary file
with open("named_life_tables_data/summary.txt", "wb") as fp:
    num_files = sum(len(named_file_dict[key]) for key in named_file_dict)
    fp.write(bytes("Total number of files:\t" +
                   str(num_files) + "\n\n", encoding="utf8"))
    for key in range(2001, 2018):
        fp.write(bytes(str(key) + "\n", encoding="utf8"))
        for name in sorted(named_file_dict[str(key)], key=key_func):
            fp.write(bytes("\t" + name.split("/")[-1] + "\n", encoding="utf8"))
