import urllib2
from bs4 import BeautifulSoup
import os
import sys
from dotenv import load_dotenv, find_dotenv
import boto3
import psycopg2

# TODO fix these
load_dotenv(find_dotenv())
HOST = os.getenv("POSTGRES_HOST")
USER = os.getenv("POSTGRES_USER")
PASS = os.getenv("POSTGRES_PASSWORD")
conn = psycopg2.connect(host=HOST, dbname="patent_data",
                        user=USER, password=PASS)    

DEBUG = True

# get main directory path
PATH = os.path.dirname(os.path.realpath(__file__))[:-3]

# open output file
try:
    os.chdir(PATH + "Unused/") 
except:
    if DEBUG: print("Output file folder doesn't exist, creating...")

if DEBUG: x = 'a+'
else: x = 'w+'
try:
    csv_file = open("sessionization.txt", x)
    if DEBUG: print("Opened output file,")
except:
    sys.exit("  Couldn't open output file.")


# 9th circuit federal court of appeals
quote_page = 'https://www.ca9.uscourts.gov/opinions/index.php?per_page=1000'
page = urllib2.urlopen(quote_page)
soup = BeautifulSoup(page, 'html.parser')
#if DEBUG: print(soup.prettify())

# Parse the table
#TODO move into function
caseTable = []
headerRow = True
counter = 0 

for tr in soup.find_all('tr'):
    
    schema = []
    ths = tr.find_all('th')
    if (headerRow and ths):
        headCounter = 0
        length = len(ths)
        if length < 3:
            continue
        if DEBUG: print("Column Headers:")
        for th in ths:
            label = th.text.rstrip()
            if label.isspace(): 
                length -= 1
                continue
            if DEBUG: print("  " + label)
            schema.append(label)
            headCounter += 1
            headerRow = False
        if DEBUG: 
            print("Columns headers expected: " + str(length))
            print("Column headers processed: " + str(headCounter))
        counter += 1
        continue
    
    tds = tr.find_all('td')
    row = []
    # print("New record: ")
    for td in tds:
        # TODO trim tds[] elements
        content = td.text.rstrip()
        if content.isspace(): continue
        # print("  " + td.text)
        if content: 
            row.append(content) # only appends non-empty lists
    
    counter += 1
    caseTable.append(row)
    if DEBUG: print("Processing row " + str(counter))
    
    
if DEBUG: print("Processed " + str(counter) + " rows of data, including a header.")
    
# send it to the RDS
# Create table
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS Circuit9(
    patnum text PRIMARY KEY,
    filedate date,
    title text,
    grantdate date,
    owner text,
    city text,
    state text,
    country text,
    class text,
    ipc text
)
""")

# Upload data

cur.copy_from(open(csv_file), 'patents', columns=('patnum', 'filedate', 'title', 'grantdate', 'owner', 'city',
                                                  'state', 'country', 'class', 'ipc'))
conn.commit()
conn.close()