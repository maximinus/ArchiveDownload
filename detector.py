# Go along left set
# if same, record

# assumption: archive shows always have > 0 songs
# matches = 0
# archive_shows = [...]
# archive_indexes = [[0, x] for x in archive_shows]
# for song in database_show:
# 	# compare all sets with this one
# 	still_working = []
# 	for archive_song in archive_indexes:
# 		# this song, at this index, is hopefully the same
# 
# 
# for all songs:
# 	is it in the archive list?
# 	yes:
# 		go to first one and grab that value for that song
# 		cut off the list up to and including that index
# 		cut off the song you found
# 	no:
# 		let's ignore it then, and continue to the next index
# 
# do this for all shows
# now we have our sets with possible lengths
# take the middle value (>2), lowest value (2), or single value (1), or leave alone

import sys
import math
from statistics import median

import gd

def getSongIndex(song, archive):
	"""Return the index of the song, or nothing"""
	for index, archive_song in enumerate(archive):
		if song == archive_song['song']:
			#print(f"Matched: {song} == {archive_song['song']}")
			return index
	# failed
	return -1


def getSets(db_show):
	if ':sets' in db_show:
		return db_show[':sets']
	return db_show[':set']


def getLength(time):
	# time is a string in format PT0M403S, i.e. 403s
	str_time = time[4:-1]
	int_time = int(str_time)
	return int_time


def getAverageSongLength(lengths):
	# convert to ints
	if len(lengths) == 0:
		return 0
	timings = [getLength(x) for x in lengths]
	timings.sort()
	true_time = math.floor(median(timings))
	return math.floor(true_time)


def getSeque(song):
	for i in [':segued', 'segued', ':sequed', 'sequed']:
		if i in song:
			return song[i]
	print(song)
	raise KeyError


def getTimingsFromMatch(new_sets):
	# Returns a list of ShowSets
	calculated_sets = []
	# go through all sets
	for i in new_sets:
		final_set = []
		# grab the first bit of info we can
		for song in i:
			name = song[0][':name']
			trans = getSeque(song[0])
			length = getAverageSongLength(song[1:])
			final_set.append(gd.SongInstance(name, length, trans))
		calculated_sets.append(gd.ShowSet(final_set))
	return calculated_sets


def getMatchedSongLengths(db_show, archive_shows):
	# we will start by matching each set against all the song lists
	# so what we do is grab all the song lists

	#for i in archive_shows:
	#	print(f"-> {i['songs']}")

	show_lists = []
	for show in archive_shows:
		show_lists.append(show['songs'])

	new_sets = []
	# now cycle through all the sets
	for db_set in getSets(db_show):
		set_songs = db_set[':songs']
		measured_set = []
		for song in set_songs:
			measured_set.append([song])
			# now the algorithm can start
			# now we need iterate over all the archive shows
			new_show_lists = []
			for archive_show in show_lists:
				index = getSongIndex(song[':name'], archive_show)
				if index < 0:
					# no match, so we just move on to the next song
					# this means we just ignore the archive part
					new_show_lists.append(archive_show)
				else:
					# Found is somewhere in the list
					# 1: Record the time, crop the archive list and go to next loop iteration
					measured_set[-1].append(archive_show[index]['length'])
					archive_show.pop(index)
					# remember the new state for next time, if there is any left
					if len(archive_show) > 0:
						new_show_lists.append(archive_show)
			# did that song, so update the archive lists
			show_lists = new_show_lists
		# save that set and carry on
		new_sets.append(measured_set)
	# we did all sets, now to compute the rest
	return getTimingsFromMatch(new_sets)
 