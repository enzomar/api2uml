from graph import Graph
from collections import OrderedDict


def _mapper(graph):

  linkmap = {}
  origins = set()
  destinations = set()

  for link in graph.links:
  
    origins.add(link.origin)
    destinations.add(link.dest)
  
    if link.origin not in linkmap:
      linkmap[link.origin] = set()
    linkmap[link.origin].add(link)

  return linkmap, origins.difference(destinations)


def _find_roots(graph):
  
  origins = set()
  destinations = set()

  for link in graph.links:
    origins.add(link.origin)
    destinations.add(link.dest)

  return origins.intersection(destinations)


def _traverse(origin, linkmap, path=[]):
  if origin in linkmap:
    destinations = linkmap[origin]
    for each in destinations:
      dest = each.dest
      path.append(dest)
      _traverse(dest, linkmap, path)
  return path


def _build(graph, linkmap, path):
  sub_graph = Graph()

  if path:
    sub_graph.name = path[0]
    for each in path:
      sub_graph.add_node(graph.nodes[each])
      if each in linkmap:
        sub_graph.links.update(linkmap[each])

  return sub_graph


def is_sub_array(A, B, n, m):  
  i = 0 
  j = 0
  while (i < n and j < m):
    if (A[i] == B[j]):
        i += 1;
        j += 1;
        if (j == m):
            return True
    else:
        i = i - j + 1
        j = 0
  return False

def _reduce(arrays):
  lenghts = {}
  for each in arrays:
    n = len(each)
    if n not in lenghts:
      lenghts[n] = []
    lenghts[n].append(each)
  
  ord_array = OrderedDict(sorted(lenghts.items()))

  paths = []

  for each in ord_array:
    for sub in each:
      paths.append(sub)

  reduced_paths = []
  for idx in range(0,len(paths)):
    A = paths[idx]
    for idx2 in range(idx,len(paths)):
      B = paths[idx+1]
      if is_sub_array(A, B, len(A), len(B)):

        pass

def cluster(graph):
  clusters = list()
  linkmap, roots = _mapper(graph)

  all_paths = list()
  for each in roots:
    all_paths.append(_traverse(each, linkmap, [each]))
  print(all_paths)

    

  clusters.append(_build(graph, linkmap, path))

  return clusters




