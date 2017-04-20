
from datetime import datetime as dt

from nfo.nodes import actors, playback, episodeguide, episodes, genres
from nfo.nodes import Date, Float, Int, Node, Nodes, String
from nfo import _oodict


_string_elements = (
	('title', None),
	('showtitle', None),
	('uniqueid', None),
	('outline', None),
	('plot', None),
	('tagline', None),
	('mpaa', None),
	('playcount', None),
	('lastplayed', None),
	('id', None),
	('set', None),
	('status', None),
	('code', None),
	('studio', None),
	('trailer', None)
	)


_int_elements = (
	('votes', None),
	('top250', None),
	('season', -1),
	('episode', -1),
	('displayseason', None),
	('displayepisode', None),
	('runtime', None)
	)


_float_elements = (('rating', None), ('epbookmark', None))


def _elements():
	elements = {
		'aired': Date('aired'),
		'dateadded': Date('dateadded', default=dt.now(), format_string='%Y-%m-%d %H:%M:%S'),
		'premiered': Date('premiered'),
		'year': Date('year', '%Y'),
		'episodeguide': episodeguide.EpisodeGuide(),
		'resume': playback.Resume(),
		'actors': actors.Actors(),
		'episodes': episodes.Episodes(),
		'genres': genres.Genres()
		}
	elements.update({k: String(k, v) for k, v in _string_elements})
	elements.update({k: Int(k, v) for k, v in _int_elements})
	elements.update({k: Float(k, v) for k, v in _float_elements})
	return elements


class TVShow(Node, _oodict.Mixin):

	def __init__(self, **details):
		super().__init__('tvshow')
		self.data = _elements()
		self.aired = details.get('aired')
		self.actors = details.get('actors', [])
		self.episodes = details.get('episodes', [])
		self.episodeguide = details.get('episodeguide', {})

	@property
	def children(self):
		elements = []
		for node in self.data.values():
			if isinstance(node, Nodes):
				elements.extend(list(node))
			else:
				elements.append(node)
		return elements
