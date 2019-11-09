#!/usr/bin/env python3

from enum import Enum

class Song(Enum):
	NONE = 'Unknown song'
	JACK_STRAW = 'Jack Straw'

SONGS = {Song.JACK_STRAW:["Jack Straw"],
		 Song.SUGAREE: ["Sugaree"],
		 Song.ON_THE_ROAD_AGAIN: ["On The Road Again"],
		 Song.IT_MUST_HAVE_BEEN_THE_ROSES: ["It Must Have Been The Roses"],
		 Song.ME_AND_MY_UNCLE: ["Me & My Uncle"],
		 Song.BIG_RIVER: ["Big River"],
		 Song.PEGGY_O: ["Peggy O"],
		 Song.LITTLE_RED_ROOSTER: ["Little Red Rooster"],
		 Song.CHINA_CAT_SUNFLOWER: ["China Cat Sunflower"],
		 Song.I_KNOW_YOU_RIDER: ["I Know You Rider"],
		 Song.TUNING: ["Tuning"],
		 Song.PLAYIN_IN_THE_BAND: ["Playin' In The Band"],
		 Song.TERRAPIN_STATION: ["Terrapin Station"],
		 Song.PLAYIN_JAM: ["Playin' Jam"],
		 Song.DRUMS: ["Drums"],
		 Song.SPACE: ["Space"],
		 Song.THE_WHEEL: ["The Wheel"],
		 Song.THE_OTHER_ONE: ["The Other One"],
		 Song.STELLA_BLUE: ["Stella Blue"],
		 Song.PLAYIN_IN_THE_BAND: ["Playin' In The Band"],
		 Song.US_BLUES: ["US Blues"]}

def showNewSong(name):
	# convert to upper case
	title = name.upper()
	# convert & to AND
	title = title.replace('&', 'AND')
	# replace spaces with '_'
	data = title.split()
	title = '_'.join(data)
	# all data only contains [A-Z]
	title = ''.join([x for x in title if x in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ_'])
	# massage data into correct format
	print('''Song.{0}: ["{1}"],'''.format(title, name))

def findSong(name):
	# iterate through the list
	for song, names in SONGS.items():
		if name in names:
			return song
	# song not found, capture this
	showNewSong(name)
	return song.NONE


if __name__ == '__main__':
	# create the required enums
	for song, names in SONGS:
		pass
 