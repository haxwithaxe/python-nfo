
from nfo.nodes import Node, thumbs


class FanArt(Node):

	def __init__(self, url, thumbs_specs):
		super().__init__('fanart')
		self.thumbs = thumbs.Thumbs(thumbs_specs)
		self.update({'url': url})

	@property
	def url(self):
		return self.attributes.get('url')

	@url.setter
	def url(self, value):
		self.update({'url': value})
