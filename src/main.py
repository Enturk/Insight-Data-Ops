import urllib2
from bs4 import BeautifulSoup
import os
import sys
#import boto3
import psycopg2

DEBUG = True

# get main directory path
PATH = os.path.dirname(os.path.realpath(__file__))[:-3]

# open output file
try:
    os.chdir(PATH + "test/") 
except:
    if DEBUG: print("Output file folder doesn't exist, creating...")

if DEBUG: x = 'w+'
else: x = 'a+'
try:
    csv_file = open("data.csv", x)
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
schema = []
rightTable = False

for tr in soup.find_all('tr'):
    
    # process header
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
        rightTable = True
        caseTable = [] # delete earlier table stuff!
        if DEBUG: 
            print("Columns headers expected: " + str(length))
            print("Column headers processed: " + str(headCounter))
        counter += 1
        continue

    # moving on to rows
    tds = tr.find_all('td')
    
    # skip bad rows, because there are many of them
    if (not rightTable) or (len(tds) > len(schema)) or (len(tds) < len(schema)): 
        if DEBUG: print("Row starting with '" + tds[0].text + 
        "' breaks with schema, which has " + str(len(schema)) + " columns.")
        continue
    
    # clean up the data file, just in case something got through...
    row = []
    
    # if DEBUG: print("New record: ")
    for td in tds:
        # TODO trim tds[] elements?
        content = td.text.rstrip()
        # if DEBUG: print("  " + td.text)
        if content and not content.isspace(): # only appends non-empty data
            row.append(content) 
    
    counter += 1
    caseTable.append(row)
    if DEBUG and (counter%50 == 0): print("Processing row " + str(counter))
    
if DEBUG: print("Processed " + str(counter) + " rows of data, including a header.")

# TODO verify that data is clean & tidy


# write data to file for now
import csv
writer = csv.writer(csv_file)
writer.writerows(caseTable)
csv_file.close()

# TODO write schema to md file
# writer = csv.writer() #FIXME need filename and path
# writer.writerow(schema)

# The following is taken rom Stephen Wilson, who is a better man than I
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
HOST = os.getenv("POSTGRES_HOST")
if DEBUG: print("Host is: " + str(HOST))
USER = os.getenv("POSTGRES_USER")
PASS = os.getenv("POSTGRES_PASSWORD")
try: 
    conn = psycopg2.connect(host=HOST, dbname="patent_data",
                        user=USER, password=PASS)    
except:
    sys.exit("I am unable to connect to the database. I quit.")
    
# TODO Clean up data to fit table

# Create table
cur = conn.cursor()
# TODO make this with for loop over headers in schema
cur.execute("""
CREATE TABLE IF NOT EXISTS public.cases( 
    CaseTitle text,
    CaseNo text PRIMARY KEY,
    CaseOrigin text,
    AuthoringJudge text,
    CaseType text,
    CaseCode text,
    Datefiled date
)
""")

# Upload data
cur.copy_from(open(csv_file), 'public.cases', columns=('CaseTitle', 
                                                    'CaseNo', 
                                                    'CaseOrigin', 
                                                    'AuthoringJudge', 
                                                    'CaseType', 
                                                    'CaseCode',
                                                    'Datefiled')) # Bad camel case in source. Don't blame me.
conn.commit()
conn.close()