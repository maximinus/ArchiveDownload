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
		json = {'venue': 'TEST',
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


class TestSong(unittest.TestCase):
	def test_CanGetNull(self):
		track = Track('', '', '', 0)
		self.assertIsNotNone(show)		

	def test_GetNonNull(self):
		self.assertEqual(1, 1)

	def test_JsonOut(self):
		self.assertEqual(1, 1)

	def test_JsonIn(self):
		self.assertEqual(1, 1)

	def test_JsonFlow(self):
		self.assertEqual(1, 1)


if __name__ == '__main__':
	unittest.main()
