#!/usr/bin/env python3

import json
import datetime
from tqdm import tqdm

import gd
import detector

# DATASET A: we a set of archive data that has:
# date
# venue
# list of songs with times
# shows are not unique

# DATASET B: and the gdshows data:
# date
# venue
# list of sets with songs with seques
# shows are unique

# For the shows, compare all A lists with B lists
# For the most comparable show, copy over all times

# Song:
# Per Show % (graph over the years) / Longest / Shortest / 
# Per Year / Before / After / 
# Avg position / First / Last /
# Avg position in sets per year (do this by each set being from 0 -> 1, even if the length of sets is different)

# Show:
# Day / Length of each set compared to other shows as % (i.e. 107% of the length of an average show) / Archive links
# Most Common Combo / 
# Most Common Song / Rarest Songs / 
# Longest by % against average / Shortest by % against average
# Bar chart average rarity per song in order
# Bar chart of song lengths in order
# Bar chart vs average length per song
# Closest shows by setlist / Furthest Away
# My Review

# Front Page:
# Longest Shows / Shortest Shows / Most Average / Most Unique (both based on setlist distance)
# Longest Songs / Longest Jams / Shortest Songs / Most Common Songs / Length By Year / Songs Per Show By Year / Total Unique Songs By Year
# First Songs Stopped / Most Common Date / Most Common Day / Most Common Combos / Shows Per Month
# Longest Lived Songs / Longest Gaps / Longest Repeats / Most Common Encores

# Combos: Same as songs, but look for combos and treat as one song:
# Scarlet > Fire
# China > Rider
# Estimated > Eyes
# Playin' > UJB
# Drums > Space

# Encores
# Most common, longest, shortest, most songs, % chance


def loadArchiveData():
	all_shows = []
	for i in [str(x) for x in [6, 7, 8, 9]]:
		filepath = f'./data/archive_parsed/grateful_dead_{i}0s.json'
		with open(filepath) as json_file:
			all_shows += json.load(json_file)
	return all_shows


def loadDatabaseData():
	# it's a dict with date:details, so instead put in an array
	all_shows = []
	for i in [str(x) for x in [6, 7, 8, 9]]:
		filepath = f'./data/db_parsed/grateful_dead_{i}0s.json'
		with open(filepath) as json_file:
			new_shows = json.load(json_file)
			for key, value in new_shows.items():
				all_shows.append([key, value])
	return all_shows


def getArchiveShows(date, archive):
	matching_shows = []
	for i in archive:
		archive_date = getDateFromArchive(i)
		if archive_date == date:
			matching_shows.append(i)
	return matching_shows


def findBestMatch(all_matches, show):
	pass


def getTimings(database, archive):
	for show in database:
		date = show['date']
		all_matches = getArchiveShows(date, archive)
		best_match = findBestMatch(all_matches, show)


def getDateFromDatabase(show):
	text_date = show[0]
	text_date = text_date.split('/')
	year = int(text_date[0])
	month = int(text_date[1].lstrip('0'))
	day = int(text_date[2].lstrip('0'))
	return datetime.date(year, month, day)


def getDateFromArchive(archive_show):
	year = archive_show['year']
	month = archive_show['month']
	day = archive_show['day']
	return datetime.date(year, month, day)


def showArchiveStats(archive):
	print('* Archive Stats:')
	print(f'  Total Shows: {len(archive)}')
	shows = set()
	for i in archive:
		shows.add(getDateFromArchive(i))
	print(f'  Total Unique Shows: {len(shows)}')


def showDatabaseStats(database):
	print('* Database Stats:')
	print(f'  Total Shows: {len(database)}')
	bad_dates = 0
	for i in database:
		try:
			getDateFromDatabase(i)
		except Exception:
			bad_dates += 1
	print(f'  Shows with bad dates: {bad_dates}')


