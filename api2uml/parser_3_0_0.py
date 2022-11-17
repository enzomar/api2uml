from node import Node
from node import Attribute
from link import Link
from link import LinkType
from graph import Graph


def _extract_plain_attrs(item, attrs):
  try:
    required = item['required']
  except Exception as ex:
    required = []

  try:
    props = item['properties']

    for each in props:
      attr = Attribute()
      attr.name = each
      attr.type = props[each].get('type', '')  
      attr.pk = each in required 
      attrs.append(attr)
  except:
    pass

  return attrs


def _findkeys(node, kv, path=None):
    if not path:
      path = []
    if isinstance(node, list):
        for i in node:
          for p,x in _findkeys(i, kv, path):
             yield p,x
    elif isinstance(node, dict):
        if kv in node:
            yield path, node[kv]
        for k, j in node.items():
            local_path = path[:]
            local_path.append(k)
            for p,x in _findkeys(j, kv, local_path):
                yield p,x

def _map_link_type(parent):
  if parent == "items":
    return LinkType.AGG

  if parent == "allOf":
    return LinkType.COMP

  return LinkType.ASSO

def _extract_links(name, item):
  """
    self.desc = str()
    self.origin = None
    self.dest = None
    self.type = None #LinkType
  """
  links = []
  for path, ref in _findkeys(item,'$ref', list()):
    link = Link()
    link.origin = name
    link.dest = ref.replace('#/components/schemas/','')
    parent = path[-1]
    link.type = _map_link_type(parent)
    links.append(link)
  return links


def _extract_attrs(item):
  attrs = list()
  try:
    attrs += _extract_plain_attrs(item, attrs)
  except Exception as ex:
    print(str(ex))

  return attrs


def _extract_items(yaml_buffer):
  graph = Graph()
  defs = yaml_buffer['components']['schemas']

  for each in defs:
    node = Node()
    node.name = each
    item = defs[each]
    node.attrs = _extract_attrs(item)
    node.raw = item
    graph.nodes.append(node) 
    graph.links += _extract_links(each, item)
  return graph


def parse(yaml_buffer):
  graph = _extract_items(yaml_buffer)
  return graph


