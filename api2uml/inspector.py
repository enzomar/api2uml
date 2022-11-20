import copy

class Inspector(object):
	@staticmethod
	def _build_network(graph):
		linkmap = {}
		origins = set()
		destinations = set()
		for link in graph.links:

			origins.add(link.origin)
			destinations.add(link.dest)

			if link.origin not in linkmap:
				linkmap[link.origin] = set()
			linkmap[link.origin].add(link)

		roots = origins.difference(destinations)
		return linkmap, roots

	@staticmethod
	def _traverse( origin, linkmap, path=[]):
		if origin in linkmap:
			destinations = linkmap[origin]
			for each in destinations:
				#new_path = copy.deepcopy(path)
				dest = each.dest
				path.append(dest)
				return Inspector._traverse(dest, linkmap, path)
		return path
				
	@staticmethod
	def _stringify_list(array):
		output = []
		for each in array:
			output.append(Inspector._stringify(each))
		return output

	@staticmethod
	def _stringify(array):
		return ','.join(array)

	@staticmethod
	def _reduce_paths(path: list, reduced_paths: list, reduced_paths_str: list,) -> None:
		path_str = Inspector._stringify(path)
		for each in reduced_paths_str:
			if path_str in each:
				return 
		reduced_paths.append(path)
		reduced_paths_str.append(path_str)
		
	@staticmethod
	def _compute_stats(unique_paths: list) -> dict:

		stats = dict()
		stats['max_depth'] = 0
		stats['avg_depth'] = 0

		sum_depth = 0
		for each in unique_paths:
			stats['max_depth'] = max(stats['max_depth'], len(each))
			sum_depth += len(each)

		try:
			stats['avg_depth'] = round(sum_depth / len(unique_paths),2)
		except:
			pass
		
		return stats 

	@staticmethod
	def _get_unique_path(network, roots):
		unique_paths = list()
		unique_paths_str = list()
		max_depth = 0
		for each in roots:
			path = Inspector._traverse(each, network, [each])
			Inspector._reduce_paths(path, unique_paths, unique_paths_str)
			max_depth = max(max_depth, len(path))
		return unique_paths	


	@staticmethod
	def inspect(graph):
		network, roots = Inspector._build_network(graph)
		unique_paths = Inspector._get_unique_path(network, roots)
		stats = Inspector._compute_stats(unique_paths)
		
		output = dict()
		output['roots'] = list(roots)
		output['unique_paths'] = unique_paths
		output['stats'] = stats

		return output
	
