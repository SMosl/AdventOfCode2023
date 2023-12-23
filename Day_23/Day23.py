import os
import time
import numpy as np
import graphviz

def main_part_1():
	data = []
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		while(len(line := f.readline()) != 0):
			data.append(list(line.strip().replace('#', '█').replace('.', ' ')))

	nodes = {}
	directions = {(-1, 0) : {'v', '█'}, 
			(0, 1) : {'<', '█'}, 
			(1, 0) : {'^', '█'},
			(0, -1) : {'>', '█'}}
	
	data = np.array(data)
	np.savetxt('maze.txt', data, fmt='%s', delimiter='', encoding='utf8')
	
	for y, row in enumerate(data):
		for x, val in enumerate(row):
			if val != '█':
				nodes[(y, x)] = set()
				for d in directions.keys():
					if (0 <= (y + d[0]) <= (len(data)-1)) and (0 <= (x + d[1]) <= (len(data[0])-1)) and (data[y+d[0]][x+d[1]] not in directions[d]):
						nodes[(y, x)].add((y + d[0], x + d[1]))

	end = (len(data) - 1, len(data[0]) - 2)
	paths = [[(0, 1)]]
	longest_path_length = 0
	while paths:
		path = paths.pop(0)
		if path[-1][0] == end[0] and path[-1][1] == end[1]:
			if len(path) > longest_path_length:
				longest_path = path
		for neighbour in nodes[path[-1]]:
			if neighbour not in path:
				paths.append(path + [neighbour])
	return(len(longest_path) - 1)

def main_part_2():
	data = []
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		while(len(line := f.readline()) != 0):
			data.append(list(line.strip().replace('#', '█').replace('.', ' ')))

	nodes = {}
	directions = {(-1, 0) : {'█'}, 
			(0, 1) : {'█'}, 
			(1, 0) : {'█'},
			(0, -1) : {'█'}}
	
	# Print data to identify how to reduce the size of the graph (just consider junctions)
	data = np.array(data)
	np.savetxt('maze.txt', data, fmt='%s', delimiter='', encoding='utf8')
	
	# Populate the dictionary of nodes and their adjacent neighbours
	for y, row in enumerate(data):
		for x, val in enumerate(row):
			if val != '█':
				nodes[(y, x)] = set()
				for d in directions.keys():
					if (0 <= (y + d[0]) <= (len(data)-1)) and (0 <= (x + d[1]) <= (len(data[0])-1)) and (data[y+d[0]][x+d[1]] != '█'):
						nodes[(y, x)].add((y + d[0], x + d[1]))
	
	# Create a dictionary of junctions and their adjacent neighbours
	junctions = {}
	for n in nodes.keys():
		if len(nodes[n]) > 2:
			junctions[n] = set(x for x in nodes[n]) 
	junctions[(0, 1)] = {(1, 1)}
	junctions[(140, 139)] = {(139, 139)}

	# Reduce the dictionary of junctions to just include each junction and the distance between neighbouring junctions
	j_distances = {}
	for j in junctions.keys():
		j_distances[j] = {}
		for choice in junctions[j]:
			prev_node = j
			next_node = choice
			dist = 1
			while next_node not in junctions.keys():
				temp_prev_node = (next_node[0], next_node[1])
				next_node = [(x[0], x[1]) for x in nodes[next_node] if x != prev_node]
				if next_node:
					next_node = next_node[0]
					prev_node = temp_prev_node 
					dist += 1
				else:
					break
			j_distances[j][next_node] = dist
	
	# Visualise the graph to get an idea of what's going on
	dot = graphviz.Digraph('Day23', comment='Day 23 Part 2 Visualisation')
	for j in junctions.keys():
		dot.node(str(j), str(j))

	for j in j_distances.keys():
		for n_j in j_distances[j].keys():
			dot.edge(str(j), str(n_j), label=str(j_distances[j][n_j]))

	dot.render(directory='doctest-output', view=True)  

	# Somehow edit the path finding algorithm for part 1 to include weights
	end = (140, 139)
	paths = [(((0,1),),0)]
	longest_path_length = 0
	
	while paths:
		new_paths = set()
		for path, dist in paths:
			for neighbour in j_distances[path[-1]].keys():
				if neighbour in path:
					continue
				if neighbour == end:
					longest_path_length = max(longest_path_length, dist + j_distances[path[-1]][neighbour])
					continue
				new_paths.add(((*path, neighbour), dist + j_distances[path[-1]][neighbour]))
		paths = new_paths

	return(longest_path_length)

if __name__ == "__main__":
	start_time = time.time()
	print(f" Part 1 solution: {main_part_1()}")
	print("Part 1 finished --- %s seconds ---" % (time.time() - start_time))
	mid_time = time.time()
	print(f" Part 2 solution: {main_part_2()}")
	print("Part 2 finished --- %s seconds ---" % (time.time() - mid_time))
