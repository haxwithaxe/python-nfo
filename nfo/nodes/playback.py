
from nfo.nodes import Node, Float


class Resume(Node):
	""" Model of a `resume` element.

	Arguments:
		position (int, optional): Position in the video to resume at.
		total (int, optional): ???

	"""

	def __init__(self, position=None, total=None):
		super().__init__('resume')
		self.position = Float('position', position)
		self.total = Float('total', total)

	@property
	def children(self):
		return (self.position, self.total)
