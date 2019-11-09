#!/usr/bin/env python3

UNKNOWN_SONG = "UNKNOWN"

SONGS = {UNKNOWN_SONG: [UNKNOWN_SONG],
		 "Jack Straw":["Jack Straw"],
		 "Sugaree": ["Sugaree"],
		 "On The Road Again": ["On The Road Again"],
		 "It Must Have Been The Roses": ["It Must Have Been The Roses"],
		 "Me & My Uncle": ["Me & My Uncle"],
		 "Big River": ["Big River"],
		 "Peggy O": ["Peggy O"],
		 "Little Red Rooster": ["Little Red Rooster"],
		 "China Cat Sunflower": ["China Cat Sunflower"],
		 "I Know You Rider": ["I Know You Rider"],
		 "Tuning": ["Tuning"],
		 "Playin' In The Band": ["Playin' In The Band"],
		 "Terrapin Station": ["Terrapin Station"],
		 "Playin' Jam": ["Playin' Jam"],
		 "Drums": ["Drums"],
		 "Space": ["Space"],
		 "The Wheel": ["The Wheel"],
		 "The Other One": ["The Other One"],
		 "Stella Blue": ["Stella Blue"],
		 "US Blues": ["US Blues"]}

def showNewSong(name):
	# massage data into correct format
	print('''"""{0}""": ["""{1}"""],'''.format(title, name))

def findSong(name):
	# iterate through the list
	for song, names in SONGS.items():
		if name in names:
			return song
	# song not found, capture this
	showNewSong(name)
	return UNKNOWN_SONG
