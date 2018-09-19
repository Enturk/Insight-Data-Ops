import urllib2
from bs4 import BeautifulSoup
import os
import sys

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
quote_page = 'https://www.ca9.uscourts.gov/opinions/'
page = urllib2.urlopen(quote_page)
soup = BeautifulSoup(page, 'html.parser')
#if DEBUG: print(soup.prettify())

# Parse the table
#TODO move into function
caseTable = []
headers = []
headerRow = True
line2 = True

for tr in soup.find_all('tr'):
    ths = tr.find_all('th')
    if (headerRow and ths):
        length = len(ths)
        if length < 3:
            continue
        if DEBUG: print("Column Headers:")
        counter = 0 
        for th in ths:
            label = th.text.rstrip()
            if label.isspace(): 
                length -= 1
                continue
            if DEBUG: print("  " + label)
            headers.append(label)
            counter += 1
            headerRow = False
        if DEBUG: 
            print("Columns headers expected: " + str(length))
            print("Column headers processed: " + str(counter))
        continue
    
    tds = tr.find_all('td')
    row = []
    # print("New record: ")
    for td in tds:
        # TODO trim tds[] elements
        content = td.text.rstrip()
        if content.isspace(): continue
        # print("  " + td.text)
        if content: row.append(content) # only appends non-empty lists
    caseTable.append(row)