from model.node import Node
from model.node import Attribute
from model.link import Link
from model.link import LinkType
from model.graph import Graph
import re

FUNC_MATCH =re.compile(r'\w+Ids{0,1}')
FUNC_SUB =re.compile(r'Ids{0,1}')


def _extract_enum_attrs(item, attrs):
  try:
    enum = item['enum']
    for each in enum:
      attr = Attribute()
      attr.name = "> "+each
      attrs.append(attr)
  except:
    pass

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
      if 'type' in props[each]:
        attr.type = props[each]['type'] 

      attr.pk = each in required 
      attrs.append(attr)
      _extract_enum_attrs(props[each], attrs)

  except Exception as ex:
    #print("{0}: {1}".format(item, ex))
    pass

def _extract_allOf_attrs(item, attrs):
  for each in item:
    if each != 'allOf':
      _extract_plain_attrs(item[each], attrs)
    else:
      for each_allof in item['allOf']:
        if '$ref' not in each_allof:
          _extract_plain_attrs(each_allof, attrs)


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

def _map_link_type(parent=None):
  if parent == "items":
    return LinkType.AGG

  if parent == "allOf":
    return LinkType.COMP

  return LinkType.ASSO


def _functional_links(name, item):
  links = set()
  try:
    props = item['properties']

    for each in props:
      if re.match(FUNC_MATCH, each):
        link = Link()
        link.origin = name
        
        dest = re.sub(FUNC_SUB, '', each)
        dest = dest[0].upper() + dest[1:]
        #print("{0}: {1} --> {2}".format(name, each, dest))

        link.dest = dest
        link.type = _map_link_type()
        links.add(link)
  except:
    pass

  return links

def _extract_links(name, item):
  """
    self.desc = str()
    self.origin = None
    self.dest = None
    self.type = None #LinkType
  """
  links = set()
  for path, ref in _findkeys(item,'$ref', list()):
    link = Link()
    link.origin = name
    link.dest = ref.replace('#/definitions/','')
    parent = path[-1]
    link.type = _map_link_type(parent)
    links.add(link)

  links = links.union(_functional_links(name, item))

  return links


def _extract_attrs(item):
  attrs = list()
  try:
    _extract_plain_attrs(item, attrs)
  except Exception as ex:
    print(str(ex))

  try:
    _extract_enum_attrs(item, attrs)
  except Exception as ex:
    print(str(ex))

  try:
    _extract_allOf_attrs(item, attrs)
  except Exception as ex:
    print(str(ex))


  return attrs


def _extract_items(yaml_buffer):
  graph = Graph()
  defs = yaml_buffer['definitions']

  for each in defs:
    node = Node()
    node.name = each
    item = defs[each]
    node.attrs = _extract_attrs(item)
    node.raw = item
    graph.add_node(node) 
    graph.links.update(_extract_links(each, item))
  return graph


def parse(yaml_buffer):
  graph = _extract_items(yaml_buffer)
  return graph


