#!/bin/bash

# cd otherwise at /
cd ~

# install necessary things
sudo apt-get update
# sudo apt-get -y upgrade # local grub package needs to be kept as-is, so maybe don't run
sudo apt-get install python-pip -y
pip install BeautifulSoup4
pip install boto3
pip install -U python-dotenv
pip install psycopg2
pip install psycopg2-binary

# do the thing we're her to do
cd /usr/src/
wget https://raw.githubusercontent.com/Enturk/Insight-Data-Ops/master/src/scraper.py
python scraper.py
