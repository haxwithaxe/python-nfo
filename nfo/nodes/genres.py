
from nfo.nodes import String, Nodes


class Genres(Nodes):
	"""Collection of `Genre` instances.

	Arguments:
		genres (list): A list of strings describing the genres the media belongs to.

	"""

	def __init__(self, genres=None):
		super().__init__(Genre, genres or [])


class Genre(String):
	"""Model of a `genre`element.

	Arguments:
		genre (str): A string describing one of the genres the media belongs to.

	"""

	def __init__(self, genre):
		super().__init__('genre', genre)
