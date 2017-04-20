
from datetime import datetime

from lxml.builder import E
from lxml.etree import _Element, tostring  # pylint: disable=no-name-in-module


def _unpack_child(child):
	if isinstance(child, Node):
		return child.__xml__()
	elif isinstance(child, _Element):
		return child
	return str(child)

def _unpack_children(children):
	unpacked = []
	for child in children:
		if not child:
			continue
		if isinstance(child, Nodes):
			for c in child:
				unpacked.append(_unpack_child(c))
		else:
			unpacked.append(_unpack_child(child))
	return unpacked


class Node:
	"""Base model for an XML node.

	Attributes:
		children:


	Arguments:
		element_name (str): The element name (aka "tag" name).
		required (bool, optional): If this is true the element will present as
		truethy even if it is empty.

	"""

	override_with_type = False

	def __init__(self, element_name, required=False):
		self.element_name = element_name
		self._required = required
		self._children = []
		self.attributes = {}

	def set(self, *values):
		"""Set the value of `children`.

		Arguments:
			*values (tuple, optional): A tuple of child nodes (str or XML/Node).

		Returns:
			Node: The Node instance being called.

		"""
		self._children = values
		return self

	@property
	def children(self):
		return self._children

	@children.setter
	def children(self, children):
		self._children = children

	def append(self, child):
		"""Append a child node to the list of children."""
		self._children.append(child)

	def update(self, attributes):
		self.attributes.update(attributes)

	def __bool__(self):
		if self._required:
			return True
		else:
			return bool(self.children or self.attributes)

	def __lt__(self, other):
		return False

	def __xml__(self):
		"""Returns the Node instance as an etree.Element."""
		return E.__getattr__(self.element_name)(
				*_unpack_children(self.children),
				**self.attributes
				)

	def __str__(self):
		return tostring(self.__xml__(), pretty_print=True).decode()

	def __repr__(self):
		values = {
			'name': self.__class__.__name__, 
			'element_name': self.element_name,
			'required': self._required, 
			'children': len(self.children),
			'attributes': self.attributes
			}
		return '''<{name} element_name = {element_name}, required = {required}, number of children = {children}, attributes = {attributes}>'''.format(**values)  # pylint: disable=line-too-long

	def debug(self, *args, **kwargs):
		print(self.__class__.__name__, 'DEBUG', *args, **kwargs)

	def __iter__(self):
		return iter((('element_name', self.element_name),
			('children', [repr(x) for x in self.children]),
			('attributes', self.attributes)))


class ValidRangeMixin:

	valid_range = None

	def set(self, value):
		if (self.valid_range and
				len(self.valid_range) == 2 and
				(value < self.valid_range[0] or value > self.valid_range[1])
				):
			raise ValueError()
		return super().set(value)


class Singleton(Node):

	default = None
	caster = None

	def __init__(self, element_name, default=None, required=False):
		super().__init__(element_name, required=required)
		self._value = default if default is not None else self.default

	def set(self, value):
		self._value = value
		return self

	def __bool__(self):
		return self._value is not None

	def __eq__(self, other):
		if isinstance(other, Node):
			return other is self
		return self._value == other

	@property
	def children(self):
		if self._value is not None:
			return [self.caster(self._value)]  # pylint: disable=not-callable
		return []

	def __repr__(self):
		values = {
			'name': self.__class__.__name__, 
			'element_name': self.element_name,
			'required': self._required, 
			'value': self._value,
			'attributes': self.attributes
			}
		return '''<{name} element_name = {element_name}, value = {value}, required = {required}, attributes = {attributes}>'''.format(**values)  # pylint: disable=line-too-long


class Int(Singleton, ValidRangeMixin):

	caster = int

	def __init__(self, element_name, valid_range=None, **kwargs):
		super().__init__(element_name, **kwargs)
		self.override_with_type = Int
		self._valid_range = valid_range


class String(Singleton):

	caster = str

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.override_with_type = String


class Float(Singleton, ValidRangeMixin):

	caster = float

	def __init__(self, element_name, valid_range=None, **kwargs):
		super().__init__(element_name, **kwargs)
		self.override_with_type = Float
		self._valid_range = valid_range


class Date(Singleton):

	default = datetime(year=1969, month=12, day=31, hour=0, minute=0)

	def __init__(self, element_name, format_string='%Y-%m-%d', default=None, required=False):
		self.__value = None
		self.format_string = format_string
		super().__init__(element_name, default, required=required)

	def caster(self, value):
		if not value:
			return None
		return value.strftime(self.format_string)

	@property
	def date(self):
		return self.__value

	@date.setter
	def date(self, value):
		self._value = value

	@property
	def _value(self):
		return self.__value

	@_value.setter
	def _value(self, value):
		if not value:
			self.__value = None
		elif isinstance(value, datetime):
			self.__value = value
		else:
			self.__value = datetime.strptime(str(value), self.format_string)

	def __bool__(self):
		if self.date is not self.default and self.date is not None:
			return True
		return super().__bool__()


class URL(String):

	def __init__(self, element_name, url, required=False, **attributes):
		super().__init__(element_name, default=url, required=required)
		self.update(attributes)

	@property
	def cache(self):
		return self.attributes.get('cache')

	@cache.setter
	def cache(self, value):
		self.attributes['cache'] = value


class Nodes:
	"""
	Arguments:
		node_class (class): The class to use to create the child nodes.
		*specs (tuple): A tuple of dict instances where the dict instances are the kwargs for `class`.

	"""

	override_with_type = False

	def __init__(self, node_class, node_specs=None, required=False):
		if not isinstance(node_class, type):
			raise TypeError()
		self._node_class = node_class
		self._nodes = []
		self._required = required
		self.set(node_specs or [])

	def set(self, node_specs):
		"""Create the nodes from `node_specs`.

		Replaces the existing nodes with the ones created from `node_specs`.

		Arguments:
			*node_specs (tuple): A tuple of dict instances where the dict instances are
			the kwargs for `class`.

		Returns:
			Node: The Node instance being called.

		"""
		#self.debug('.set _nodes', self._nodes)
		#self.debug('.set node_specs', node_specs)
		self._nodes = []
		self.extend(node_specs)
		#self.debug('.set after reset and extend _nodes', self._nodes)
		return self

	def extend(self, node_specs):
		#self.debug('.extend node_specs', node_specs)
		for spec in node_specs:
			if spec:
				self.append(spec)

	def append(self, n_spec):
		#self.debug('.append node_spec', node_spec)
		if n_spec and isinstance(n_spec, dict):
			self._nodes.append(self._node_class(**n_spec))
		elif n_spec and isinstance(n_spec, Node):
			self._nodes.append(n_spec)
		else:
			pass
			#self.debug('WRONG node_spec type!', node_spec)

	def sort(self, **kwargs):
		self._nodes.sort(**kwargs)

	def __iter__(self):
		return iter(self._nodes)

	def __bool__(self):
		if self._required:
			return True
		else:
			return bool([x for x in self._nodes if x])

	def debug(self, *args, **kwargs):
		print(self.__class__.__name__, 'DEBUG', *args, **kwargs)

	def __repr__(self):
		values = {
			'name': self.__class__.__name__, 
			'node_class': self._node_class.__name__,
			'required': self._required, 
			'nodes': len(self._nodes),
			}
		return '''<{name} node_class = {node_class}, required = {required}, number of children = {nodes}>'''.format(**values)  # pylint: disable=line-too-long
