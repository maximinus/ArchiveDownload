#!/usr/bin/env python3

import os
import json
import fuzzywuzzy
from tqdm import tqdm
from bs4 import BeautifulSoup

SHOW_DIR = './data/archive_source/90s'
from gd_data import Show, Track

# load the archive files and extract the song data for now

def cleanName(name):
    if len(name) == 0:
        return
    # clean the data given. Based on what we have so far:
    # remove whitespace from start and end
    name = name.strip()
    # remove junk at end
    while(name[-1] in ['-', '>', '*']):
        name = name[:-1]
    # if starting with '[0-9]+', remove those digits
    while(name[0].isdigit()):
        name = name[1:]
    # return None if there is an error, else return a string
    if len(name) == 9:
        return
    # sometimes whitespace can appear again
    return name.strip()

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
        #links = [x['href'] for x in t.findAll('link')]
        songs.append(Track(name, duration, order))
        order += 1
    return songs

def extractSinglePage(file):
    # load the file - exit out if the file does not load
    archive_file = open(file, 'r')
    archive_text = archive_file.read()
    return extractPageData(archive_text)

def getAllFiles(directory):
    return [x for x in os.listdir(path=directory) if os.path.isfile(f'{directory}/{x}')]

def exportTrackNames(songs):
    # grab all the names
    names = [x.song for x in songs]
    # remove similar strings
    names = list(set(names))
    cleaned_names = []
    for i in names:
        cleaned = cleanName(i)
        if cleaned is not None:
            cleaned_names.append(cleaned)
    # make unique and sort
    cleaned_names = list(set(cleaned_names))
    cleaned_names.sort()
    # export to json
    with open('./data/song_names.json', 'w') as json_file:
        json.dump(cleaned_names, json_file, indent=4)

if __name__ == '__main__':
    files = getAllFiles(SHOW_DIR)
    # sort alphabetically to ensure runs are the same all the time
    files.sort()
    songs = []
    # grab some
    for i in files[:50]:
        # add full path
        filepath = f'{SHOW_DIR}/{i}'
        print(f'* Extracting: {i}')
        songs.extend(extractSinglePage(filepath))
    exportTrackNames(songs)
    print('* Song names extracted to ./data/song_names.json')
