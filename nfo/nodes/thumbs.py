
from nfo.nodes import String, Nodes


ASPECT_BANNER = 'banner'
ASPECT_POSTER = 'poster'


class Thumbs(Nodes):
	"""A collection of `Thumb` instances.

	Arguments:
		thumb_specs (list, optional): A list of `Thumb` constructor dict instances.
		
	"""

	def __init__(self, thumb_specs=None):
		super().__init__(Thumb, thumb_specs)


class Thumb(String):

	def __init__(self, thumbnail=None, required=False, **attributes):
		"""Model of a `thumb` element.

		Arguments:
			thumbnail (str, optional): The path or URL of the thumbnail image. Defaults to None.
			required (bool): Inherited from `nodes.Node`.
			**attributes: See keyword arguments. These are naively used as element attributes. All items with a value of
			None are omitted from the element's attributes.

		Keyword arguments:
			aspect (str, optional): banner|poster
			type (str, optional): season|
			season (int, optional):
			dim (str, optional): Dimensions "XxY"
			colors (list, optional): "|0,177,205|1,60,92|3,52,84|"
			preview (str, optional): The additional path to the preview image to append to the URL. For example `"_cache/fanart/original/72306-4.jpg"`.

		"""
		super().__init__('thumb', default=thumbnail, required=required)
		self.update({k.strip('_'): v for k, v in attributes.items() if v is not None})
