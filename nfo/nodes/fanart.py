
from nfo.nodes import Node, thumbs


class FanArt(Node):
	"""Model of the `fanart` element.

	Arguments:
		url (str): Base URL for the fan art.
		thumb_specs (list): A list of `thumbs.Thumb` constructor dicts.

	Attributes:
		thumbs (list): A list of `thumbs.Thumb`.
		url (str): The base URL for the fan art.

	Example:
		FIXME :(

	"""

	def __init__(self, url, thumb_specs):
		super().__init__('fanart')
		self.thumbs = thumbs.Thumbs(thumb_specs)
		self.update({'url': url})

	@property
	def url(self):
		return self.attributes.get('url')

	@url.setter
	def url(self, value):
		self.update({'url': value})
