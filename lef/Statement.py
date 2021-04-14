'''
Created on Apr 18, 2017

@author: quannguyen
'''
from svi.common import Enum
from svi.common.Utils import compare_metal
from svi.models.lef.LayerDef import LayerDef


class LefStatement:
	"""
	General class for all types of Statements in the LEF file
	"""

	def __init__(self):
		pass

	def parse_next(self, data):
		"""
		Method to add information from a statement from LEF file to the
		LefStatement object.
		:param data: a list of strings that contains pieces of information
		:return: 1 if parsing is done, -1 if error, otherwise, return the
		object that will be parsed next.
		"""
		# the program assumes the syntax of LEF file is correct
		if data[0] == Enum.LEF_KEYS.LEF_MACRO_KEY and len(data) == 2:
			name = data[1]
			new_state = Macro(name)
			return new_state
		elif data[0] == Enum.LEF_KEYS.LEF_LAYER_KEY:  # and len(data) == 2: # does not have ;
			name = data[1]
			new_state = Layer(name) 
			return new_state
		elif data[0] == Enum.LEF_KEYS.LEF_VIA_KEY:
			name = data[1]
			new_state = Via(name)
			return new_state
		elif data[0] == Enum.LEF_KEYS.LEF_END_KEY:
			return 1
		return 0

	def __str__(self):
		"""
		turn a statement object into string
		:return: string representation of VerilogStatement objects
		"""
		s = ""
		# s += self.type + " " + self.name
		
		return s


class Macro(LefStatement):
	"""
	Macro class represents a MACRO (cell) in the LEF file.
	"""

	def __init__(self, name):
		# initiate the VerilogStatement superclass
		LefStatement.__init__(self)
		self.type = Enum.LEF_KEYS.LEF_MACRO_KEY
		self.name = name
		# other info is stored in this dictionary
		self.info = {}
		# pin dictionary
		self.pin_dict = {}
		self.pins = []

	def __str__(self):
		"""
		turn a statement object into string
		:return: string representation of VerilogStatement objects
		"""
		s = ""
		s += self.type + " " + self.name + "\n"
		for key in self.info:
			if key == Enum.LEF_KEYS.LEF_PIN_KEY:
				s += "	" + key + ":\n"
				for pin in self.info[key]:
					s += "	" + str(pin) + "\n"
			else:
				s += "	" + key + ": " + str(self.info[key]) + "\n"
		return s

	def parse_next(self, data):
		"""
		Method to add information from a statement from LEF file to a Macro
		object.
		:param data: a list of strings that contains pieces of information
		:return: 0 if in progress, 1 if parsing is done, -1 if error,
		otherwise, return the object that will be parsed next.
		"""
		if data[0] == Enum.LEF_KEYS.LEF_CLASS_KEY:
			self.info[Enum.LEF_KEYS.LEF_CLASS_KEY] = data[1]
		elif data[0] == Enum.LEF_KEYS.LEF_ORIGIN_KEY:
			x_cor = float(data[1])
			y_cor = float(data[2])
			self.info[Enum.LEF_KEYS.LEF_ORIGIN_KEY] = (x_cor, y_cor)
		elif data[0] == Enum.LEF_KEYS.LEF_FOREIGN_KEY:
			self.info[Enum.LEF_KEYS.LEF_FOREIGN_KEY] = data[1:]
		elif data[0] == Enum.LEF_KEYS.LEF_SIZE_KEY:
			width = float(data[1])
			height = float(data[3])
			self.info[Enum.LEF_KEYS.LEF_SIZE_KEY] = (width, height)
		elif data[0] == Enum.LEF_KEYS.LEF_SYMMETRY_KEY:
			self.info[Enum.LEF_KEYS.LEF_SYMMETRY_KEY] = data[1:]
		elif data[0] == Enum.LEF_KEYS.LEF_SITE_KEY:
			self.info[Enum.LEF_KEYS.LEF_SITE_KEY] = data[1]
		elif data[0] == Enum.LEF_KEYS.LEF_PIN_KEY:
			new_pin = Pin(data[1])
			self.pin_dict[data[1]] = new_pin
			self.pins.append(data[1])
			if Enum.LEF_KEYS.LEF_PIN_KEY in self.info:
				self.info[Enum.LEF_KEYS.LEF_PIN_KEY].append(new_pin)
			else:
				self.info[Enum.LEF_KEYS.LEF_PIN_KEY] = [new_pin]
			return new_pin
		elif data[0] == Enum.LEF_KEYS.LEF_OBS_KEY:
			new_obs = Obs()
			self.info[Enum.LEF_KEYS.LEF_OBS_KEY] = new_obs
			return new_obs
		elif data[0] == Enum.LEF_KEYS.LEF_END_KEY:
			if data[1] == self.name:
				return 1
			else:
				return -1
		return 0

	def get_pin(self, pin_name):
		return self.pin_dict[pin_name]


