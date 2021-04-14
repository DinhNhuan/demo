'''
Created on Apr 18, 2017

@author: quannguyen
'''
from svi.common.Utils import is_int


class Rect:
	"""
    Class Rect represents a Rect definition in a LayerDef
    """

	# Question: Do I really need a Rect class?
	def __init__(self, points, data):
		self.type = "RECT"


		x1 = points[0][0]
		y1 = points[0][1]
		x2 = points[1][0]
		y2 = points[1][1]

		if is_int(x1):
			x1 = int(x1)

		if is_int(x2):
			x2 = int(x2)

		if is_int(y1):
			y1 = int(y1)

		if is_int(y2):
			y2 = int(y2)


		self.xBottom = x1
		self.yBottom = y1
		self.xTop = x2
		self.yTop = y2

		points = [[x1, y1], [x2, y2]]
		self.points = points
		self.data = data

	def __str__(self):
		"""
		turn a statement object into string
		:return: string representation of VerilogStatement objects
		"""
		s = "%s" % (self.points)
		# s += self.type + " " + self.name
		return s
