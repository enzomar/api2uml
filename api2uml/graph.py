class Graph(object):
		def __init__(self):
			self.nodes = dict()
			self.links = set()
			self.name = str()

		def add_node(self, node):
			self.nodes[node.name] = node

