
from nfo.nodes import Node, URL


class EpisodeGuide(Node):

	def __init__(self, url=None, cache=None):
		super().__init__('episodeguide')
		self.url = url
		self.cache = cache

	@property
	def children(self):
		return [URL('url', self.url, cache=self.cache)]
