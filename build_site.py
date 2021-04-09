#!/usr/bin/env python3

import os
import math
import pickle
from datetime import date
from gd import SongData, SongStats
from jinja2 import Template

# produce the HTML pages from the saved data

"""
self.name                       -> string
self.times_played               -> int
self.first_five                 -> list<SongData>
self.last_five                  -> list<SongData>
self.longest_five               -> list<SongData>
self.shortest_five              -> list<SongData>
self.before                     -> list<SongData>
self.after                      -> list<SongData>
self.played_per_year            -> list<int>
self.average_length             -> int
self.average_length_by_years    -> list<int>
"""


def getDateText(date):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    # return as "13th Oct 1990" or similar
    if 4 <= date.day <= 20 or 24 <= date.day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][date.day % 10 - 1]
    month_text = months[date.month - 1]
    return f'{date.day}{suffix} {month_text} {str(date.year)[-2:]}'


def getLengthText(length):
    if length == 0:
        return 'Unknown'
    minutes = length // 60
    seconds = length - (minutes * 60)
    return f'{minutes}m {seconds}s'


def getTimeBetween(start, end):
    # From https://stackoverflow.com/questions/4436957/pythonic-difference-between-two-dates-in-years/8971809
    if start == end:
        return 'Played only once'
    try:
        from_in_this_year = date(end.year, start.month, start.day)
    except:
        # today is feb in leap year
        from_in_this_year = date(end.year, start.month, start.day - 1)

    if from_in_this_year <= end:
        years = end.year - start.year
        days = (end - from_in_this_year).days
    else:
        years = end.year - start.year - 1
        try:
            from_in_prev_year = date(end.year - 1, start.month, start.day)
        except:
            # today is feb in leap year
            from_in_prev_year = date(end.year - 1, start.month, start.day-1)
        days = (end - from_in_prev_year).days
    if years == 0 and days == 0:
        return 'Played only once'
    if years == 0:
        # only days
        return f'{days} days'
    return f'{years} years, {days} days'


def getLengthVersions(longest_five):
    data = []
    for index, i in enumerate(longest_five):
        data.append([index + 1, getDateText(i.date), getLengthText(i.length)])
    return data


def buildSongStats(song, song_template):
# song is a gd.SongStats, as documented above
    # we put data into a special dict for the template
    start_date = song.first_five[0].date
    end_date = song.last_five[0].date
    data = {'name': song.name,
            'total_played': song.times_played,
            'start_date': getDateText(start_date),
            'end_date': getDateText(end_date),
            'length_active': getTimeBetween(start_date, end_date),
            'longest_versions': getLengthVersions(song.longest_five),
            'shortest_versions': getLengthVersions(song.shortest_five),
            'songs_before': song.before,
            'songs_after': song.after,
            'chance_played': ','.join([str(x * 100.0) for x in song.played_per_year]),
            'order_played': song.order_played,
            'show_number': song.show_number,
            'first_five': [[getDateText(x.date), x.venue] for x in song.first_five],
            'last_five': [[getDateText(x.date), x.venue] for x in song.last_five],
            'average_length': getLengthText(song.average_length),
            'year_lengths': ','.join([str(x) for x in song.average_length_by_years]),
            'average_position': ','.join([str(x) for x in song.average_position])
    }
    html_page = song_template.render(data)
    # and then save
    filename = song.name
    filename = filename.replace(' ', '_')
    filename = filename.replace('/', '_')
    html_file = open(f'./website/static/songs/{filename}.html', 'w')
    html_file.write(html_page)
    html_file.close()


def loadAllSongStats():
    song_stats = []
    for pickle_file in os.listdir('./data/stats/songs'):
        song_stats.append(pickle.load(open(f'./data/stats/songs/{pickle_file}', 'rb')))
    return song_stats


if __name__ == '__main__':
    print('* Building static site')
    songs = loadAllSongStats()
    with open('./website/song_template.html') as f:
        html_template = f.read()
    song_template = Template(html_template)
    for i in songs:
        print(f'  Building "{i.name}"')
        buildSongStats(i, song_template)
