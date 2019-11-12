#!/usr/bin/env python3

# tests for class items

import unittest
from grab import Show, Track

class TestShow(unittest.TestCase):
	def test_CanGetNull(self):
		show = Show('', '')
		self.assertIsNotNone(show)

	def test_GetVenue(self):
		show = Show({'data-id': 'gd1989-08-18.xxx'},'TEST:TEST')
		self.assertEqual('TEST', show.venue)

	def test_JsonOut(self):
		show = Show({'data-id': 'gd1989-08-18.xxx'},'TEST:TEST')
		json_data = show.toJSON()
		self.assertEqual(json_data['venue'], 'TEST')

	def test_JsonIn(self):
		json = {'title': 'what.a.great.show',
				'venue': 'TEST',
		        'year': 1977,
		        'month': 11,
		        'day': 5,
		        'songs': []}
		show = Show.fromJSON(json)
		self.assertEqual(show.venue, 'TEST')

	def test_JsonFlow(self):
		show = Show({'data-id': 'gd1989-08-18.xxx'},'TEST:TEST')
		json_data = show.toJSON()
		other_one = Show.fromJSON(json_data)
		self.assertEqual(show.date, other_one.date)

	def test_CanWriteFile(self):
		show = Show({'data-id': 'gd1989-08-18.xxx'},'TEST:TEST')
		show.saveData()
		self.assertEqual(True, True)

	def test_RewriteWithSongs(self):
		track1 = Track('Dark Star', 'PT0M304S', ['song.ogg', 'song.mp3'], 0)
		track2 = Track('Dark Star', 'PT0M304S', ['song.ogg', 'song.mp3'], 0)
		show = Show({'data-id': 'gd1989-08-18.yyy'},'TEST:TEST')
		show.songs = [track1, track2]
		show.saveData()
		self.assertEqual(True, True)

class TestSong(unittest.TestCase):
	def test_CanGetNull(self):
		track = Track('', '', '', 0)
		self.assertIsNotNone(track)

	def test_GetNonNull(self):
		track = Track('Dark Star', 'PT0M304S', ['song.ogg', 'song.mp3'], 0)
		self.assertEqual(track.song, 'Dark Star')

	def test_JsonOut(self):
		track = Track('Dark Star', 'PT0M304S', ['song.ogg', 'song.mp3'], 0)
		json_data = track.toJSON()
		self.assertEqual(json_data['song'], 'Dark Star')

	def test_JsonIn(self):
		json = {'song': 'Dark Star',
		        'length': 240,
		        'order': 3,
		        'mp3': 'song.mp3',
		        'ogg': 'song.ogg'}
		track = Track.fromJSON(json)
		self.assertEqual(track.title, 'Dark Star')

	def test_JsonFlow(self):
		track = Track('Dark Star', 'PT0M304S', ['song.ogg', 'song.mp3'], 0)
		json_data = track.toJSON()
		other_one = Track.fromJSON(json_data)
		self.assertEqual(track.length, other_one.length)


if __name__ == '__main__':
	unittest.main()
