#!/usr/bin/env python3

import os
import json
from fuzzywuzzy import fuzz
from tqdm import tqdm
from bs4 import BeautifulSoup

from songs import SONGS

ALL_FILES = ['60s', '70s', '80s', '90s']

SHOW_DIR = './data/archive_source/'
from gd_data import Show, Track

# score required for a match
FUZZY_FILTER = 60

# load the archive files and extract the song data for now

def cleanName(name):
    # before we compare, clean up the input
    # strip white space
    name = name.strip()
    # remove all * at end
    while name.endswith('*'):
        name = name[:-1]
    # compare as lowercase
    name = name.lower()
    # remove any > or ->
    if name.endswith('>'):
        name = name[:-1]
    elif name.endswith('->'):
        name = name[:-2]
    # remove // and ..
    name = name.replace('..', '')
    name = name.replace('//', '')
    # remove E: or e: at start
    if name.startswith('e:'):
        name = name[2:]
    # remove 'set break' at end
    if name.endswith('set break'):
        name = name[:-9]
    # if starting with '[0-9]+', remove those digits
    while((len(name) > 0) and name[0].isdigit()):
        name = name[1:]
    # remove whitespace again
    name = name.strip()
    return name.lower()

def matchStringStart(name):
    # try and see if the start or end of the string matches a song
    # this matches things like "comes a time -> days between intro"
    # or "gd95-05-29 t02 jack-a-roe"
    for song in SONGS:
        for songname in song:
            if name.startswith(songname.lower()):
                return song[0]
            if name.endswith(songname.lower()):
                return song[0]

def getMatch(name):
    # find an identical match
    for song in SONGS:
        for songname in song:
            if name == songname.lower():
                return song[0]

def getFuzzyMatch(name, filename):
    match = matchStringStart(name)
    if match is not None:
        return match
    highest_score = 0
    match = ''
    for song in SONGS:
        for songname in song:
            score = fuzz.ratio(songname, name)
            if score > highest_score:
                match = song[0]
                highest_score = score
    if highest_score < FUZZY_FILTER:
        # still rejected. Output
        #print(f'Rejected: {name}')
        return
    return match

def getRealSongName(name, filename):
    if len(name) == 0:
        return
    clean_name = cleanName(name)
    result = getMatch(clean_name)
    if result is not None:
        return result
    # no exact match, let's try a fuzzy match
    result = getFuzzyMatch(clean_name, filename)
    return result

def extractSongData(page, filename):
    # parse the HTML to get the links
    soup = BeautifulSoup(page, features='html.parser')
    main_wrap = soup.find('div', {'id': 'theatre-ia-wrap'})
    # now find the tracks in this
    tracks = main_wrap.findAll('div', {'itemprop':'track'})
    songs = []
    order = 1
    for t in tracks:
        name = t.find('meta', {'itemprop': 'name'})['content']
        name = getRealSongName(name, filename)
        duration = t.find('meta', {'itemprop': 'duration'})['content']
        # links = [x['href'] for x in t.findAll('link')]
        if name is not None:
            songs.append(Track(name, duration, order))
        order += 1
    return songs

def getSinglePage(file):
    # load the file - exit out if the file does not load
    archive_file = open(file, 'r')
    return archive_file.read()

def getAllFiles(directory):
    return [x for x in os.listdir(path=directory) if os.path.isfile(f'{directory}/{x}')]

def exportTrackNames(songs):
    # grab all the names
    names = [x.song for x in songs]
    # remove similar strings
    names = list(set(names))
    cleaned_names = []
    for i in names:
        # go and find the actual real value
        data = getRealSongName(i)
        if data is not None:
            cleaned_names.append(data)
    # make unique and sort
    cleaned_names = list(set(cleaned_names))
    cleaned_names.sort()
    # export to json
    #with open('./data/song_fails.json', 'w') as json_file:
    #    json.dump(cleaned_names, json_file, indent=4)

def saveShows(shows, filename):
    # save all as json
    json_data = []
    print('* Exporting shows')
    for i in tqdm(shows):
        data = i.toJSON()
        if data is not None:
            json_data.append(data)
    with open(filename, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)


def getDecade(decade):
    files = getAllFiles(f'{SHOW_DIR}/{decade}')
    # sort alphabetically to ensure runs are the same all the time
    files.sort()
    songs = []
    shows = []
    # grab some
    for i in tqdm(files):
        # add full path
        filepath = f'{SHOW_DIR}/{decade}/{i}'
        # print(filepath)
        archive_text = getSinglePage(filepath)
        songs = extractSongData(archive_text, filepath)
        new_show = Show.getFromArchivePage(archive_text)
        new_show.songs = songs
        shows.append(new_show)
    saveShows(shows, f'grateful_dead_{decade}.json')


if __name__ == '__main__':
    for i in ALL_FILES:
        print(f'* Calculating {i}')
        getDecade(i)
