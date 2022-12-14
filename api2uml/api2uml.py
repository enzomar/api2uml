#!/usr/bin/env python3

import yaml
import argparse
import json
import parser
from umldrawer import UMLDrawer


def parse_arg():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-n', '--node', default=None)
    args = parser.parse_args()

    return args.input, args.node


def load(filename):
    spec = None
    with open(filename, "r") as stream:
        try:
            spec = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return spec


def parse(spec):
    return parser.parse(spec)


def run(filename, node_name):
    spec = load(filename)
    graph = parse(spec)
    with open('out_{0}.plantuml'.format(graph.name), 'w') as fp:
        ud = UMLDrawer()
        plantuml = ud.to_plantuml(graph, node_name)
        fp.write(plantuml)

    return


if __name__ == "__main__":
    filename, node_name = parse_arg()
    run(filename, node_name)
