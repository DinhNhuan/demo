'''
Created on Apr 18, 2017

@author: quannguyen
'''
import sys

from svi.models.lef.Polygon import Polygon
from svi.models.lef.Rect import Rect


class LayerDef:
	"""
	Class LayerDef represents the Layer definition inside a PORT or OBS
	statement.
	"""

	# NOTE: LayerDef has no END statement
	# I think I still need a LayerDef class, but it will not be a subclass of
	#  Statement. It will be a normal object that stores information.
	def __init__(self, name):
		self.type = "LayerDef"
		self.name = name
		self.shapes = []

	def add_rect(self, data):
		
		data = filter(None, data)
		if len(data) < 5:
			print "[ERR] Data %s is not a valid rect" %(data)
			sys.exit()
		#print data
		try:
			x0 = float(data[-4])
			y0 = float(data[-3])
			x1 = float(data[-2])
			y1 = float(data[-1])
		except:
			print "[ERR] Data %s is not a valid rect" %(data)
			sys.exit()
		
		points = [(x0, y0), (x1, y1)]
		#print points
		rect = Rect(points, data)
		self.shapes.append(rect)
	
	def __str__(self):
		"""
		turn a statement object into string
		:return: string representation of VerilogStatement objects
		"""
		s = "%s" %(self.name)
		# s += self.type + " " + self.name
		return s
	
	def add_polygon(self, data):
		points = []
		data = filter(None, data)
		# add each pair of (x, y) points to a list
		for idx in range(1, len(data), 2):
			try:
				x_cor = float(data[len(data) - idx - 1])
				y_cor = float(data[len(data) - idx])
			except:
				break
			points.append([x_cor, y_cor])
		points = points[::-1]
		polygon = Polygon(points, data)
		self.shapes.append(polygon)
		