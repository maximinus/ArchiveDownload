#!/usr/bin/env python3

UNKNOWN_SONG = "UNKNOWN"

SONGS = [["Jack Straw"],
		 ["Sugaree"],
		 ["On The Road Again"],
		 ["It Must Have Been The Roses"],
		 ["Me & My Uncle"],
		 ["Big River"],
		 ["Peggy O"],
		 ["Little Red Rooster"],
		 ["China Cat Sunflower"],
		 ["I Know You Rider"],
		 ["Tuning"],
		 ["Playin' In The Band"],
		 ["Terrapin Station"],
		 ["Playin' Jam"],
		 ["Drums"],
		 ["Space"],
		 ["The Wheel"],
		 ["The Other One"],
		 ["Stella Blue"],
		 ["US Blues"]]

def showNewSong(name):
	# massage data into correct format
	print('''"""{0}""": ["""{1}"""],'''.format(title, name))

def findSong(name):
	# iterate through the list
	for song in SONGS:
		if name in song:
			return song[0]
	# song not found, capture this
	showNewSong(name)
	return UNKNOWN_SONG
