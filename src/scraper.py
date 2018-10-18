import urllib2
from bs4 import BeautifulSoup
import os
import sys
#import boto3
import psycopg2
import datetime

DEBUG = True

# get main directory path
PATH = os.path.dirname(os.path.realpath(__file__))[:]

# open output file
try:
    os.chdir(PATH + "/test/")
except:
    if DEBUG: print("Output file folder doesn't exist, creating...")
    os.makedirs(PATH + "test/")
    os.chdir(PATH + "/test/")

try:
    csv_file = open("data.csv", 'a+')
    if DEBUG: print("Opened output file,")
except IOError as e:
    sys.exit( "Can't open output file. Path is " + os.path.dirname(os.path.realpath(__file__))[:] + " and base PATH is "+ PATH + "\nI/O error({0}): {1} ".format(e.errno, e.strerror))
except:
    sys.exit("Can't open output file. PATH is " + PATH + " Unexpected error: " + sys.exc_info()[0])

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
good_data = 0
caseNos = []
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

    # validate & clean up the datat
    row = []
    i = 0
    goodRow = True

    for td in tds:

        # check if data bad
        content = td.text.rstrip()
        if (
                content == 'NO OPINIONS FILED TODAY' or
                content == 'NO OPINIONS TODAY' or
                content in caseNos
            ):
            goodRow = False
            break

        # update unique id list
        if i == 1: caseNos.append(content)

        # reformat date
        isDate = False
        if content:
            isDate = len(content) > 7 and len(content) < content.find('/')> 0 and content.find('/') < 3 and content.find('/', 3) != -1 and content.find('/',3) < 7
        # put date in last column, properly formatted
        if isDate:
            content = datetime.datetime.strptime(content, '%m/%d/%Y').strftime('%Y-%m-%d')
            for n in range(i,7):
                if n == 6: row.append(content)
                else: row.append('')
        else:
            row.append(content)
        i += 1

    counter += 1
    if goodRow: caseTable.append(row)
    if DEBUG and (counter % 100 == 0): print("Processing row " + str(counter) + " into list.")

if DEBUG: print("Processed " + str(counter) + " rows of data, plus a header.")

# TODO verify that data is clean & tidy


# write data to file for now
import csv
writer = csv.writer(csv_file)
writer.writerows(caseTable)
csv_file.close()
if DEBUG: print("Data now in csv_file.")

# TODO write schema to md file

# If you're reading all of this, you should check this out:
# https://www.youtube.com/watch?v=LVyOWbrxjHM

# The following is taken from @stephenjwilson, who is a better man than I
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
HOST = os.getenv("POSTGRES_HOST")
USER = os.getenv("POSTGRES_USER")
PASS = os.getenv("POSTGRES_PASSWORD")

# from IPython import embed
# embed()
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
    # test data

    cur.execute("""INSERT INTO public.cases (CaseTitle, CaseNo, CaseOrigin, AuthoringJudge, CaseType, CaseCode, Datefiled)
            VALUES ('Nazim v. Nazim', '-7', 'Southern France', 'Unlearned Hand', '', '', '2050-01-01')
            ON CONFLICT (CaseNo) DO NOTHING;
            """)

    if DEBUG: print("Uploaded test data.")

    csv_file = open("data.csv", 'r')

    # Upload data
    copy_sql = """
               COPY {} FROM stdin WITH CSV HEADER
               DELIMITER as ','
               """.format('cases')
    cur.copy_expert(sql=copy_sql, file=csv_file)

    csv_file.close()

    if DEBUG: print("Uploaded csv file to DB. I'm done.")
except Exception as e:
    print(e)
    print("Upload to DB failed. I quit.")
conn.commit()
conn.close()
