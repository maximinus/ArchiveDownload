#!/usr/bin/env python3

class Show:
    def __init__(self, item, title):
        self.venue = ''
        self.date = None
        self.city = ''
        self.state = ''
        self.songs = []

    def getVenue(self, title):
        try:
            self.venue = title.split(':')[-1].strip()
        except:
            self.venue = "Unknown"

    @classmethod
    def getFromArchive(cls, item, title):
        show = Show()
        try:
            show.getVenue(title)
            show.getDetails(item)
        except:
            pass
        return(show)

    @classmethod
    def getFromEtree(cls):
        show = Show()
        return(show)

    def getDetails(self, item):
        self.title = item['data-id']
        data = self.title.split('.')[0]
        # result = gd1989-08-18
        data = data[2:].split('-')
        year = int(data[0])
        month = int(data[1])
        day = int(data[2])
        self.date = date(year, month, day)

    def downloadPage(self):
        # returns the archive page, or '' if no joy
        url = '{0}{1}'.format(ARCHIVE_BASE_URL, self.title)
        # use requests to load the page
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            # some error
            return ''

    def getFilePath(self):
        return './{0}/{1}.json'.format(SHOWS_DIRECTORY, self.title)

    def saveData(self):
        json_data = self.toJSON()
        with open(self.getFilePath(), 'w') as json_file:
            json.dump(json_data, json_file, indent=4)

    def toJSON(self):
        return {'title': self.title,
                'venue': self.venue,
                'year': self.date.year,
                'month': self.date.month,
                'day': self.date.day,
                'city': self.city,
                'state': self.state,
                'songs': [x.toJSON() for x in self.songs]}

    @classmethod
    def fromJSON(cls, json_data):
        new_show = Show()
        new_show.title = json_data['title']
        new_show.venue = json_data['venue']
        new_show.city = json_data['city']
        new_show.state = json_data['state']
        new_show.date = date(json_data['year'], json_data['month'], json_data['day'])
        new_show.songs = [Track.fromJSON(x) for x in json_data['songs']]
        return new_show

    def __repr__(self):
        date_format = self.date.strftime('%a %d %b %y')
        recording = self.title.split('.')[-1]
        return '{0}: {1}'.format(date_format, recording)

class Track:
    def __init__(self, name, duration, index):
        # we can extract many things from this data
        try:
            self.getSong(name)
            self.track_number = index
            self.getLength(duration)
        except Exception as e:
            print(' * Error: {0}'.format(e))
            print(' * {0} : {1}'.format(name, duration))

    def getSong(self, name):
        # starts with gd?
        if name.startswith('gd'):
            data = ' '.join(name.split()[2:])
            self.song = data
        else:
            self.song = name

    def getLength(self, duration):
        # example of this data: PT0M304S
        # always of the format
        data = duration[4:-1]
        self.length = int(data)

    def getTimeString(self):
        minutes = self.length // 60
        seconds = self.length - (minutes * 60)
        return('{0}m {1}s'.format(minutes, seconds))

    def toJSON(self):
        ogg_file = self.ogg if self.ogg is not None else ''
        mp3_file = self.mp3 if self.mp3 is not None else ''
        return {'song': self.song,
                'order': self.track_number,
                'length': self.length,
                'ogg': ogg_file,
                'mp3': mp3_file}

    @classmethod
    def fromJSON(cls, json_data):
        new_track = Track('', '', '', 0)
        new_track.title = json_data['song']
        new_track.track_number = json_data['order']
        new_track.length = json_data['length']
        new_track.ogg = json_data['ogg']
        if new_track.ogg != '':
             new_track.ogg = None
        new_track.mp3 = json_data['mp3']
        if new_track.mp3 != '':
            new_track.mp3 = None
        return new_track

    def __repr__(self):
        return(f'{self.song}, {self.getTimeString()}')
