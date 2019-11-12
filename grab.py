#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from datetime import date
from songs import findSong

ARCHIVE_BASE_URL = 'https://archive.org/details/'

class Show:
	def __init__(self, item, title):
		self.venue = ''
		self.date = None
		try:
			self.getVenue(title)
			self.getDetails(item)
		except:
			pass
		self.songs = []

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

	def saveData(self):
		pass


	def toJSON(self):
		return {'venue': self.venue,
				'year': self.date.year,
				'month': self.date.month,
				'day': self.date.day,
				'songs': [x.toJSON() for x in self.songs]}

	@classmethod
	def fromJSON(cls, json_data):
		new_show = Show('', '')
		new_show.venue = json_data['venue']
		new_show.date = date(json_data['year'], json_data['month'], json_data['day'])
		new_show.songs = [Track.fromJSON(x) for x in json_data['songs']]
		return new_show


	def __repr__(self):
		date_format = self.date.strftime('%a %d %b %y')
		recording = self.title.split('.')[-1]
		return '{0}: {1}'.format(date_format, recording)

class Track:
	def __init__(self, name, duration, links, index):
		# we can extract many things from this data
		try:
			self.getSong(name)
			self.track_number = index
			self.getLength(duration)
			self.getLinks(links)
		except:
			pass

	def getSong(self, name):
		# starts with gd?
		if name.startswith('gd'):
			data = ' '.join(name.split()[2:])
			self.song = findSong(data)
		else:
			self.song = findSong(name)

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

	def toJSON(self):
		ogg_file = self.ogg if self.ogg is not None else ''
		mp3_file = self.mp3 if self.mp3 is not None else ''
		return {'title': self.song,
				'order': self.track_number,
				'length': self.length,
				'ogg': ogg_file,
				'mp3': mp3_file}

	@classmethod
	def fromJSON(cls, json_data):
		new_track = Track('', '', '', 0)
		new_show.title = json_data['title']
		new_show.track_number = json['order']
		new_show.length = json['length']
		new_show.ogg = json['ogg']
		if new_show.ogg != '':
			 new_show.ogg = None
		new_show.mp3 = json['mp3']
		if new_show.mp3 != '':
			new_show.mp3 = None
		return new_track

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
	order = 1
	for t in tracks:
		name = t.find('meta', {'itemprop': 'name'})['content']
		duration = t.find('meta', {'itemprop': 'duration'})['content']
		links = [x['href'] for x in t.findAll('link')]
		songs.append(Track(name, duration, links, order))
		order += 1
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
	page = loadFile('./html/single_show.html')
	data = loadYearData()
	shows = extractYearData(data)
	# now go through the shows
	for show in shows[:1]:
		show_page = shows[0].downloadPage()
		show.songs = extractPageData(page)
		show.saveData()
