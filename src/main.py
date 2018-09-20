import urllib2
from bs4 import BeautifulSoup
import os
import sys
from dotenv import load_dotenv, find_dotenv
#import boto3
import psycopg2

DEBUG = True

# get main directory path
PATH = os.path.dirname(os.path.realpath(__file__))[:-3]

# open output file
try:
    os.chdir(PATH + "tools/") 
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
        caseTable = [] # delete earlier table stuff!
        if DEBUG: 
            print("Columns headers expected: " + str(length))
            print("Column headers processed: " + str(headCounter))
        counter += 1
        continue

    tds = tr.find_all('td')
    
    # skip until right table
    # if not rightTable:
    #     for td in tds:
    #         if td.text[:7] == "Results:" :
    #             rightTable = True
    #             break
    #     continue

    # skip weird rows, because there are many of them
    if (len(tds) > len(schema)) or (len(tds) + 3 < len(schema)): 
        if DEBUG: print("Row starting with '" + tds[0].text + 
        "' breaks with schema, which has " + str(len(schema)) + " columns.")
        continue

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
    if DEBUG and (counter%50 == 0): print("Processing row " + str(counter))
    
if DEBUG: print("Processed " + str(counter) + " rows of data, including a header.")

# clean up data


# write data to file for now
import csv
writer = csv.writer(csv_file)
# writer.writerow(schema) #TODO what do we do with this?
writer.writerows(caseTable)

# TODO fix these
# load_dotenv(find_dotenv())
# HOST = os.getenv("POSTGRES_HOST")
# USER = os.getenv("POSTGRES_USER")
# PASS = os.getenv("POSTGRES_PASSWORD")
# conn = psycopg2.connect(host=HOST, dbname="patent_data",
#                         user=USER, password=PASS)    
 
# TODO Clean up data to fit table


# Create table
# cur = conn.cursor()
# cur.execute("""
# CREATE TABLE IF NOT EXISTS Circuit9( # TODO make this with for header in schema
#     CaseTitle text,
#     CaseNo. text PRIMARY KEY,
#     CaseOrigin text,
#     AuthoringJudge text,
#     CaseType text,
#     CaseCode text,
#     Datefiled date,
# )
# """)

# # Upload data
# cur.copy_from(open(csv_file), 'patents', columns=('CaseTitle', 
#                                                     'CaseNo.', 
#                                                     'CaseOrigin', 
#                                                     'AuthoringJudge', 
#                                                     'CaseType', 
#                                                     'CaseCode',
#                                                     'Datefiled'))
# conn.commit()
# conn.close()