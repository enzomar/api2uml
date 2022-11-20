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
	def _traverse2(origin, linkmap, path=[]):
		result = []
		for origin in linkmap:
			destination = linkmap[origin]
			new_path = copy.deepcopy(path).append(destination)
			result.extend(Inspector._traverse2(destination, linkmap, path = new_path))
		return result


		return path

	def _traverseDFS(origin, linkmap):
		
		stack = [(origin, [origin])]
		gpath=[]

		while stack:
			top, path = stack.pop()
			if top in linkmap:
				for each in linkmap[top]:
					dest = each.dest
					stack.append((dest, path + [dest]))
			else:
				gpath.append(path)

		return gpath


	@staticmethod
	def _traverse(origin, linkmap, lpath=[], gpath=[]):
		destinations = linkmap[origin]
		for each in destinations:
			dest = each.dest
			tmp_path = copy.deepcopy(lpath)
			tmp_path.append(dest)
			if dest in linkmap:
				Inspector._traverse(dest, linkmap, lpath=tmp_path, gpath=gpath)
			else:
				gpath.append(tmp_path)
		return gpath
				
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
	def _compute_stats(unique_paths: list) -> dict:

		stats = dict()
		stats['max_depth'] = 0
		stats['avg_depth'] = 0

		sum_depth = 0
		for each in unique_paths:
			stats['max_depth'] = max(stats['max_depth'], len(each)-1)
			sum_depth += len(each)-1

		try:
			stats['avg_depth'] = round(sum_depth / len(unique_paths),2)
		except:
			pass
		
		return stats 

	@staticmethod
	def _reduce_paths(path: list, reduced_paths: list, reduced_paths_str: list,) -> None:
		path_str = Inspector._stringify(path)
		for each in reduced_paths_str:
			if path_str in each:
				return 
		reduced_paths.append(path)
		reduced_paths_str.append(path_str)
		
	@staticmethod
	def _get_unique_path(network, roots):
		unique_paths = list()
		unique_paths_str = list()
		max_depth = 0
		for each in roots:
			paths = Inspector._traverseDFS(each, network)
			for path in paths:
				Inspector._reduce_paths(path, unique_paths, unique_paths_str)
			max_depth = max(max_depth, len(path))
		return unique_paths	


	@staticmethod
	def inspect(graph):
		network, roots = Inspector._build_network(graph)
		#unique_paths = Inspector._get_unique_path(network, roots)
		#stats = Inspector._compute_stats(unique_paths)
		
		output = dict()
		output['roots'] = list(roots)
		output['unique_paths'] = unique_paths
		output['stats'] = stats

		return output
	
