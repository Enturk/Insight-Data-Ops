import urllib2
from bs4 import BeautifulSoup
import os
import sys
#import boto3
import psycopg2

DEBUG = True

# get main directory path
PATH = os.path.dirname(os.path.realpath(__file__))[]

# open output file
try:
    os.chdir(PATH + "test/")
except:
    if DEBUG: print("Output file folder doesn't exist, creating...")
    os.makedirs(PATH + "test/")

try:
    csv_file = open("data.csv", 'r+')
    if DEBUG: print("Opened output file,")
except IOError as e:
    sys.exit( "Can't open output file. Path is " + PATH + " I/O error({0}): {1} ".format(e.errno, e.strerror))
except:
    sys.exit("Can't open output file. Path is " + PATH + " Unexpected error: " + sys.exc_info()[0])

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
        if DEBUG: print("Discarding row starting with " + tds[0].text +
        "because it has " + str(len(tds)) + " columns, and breaks with schema, which has "
        + str(len(schema)) + " columns.")
        continue

    # clean up the data list, just in case something got through...
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
    if DEBUG and (counter%100 == 0): print("Processing row " + str(counter) + " into list.")

if DEBUG: print("Processed " + str(counter) + " rows of data, plus a header.")

# TODO verify that data is clean & tidy


# write data to file for now
import csv
writer = csv.writer(csv_file)
writer.writerows(caseTable)
if DEBUG: print("Data now in csv_file.")

# TODO write schema to md file
# writer = csv.writer() #FIXME need filename and path
# writer.writerow(schema)

# If you're really reading all of this, you should check this out:
# https://www.youtube.com/watch?v=LVyOWbrxjHM

# The following is taken rom Stephen Wilson, who is a better man than I
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
HOST = os.getenv("POSTGRES_HOST")
USER = os.getenv("POSTGRES_USER")
PASS = os.getenv("POSTGRES_PASSWORD")

from IPython import embed
embed()
try:
    if DEBUG: print("Attempting connection with host: " + str(HOST))
    # note: make sure DB accepts incoming data from this IP
    # on c9, check ip with: wget http://ipinfo.io/ip -qO -
    conn = psycopg2.connect(host=HOST, dbname="Circuit9",
                        user=USER, password=PASS)
    if DEBUG: print("   Connected!")
except:
    sys.exit("I am unable to connect to the database. I quit.")

# TODO Clean up data to fit table

# Create table
cur = conn.cursor()
# TODO make this with for loop over headers in schema
# TODO need primary key!
try:
    cur.execute("""
    CREATE TABLE IF NOT EXISTS public.cases(
        CaseTitle text,
        CaseNo text,
        CaseOrigin text,
        AuthoringJudge text,
        CaseType text,
        CaseCode text,
        Datefiled date
    )
    """)

    # Upload data
    cur.copy_from(csv_file, 'public.cases', sep=',', columns=('CaseTitle',
                                                        'CaseNo',
                                                        'CaseOrigin',
                                                        'AuthoringJudge',
                                                        'CaseType',
                                                        'CaseCode',
                                                        'Datefiled')) # Bad camel case in source. Don't blame me.
    if DEBUG: print("Uploaded csv file to DB. I'm done.")
except:
    print("Upload to DB failed. I quit.")
conn.commit()
conn.close()
csv_file.close()