def getPerfectMatch(show, archive_shows):
	# convert each set into a string
	song_string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXY1234567890!"£$%^&*()-=_+;:@#~[]{}'
	index = 0
	songs = {}
	archive_string = ''
	# run through the database show and convert into a setlist
	set_name = ':sets'
	if set_name not in show:
		set_name = ':set'
	for show_set in show[set_name]:
		for song in show_set[':songs']:
			# a song is this: {":uuid": "2", ":name": "Jack Straw", ":segued": false}
			song_name = song[':name']
			if song_name in songs:
				archive_string += songs[song_name]
			else:
				# add it
				songs[song_name] = song_string[index]
				archive_string += songs[song_name]
				index += 1
	# now we have the show string, repeat for the archive shows to see matches
	for i in archive_shows:
		show_string = ''
		for song in i['songs']:
			song_name = song['song']
			if song_name in songs:
				show_string += songs[song_name]
			else:
				songs[song_name] = song_string[index]
				show_string += songs[song_name]
				index += 1
		# do we have a match?
		if show_string == archive_string:
			# return first one found
			return i
	return


def compareSongStrings(database_string, show_string):
	# now we have a string to compare with
	# traverse the database string
	database_index = 0
	show_index = 0
	while((database_index < len(database_string)) and (show_index < len(show_string))):
		if database_string[database_index] == show_string[show_index]:
			current_song = database_string[database_index]
			database_index += 1
			show_index += 1
			# if database has nn and show has n, also valid
			while database_index < len(database_string) and show_index < len(show_string):
				if database_string[database_index] == current_song and show_string[show_index] != current_song:
					# move past on database
					database_index += 1
				else:
					# no match, ignore
					break
		else:
			show_index += 1
	# get to the end of the database entry?
	return database_index >= len(database_string)


def testStrings():
	tests = [['abc', 'abc'],
			 ['abcdr', 'abcdr'],
			 ['abcdef', 'abycdhef'],
			 ['abcdefghijklmnnopq', 'abcdefgrhijklmtnopq']]
	for i in tests:
		if compareSongStrings(i[0], i[1]) == False:
			print(f'{i[0]} not matching {i[1]}')


def getLinearMatch(show, archive_shows):
	# convert into strings, then see how many match
	song_string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXY1234567890!"£$%^&*()-=_+;:@#~[]{}'
	index = 0
	songs = {}
	database_string = ''
	# run through the database show and convert into a setlist
	set_name = ':sets'
	if set_name not in show:
		set_name = ':set'
	for show_set in show[set_name]:
		for song in show_set[':songs']:
			# a song is this: {":uuid": "2", ":name": "Jack Straw", ":segued": false}
			song_name = song[':name']
			if song_name in songs:
				database_string += songs[song_name]
			else:
				# add it
				songs[song_name] = song_string[index]
				database_string += songs[song_name]
				index += 1
	# now we have the show string, repeat for the archive shows to see matches
	for i in archive_shows:
		show_string = ''
		for song in i['songs']:
			song_name = song['song']
			if song_name in songs:
				show_string += songs[song_name]
			else:
				songs[song_name] = song_string[index]
				show_string += songs[song_name]
				index += 1
		if compareSongStrings(database_string, show_string):
			# we found a match, we'll just take the first one thanks
			return(i)


def noSets(show):
	if ':sets' in show:
		if len(show[':sets']) == 0:
			return True
	if ':set' in show:
		if len(show[':set']) == 0:
			return True
	return False


def showWithNoSongs(show, show_date):
	venue = show[':venue']
	city = show[':city']
	state = show[':state']
	country = show[':country']
	new_venue = gd.Venue(venue, city, state, country)
	new_show = gd.Show(show_date, [], new_venue)
	return new_show


def getLength(song):
	# time is a string in format PT0M403S, i.e. 403s
	time = song['length']
	str_time = time[4:-1]
	int_time = int(str_time)
	return int_time