class Pin(LefStatement):
	"""
	Class Pin represents a PIN statement in the LEF file.
	"""

	def __init__(self, name):
		LefStatement.__init__(self)
		self.type = Enum.LEF_KEYS.LEF_PIN_KEY
		self.name = name
		self.info = {}

	def __str__(self):
		s = self.name
		# for layer in self.info["PORT"].info["LAYER"]:
		# 	s += layer.type + " " + layer.name + "\n"
		return s

	def parse_next(self, data):
		if data[0] == Enum.LEF_KEYS.LEF_DIRECTION_KEY:
			self.info[Enum.LEF_KEYS.LEF_DIRECTION_KEY] = data[1]
		elif data[0] == Enum.LEF_KEYS.LEF_USE_KEY:
			self.info[Enum.LEF_KEYS.LEF_USE_KEY] = data[1]
		elif data[0] == Enum.LEF_KEYS.LEF_PORT_KEY:
			new_port = Port()
			if Enum.LEF_KEYS.LEF_PORT_KEY in self.info:
				self.info[Enum.LEF_KEYS.LEF_PORT_KEY].append(new_port)
			else:
				self.info[Enum.LEF_KEYS.LEF_PORT_KEY] = [new_port]
			return new_port
		elif data[0] == Enum.LEF_KEYS.LEF_SHAPE_KEY:
			self.info[Enum.LEF_KEYS.LEF_SHAPE_KEY] = data[1]
		elif data[0] == Enum.LEF_KEYS.LEF_END_KEY:
			if data[1] == self.name:
				return 1
			else:
				return -1
		# return 0 when we parse a undefined statement
		return 0

	def is_lower_metal(self, split_layer):
		return self.info[Enum.LEF_KEYS.LEF_PORT_KEY].is_lower_metal(split_layer)

	def get_top_metal(self):
		return self.info[Enum.LEF_KEYS.LEF_PORT_KEY].get_top_metal()


class Port(LefStatement):
	"""
	Class Port represents an PORT statement in the LEF file.
	"""

	# Note: PORT statement does not have name
	def __init__(self):
		LefStatement.__init__(self)
		self.type = Enum.LEF_KEYS.LEF_PORT_KEY
		self.name = ""
		self.info = {}

	def parse_next(self, data):
		if data[0] == Enum.LEF_KEYS.LEF_END_KEY:
			return 1
		elif data[0] == Enum.LEF_KEYS.LEF_LAYER_KEY:
			new_layerdef = LayerDef(data[1])
			if Enum.LEF_KEYS.LEF_LAYER_KEY in self.info:
				self.info[Enum.LEF_KEYS.LEF_LAYER_KEY].append(new_layerdef)
			else:
				self.info[Enum.LEF_KEYS.LEF_LAYER_KEY] = [new_layerdef]
		elif data[0] == Enum.LEF_KEYS.LEF_RECT_KEY:
			# error if the self.info["LAYER"] does not exist
			self.info[Enum.LEF_KEYS.LEF_LAYER_KEY][-1].add_rect(data)
		elif data[0] == Enum.LEF_KEYS.LEF_POLYGON_KEY:
			self.info[Enum.LEF_KEYS.LEF_LAYER_KEY][-1].add_polygon(data)
		return 0

	def is_lower_metal(self, split_layer):
		lower = True
		for layer in self.info[Enum.LEF_KEYS.LEF_LAYER_KEY]:
			if compare_metal(layer.name, split_layer) >= 0:
				lower = False
				break
		return lower

	def get_top_metal(self):
		highest = "poly"
		for layer in self.info[Enum.LEF_KEYS.LEF_LAYER_KEY]:
			if compare_metal(layer.name, highest) > 0:
				highest = layer.name
		return highest




