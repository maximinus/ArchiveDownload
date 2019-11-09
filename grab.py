#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from datetime import date
from songs import findSong

URL = 'https://archive.org/details/gd1982-07-27.141510.sbd.pcm.streeter.dalton.miller.clugston.flac1644'


class Track:
	def __init__(self, name, duration, links):
		# we can extract many things from this data
		self.getSong(name)
		self.getDate(name)
		self.getTrackNumber(name)
		self.getLength(duration)
		#self.mp3_link
		#self.ogg_link

	def getSong(self, name):
		data = ' '.join(name.split()[2:])
		self.song = findSong(data)

	def getDate(self, name):
		# [2:] - remove 'gd' part
		data = name.split()[0][2:]
		date_info = data.split('-')
		year = int(date_info[0]) + 1900
		month = int(date_info[1])
		day = int(date_info[2])
		self.date = date(year, month, day)

	def getTrackNumber(self, name):
		# [1:] - remove 't'
		data = name.split()[1][1:]
		self.track_number = int(data)

	def getLength(self, duration):
		# example of this data: PT0M304S
		# always of the format
		data = duration[4:-1]
		self.length = int(data)

	def getTimeString(self):
		minutes = self.length // 60
		seconds = self.length - (minutes * 60)
		return('{0}m {1}s'.format(minutes, seconds))

	def __repr__(self):
		return '{0}: {1}s'.format(self.song, self.getTimeString())

def getBytesAndSave():
	response = requests.get(URL)
	if response.status_code != 200:
		print('  Error in response, got HTTP {0}'.format(response.status_code))
		return
	# response data is bytes, we need as a string
	return response.text

def loadFile(name):
	with open(name, 'r') as foo:
		page = foo.read()
	return page

def extractPageData(page):
	# parse the HTML to get the links
	soup = BeautifulSoup(page, features='html.parser')
	main_wrap = soup.find('div', {'id': 'theatre-ia-wrap'})
	# now find the tracks in this
	tracks = main_wrap.findAll('div', {'itemprop':'track'})
	songs = []
	for t in tracks:
		name = t.find('meta', {'itemprop': 'name'})['content']
		duration = t.find('meta', {'itemprop': 'duration'})['content']
		links = [x['href'] for x in t.findAll('link')]
		songs.append(Track(name, duration, links))
	return songs

if __name__ == '__main__':
	page = loadFile('page.html')
	songs = extractPageData(page)
	for i in songs:
		print(i)

