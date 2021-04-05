#!/usr/bin/env python3

import yaml
import json

from translate_songs import TRANSLATIONS


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

if __name__ == '__main__':
    songs = getSongs()
    trans = getTranslation(TRANSLATIONS)
    titles = []

    # go through their names
    for song in songs:
        # looks like {'Your Love At Home': '9c7db7c1-603a-4e71-acfc-03ddfec744b8'}
        for name, id_value in song.items():
            # the name must exist in our file
            my_name = trans[name]
            # and now we have all data
            titles.append(makeDictionary(my_name, name, id_value))

    # save as json
    with open('./data/all_songs.json', 'w') as json_file:
        json.dump(titles, json_file, indent=4)

    print('* Saved as ./data/all_songs.json')
