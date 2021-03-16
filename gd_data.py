#!/usr/bin/env python3

from datetime import date
from bs4 import BeautifulSoup

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
        date_data = date_text.split('-')
        date_data = [int(x) for x in date_data]
        show.date = date(date_data[0], date_data[1], date_data[2])
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
        return {'venue': self.venue,
                'year': self.date.year,
                'month': self.date.month,
                'day': self.date.day,
                'location': self.location,
                'songs': [x.toJSON() for x in self.songs]}

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
        if self.name == other.name:
            return True
        print(f'{self.name} != {other.name}')
        return False

    def __repr__(self):
        return(f'{self.name}, {self.getTimeString()}')
