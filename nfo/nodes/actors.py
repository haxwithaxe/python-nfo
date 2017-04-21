
from nfo.nodes import Int, Node, Nodes, String, thumbs


class Actors(Nodes):

	def __init__(self, actors=[]):
		super().__init__(Actor, actors)


class Actor(Node):
	"""Model of an `actor` element.

	Keyword Arguments:
		name (str): The actor's name.
		role (str): The role played by the actor.
		thumb (str): The filename or URL of the actor's photo.

	"""

	def __init__(self, name=None, role=None, thumb=None, order=None):
		super().__init__('actor')
		self.name = name
		self.role = role
		self.thumb = thumbs.Thumb(thumb)
		self.order = order

	@property
	def children(self):
		"""Overrides Node.children attribute."""
		return (String('name', self.name), String('role', self.role), self.thumb, Int('order', self.order))

	def __lt__(self, other):
		return self.order and other.order and self.order < other.order
