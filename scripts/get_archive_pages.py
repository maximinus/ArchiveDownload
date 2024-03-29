#!/usr/bin/env python3

import os
#!/usr/bin/env python3

import sys
import json
import requests
import time
from tqdm import tqdm
from datetime import date
from bs4 import BeautifulSoup
from get_etree_links import ETREE_FOLDER

# if the file shows.json has been generated by get_etree_links.py, you can call this to
# grab all the archive pages.
# this will take some time!

# you can run the code again if some pages fail: pages already obtained will not be re-downloaded

ARCHIVE_FOLDER = './data/archive_source'
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0'}


# we have a page of archive links, grab all the pages and extract the data
def getArchivePageData(url):
    # perform a GET on this url if we don't have it
    # return False if the page could not be found or obtained
    filename = f"{ARCHIVE_FOLDER}/{url.split('/')[-1]}.html"
    if os.path.isfile(filename):
        return True
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f'* HTTP {response.status_code}: {url}')
        return False
    # save for later
    with open(filename, 'w') as page_file:
        page_file.write(response.text)
        return True


def grabAllArchiveLinks():
    # load the json file
    data = []
    failed = []
    with open(f'{ETREE_FOLDER}/shows.json') as json_file:
        data = json.load(json_file)
    print(' * Extracting all shows')
    for show_url in tqdm(data):
        if getArchivePageData(show_url) == False:
            failed.append(show_url)
    return failed


if __name__ == '__main__':
    # download all the archive pages
    fails = grabAllArchiveLinks()
    # save as json
    with open('./data/fails.json', 'w') as json_file:
        json.dump(fails, json_file, indent=4)
