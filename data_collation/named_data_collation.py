import os

import pandas as pd

"""
This script collates the data in [named_life_tables_data] into a single
comprehensive [.csv] file.

NOTE: this script should not be used until [named_life_table_extraction.py] has
already been run.
"""

# Verify that data directory has been created
if not os.path.isdir("named_life_tables_data"):
    print("Directory [named_life_tables_data] does not exist - please run "
          + "[named_life_table_extraction.py] first.")
    exit(1)

# Verify that data file has not been created yet
if os.path.exists("life_tables_master.csv"):
    print("File [life_tables_master.csv] already exists - are you sure "
          + "that this is the first time you're running this script?")
    exit(1)


# Define new master dataframe for collated data
cols = ["Year", "Demographic", "Sex", "Age Range",
        "q(x)", "l(x)", "d(x)", "L(x)", "T(x)", "e(x)"]
master_df = pd.DataFrame(columns=cols)

# Define mappings of table number to demographic and sex
table_numbers = {
    "1": ("total", "total"),
    "2": ("total", "male"),
    "3": ("total", "female"),
    "4": ("white", "total"),
    "5": ("white", "male"),
    "6": ("white", "female"),
    "7": ("black", "total"),
    "8": ("black", "male"),
    "9": ("black", "female")
}

# Iterate over years
for year in sorted(os.listdir("named_life_tables_data")):
    # Ignore summary file
    if year == "summary.txt":
        continue
    print("Collating ", year, ":", sep="")
    encountered_numbers = []
    # Iterate over tables
    for table_name in sorted(os.listdir(os.path.join("named_life_tables_data", str(year)))):
        # Skip irrelevant files (duplicates of existing information)
        table_number = table_name.split()[1]
        if not table_number in table_numbers.keys() or table_number in encountered_numbers:
            continue

        # Record table number
        encountered_numbers.append(table_number)
        print("\tTable", table_number)

        # Extract table demographic and sex
        table_demographic, table_sex = table_numbers[table_number]

        # Load table
        table_df = pd.read_excel(os.path.join("named_life_tables_data", str(
            year), table_name), header=(2 if int(year) > 2010 else 6))

        # Drop citation row in relevant tables (why would they include this in the first place???)
        if int(year) > 2010:
            table_df.drop(table_df.tail(1).index, inplace=True)

        # Iterate through table rows
        for _, table_row in table_df.iterrows():
            # Add row to master dataframe
            master_df = master_df.append(dict(zip(cols, [
                year, table_demographic, table_sex] + table_row.tolist())), ignore_index=True)

# Write master dataframe to a csv
master_df.to_csv("life_tables_master.csv")
print("Done!")
