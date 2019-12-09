
from datetime import datetime as dt

from nfo.nodes import actors, playback, episodeguide, episodes, genres, thumbs
from nfo.nodes import Date, Float, Int, Node, String
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
	('season', None),
	('episode', None),
	('displayseason', None),
	('displayepisode', None),
	('runtime', None)
	)


_float_elements = (('rating', None), ('epbookmark', None))


def _elements():
	elements = {
		'aired': Date('aired'),
		'dateadded': Date('dateadded', format_string='%Y-%m-%d %H:%M:%S'),
		'premiered': Date('premiered'),
		'year': Date('year', '%Y'),
		'episodeguide': episodeguide.EpisodeGuide(),
		'resume': playback.Resume(),
		'actors': actors.Actors(),
		'episodes': episodes.Episodes(),
		'genres': genres.Genres(),
		'thumbs': thumbs.Thumbs()
		}
	elements.update({k: String(k, v) for k, v in _string_elements})
	elements.update({k: Int(k, v) for k, v in _int_elements})
	elements.update({k: Float(k, v) for k, v in _float_elements})
	return elements


class TVShow(Node, _oodict.Mixin):

    root_node = "tvshow"

	def __init__(self, **details):
		super().__init__(self.root_node)
		self.data = _elements()
		self.update_data(details)

	@property
	def children(self):
		for epp in self.episodes:
			epp.genres = self.genres
		return self.data.values()
