
from nfo.nodes import String, Nodes


ASPECT_BANNER = 'banner'
ASPECT_POSTER = 'poster'


class Thumbs(Nodes):

	def __init__(self, thumbs=[]):
		super().__init__(Thumb, thumbs)


class Thumb(String):

	def __init__(self, thumbnail=None, required=False, **attributes):
		"""
		
		XML Attributes:
			aspect: banner|poster
			type: season|
			season (int):
			dim: Dimensions "XxY"
			colors: "|0,177,205|1,60,92|3,52,84|"
			preview: image url path "_cache/fanart/original/72306-4.jpg"

		"""
		super().__init__('thumb', default=thumbnail, required=required)
		self.update({k.strip('_'): v for k, v in attributes.items() if v is not None})
