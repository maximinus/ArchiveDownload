#!/usr/bin/env python3

from datetime import date
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz

import unittest

class Show:
    def __init__(self):
        self.venue = ''
        self.date = None
        self.location = ''
        self.songs = []

    @classmethod
    def getFromArchivePage(cls, page):
        show = Show()
        soup = BeautifulSoup(page, features='html.parser')
        date_text = soup.find('span', {'itemprop': 'datePublished'}).text
        # this is in the format YYYY-MM-DD
        try:
            date_data = date_text.split('-')
            date_data = [int(x) for x in date_data]
            show.date = date(date_data[0], date_data[1], date_data[2])
        except:
            print('Bad date: {date_text}')
        # need location and venue
        metadata = soup.find('div', {'class': 'metadata-expandable-list'})
        for i in metadata.find_all('dl'):
            dt_tag = i.find('dt')
            if dt_tag.text.lower() == 'location':
                show.location = i.find('dd').text.strip()
            elif dt_tag.text.lower() == 'venue':
                show.venue = i.find('dd').text.strip()
        return(show)

    def toJSON(self):
        try:
            data = {'venue': self.venue,
                    'year': self.date.year,
                    'month': self.date.month,
                    'day': self.date.day,
                    'location': self.location,
                    'songs': [x.toJSON() for x in self.songs]}
            return data
        except:
            return

    @classmethod
    def fromJSON(cls, json_data):
        new_show = Show()
        new_show.venue = json_data['venue']
        new_show.location = json_data['location']
        new_show.date = date(json_data['year'], json_data['month'], json_data['day'])
        new_show.songs = [Track.fromJSON(x) for x in json_data['songs']]
        return new_show

    def compare(self, other):
        # all songs must be the same
        if len(self.songs) != len(other.songs):
            return False
        for i in range(len(self.songs)):
            if self.songs[i].compare(other.songs[i]) == False:
                return False
        return True

    def __repr__(self):
        date_format = self.date.strftime('%a %d %b %y')
        return f'{date_format}: {self.venue}'

class Track:
    # duration of -1 means info is missing
    def __init__(self, name, duration, index):
        # we can extract many things from this data
        try:
            self.name = name
            self.track_number = index
            self.length = duration
        except Exception as e:
            print(' * Error: {0}'.format(e))
            print(' * {0} : {1}'.format(name, duration))

    def getTimeString(self):
        return '0'
        minutes = self.length // 60
        seconds = self.length - (minutes * 60)
        return('{0}m {1}s'.format(minutes, seconds))

    def toJSON(self):
        return {'song': self.name,
                'length': self.length}

    @classmethod
    def fromJSON(cls, json_data):
        new_track = Track('', '', 0)
        new_track.name = json_data['song']
        new_track.length = json_data['length']
        return new_track

    def compare(self, other):
        return self.name == other.name

    def __repr__(self):
        return(f'{self.name}, {self.getTimeString()}')

def makeStringsFromShows(shows):
    # 74 possible different songs should be enough
    master = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890[](){}!$%^'
    index = 0
    all_songs = {}
    show_strings_mapped = []
    for i in shows:
        new_string = []
        for j in i.songs:
            if j.name in all_songs:
                new_string.append(all_songs[j.name])
            else:
                all_songs[j.name] = master[index]
                new_string.append(master[index])
                index += 1
        show_strings_mapped.append([i, ''.join(new_string)])
    return show_strings_mapped

# add testcases here as well
class TestDistance(unittest.TestCase):
    def test_given(self):
        SET_ONE = ['Touch Of Gray', 'Greatest Story', 'Jack-A-Roe', 'Little Red Rooster', 'Stagger Lee', 'Queen Jane Approximately', 'The Last Time', 'Cassidy', 'Deal', 'China Cat Sunflower',
                   'I Know You Rider', 'Just A Little Light', 'Estimated Prophet', 'Eyes Of The World', 'Drums', 'Space', 'The Wheel', 'Gimme Some Lovin', 'Wharf Rat', 'Sugar Magnolia', 'Knockin On Heavens Door']
        SET_TWO = ['Touch Of Gray', 'Greatest Story', 'Jack-A-Roe', 'Little Red Rooster', 'Stagger Lee', 'High Time', 'Memphis Blues Again', 'Cassidy', 'Deal', 'China Cat Sunflower',
                   'I Know You Rider', 'Just A Little Light', 'Estimated Prophet', 'Eyes Of The World', 'Drums', 'Space', 'The Wheel', 'Gimme Some Lovin', 'Wharf Rat', 'Sugar Magnolia', 'Encore Break', 'Knockin On Heavens Door']
        s1 = [Track(x, 0, 0) for x in SET_ONE]
        s2 = [Track(x, 0, 0) for x in SET_TWO]
        results = makeStringsFromShows([s1, s2])
        print(fuzz.ratio(results[0], results[1]))


if __name__ == '__main__':
    unittest.main()
