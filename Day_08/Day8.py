import os
import time
import re
import math

def main1():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		lines = f.read().split('\n\n')
		directions = lines[0]
		raw_nodes = lines[1].splitlines()
	
	nodes = dict()
	for node in raw_nodes:
		data = re.findall(r'(\w+)', node)
		nodes[data[0]] = (data[1], data[2])
	
	current_node = 'AAA'
	steps = 0
	while current_node != 'ZZZ':
		instruction = directions[steps % len(directions)]
		if instruction == 'L':
			current_node = nodes[current_node][0]
		elif instruction == 'R':
			current_node = nodes[current_node][1]
		steps += 1
	
	return steps

def main2():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		lines = f.read().split('\n\n')
		directions = lines[0]
		raw_nodes = lines[1].splitlines()
	
	nodes = dict()
	starting_nodes = []
	for node in raw_nodes:
		data = re.findall(r'(\w+)', node)
		nodes[data[0]] = (data[1], data[2])
		if data[0][2] == 'A':
			starting_nodes.append(data[0])

	path_lengths = []
	for current_node in starting_nodes:
		steps = 0
		while current_node[-1] != 'Z':
			instruction = directions[steps % len(directions)]
			if instruction == 'L':
				current_node = nodes[current_node][0]
			elif instruction == 'R':
				current_node = nodes[current_node][1]
			steps += 1
		path_lengths.append(steps)

	return(math.lcm(*path_lengths))

if __name__ == "__main__":
	start_time = time.time()
	print(f" Part 1 solution: {main1()}")
	print("Part 1 finished --- %s seconds ---" % (time.time() - start_time))
	mid_time = time.time()
	print(f" Part 2 solution: {main2()}")
	print("Part 2 finished --- %s seconds ---" % (time.time() - mid_time))
