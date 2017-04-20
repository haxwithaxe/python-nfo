
from nfo.nodes import String, Nodes


class Genres(Nodes):

	def __init__(self, genres=[]):
		super().__init__(Genre, genres)


class Genre(String):

	def __init__(self, genre):
		super().__init__('genre', genre)
