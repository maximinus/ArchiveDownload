#!/usr/bin/env python3

import json
from tqdm import tqdm
from datetime import date
from fuzzywuzzy import fuzz

from gd_data import Show, Track, makeStringsFromShows
from songs import REPLACE_SONGS, NOT_SONGS

GD_DATA = 'grateful_dead.json'
SHOW_FOLDER = './json/90s'

def getShows():
    # load shows from JSON
    with open(GD_DATA, 'r') as json_file:
        data = json.load(json_file)
    print('* Importing Shows')
    shows = []
    for i in tqdm(data):
        shows.append(Show.fromJSON(i))
    return shows

def replaceMultipleSongs(show):
    # go through songs and find a hit
    new_songs = []
    for song in show.songs:
        if song.name in REPLACE_SONGS:
            # add the new songs with timings of 0
            for i in REPLACE_SONGS[song.name]:
                new_songs.append(Track(i, -1, 0))
        else:
            new_songs.append(song)
    show.songs = new_songs
    return show

def removeUnwantedSongs(show):
    new_songs = []
    for song in show.songs:
        if song.name not in NOT_SONGS:
            new_songs.append(song)
    show.songs = new_songs
    return show

def mapShows(shows):
    # map all shows into a dict of lists (recordings per show)
    mapped_shows = {}
    print('* Mapping same shows together')
    for i in tqdm(shows):
        # format is YYYY-MM-DD
        date_string = f'{i.date.year}-{i.date.month:02}-{i.date.day:02}'
        if date_string in mapped_shows:
            mapped_shows[date_string].append(i)
        else:
            mapped_shows[date_string] = [i]
    return mapped_shows

def showsEqual(shows, date):
    # passed a list of shows. Are they equal?
    # compare each one to all others
    index = None
    max_equal = 0
    for i in shows:
        equal = 0
        for j in shows:
            if i.compare(j) == True:
                equal += 1
        # we compared them all, highest yet?
        if equal > max_equal:
            index = i
            max_equal = equal
    if max_equal != len(shows):
        print(f'{date}: {max_equal}/{len(shows)}')
        return False
    return True

def getClosestShow(shows):
    # return the show with the lowest distance to all other shows
    strings = makeStringsFromShows(shows)
    lowest_score = 50000
    for i in strings:
        show = i[0]
        string = i[1]
        # match against all the others
        total_score = 0
        for j in strings:
            total_score += fuzz.ratio(string, j[1])
        if total_score < lowest_score:
            lowest_score = total_score
            choice = show
    return choice

def compareShows(shows):
    # now let's compare
    print('* Comparing shows in same recordings')
    compared_shows = {}
    for key in tqdm(shows):
        value = shows[key]
        # key is just the date, ignore that
        # only 1 show? Don't do anything
        if len(value) == 1:
            compared_shows[key] = value[0]
        elif len(value) == 2:
            # hardest to deal with
            if showsEqual(value, key):
                compared_shows[key] = value[0]
            else:
                print(f'2 shows not same: {key}')
        else:
            # >2 shows
            compared_shows[key] = getClosestShow(value)
    # we only want the show, not the keys
    return [x for x in compared_shows.values()]

def saveShows(shows):
    # save all as json
    json_data = []
    print('* Exporting shows')
    for i in tqdm(shows):
        json_data.append(i.toJSON())
    with open('gd_database_shows.json', 'w') as json_file:
        json.dump(json_data, json_file, indent=4)

def printSingleShow(show):
    for i in show:
        for j in i.songs:
            print(j)
        print('----')

if __name__ == '__main__':
    shows = getShows()
    slen = len(shows)
    # add back multiple songs
    print('* Checking for multiple songs')
    new_shows = []
    for i in tqdm(shows):
        new_shows.append(replaceMultipleSongs(i))
    shows = new_shows
    # remove all the tracks that are not needed
    print('* Removing non-song songs')
    new_shows = []
    for i in tqdm(shows):
        new_shows.append(removeUnwantedSongs(i))
    shows = new_shows
    # map into recordings per shows
    shows = mapShows(shows)
    shows = compareShows(shows)
    saveShows(shows)
