#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from datetime import date
from songs import findSong

URL = 'https://archive.org/details/gd1982-07-27.141510.sbd.pcm.streeter.dalton.miller.clugston.flac1644'


class Show:
	def __init__(self, item, title):
		self.getVenue(title)
		self.getDetails(item)

	def getVenue(self, title):
		try:
			self.venue = title.split(':')[-1].strip()
		except:
			self.venue = "Unknown"

	def getDetails(self, item):
		self.title = item['data-id']
		data = self.title.split('.')[0]
		# result = gd1989-08-18
		data = data[2:].split('-')
		year = int(data[0])
		month = int(data[1])
		day = int(data[2])
		self.date = date(year, month, day)

	def __repr__(self):
		date_format = self.date.strftime('%a %d %b %y')
		recording = self.title.split('.')[-1]
		return '{0}: {1}'.format(date_format, recording)

class Track:
	def __init__(self, name, duration, links):
		# we can extract many things from this data
		self.getSong(name)
		self.getDate(name)
		self.getTrackNumber(name)
		self.getLength(duration)
		self.getLinks(links)

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

	def getLinks(self, links):
		# grab the URL links
		self.ogg = None
		self.mp3 = None
		for i in links:
			# just grab the first for now
			if i.endswith('mp3') and self.mp3 is None:
				self.mp3 = i
			if i.endswith('ogg') and self.ogg is None:
				self.ogg = i

	def linkTxt(self):
		texts = []
		if self.mp3 is not None:
			texts.append('MP3')
		if self.ogg is not None:
			texts.append('OGG')
		return '[{0}]'.format(', '.join(texts))

	def __repr__(self):
		return('{: >30} {: >10} {: >12}'.format(self.song, self.getTimeString(), self.linkTxt()))


def getYearData():
	#url = 'https://archive.org/details/GratefulDead?&and[]=year%3A"1967"'
	url = 'https://archive.org/search.php?query=collection%3AGratefulDead&page=1'
	# perform a GET on this url
	response = requests.get(url)
	# save this reponse
	with open('get.html', 'w') as foo:
		foo.write(response.text)

def getBytes():
	response = requests.get(URL)
	if response.status_code != 200:
		print('  Error in response, got HTTP {0}'.format(response.status_code))
		return
	# response data is bytes, we need as a string
	return response.text
1
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

def loadYearData():
	with open('./html/get.html', 'r') as data_file:
		year_data = data_file.read()
	return year_data

def extractYearData(year):
	# get the results
	soup = BeautifulSoup(year, features='html.parser')
	results = soup.find('div', {'class': 'results'})
	# all the shows we found, please
	matches = results.findAll('div', class_='item-ia')
	# filter this by ones which have a 'data-id'
	shows = []
	for i in matches:
		data = i['data-id']
		if data.startswith('gd19'):
			shows.append(i)
	# now grab the data we need
	extracted_shows = []
	for i in shows:
		title = i.findAll('a')[1]['title']
		extracted_shows.append(Show(i, title))
	return extracted_shows

if __name__ == '__main__':
	#page = loadFile('page.html')
	#songs = extractPageData(page)
	#for i in songs:
	#	print(i)
	#getYearData()
	data = loadYearData()
	shows = extractYearData(data)
	for i in shows:
		print(i)
