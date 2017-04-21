
from nfo.nodes import actors, fileinfo, thumbs
from nfo.nodes import Date, Int, Float, Node, Nodes, String
from nfo import _oodict


def new_data():
	data = {
		'actors': actors.Actors(),
		'thumbs': thumbs.Thumbs(),
		'fileinfo': fileinfo.FileInfo(), 
		'title': String('title'),
		'showtitle': String('showtitle'),  # the title of the show
		'plot': String('plot'),
		'thumb': thumbs.Thumb(),
		'credits': String('credits'),
		'director': String('director'),
		'studio': String('studio'),  # Production studio or channel
		'mpaa': String('mpaa'),  # MPAA certification
		'rating': Float('rating', valid_range=(1, 10)),
		'season': Int('season'),
		'episode': Int('episode'),
		'playcount': Int('playcount', 0),
		'lastplayed': Int('lastplayed'),
		'epbookmark': Int('epbookmark'),  # For media files containing multiple episodes, where value is the time where the next episode begins in seconds.
		'displayseason': Int('displayseason'),  # For TV show specials, determines how the special episode is sorted in "all" and season views.
		'displayepisode': Int('displayepisode'),  # For TV show specials, determines how the special episode is sorted in "all" and season views. If marked as episode 7, the special will come before the real episode 7.
		'aired': Date('aired'),
		'premiered': Date('premiered')
		}
	return data


class Episodes(Nodes):

	def __init__(self, episodes=[], showtitle=None):
		super().__init__(Episode, node_specs=episodes, common_specs={'showtitle': showtitle})
		self.override_with_type = Nodes


class Episode(Node, _oodict.Mixin):

	def __init__(self, **details):
		super().__init__('episodedetails')
		self.data = new_data()
		self.override_with_type = Episode
		self.update_data(details)

	@property
	def children(self):
		return self.data.values()
