#!/usr/bin/env python3

import json

SONG_FILE = 'songs.json'

SONGS = None

def initSongs():
	global SONGS

	# load the songs
	with open('songs.json') as json_file:
		song_data = json.load(json_file)
	SONGS = song_data

def addNewSong(name):
	global SONGS

	SONGS.append([name])
	# update the json
	with open(SONG_FILE, 'w') as json_file:
		json.dump(SONGS, json_file, indent=4)

def findSong(name):
	# all unknown songs are added to the list of known ones
	if SONGS is None:
		initSongs()
	# iterate through the list
	# ends in '*'? then remove and strip whitespace
	if name.endswith('*'):
		name = name[:-2]
		name.strip()
	for song in SONGS:
		if name in song:
			return song[0]
	# song not found, capture this
	addNewSong(name)
	return name
