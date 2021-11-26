from ftplib import FTP
import os
import re
import requests

from bs4 import BeautifulSoup
import pandas as pd

"""
This script executes the same behavior as [raw_life_table_extraction.py], but
gives files more interpretable names.

Files are saved in [named_life_tables_data] with the same subdirectory system
as in [raw_life_tables_data]. Individual files are named according to the title
in the first row of each table.
"""

# Prepare regular expression patterns
year_pat = re.compile("\d{4}")
title_pat = re.compile("[\W^ ]+")

# Verify that data directory has not been created yet
if os.path.isdir("named_life_tables_data"):
    print("Directory [named_life_tables_data] already exists - are you sure "
          + "that this is the first time you're running this script?")
    exit(1)

# Dig through data portal page
print("Accessing data portal...")
portal_url = "https://www.cdc.gov/nchs/nvss/life-expectancy.htm"
portal_page = requests.get(portal_url)
if portal_page.status_code == 200:
    # Isolate table
    print("Eating soup...")
    soup = BeautifulSoup(portal_page.content, features="lxml")
    table = soup.find("table")
    entries = table.find_all("a")

    # Iterate through entries of table
    for entry in entries:
        # Extract FTP server information from entry
        year = entry.contents[0]
        dissected_href = entry["href"].split("/", 3)
        ftp_url = dissected_href[2]
        ftp_dir = dissected_href[3][:-1]

        # Access FTP server
        ftp = FTP(ftp_url)
        ftp.login()
        ftp.cwd(ftp_dir)

        # Download files
        print("Downloading files for " + year + ":")
        os.makedirs("named_life_tables_data/" + year)
        for fname in ftp.nlst():
            print("\t" + fname)
            # Get file type
            ftype = fname.split(".")[-1]

            # Write file to temporary location
            with open("tmp." + ftype, "wb") as fp:
                ftp.retrbinary("RETR " + fname, fp.write)

            # Get in-document title
            df = pd.read_excel("tmp." + ftype, header=None)
            ftitle = df[0][0]

            # Remove temporary file
            os.remove("tmp." + ftype)

            # Clean title
            clean_title = title_pat.sub(" ", ftitle).strip()

            # Write file to permanent location
            with open("named_life_tables_data/" + year + "/" + clean_title + "." + ftype, "wb") as final_path:
                ftp.retrbinary("RETR " + fname, final_path.write)

        # Close FTP server connection
        ftp.quit()
else:
    print("Portal page returned status", portal_page.status_code)
