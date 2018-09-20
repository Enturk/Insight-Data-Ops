import urllib2
from bs4 import BeautifulSoup
import os
import sys
from dotenv import dotenv_values

HOST = os.getenv("POS")

DEBUG = True

# get main directory path
PATH = os.path.dirname(os.path.realpath(__file__))[:-3]

# open output file
# try:
#     os.chdir(PATH + "Unused/") 
# except:
#     if DEBUG: print("Output file folder doesn't exist, creating...")

# if DEBUG: x = 'a+'
# else: x = 'w+'
# try:
#     o = open("sessionization.txt", x)
#     if DEBUG: print("Opened output file,")
# except:
#     sys.exit("  Couldn't open output file.")


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
    
    headers = []
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
            headers.append(label)
            headCounter += 1
            headerRow = False
        if DEBUG: 
            print("Columns headers expected: " + str(length))
            print("Column headers processed: " + str(headCounter))
        caseTable.append(headers)
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