class Obs(LefStatement):
	"""
	Class Obs represents an OBS statement in the LEF file.
	"""

	# Note: OBS statement does not have name
	def __init__(self):
		LefStatement.__init__(self)
		self.type = Enum.LEF_KEYS.LEF_OBS_KEY
		self.name = ""
		self.info = {}

	def __str__(self):
		s = "Obs: "
		if Enum.LEF_KEYS.LEF_LAYER_KEY in self.info:
			for layer in self.info[Enum.LEF_KEYS.LEF_LAYER_KEY]:
				s += layer.type + " " + layer.name + "\n"
		return s

	def parse_next(self, data):
		if data[0] == Enum.LEF_KEYS.LEF_END_KEY:
			return 1
		elif data[0] == Enum.LEF_KEYS.LEF_LAYER_KEY:
			new_layerdef = LayerDef(data[1])
			if Enum.LEF_KEYS.LEF_LAYER_KEY in self.info:
				self.info[Enum.LEF_KEYS.LEF_LAYER_KEY].append(new_layerdef)
			else:
				self.info[Enum.LEF_KEYS.LEF_LAYER_KEY] = [new_layerdef]
		elif data[0] == Enum.LEF_KEYS.LEF_RECT_KEY:
			# error if the self.info["LAYER"] does not exist
			self.info[Enum.LEF_KEYS.LEF_LAYER_KEY][-1].add_rect(data)  # [-1] means the latest layer
		elif data[0] == Enum.LEF_KEYS.LEF_POLYGON_KEY:
			self.info[Enum.LEF_KEYS.LEF_LAYER_KEY][-1].add_polygon(data)
		return 0


class Via(LefStatement):
	"""
	Via class represents a VIA section in LEF file.
	"""
	def __init__(self, name):
		# initiate the VerilogStatement superclass
		LefStatement.__init__(self)
		self.type = Enum.LEF_KEYS.LEF_VIA_KEY
		self.name = name
		self.layers = []

	def parse_next(self, data):
		if data[0] == Enum.LEF_KEYS.LEF_END_KEY:
			return 1
		elif data[0] == Enum.LEF_KEYS.LEF_LAYER_KEY:
			new_layerdef = LayerDef(data[1])
			self.layers.append(new_layerdef)
		elif data[0] == Enum.LEF_KEYS.LEF_RECT_KEY:
			self.layers[-1].add_rect(data)  # [-1] means the latest layer
		elif data[0] == Enum.LEF_KEYS.LEF_POLYGON_KEY:
			self.layers.add_polygon(data)
		return 0


class Layer(LefStatement):
	"""
	Layer class represents a LAYER section in LEF file.
	"""
	def __init__(self, name):
		# initiate the VerilogStatement superclass
		LefStatement.__init__(self)
		self.type = Enum.LEF_KEYS.LEF_LAYER_KEY
		self.name = name
		self.layer_type = None
		self.spacing_table = None
		self.spacing = None
		self.width = None
		self.pitch = None
		self.direction = None
		self.offset = None
		self.resistance = None
		self.thickness = None
		self.height = None
		self.capacitance = None
		self.edge_cap = None
		self.property = None

	def parse_next(self, data):
		"""
		Method to add information from a statement from LEF file to a Layer
		object.
		:param data: a list of strings that contains pieces of information
		:return: 0 if in progress, 1 if parsing is done, -1 if error,
		otherwise, return the object that will be parsed next.
		"""
		if data[0] == Enum.LEF_KEYS.LEF_TYPE_KEY:
			self.layer_type = data[1]
		elif data[0] == Enum.LEF_KEYS.LEF_SPACINGTABLE_KEY:
			pass
		elif data[0] == Enum.LEF_KEYS.LEF_SPACING_KEY:
			self.spacing = float(data[1])
		elif data[0] == Enum.LEF_KEYS.LEF_WIDTH_KEY:
			self.width = float(data[1])
		elif data[0] == Enum.LEF_KEYS.LEF_PITCH_KEY:
			self.pitch = float(data[1])
		elif data[0] == Enum.LEF_KEYS.LEF_DIRECTION_KEY:
			self.direction = data[1]
		elif data[0] == Enum.LEF_KEYS.LEF_OFFSET_KEY:
			self.offset = (float(data[1]), float(data[2]))
		elif data[0] == Enum.LEF_KEYS.LEF_RESISTANCE_KEY:
			if self.layer_type == Enum.LEF_KEYS.LEF_ROUTING_KEY:
				self.resistance = (data[1], float(data[2]))
			elif self.layer_type == Enum.LEF_KEYS.LEF_CUT_KEY:
				self.resistance = float(data[1])
		elif data[0] == Enum.LEF_KEYS.LEF_THICKNESS_KEY:
			self.thickness = float(data[1])
		elif data[0] == Enum.LEF_KEYS.LEF_HEIGHT_KEY:
			self.height = float(data[1])
		elif data[0] == Enum.LEF_KEYS.LEF_CAPACITANCE_KEY:
			self.capacitance = (data[1], float(data[2]))
		elif data[0] == Enum.LEF_KEYS.LEF_EDGECAPACITANCE_KEY:
			self.edge_cap = float(data[1])
		elif data[0] == Enum.LEF_KEYS.LEF_PROPERTY_KEY:
			self.property = (data[1], float(data[2]))
		elif data[0] == Enum.LEF_KEYS.LEF_END_KEY:
			if data[1] == self.name:
				return 1
			else:
				return -1
		return 0
