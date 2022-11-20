import pickle
import codecs

class Graph(object):
		def __init__(self):
			self.nodes = dict()
			self.links = set()
			self.name = str()

		def add_node(self, node):
			self.nodes[node.name] = node

		def serialize(self) -> str:
			return codecs.encode(pickle.dumps(self), "base64").decode()

		def display(self):
			print(self.name)
			for each in self.nodes:
				print("{0}: {1}", each, self.nodes[each])
			for each in self.links:
				print("{0}".format(each))


		

def deserialize(buffer: str) -> Graph:
	return pickle.loads(codecs.decode(buffer.encode(), "base64"))
