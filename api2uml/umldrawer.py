from io import StringIO
import os

class UMLDrawer(object):


	def write(self, buffer, output):
		output.write(buffer+os.linesep)

	def draw_attr(self, attr, output):
		if attr.pk:
			self.write("{0} {1}".format("{static}", attr.name), output)
		else:
			self.write("{0}".format(attr.name), output)

	def draw_node(self, node, output):
		self.write("class {0} {{".format(node.name), output)
		if node.attrs:
			for attrs in node.attrs:
				self.draw_attr(attrs, output)
		self.write("}", output)

	def draw_link(self, link, output):

		if link.type == 1:
			linktype = "--"
		elif link.type == 2:
			linktype = "o--"
		elif link.type == 3:
			linktype = "*--"

		if link.desc:
			self.write("{0} {1} {2}: {3}".format(link.origin, 
				linktype, link.dest, desc), output)
		else:
			self.write("{0} {1} {2}".format(link.origin, 
				linktype, link.dest), output)


	def to_plantuml(self, graph):
		output = StringIO()
		self.write("@startuml", output)

		for node in graph.nodes:
			self.draw_node(graph.nodes[node], output)
		for link in graph.links:
			self.draw_link(link, output)

		self.write("@enduml", output)

		return output.getvalue()
