#!/usr/bin/env python3

from pony.orm import *
from songs import SONGS, NOT_SONGS, REPLACE_SONGS

DB_NAME = 'grateful_dead.sqlite'


db = Database()
db.bind(provider='sqlite', filename=DB_NAME, create_db=True)


class Song(db.Entity):
	title = Required(str)


def getSongs():
	all_songs = []
	for i in SONGS:
		title = i[0]
		if title not in REPLACE_SONGS and title not in NOT_SONGS:
			all_songs.append(title)
	# remove duplicates
	print(all_songs)
	return list(set(all_songs))


@db_session
def makeDatabase():
	songs = getSongs()
	for i in songs:
		Song(title=i)
	db.commit()



if __name__ == '__main__':
	db.generate_mapping(create_tables=True)
	makeDatabase()
	print(f'  * Database saved as {DB_NAME}')
