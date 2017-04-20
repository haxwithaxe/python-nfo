
from nfo.nodes import String, Nodes


class Thumbs(Nodes):

	def __init__(self, thumbs=[]):
		super().__init__(Thumb, thumbs)


class Thumb(String):

	def __init__(self, thumbnail=None, required=False):
		super().__init__('thumb', default=thumbnail, required=required)
