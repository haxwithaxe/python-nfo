"""Models for `actor` elements and lists of `actor` elements."""

from nfo.nodes import Int, Node, Nodes, String, thumbs


class Actors(Nodes):
	"""A list of Actor instances.

	Arguments:
		actor_specs (list, optional): A list of dict instances.

	"""

	def __init__(self, actor_specs=[]):
		super().__init__(Actor, actor_specs)


class Actor(Node):
	"""Model of an `actor` element.

	Arguments:
		name (str, optional): The actor's name.
		role (str, optional): The role played by the actor.
		thumb (str, optional): The filename or URL of the actor's photo.
		order (int, optional): The display order of this actor's entry.

	Attributes:
		name (str): The actor's name.
		role (str): The role played by the actor.
		thumb (thumbs.Thumb): A `thumbs.Thumb` for the actor's photo.
		order (int): The display order of this actor's entry.

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
		return (
				String('name', self.name),
				String('role', self.role),
				self.thumb,
				Int('order', self.order))

	def __lt__(self, other):
		return self.order and other.order and self.order < other.order
