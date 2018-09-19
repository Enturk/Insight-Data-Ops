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
secondRow = False
line2 = True

for tr in soup.find_all('tr'):
    if headerRow:
        ths = tr.find_all('th')
        length = len(ths) # TODO is this used?
        if DEBUG: print("Number of columns: " + str(length))
        if DEBUG: print("Column Headers:")
        for th in ths:
            counter = 0 
            label = th.text.rstrip()
            if label.isspace(): 
                length -= 1
                continue
            if DEBUG: print("  " + label)
            headers.append(label)
            counter += 1
        headerRow = False
        secondRow = True
        if DEBUG: print("Column Headers processed: " + str(counter))
        continue
    
    tds = tr.find_all('td')
   
    if secondRow:
        length = len(tds) # TODO is this used?
        if DEBUG: print("Number of columns in second row: " + str(length))
        if DEBUG: print("Second row headers:")
        for td in tds:
            counter = 0 
            label = td.text.rstrip()
            if label.isspace(): continue
            if DEBUG: print("  " + label)
            headers.append(label)
            counter += 1
        secondRow = False
        if DEBUG: print("Second row headers processed: " + str(counter))
        continue

    
    row = []
    # print("New record: ")
    for td in tds:
        # TODO trim tds[] elements
        content = td.text.rstrip()
        if content.isspace(): continue
        # print("  " + td.text)
        row.append(content)
    caseTable.append(row)

