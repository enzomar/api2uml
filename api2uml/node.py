class Attribute(object):
	def __init__(self):
		self.name = str()
		self.pk = False
		self.type = str()

	def __str__(self):
		return self.name

class Node(object):
	def __init__(self):
		self.name = str()
		self.attrs = []
		self.raw = str()

	def __str__(self):
		return self.name

