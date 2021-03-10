#!/usr/bin/env python3

import sys
import json
import requests
import time
from tqdm import tqdm
from datetime import date
from bs4 import BeautifulSoup

ARCHIVE_COLLECTION = 'https://archive.org/search.php?query=collection%3AGratefulDead&page='
ARCHIVE_BASE_URL = 'https://archive.org/details/'
ETREE_BASE_URL = 'https://db.etree.org/db/shows/browse/artist_key/2/year/'
ARCHIVE_URL = 'www.archive.org'
SHOWS_DIRECTORY = 'shows'

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
	def __init__(self, name, duration, links, index):
		# we can extract many things from this data
		try:
			self.getSong(name)
			self.track_number = index
			self.getLength(duration)
			self.getLinks(links)
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
		return('{: >30} {: >10} {: >12}'.format(self.song, self.getTimeString(), self.linkTxt()))


def getYearPageData(page_index):
	print(' * Collecting shows from page {0}'.format(page_index))
	url = '{0}{1}'.format(ARCHIVE_COLLECTION, page_index)
	# perform a GET on this url
	response = requests.get(url)
	if response.status_code != 200:
		print('  Error: Got HTTP {0}'.format(response.status_code))
		return ''
	# save this reponse
	return response.text

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
		extracted_shows.append(Show.getFromArchive(i, title))
	return extracted_shows

def extractSinglePage(single_page):
	data = loadYearData()


def getArchiveData():
	index = 1
	for index in range(113, 199):
		time.sleep(5)
		data = getYearPageData(index + 1)
		if len(data) == 0:
			print('Could not get page {0}'.format(index))
			continue
		else:
			with open('./raw_data/page_{0}.html'.format(index), 'w') as page_file:
				page_file.write(data)
		for show in tqdm(shows):
			show_page = show.downloadPage()
			show.songs = extractPageData(show_page)
			show.saveData()
			time.sleep(2)

def getEtreeYear(year):
	url = '{0}{1}'.format(ETREE_BASE_URL, year)
	response = requests.get(url)
	if response.status_code == 200:
		return response.text
	else:
		return ''

def getEtreeData():
	print('Obtaining Etree list')
	for i in tqdm(range(1965, 1995)):
		data = getEtreeYear(i)
		with open('./etree_source/year_{0}.html'.format(i), 'w') as page_file:
			page_file.write(data)

def extractEtreeYear(year):
	# load the page, insert into bs4
	with open('./etree_source/year_{0}.html'.format(year), 'r') as page_file:
		data = page_file.read()
	soup = BeautifulSoup(data, features='html.parser')
	# get the first table you see
	table = soup.find('table')
	# grab all the TR's in that table except the first
	shows = table.findAll('tr')[1:]
	# tds from first to last are:
	# etree link, venue, city, state, download, add link, etree sources
	# we only want the links
	show_links = []
	for show in shows:
		downloads = show.findAll('td')[4]
		# we need all the links
		links = downloads.findAll('a')
		for l in links:
			# save the archive ones. grab the href
			show_link = l['href']
			if ARCHIVE_URL in show_link:
				# store the link
				show_links.append(show_link)
	return(show_links)

def getArchiveListFromEtree():
	shows = extractEtreeData(data)
	# now go through the shows
	for show in tqdm(shows):
		show_page = show.downloadPage()
		show.songs = extractPageData(show_page)
		show.saveData()

if __name__ == '__main__':
	archive_links = []
	for i in tqdm(range(1965, 1995)):
		new_data = extractEtreeYear(i)
		archive_links.extend(new_data)
	# save the data
	print('Saving...')
	with open('./etree_source/shows.json', 'w') as json_file:
		json.dump(archive_links, json_file, indent=4)
