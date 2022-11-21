from io import StringIO
import os
import sys

class UMLDrawer(object):


  def _write(self, buffer, output):
    output.write(buffer+os.linesep)

  def _draw_attr(self, attr, output):
    if attr.pk:
      self._write("{0} {1}".format("{static}", attr.name), output)
    else:
      self._write("{0}".format(attr.name), output)

  def _draw_node(self, node, output):
    self._write("class {0} {{".format(node.name), output)
    if node.attrs:
      for attrs in node.attrs:
        self._draw_attr(attrs, output)
    self._write("}", output)

  def _draw_link(self, link, output):

    if link.type == 1:
      linktype = "-->"
    elif link.type == 2:
      linktype = "o--"
    elif link.type == 3:
      linktype = "*--"

    if link.desc:
      self._write("{0} {1} {2}: {3}".format(link.origin, 
        linktype, link.dest, desc), output)
    else:
      self._write("{0} {1} {2}".format(link.origin, 
        linktype, link.dest), output)


  def _link_mapper(self, graph):

    linkmap = {}
    for link in graph.links:  
      
      if link.origin not in linkmap:
        linkmap[link.origin] = set()
      linkmap[link.origin].add(link)

    return linkmap


  def _draw_all(self, graph):
    output = StringIO()
    self._write("@startuml", output)

    for node in graph.nodes:
      self._draw_node(graph.nodes[node], output)
    for link in graph.links:
      self._draw_link(link, output)

    self._write("@enduml", output)

    return output.getvalue()


  def _traverse_and_draw(self, node_name, linkmap, graph, output, already_drawn=[]):
    if node_name in already_drawn:
      return
    already_drawn.append(node_name)
    if node_name in graph.nodes:
      self._draw_node(graph.nodes[node_name], output)

    if node_name in linkmap:
      links = linkmap[node_name]
      for link in links:
        next_node_name = link.dest
        self._draw_link(link, output)
        self._traverse_and_draw(next_node_name, linkmap, graph, output, already_drawn)


  def _draw_from_node(self, graph, node_name):
    output = StringIO()
    linkmap = self._link_mapper(graph)
  
    self._write("@startuml", output)
    print(node_name)
    self._traverse_and_draw(node_name, linkmap, graph, output, [])
    self._write("@enduml", output)

    return output.getvalue()


  def to_plantuml(self, graph, node_name):
    if  node_name:
      return self._draw_from_node(graph, node_name)
    else:
      return self._draw_all(graph) 
