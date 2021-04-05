#!/usr/bin/env python3

ROOT_FOLDER = './gdshowsdb/data/gdshowsdb'

import sys
import yaml
import json

from translate_songs import TRANSLATIONS

with open('./data/all_songs.json') as json_file:
    SONGS = json.load(json_file)


def getSongs():
    file = open(f'./gdshowsdb/data/gdshowsdb/song_refs.yaml')
    yaml_data = file.read()
    return(yaml.load(yaml_data))

def makeDictionary(my_name, their_name, id):
    return {'my_name':my_name,
            'their_name': their_name,
            'id':id}

def getTranslation(data):
    # swap keys and values
    return {value:key for key, value in data.items()}

def convertSongs(show):
    # find the sets in the show
    index_key = ':sets'
    if index_key not in show:
        index_key = ':set'
    for i in show[index_key]:
        for j in i[':songs']:
            # look for uuid to be precise
            # this is a list of dicts we have here
            song_name = j[':name']
            # replace :name with correct value, just brite force
            found = False
            for k in SONGS:
                if k['their_name'] == song_name:
                    j[':name'] = k['my_name']
                    found = True
                    break
            if found == False:
                print(f'* Error: Name mis-match in {j[":name"]}')
                sys.exit(False)
    return show    


if __name__ == '__main__':
    # do the 60's
    shows = {}
    for file in [f'{x}.yaml' for x in range(1990, 1996)]:
        # read the file
        print(f'* Getting {file}')
        f = open(f'{ROOT_FOLDER}/{file}')
        yaml_data = f.read()
        pdata = yaml.load(yaml_data)
        # this is a dict of string date <-> dict show
        for key, value in pdata.items():
            try:
                shows[key] = convertSongs(value)
            except Exception as ex:
                print(value)
                raise ex

    # save as json
    with open('./data/db_parsed/grateful_dead_90s.json', 'w') as json_file:
        json.dump(shows, json_file, indent=4)

    print('* Saved as ./data/db_parsed/grateful_dead_90s.json')
