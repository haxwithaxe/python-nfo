"""Models of elements that describe actors."""

from nfo.nodes import Int, Node, Nodes, String, thumbs


class Actors(Nodes):
	"""A list of Actor instances.

	Arguments:
		actor_specs (list, optional): A list of `Actor` constructor dict instances.

	"""

	def __init__(self, actor_specs=[]):
		super().__init__(Actor, actor_specs)


class Actor(Node):
	"""Model of an `actor` element.

	Arguments:
		name (str, optional): The actor's name. Defaults to None.
		role (str, optional): The role played by the actor. Defaults to None.
		thumb (str, optional): The filename or URL of the actor's photo. Defaults to None.
		order (int, optional): The display order of this actor's entry. Defaults to None.

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
		"""Overrides Node.children attribute.
		
		Returns:
			tuple: A tuple with the Node instances for the name, role, thumb, and order.

		"""
		return (
				String('name', self.name),
				String('role', self.role),
				self.thumb,
				Int('order', self.order)
				)

	def __lt__(self, other):
		"""Used for ordering Actor elements."""
		return self.order and other.order and self.order < other.order
