
from nfo.nodes import Node, Nodes, String, thumbs


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

	def __init__(self, name=None, role=None, thumb=None):
		super().__init__('actor')
		self.name = String('name', name)
		self.role = String('role', role)
		self.thumb = thumbs.Thumb(thumb)

	@property
	def children(self):
		"""Overrides Node.children attribute."""
		return (self.name, self.role, self.thumb)
