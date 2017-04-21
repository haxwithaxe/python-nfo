
from datetime import datetime as dt
import glob
import re
import os

import requests
from lxml.etree import tostring  # pylint: disable=no-name-in-module
from lxml.html import fromstring

from nfo import tvshow, nodes
from nfo.tvshow import episodes

DEFAULT_THUMB_EXT = 'jpg'
SEARCH_FILTERS = [
	(lambda name: 'h_cek' in name.lower(), 'háček'),
	(lambda name: name.lower().strip() == 'welcome',
		'Opening Remarks, Rumblings, Ruminations, and Rants'),
	(lambda name: 'LeveragingThreatIntelDisinformationCampaigns'.lower() == name.lower().strip(),
		'The Threat Intel Results are in'),
	(lambda name: 'QuickDirtyArmEmulation'.lower() == name.lower().strip(),
		'Quick and Dirty Emulation of ARM Firmware'),
	(lambda name: 'firetalks' in name.lower(), 'Firetalks')
	]


def normalize_name(name):
	de_punct = re.sub(r'[#.,…;:?’)(]+', r'', name.strip().replace('&', 'and'))
	return re.sub(r'[\s_\u2010-\u2015-]+', r'', de_punct).lower()


def _scraper_friendly_name_format(name):
	de_punct = re.sub(r'[#.,…;:?’)(]+', r'', name.strip().replace('&', 'and'))
	de_dashed = re.sub(r'[\u2010-\u2015]+', r'', de_punct.strip())
	dotted = re.sub(r'\s+', r'.', de_dashed.strip())
	return dotted.lower()


def _get_title_of(filename):
	return filename.split(' - ', 1)[1].split('.')[0]


class Khanfu:

	def __init__(self, event_id, title, year, season, target_dir='.'):
		self._target_dir = os.path.abspath(target_dir)
		self.conference = Conference(title=title, season=season, target_dir=self._target_dir, studio='The Shmoo Group')
		self.url = 'https://www.khanfu.com/m/plain/%s/talks' % event_id
		self.year = year
		self.load()
		self.merge_firetalks()

	def load(self):
		response = requests.get(self.url)
		index = response.text
		tree = fromstring(index)
		for talk in [li.find('a').attrib['href'] for li in tree.xpath('body/ul/li')]:
			speakers = []
			response = requests.get('https://www.khanfu.com'+talk)
			tree = fromstring(response.text)
			spec_elems = tree.xpath('//div[@title]')
			if spec_elems:
				spec = spec_elems[0]
			else:
				print('tree', tostring(tree, pretty_print=True).decode())
				return
			title = spec.xpath('//h1/a')[0].text
			for elem in spec.xpath('h2'):
				if elem.text == 'Presented by':
					for h2_elem in elem.itersiblings():
						if h2_elem.tag.lower() == 'fieldset':
							for a_elem in h2_elem.xpath('//div/label/p[@class="celltitle"]/a'):
								speakers.append({'name': a_elem.text, 'role': 'speaker'})
			when, where = spec.xpath('fieldset/div/label')[:2]
			plot_element = spec.xpath('//div/div/p')
			if plot_element:
				plot = plot_element[0].text
			else:
				plot = ''
			self.conference.episodes.append(
					{
						'title': title.strip(),
						'start_time': self.__to_time_range(when.text.strip())[0],
						'end_time': self.__to_time_range(when.text.strip())[1],
						'track': where.text.strip(),
						'plot': plot.strip(),
						'actors': speakers
						}
					)

	def merge_firetalks(self):
		firetalks = [x for x in self.conference.episodes if x.track.lower().strip() == 'firetalks']
		for epp in firetalks:
			epp.episode = 0
		firetalks.sort(key=lambda x: x.start_time)
		firetalks_episode = {
				'title': 'Firetalks',
				'start_time': firetalks[0].start_time,
				'end_time': firetalks[-1].end_time,
				'track': firetalks[0].track
				}
		firetalks_episode['actors'] = [a for t in firetalks for a in t.actors]
		talks = []
		for fire in firetalks:
			title = fire.title
			actors = ' by '+', '.join(x.name for x in firetalks_episode['actors'])
			plot = fire.plot
			talks.append('{} by {}\n\t{}'.format(title, actors, plot))
		firetalks_episode['plot'] = '\n* '.join(talks)
		self.conference.episodes.append(firetalks_episode)

	def __findall(self, name):
		return [x for x in self.conference.episodes if normalize_name(name) in normalize_name(x.title._value)]

	def __tryharder(self, name, rellength=0.4):
		length = rellength*len(name)
		trythese = [
				name,
				''.join(name.split()),
				name[:int(length)],
				''.join(name[:int(length)].split()),
				name[int(length):],
				''.join(name[int(length):].split())
				]
		for trial in trythese:
			matches = self.__findall(trial)
			if matches:
				return matches
		print('No matches. Tried these:', [normalize_name(z) for z in trythese])

	def __find_episode(self, name=None, track=None):
		if track:
			return [e for e in self.conference.episodes if e['where'].lower().strip() == track.lower().strip()]
		for filtr in SEARCH_FILTERS:
			if filtr[0](name):
				name = filtr[1]
				break
		found = self.__tryharder(name)
		if found:
			if len(found) > 1:
				raise ValueError('too many matches for "%s": "%s"' % (name, [x['title'] for x in found]))
			return found[0]
		else:
			return None
	
	def map_to_files(self, files):
		for filename in files:
			episode = self.__find_episode(name=_get_title_of(filename))
			episode.filename = filename

	def __to_time_range(self, when):
		day, times = when.split(',')
		start, end = times.split(' - ')
		return (
				dt.strptime('%s %s %s' % (self.year, day.strip(), start.strip()), '%Y %B %d %H:%M'),
				dt.strptime('%s %s %s' % (self.year, day.strip(), end.strip()), '%Y %B %d %H:%M')
				)


