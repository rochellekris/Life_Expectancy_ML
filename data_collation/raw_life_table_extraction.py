from ftplib import FTP
import os
import requests

from bs4 import BeautifulSoup

"""
This script downloads life table data from the following URL:
https://www.cdc.gov/nchs/nvss/life-expectancy.htm#data

Data, comprised of [.xls] and [.xlsx] files, is saved in the newly created
directory [raw_life_tables_data] and sorted into subdirectories according to
their corresponding years. Note that individual files retain their names from
within the FTP database.
"""

# Verify that data directory has not been created yet
if os.path.isdir("raw_life_tables_data"):
    print("Directory [raw_life_tables_data] already exists - are you sure "
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
        os.makedirs("raw_life_tables_data/" + year)
        for file_name in ftp.nlst():
            with open("raw_life_tables_data/" + year + "/" + file_name, "wb") as fp:
                ftp.retrbinary("RETR " + file_name, fp.write)
        print("Files for", year, "downloaded!")

        # Close FTP server connection
        ftp.quit()
else:
    print("Portal page returned status", portal_page.status_code)
