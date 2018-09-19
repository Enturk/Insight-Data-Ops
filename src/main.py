import urllib2
from bs4 import BeautifulSoup
DEBUG = True

quote_page = 'https://www.ca9.uscourts.gov/opinions/'
page = urllib2.urlopen(quote_page)
soup = BeautifulSoup(page, 'html.parser')
#if DEBUG: print(soup.prettify())

# Parse the table
caseTable = []
for tr in soup.find_all('tr')[2:]:
    tds = tr.find_all('td')
    length = len(tds)
    row = []
    for td in tds:
        # TODO trim tds[] elements
        print(td.text)
        row.append(td.text)
    caseTable.append(row)
# if (DEBUG && name_box==None): print("name_box is empty.")
# name = name_box.text.strip() # strip() is used to remove starting and trailing
# print name
