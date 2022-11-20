import pytest
from inspector import Inspector
import graph
import node
import link


def _build_g0():
    network = [('NodeA','NodeB')]
    g = graph.Graph()
    ls = set()
    for each in network:
        l = link.Link()
        l.set(each[0], each[1])
        ls.add(l)
    g.links = ls
    #g.display()
    return g

def _build_g1():
    network = [('NodeF','NodeG'),('NodeA','NodeB'),('NodeG','NodeB'),('NodeG','NodeI'),('NodeH','NodeI'),('NodeB','NodeC'),
    ('NodeB','NodeE'),('NodeC','NodeD'),('NodeJ','NodeK')]
    g = graph.Graph()
    ls = set()
    for each in network:
        l = link.Link()
        l.set(each[0], each[1])
        ls.add(l)
        
    g.links = ls
    #g.display()
    return g

"""

def test_strigify_path():
    path = ['a','b']
    assert(Inspector._stringify(path) == 'a,b')

def test_reduce_nothing():
    path = ['a','b']
    all = [['b'],['d','b','a']]
    all_str = Inspector._stringify_list(all)
    Inspector._reduce_paths(path, all, all_str)
    assert(all == [['b'],['d','b','a'],['a','b']])
    assert(all_str == ['b', 'd,b,a', 'a,b'])


def test_reduce_one():
    path = ['a','b']
    all = [['b'],['d','b','a'], ['a','b']]
    all_str = Inspector._stringify_list(all)
    Inspector._reduce_paths(path, all, all_str)
    assert(all == [['b'],['d','b','a'],['a','b']])
    assert(all_str == ['b', 'd,b,a', 'a,b'])

def test_reduce_one_inner():
    path = ['b','a']
    all = [['b'],['d','b','a'], ['a','b']]
    all_str = Inspector._stringify_list(all)
    Inspector._reduce_paths(path, all, all_str)
    assert(all == [['b'],['d','b','a'],['a','b']])
    assert(all_str == ['b', 'd,b,a', 'a,b'])


def test_build_network():
    # ( origin, linkmap, paths=[]):
    g = _build_g1()
    linkmap, roots = Inspector._build_network(g)
    assert(len(roots) == 4)
    assert(len(linkmap) == 7)
    assert(len(linkmap['NodeB']) == 2)
    assert(len(linkmap['NodeG']) == 2)
    assert(len(linkmap['NodeF']) == 1)
    assert(len(linkmap['NodeC']) == 1)
    assert(len(linkmap['NodeH']) == 1)
    assert(len(linkmap['NodeA']) == 1)
    assert(len(linkmap['NodeJ']) == 1)
    for each in linkmap:
        for l in linkmap[each]:
            print("{0} -> {1}".format(each, l))
            pass
            
def _check_same_list(l1, l2):
    assert(len(l1) == len(l2))
    for idx in range(0, len(l1)):
        assert(l1[idx] == l2[idx])


def test_traverse_0():
    g0 = _build_g0()
    linkmap, roots = Inspector._build_network(g0)
    gpaths = Inspector._traverse('NodeA',linkmap, lpath=['NodeA'],gpath=[])
    _check_same_list(gpaths, [['NodeA', 'NodeB']])




def test_traverse_1():
    g = _build_g1()
    linkmap, roots = Inspector._build_network(g)
    gpaths = Inspector._traverse('NodeB',linkmap, lpath=['NodeB'], gpath=[])
    print(gpaths)
    assert(len(gpaths) == 2)
    assert(len(gpaths[0]) + len(gpaths[1]) == 5)


def test_traverse_1():
    g = _build_g1()
    linkmap, roots = Inspector._build_network(g)
    gpaths = Inspector._traverse('NodeF',linkmap, lpath=['NodeF'], gpath=[])
    print(gpaths)
    assert(len(gpaths) == 3)

"""

def test_traverse_FDS():
    g = _build_g1()
    linkmap, roots = Inspector._build_network(g)
    gpaths = Inspector._traverseDFS('NodeB',linkmap)
    print(gpaths)
    assert(len(gpaths) == 2)
    assert(len(gpaths[0]) + len(gpaths[1]) == 5)


