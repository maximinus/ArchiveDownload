#!/usr/bin/env python3

import os
import sys
import json
import math
import pickle
import operator

import datetime

# keep this as simple as possible

# we need:
# get all instances of a song
#   - tally all shows by year
#       Calculate % chance of being played
#   - get show position, and compute yearly average


class SongData:
    def __init__(self, date, before, after, length, venue):
        self.date = date
        self.before = before
        self.after = after
        self.length = length
        self.venue = venue


def sortSongDataByDate(songs):
    return sorted(songs, key=operator.attrgetter('date'))


def sortSongDataByLength(songs):
    # group all songs with length != 0
    non_zero_songs = []
    for i in songs:
        if i.length != 0:
            non_zero_songs.append(i)
    return sorted(non_zero_songs, key=operator.attrgetter('length'))


def getPlayedPerYear(songs, shows):
    # get counts for shows
    shows_per_year = [0 for x in range(31)]
    for show in shows:
        shows_per_year[int(show.date.year) - 1965] += 1
    # count all times played
    years = [0 for x in range(31)]
    for song in songs:
        played_in_year = int(song.date.year) - 1965
        years[played_in_year] += 1
    # we want the % chance of being played, which is simple: played / shows
    chance_of_being_played = []
    for x in range(31):
        if shows_per_year[x] == 0:
            chance_of_being_played.append(0.0)
        else:
            chance_of_being_played.append(float(years[x] / float(shows_per_year[x])))
    return chance_of_being_played


def getAdjoiningSongs(songs):
    before_songs = {}
    after_songs = {}
    for song in songs:
        if song.before not in before_songs:
            before_songs[song.before] = 1
        else:
            before_songs[song.before] += 1
        if song.after not in after_songs:
            after_songs[song.after] = 1
        else:
            after_songs[song.after] += 1
    # we have all the songs sort by value
    sorted_before = sorted(before_songs.items(), key=operator.itemgetter(1))
    sorted_after = sorted(after_songs.items(), key=operator.itemgetter(1))
    # only return what we have
    sorted_before.reverse()
    sorted_after.reverse()
    return sorted_before[:5], sorted_after[:5]


def getAverageLengths(songs):
    # returns an array where n[0] = average length, n[1:] int of % length per year
    # list is [total_played, total_length]
    years = [[0, 0] for x in range(31)]
    for song in songs:
        year_played = int(song.date.year) - 1965
        years[year_played][0] += 1
        years[year_played][1] += song.length
    # add up and get the average length
    total_played = 0
    total_time = 0
    for year in years:
        total_played += year[0]
        total_time += year[1]
    # impossible for total played to be 0
    average_length = float(total_time) / float(total_played)

    # if the average length is 0, we have no timings
    if int(average_length) == 0: 
        return 0, [0 for x in range(31)]

    # now calulate the difference in times
    average_length_per_year = []
    for year in years:
        # could be a zero
        if year[0] == 0:
            average_length_per_year.append(0)
        else:
            year_length = float(year[1]) / float(year[0])
            # make this a %
            year_length = int((year_length / average_length) * 100.0)
            average_length_per_year.append(year_length)
    return int(average_length), average_length_per_year



def getOrdinal(n):
    # Convert an integer into its ordinal representation::
    n = int(n)
    suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    return str(n) + suffix


class SongStats:
    def __init__(self, name, songs, shows):
        print(f'* Getting stats for {name}')
        song_details = songs.pop(0)
        self.name = name
        self.songs = songs
        self.times_played = len(songs)
        self.order_played = getOrdinal(song_details[0])
        self.show_number = getOrdinal(song_details[1])
        sorted_by_date = sortSongDataByDate(songs)
        if len(sorted_by_date) > 5:
            self.first_five = sorted_by_date[:5]
            self.last_five = sorted_by_date[-5:]
        else:
            self.first_five = sorted_by_date
            self.last_five = sorted_by_date
        self.last_five.reverse()
        sorted_by_length = sortSongDataByLength(songs)
        if len(sorted_by_length) > 5:
            self.longest_five = sorted_by_length[-5:]
            self.shortest_five = sorted_by_length[:5]
        else:
            self.longest_five = sorted_by_length
            self.shortest_five = sorted_by_length
        self.longest_five.reverse()
        self.before, self.after = getAdjoiningSongs(songs)
        self.played_per_year = getPlayedPerYear(songs, shows)
        self.average_length, self.average_length_by_years = getAverageLengths(songs)
        self.average_position = getAveragePosition(name, shows)

    def save(self):
        filename = self.name
        filename = filename.replace(' ', '_')
        filename = filename.replace('/', '_')
        filename += '.pickle'
        pickle.dump(self, open('./data/stats/songs/' + filename, 'wb'))

    def printStats(self):
        print(f'* Stats for {self.name}')
        print(f'  First Five:')
        first = ', '.join([str(x.date) for x in self.first_five])
        print(f'     {first}')
        last = ', '.join([str(x.date) for x in self.last_five])
        print(f'     {last}')


