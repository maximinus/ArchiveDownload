#!/usr/bin/env python3

import os
from tqdm import tqdm
from bs4 import BeautifulSoup

SHOW_DIR = './data/archive_source/90s'
from gd_data import Show, Track

# load the archive files and extract the data

def extractPageData(page):
    # parse the HTML to get the links
    soup = BeautifulSoup(page, features='html.parser')
    main_wrap = soup.find('div', {'id': 'theatre-ia-wrap'})
    # now find the tracks in this
    tracks = main_wrap.findAll('div', {'itemprop':'track'})
    songs = []
    order = 1
    for t in tracks:
        name = t.find('meta', {'itemprop': 'name'})['content']
        duration = t.find('meta', {'itemprop': 'duration'})['content']
        links = [x['href'] for x in t.findAll('link')]
        songs.append(Track(name, duration, links, order))
        order += 1
    return songs

def extractSinglePage(file):
	# load the file - exit out if the file does not load
	archive_file = open(file, 'r')
	archive_text = archive_file.read()
	return extractPageData(archive_text)

def getAllFiles(directory):
	return [x for x in os.listdir(path=directory) if os.path.isfile(f'{directory}/{x}')]

if __name__ == '__main__':
	files = getAllFiles(SHOW_DIR)
	# sort alphabetically to ensure runs are the same all the time
	files.sort()
	shows = []
	# grab some
	for i in files[:5]:
		# add full path
		filepath = f'{SHOW_DIR}/{i}'
		print(f'* Extracting: {i}')
		shows.append(extractSinglePage(filepath))
	print('* Complete')
	for i in shows[0]:
		print(i)