class Talk(episodes.Episode):

	def __init__(self, **details):
		super().__init__(**details)
		self._scraper_friendly_filename = None
		self.filename = details.get('filename')
		self._thumb_ext = details.get('thumb_ext')
		self.track = details.get('track')
		self.start_time = details.get('start_time')
		self.end_time = details.get('end_time')
		# The below are elements
		if self.start_time:
			self.aired = self.start_time
			self.premiered = self.start_time
			self.year = self.start_time

	def find_thumbnails(self, filename, target_dir):
		image_prefix_dir = os.path.join(target_dir)
		image_name_prefix = os.path.splitext(os.path.basename(filename))[0]
		image_prefix = os.path.join(image_prefix_dir, image_name_prefix)
		image_glob = '{}*.{}'.format(image_prefix, self._thumb_ext or DEFAULT_THUMB_EXT)
		image_files = glob.glob(image_glob)
		self.thumbs = [{'thumbnail': x} for x in image_files if x]

	def _scraper_friendly_basename(self):
		if self._scraper_friendly_filename:
			return self._scraper_friendly_filename
		elif not self.filename:
			self.debug('scrapper_friendly_filename no file for', self.title)
			return None
		else:
			values = {
					'conference': _scraper_friendly_name_format(self.showtitle.value),
					'season': self.season.value,
					'episode': self.episode.value,
					'title': _scraper_friendly_name_format(self.title.value),
					}
			return '{conference}-s{season:02d}e{episode:02d}-{title}'.format(**values)

	def scraper_friendly_nfoname(self):
		sffilename = self._scraper_friendly_basename()
		if sffilename:
			return sffilename+'.nfo'

	def scraper_friendly_filename(self):
		sffilename = self._scraper_friendly_basename()
		if sffilename:
			return sffilename+os.path.splitext(self.filename)[1]


	def __lt__(self, other):
		try:
			if other.start_time == self.start_time:
				if self.track and other.track:
					return self.track < other.track
				return False
			elif self.start_time < other.start_time:
				return True
		except TypeError:
			pass
		return False


class Talks(nodes.Nodes):

	def __init__(self, season=None, showtitle=None, genres=None):
		super().__init__(Talk, common_specs={'showtitle': showtitle, 'season': season, 'genres': genres})


class Conference(tvshow.TVShow):

	def __init__(self, title, season, target_dir=None, studio=None, first_show=None):
		super().__init__(title=title, showtitle=title, season=season, genres=['Documentary', 'Special Interest',
			'Conference'], episodes=Talks(showtitle=title, season=season))
		self._target_dir = target_dir
		self.studio = studio
		if first_show:
			self.aired = first_show
			self.year = first_show
			self.premiered = first_show
		self.thumbs.append({'season': 13, 'aspect': 'banner', 'thumbnail': 'http://3f7muexklyg3r0dc37ttz512.wpengine.netdna-cdn.com/wp-content/uploads/2016/09/ShmooBanner2017.png'})

	def set_episode_thumbnails(self):
		self.episodes.sort()
		for episode in self.episodes:
			if episode.filename:
				episode.find_thumbnails(episode.filename, self._target_dir)

	def set_episode_numbers(self):
		self.episodes.sort()
		for i, episode in enumerate(self.episodes):
			if not episode.episode:
				episode.episode = i+1

	def __xml__(self):
		self.set_episode_numbers()
		self.set_episode_thumbnails()
		return super().__xml__()

if __name__ == '__main__':
	import sys
	dest = sys.argv[1]
	dest = os.path.join(dest, 'shmoocon.13')
	os.makedirs(dest, exist_ok=True)
	files = sys.argv[2:]
	con = Khanfu(76, 'ShmooCon', 2017, 13, target_dir=dest)
	con.conference.set_episode_numbers()
	con.map_to_files(files)
	for talk in con.conference.episodes:
		if talk.filename:
			os.symlink(talk.filename, os.path.join(dest, talk.scraper_friendly_filename()))
			with open(os.path.join(dest, talk.scraper_friendly_nfoname()), 'w') as talknfo:
				talknfo.write(str(talk))
	with open(os.path.join(dest, 'tvshow.nfo'), 'w') as connfo:
		con.conference.episodes = []
		connfo.write(str(con.conference))