def getSetListFromPerfect(show, archive):
	finished_sets = []
	set_name = ':sets'
	if set_name not in show:
		set_name = ':set'
	archive_index = 0
	for single_set in show[set_name]:
		new_set = gd.ShowSet([])
		for single_song in single_set[':songs']:
			name = single_song[':name']
			length = getLength(archive[archive_index])
			trans = single_song[':segued']
			new_set.songs.append(gd.SongInstance(name, length, trans))
			archive_index += 1
		finished_sets.append(new_set)
	return finished_sets


def getSetListFromLinear(show, archive):
	# this is the case where database has nn, and the show has n
	# so we do the same as perfect, except to skip the doubled songs
	last_song = ''
	finished_sets = []
	set_name = ':sets'
	if set_name not in show:
		set_name = ':set'
	archive_index = 0
	for single_set in show[set_name]:
		new_set = []
		for single_song in single_set[':songs']:
			name = single_song[':name']
			# same as the last song? Different from archive?
			if name == last_song and archive[archive_index]['song'] != name:
				# skip past this one and do not advance the archive index
				continue
			length = getLength(archive[archive_index])
			#print(f'Matching: {name} == {archive[archive_index]["song"]}')
			trans = single_song[':segued']
			new_set.append(gd.SongInstance(name, length, trans))
			archive_index += 1
		finished_sets.append(new_set)
	return finished_sets


def getPossibleArchiveSet(show_date, archive, database_show):
	# the database has no set data for this show
	# get all the shows that match this
	matches = getArchiveShows(show_date, archive)
	if len(matches) <= 0:
		# nothing!
		return
	# find the one with the most songs
	best_match = matches[0]
	max_songs = -1
	for i in matches:
		total_songs = len(i['songs'])
		if total_songs > max_songs:
			max_songs = total_songs
			best_match = i
	if max_songs <= 0:
		# found nothing
		return
	# return the gd.ShowInstance
	new_show = showWithNoSongs(database_show, show_date)
	# no set info, ah well (!), also we lose all transitions
	songs = []
	for i in best_match['songs']:
		length = getLength(i)
		songs.append(gd.SongInstance(i['song'], length, False))
		new_show.sets = [gd.ShowSet(songs)]
	return new_show


def matchupShows(archive, database):
	# go through the database one by one
	collated_shows = []
	for show in tqdm(database):
		# find all shows in archive that match this show
		show_date = getDateFromDatabase(show)
		if noSets(show[1]) == True:
			# we can add this one easily
			# we need to add from the archive. Take the most complete one
			archive_result = getPossibleArchiveSet(show_date, archive, show[1])
			if archive_result is not None:
				#print(f'Check values for {show_date} taken from archive')
				collated_shows.append(archive_result)
			# and then carry on
			continue
		archive_shows = getArchiveShows(show_date, archive)
		new_show = showWithNoSongs(show[1], show_date)
		if len(archive_shows) == 0:
			# we add with no sets
			new_show.sets = []
			collated_shows.append(new_show)
			continue
		else:
			# some matches. See if any are perfect
			same_set = getPerfectMatch(show[1], archive_shows)
			if same_set is not None:
				new_show.sets = getSetListFromPerfect(show[1], same_set['songs'])
				collated_shows.append(new_show)
				# perfect match - easy
				continue

			show_sets = detector.getMatchedSongLengths(show[1], archive_shows)
			new_show.sets = show_sets
			collated_shows.append(new_show)
			continue

			# try with the linear match format
			#same_set = getLinearMatch(show[1], archive_shows)
			#if same_set is not None:
			#	# great, this is easy
			#	new_show = showWithNoSongs(show[1], show_date)
			#	# bit buggy for now
			#	new_show.sets = getSetListFromLinear(show[1], same_set['songs'])
			#	collated_shows.append(new_show)

	print(f'*   Handled: {len(collated_shows)}')
	return(collated_shows)


if __name__ == '__main__':
	archive = loadArchiveData()
	#showArchiveStats(archive)
	database = loadDatabaseData()
	#showDatabaseStats(database)
	final_shows = matchupShows(archive, database)
	gd.saveShows(final_shows, 'gd_database.pickle')
