#!/usr/bin/env python3

import os
import sys
import json
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

# grab all links from etree and put them into one file
# they are all placed in the following folder

ETREE_FOLDER = './data/etree_links'
ETREE_BASE_URL = 'https://db.etree.org/db/shows/browse/artist_key/2/year/'

# fake a real browser in the headers
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0'}


# code to download and extract data from etree
def getEtreeYear(year):
    url = f'{ETREE_BASE_URL}{year}'
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.text
    else:
        return ''

def getEtreeData():
    print('* Obtaining Etree list')
    for i in tqdm(range(1965, 1996)):
        data = getEtreeYear(i)
        with open(f'{ETREE_FOLDER}/year_{i}.html', 'w') as page_file:
            page_file.write(data)

def extractEtreeYear(year):
    # load the page, insert into bs4
    print('* Extracting archive links from etree years')
    with open(f'{ETREE_FOLDER}/year_{year}.html', 'r') as page_file:
        data = page_file.read()
    soup = BeautifulSoup(data, features='html.parser')
    # get the first table you see
    table = soup.find('table')
    # grab all the TR's in that table except the first
    shows = table.findAll('tr')[1:]
    # tds from first to last are:
    # etree link, venue, city, state, download, add link, etree sources
    # we only want the links
    show_links = []
    for show in shows:
        downloads = show.findAll('td')[4]
        # we need all the links
        links = downloads.findAll('a')
        for l in links:
            # save the archive ones. grab the href
            show_link = l['href']
            if ARCHIVE_URL in show_link:
                # store the link
                show_links.append(show_link)
    return(show_links)

def getEtreeArchiveLinks():
    # grab all etree links and make a json file of the archive links
    getEtreeData()
    archive_links = []
    for i in tqdm(range(1965, 1996)):
        new_data = extractEtreeYear(i)
        archive_links.extend(new_data)
    # save the data
    print('Saving...')
    with open(f'{ETREE_FOLDER}/shows.json', 'w') as json_file:
        json.dump(archive_links, json_file, indent=4)


if __name__ == '__main__':
    # download all the etree data and place it as a json file
    # ETREE_FOLDER/shows.json
    getEtreeArchiveLinks()
