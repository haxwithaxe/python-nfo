
from lxml.builder import E

from nfo.nodes import Node, Float, String, Singleton
from nfo.nodes import Nodes


class FileInfo(Node):
	"""Model of a `fileinfo` element.

	Keyword Arguments:
		video (str, optional): Video filename or URL. See the notes below on using this element.

	From the (http://kodi.wiki/view/NFO_files/tvepisodes)[Kodi wiki] in
	reference to `fileinfo/streamdetails`:
		While it is possible to manually set the information contained within
		the "streamdetails" tag,there is little point in doing so, as the
		software will always overwrite this data when it plays back the video
		file. In other words, no matter how many times you try to manually set
		it, it will be undone the moment the video is played.

	"""

	def __init__(self, **details):
		super().__init__('fileinfo')
		self.video = None
		self.set(details)


	def set(self, details):
		self.video = details.get('video', self.video)

	@property
	def children(self):
		if self.video:
			return [E.streamdetails(E.video(self.video))]
		return [E.streamdetails(E.video())]
