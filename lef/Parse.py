'''
Created on Apr 18, 2017

@author: quannguyen
'''
import collections
import time

from svi.common import Enum
from svi.common.Utils import str_to_list, sortByString
from svi.models.lef.LefStatement import LefStatement, Macro, Layer, Via


class LefParser:
	"""
	LefParser object will parse the LEF file and store information about the
	cell library.
	"""
	def __init__(self, lef_file):
		self.lef_path = lef_file # duong dan chua file
		# dictionaries to map the definitions
		self.cell_dict = []
		self.cell_dict2 = {}
		self.layer_dict = {}
		self.via_dict = {}
		# can make the stack to be an object if needed
		self.stack = []
		# store the statements info in a list
		self.statements = []
		self.cell_height = -1

	def get_cell_height(self):
		"""
		Get the general cell height in the library
		:return: void
		"""
		for macro in self.cell_dict:
			self.cell_height = macro.info[Enum.LEF_KEYS.LEF_SIZE_KEY][1]

			break

	def parse(self):

		# Now try using my data structure to parse
		# open the file and start reading
		time1 = time.time()
		numLines = sum(1 for line in open(self.lef_path))

		print "Start parsing LEF file " + self.lef_path + " - %s lines" % (numLines)
		f = open(self.lef_path, "r")

		countLine = 0


		# the program will run until the end of file f
		for line in f:
			countLine += 1
			if countLine % 100000 == 0:
				print "Processing %s/%s lines" % (countLine, numLines)
			info = str_to_list(line)
# 			print "-----------------"
# 			print line
			if len(info) != 0:
				# if info is a blank line, then move to next line
				# check if the program is processing a statement
				# print (info)
				# print self.stack
				if len(self.stack) != 0:
					curState = self.stack[len(self.stack) - 1]
					nextState = curState.parse_next(info)
				else:
					curState = LefStatement()
					nextState = curState.parse_next(info)
				# print curState
				# print nextState
				# check the status return from parse_next function
				if nextState == 0:
					# continue as normal
					pass
				elif nextState == 1:
					# remove the done statement from stack, and add it to the statements
					# list
					if len(self.stack) != 0:
						# add the done statement to a dictionary
						done_obj = self.stack.pop()
						# print done_obj
						if isinstance(done_obj, Macro):
							self.cell_dict.append(done_obj)
							self.cell_dict2[done_obj.name] = done_obj
						elif isinstance(done_obj, Layer):
							self.layer_dict[done_obj.name] = done_obj
						elif isinstance(done_obj, Via):
							self.via_dict[done_obj.name] = done_obj
						self.statements.append(done_obj)
				elif nextState == -1:
					pass
				else:
					self.stack.append(nextState)
					# print nextState
		f.close()
		# get the cell height of the library
		self.get_cell_height()

		time3 = time.time()
		print "Sorting statements: %s obj" % (len(self.statements))
		self.statements = sorted(self.statements, cmp = lambda x, y: sortByString(x, y))
		print "Sorting cell dict: %s obj" % (len(self.cell_dict))
		self.cell_dict = sorted(self.cell_dict, cmp = lambda x, y: sortByString(x, y))

		time4 = time.time()
		diff = int(time4 - time3)
		minutes, seconds = diff // 60, diff % 60
		print "Time sorting: " + str(minutes) + ':' + str(seconds).zfill(2)

		time2 = time.time()
		diff = int(time2 - time1)
		minutes, seconds = diff // 60, diff % 60
		print "Parsing LEF file done: " + str(minutes) + ':' + str(seconds).zfill(2)

