#!/usr/bin/env python3

import yaml
import argparse
import json
import parser
from umldrawer import UMLDrawer
import cluster

def parse_arg():
	parser = argparse.ArgumentParser()

	parser.add_argument('-i', '--input')  
	args = parser.parse_args()

	return args.input


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


def run():
	filename = parse_arg()
	spec = load(filename)
	graph = parse(spec)

	#clusters = cluster.cluster(graph)
	
	#for each in clusters:
	with open('out_{0}.plantuml'.format(graph.name), 'w') as fp:
			ud = UMLDrawer()
			plantuml =ud.to_plantuml(graph)
			fp.write(plantuml)


	return



if __name__ == "__main__":
	run()


