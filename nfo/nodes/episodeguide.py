"""Model for the `episodeguide` element."""
from nfo.nodes import Node, URL


class EpisodeGuide(Node):
	"""Model for the `episodeguide` element.
	
	Arguments:
		url (str, optional): Episode guide URL. Defaults to None.
		cache (str, optional): Filename of the cached episode guide. Defaults to None.
	
	"""

	def __init__(self, url=None, cache=None):
		super().__init__('episodeguide')
		self.url = url
		self.cache = cache

	@property
	def children(self):
		return [URL('url', self.url, cache=self.cache)]

	def __bool__(self):
		"""This element is falsey if it has no values set."""
		return self.url and self.cache
