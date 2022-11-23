import pytest
from utils.inspector import Inspector
from model.graph import Graph
from model.link import Link


def _build_g0():
    network = [('NodeA', 'NodeB')]
    g = Graph()
    ls = set()
    for each in network:
        l = Link()
        l.set(each[0], each[1])
        ls.add(l)
    g.links = ls
    # g.display()
    return g


def _build_g1():
    network = [('NodeF', 'NodeG'), ('NodeA', 'NodeB'), ('NodeG', 'NodeB'), ('NodeG', 'NodeI'),
               ('NodeH', 'NodeI'), ('NodeB', 'NodeC'), ('NodeB', 'NodeE'), ('NodeC', 'NodeD'), ('NodeJ', 'NodeK')]
    g = Graph()
    ls = set()
    for each in network:
        l = Link()
        l.set(each[0], each[1])
        ls.add(l)

    g.links = ls
    # g.display()
    return g


def _build_g2():
    network = [('NodeF', 'NodeG'), ('NodeA', 'NodeB'), ('NodeG', 'NodeB'), ('NodeG', 'NodeI'),
               ('NodeH', 'NodeI'), ('NodeB', 'NodeC'), ('NodeC', 'NodeD'), ('NodeJ', 'NodeK')]
    g = Graph()
    ls = set()
    for each in network:
        l = Link()
        l.set(each[0], each[1])
        ls.add(l)

    g.links = ls
    # g.display()
    return g


def test_strigify_path():
    path = ['a', 'b']
    assert (Inspector._stringify(path) == 'a,b')


def test_reduce_nothing():
    path = ['a', 'b']
    all = [['b'], ['d', 'b', 'a']]
    all_str = Inspector._stringify_list(all)
    Inspector._reduce_paths(path, all, all_str)
    assert (all == [['b'], ['d', 'b', 'a'], ['a', 'b']])
    assert (all_str == ['b', 'd,b,a', 'a,b'])


def test_reduce_one():
    path = ['a', 'b']
    all = [['b'], ['d', 'b', 'a'], ['a', 'b']]
    all_str = Inspector._stringify_list(all)
    Inspector._reduce_paths(path, all, all_str)
    assert (all == [['b'], ['d', 'b', 'a'], ['a', 'b']])
    assert (all_str == ['b', 'd,b,a', 'a,b'])


def test_reduce_one_inner():
    path = ['b', 'a']
    all = [['b'], ['d', 'b', 'a'], ['a', 'b']]
    all_str = Inspector._stringify_list(all)
    Inspector._reduce_paths(path, all, all_str)
    assert (all == [['b'], ['d', 'b', 'a'], ['a', 'b']])
    assert (all_str == ['b', 'd,b,a', 'a,b'])


def test_build_network():
    # ( origin, linkmap, paths=[]):
    g = _build_g1()
    linkmap, roots = Inspector._build_network(g)
    assert (len(roots) == 4)
    assert (len(linkmap) == 7)
    assert (len(linkmap['NodeB']) == 2)
    assert (len(linkmap['NodeG']) == 2)
    assert (len(linkmap['NodeF']) == 1)
    assert (len(linkmap['NodeC']) == 1)
    assert (len(linkmap['NodeH']) == 1)
    assert (len(linkmap['NodeA']) == 1)
    assert (len(linkmap['NodeJ']) == 1)
    for each in linkmap:
        for l in linkmap[each]:
            print("{0} -> {1}".format(each, l))
            pass


def _check_same_list(l1, l2):
    assert (len(l1) == len(l2))
    for idx in range(0, len(l1)):
        assert (l1[idx] == l2[idx])


def test_traverse_FDS():
    g = _build_g1()
    linkmap, roots = Inspector._build_network(g)
    gpaths = Inspector._traverseDFS('NodeB', linkmap)
    print(gpaths)
    assert (len(gpaths) == 2)
    assert (len(gpaths[0]) + len(gpaths[1]) == 5)


def test_traverse_FDS2():
    g = _build_g1()
    linkmap, roots = Inspector._build_network(g)
    gpaths = Inspector._traverseDFS('NodeF', linkmap)
    print(gpaths)
    assert (len(gpaths) == 3)
    assert (len(gpaths[0]) + len(gpaths[1]) + len(gpaths[2]) == 12)


def test_computedepth_0():
    paths = []
    stats = Inspector._compute_depths(paths)
    assert (stats['max'] == 0)
    assert (stats['avg'] == 0)


def test_computedepth_1():
    paths = []
    paths.append(['NodeF', 'NodeG', 'NodeI'])
    paths.append(['NodeF', 'NodeG', 'NodeB', 'NodeE'])
    paths.append(['NodeF', 'NodeG', 'NodeB', 'NodeC', 'NodeD'])
    stats = Inspector._compute_depths(paths)

    assert (stats['max'] == 4)
    assert (stats['avg'] == 3)


def test_computedepth_2():
    paths = []
    paths.append(['NodeF'])
    stats = Inspector._compute_depths(paths)

    assert (stats['max'] == 0)
    assert (stats['avg'] == 0)


def test_computedepth_3():
    paths = []
    paths.append(['A', 'B'])
    paths.append(['A', 'B'])
    stats = Inspector._compute_depths(paths)

    assert (stats['max'] == 1)
    assert (stats['avg'] == 1)


def test_most_connected_0():
    g = _build_g1()
    conns = Inspector._get_most_connected(g)
    assert (len(conns) == 1)
    assert (conns[0] == 'NodeB')


def test_most_connected_2():
    g = _build_g2()
    conns = Inspector._get_most_connected(g)
    assert (len(conns) == 2)
    assert ('NodeB' in conns)
    assert ('NodeG' in conns)
