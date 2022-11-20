import pytest
from inspector import Inspector


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


@pytest.mark.skip(reason="draft")
def test_reduce_one():
    path = ['a','b']
    all = [['b'],['d','b','a'], ['a','b']]
    all_str = Inspector._stringify_list(all)
    Inspector._reduce_paths(path, all, all_str)
    assert(all == [['b'],['d','b','a'],['a','b']])
    assert(all_str == ['b', 'd,b,a', 'a,b'])

@pytest.mark.skip(reason="draft")
def test_reduce_one_inner():
    path = ['b','a']
    all = [['b'],['d','b','a'], ['a','b']]
    all_str = Inspector._stringify_list(all)
    Inspector._reduce_paths(path, all, all_str)
    assert(all == [['b'],['d','b','a'],['a','b']])
    assert(all_str == ['b', 'd,b,a', 'a,b'])
