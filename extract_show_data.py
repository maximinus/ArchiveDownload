#!/usr/bin/env python3

import os
import json
from fuzzywuzzy import fuzz
from tqdm import tqdm
from bs4 import BeautifulSoup

from songs import SONGS

SHOW_DIR = './data/archive_source/90s'
from gd_data import Show, Track

# load the archive files and extract the song data for now

def cleanName(name):
    # before we compare, clean up the input
    # strip white space
    name = name.strip()
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
    highest_score = 0
    match = ''
    for song in SONGS:
        for songname in song:
            score = fuzz.ratio(songname, name)
            if score > highest_score:
                match = song[0]
                highest_score = score
    if highest_score < 50:
        # still rejected. Search for a song name at the start
        return matchStringStart(name)
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

def saveShows(shows):
    # save all as json
    json_data = []
    print('* Exporting shows')
    for i in tqdm(shows):
        json_data.append(i.toJSON())
    with open('grateful_dead.json', 'w') as json_file:
        json.dump(json_data, json_file, indent=4)


if __name__ == '__main__':
    # current results: 1225 fails
    files = getAllFiles(SHOW_DIR)
    # sort alphabetically to ensure runs are the same all the time
    files.sort()
    songs = []
    shows = []
    # grab some
    print('* Importing Data')
    for i in tqdm(files):
        # add full path
        filepath = f'{SHOW_DIR}/{i}'
        # print(filepath)
        archive_text = getSinglePage(filepath)
        songs = extractSongData(archive_text, filepath)
        new_show = Show.getFromArchivePage(archive_text)
        new_show.songs = songs
        shows.append(new_show)
    saveShows(shows)