def getAveragePosition(track, shows):
    # seperated from getStats for ease of coding
    years = [[] for x in range(31)]
    for show in shows:
        # start on first set
        set_position = 1
        for played_set in show.sets:
            if len(played_set.songs) == 0:
                continue
            internal_set_offset = 1.0 / float(len(played_set.songs))
            for index, song in enumerate(played_set.songs):
                if song.name == track:
                    year_index = int(show.date.year) - 1965
                    years[year_index].append(set_position + (index * internal_set_offset))
            set_position = math.floor(set_position) + 1
    final_totals = []
    for i in years:
        if len(i) == 0:
            final_totals.append(0)
        else:
            final_totals.append(float(sum(i)) / float(len(i)))
    return final_totals


def getStats(shows):
    songs = {}
    song_added = {}
    # start at 1: 1st, 2nd etc..
    show_index = 1
    song_added = 1
    for show in shows:
        for set_number, played_set in enumerate(show.sets):
            for index, song in enumerate(played_set.songs):
                # a song - does it exist?
                if song.name not in songs:
                    songs[song.name] = [[song_added, show_index]]
                    song_added += 1
                # add the data
                # before
                if index == 0:
                    before = f'Start of Set {set_number + 1}'
                else:
                    before = played_set.songs[index - 1].name
                # after
                if index + 1 == len(played_set.songs):
                    after = f'End of Set {set_number + 1}'
                else:
                    after = played_set.songs[index + 1].name
                # add the data
                songs[song.name].append(SongData(show.date, before, after, song.length, show.venue))
        show_index += 1
    return songs


def getLengthText(length):
    if length == 0:
        return 'Unknown'
    minutes = length // 60
    seconds = length - (minutes * 60)
    return f'{minutes}m {seconds}s'


class SongInstance:
    def __init__(self, name, length, trans):
        self.name = name
        self.length = length
        self.transition = trans

    def __repr__(self):
        if self.transition is True:
            return f'{self.name}:{self.length}s >'
        else:
            return f'{self.name}:{self.length}s'

    def asJson(self):
        return {'name': self.name,
                'length': getLengthText(self.length),
                'transition': self.transition}

    @staticmethod
    def importJson(self, data):
        name = data['name']
        # convert length to m+s
        length = data['length']
        transisition = data['transition']
        return SongInstance(name, length, transition)


class Venue:
    def __init__(self, venue, city, state, country):
        self.venue = venue
        self.city = city
        self.state = state
        self.country = country

    def __repr__(self):
        return self.venue

    def asJson(self):
        # all strings, no problems
        return {'venue': self.venue,
                'city': self.city,
                'state': self.state,
                'country': self.country}

    @staticmethod
    def importJson(self, data):
        venue = data['venue']
        city = data['city']
        state = data['state']
        country = data['country']
        return Venue(venue, cirt, state, country)


class ShowSet:
    def __init__(self, songs):
        self.songs = songs

    def toJson(self):
        return {'songs': [x.asJson() for x in self.songs]}

    @staticmethod
    def importJson(self, data):
        songs = [SongInstance(x) for x in data]
        return ShowSet(songs)


class Show:
    def __init__(self, date, sets, venue):
        # date is a date object; sets is a list of ShowSets, venue is a Venue
        self.date = date
        self.sets = sets
        self.venue = venue

    def printShow(self):
        print(self)
        count = 0
        for i in self.sets:
            print(count)
            count += 1
            for j in i.songs:
                print(f'  {j}')

    def __repr__(self):
        return f'{str(self.date)} : {self.venue}'

    def getFilename(self):
        return f'{self.date.year}-{self.date.month}-{self.date.day}'

    def asJson(self):
        return {'year': int(self.date.year),
                'month': int(self.date.month),
                'day': int(self.date.day),
                'venue': self.venue.asJson(),
                'sets': [x.toJson() for x in self.sets]}

    def exportJson(self, filename):
        print(f'* Exporting {filename}')
        with open(filename, 'w') as json_file:
            json.dump(self.asJson(), json_file, indent=4)

    @staticmethod
    def importJson(self, filename):
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
        year = data['year']
        month = data['month']
        day = data['day']
        date = datetime.date(year, month, day)
        show_sets = [ShowSet.importJson(x) for x in data['sets']]
        venue = Venue.importJson(data['venue'])
        return Show(date, sets, venue)


# helper functions
def exportShowsAsJson(shows):
    EXPORT_FOLDER = './data/all_shows'
    # save the shows as JSON info
    for i in shows:
        year = str(i.date.year)[2:]
        filename = i.getFilename()
        fullpath = f'{EXPORT_FOLDER}/{year}/{filename}.json'
        # copy of this already exists?
        index = 2
        while os.path.exists(fullpath):
            fullpath = f'{EXPORT_FOLDER}/{year}/{filename}_{index}.json'
            index += 1
        i.exportJson(fullpath)


def saveShows(shows, filename):
    pickle.dump(shows, open(filename, 'wb'))


def loadShows(filename):
    shows = pickle.load(open(filename, 'rb' ))
    return shows


if __name__ == '__main__':
    shows = loadShows('gd_database.pickle')
    songs = getStats(shows)
    for key, value in songs.items():
        song_stats = SongStats(key, value, shows)
        song_stats.save()
