import os
import time
import re
import math

def main_part_1():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		[raw_workflows, raw_ratings] = f.read().split('\n\n')

	workflows = {}
	parts = []
	A = set()

	raw_workflows = raw_workflows.splitlines()
	for w in raw_workflows:
		w_name, w_instructions = w[:-1].split('{')
		w_instructions = w_instructions.split(',')
		workflows[w_name] = []
		for instruction in w_instructions[:-1]:
			b = re.match(r'(?P<category>[a-zA-Z]+)(?P<operator>[><])(?P<value>\d+):(?P<destination>[a-zA-Z]+)', instruction)
			workflows[w_name].append([b['category'], b['operator'], int(b['value']), b['destination']])
		workflows[w_name].append(w_instructions[-1])

	raw_ratings = raw_ratings.splitlines()
	for r in raw_ratings:
		parts.append([int(x) for x in re.split(',|=', r[1:-1]) if x.isnumeric()])
	
	for part in parts:
		w_name = 'in'
		while w_name not in {'A','R'}:
			w_name = find_next_w(part, w_name, workflows)
		if w_name == 'A':
			A.add(sum(part))
	return(sum(A))

def main_part_2():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		raw_workflows = f.read().split('\n\n')[0]

	workflows = {}

	raw_workflows = raw_workflows.splitlines()
	for w in raw_workflows:
		w_name, w_instructions = w[:-1].split('{')
		w_instructions = w_instructions.split(',')
		workflows[w_name] = []
		for instruction in w_instructions[:-1]:
			b = re.match(r'(?P<category>[a-zA-Z]+)(?P<operator>[><])(?P<value>\d+):(?P<destination>[a-zA-Z]+)', instruction)
			workflows[w_name].append([b['category'], b['operator'], int(b['value']), b['destination']])
		workflows[w_name].append(w_instructions[-1])

	parts = [[(1,4000), (1,4000), (1,4000), (1,4000), 'in']]
	A = 0
	while parts:
		p = parts.pop(0)
		if p[-1] == 'A':
			A += math.prod([(x[1] - x[0] + 1) for x in p[:-1]])
		elif p[-1] != 'R':
			parts += find_next_w_regions(p, workflows[p[-1]])

	return(A)



def find_next_w(part, w_name, workflows):
	categories = 'xmas'
	for instruction in workflows[w_name]:
		if isinstance(instruction, str):
			return instruction
		elif instruction[1] == '<':
			if part[categories.index(instruction[0])] < instruction[2]:
				return instruction[3]
		elif instruction[1] == '>':
			if part[categories.index(instruction[0])] > instruction[2]:
				return instruction[3]

def find_next_w_regions(p, workflow):
	categories = 'xmas'
	mapping = []
	for instruction in workflow:
		if isinstance(instruction, str):
			mapping.append(p[:-1] + [instruction])
		elif instruction[1] == '<':
			changed_index = categories.index(instruction[0])
			changed_region = [x if (i != changed_index) else 0 for i, x in enumerate(p)]
			if p[changed_index][0] < instruction[2]:
				changed_region[changed_index] = (p[changed_index][0], instruction[2] - 1)
				changed_region[-1] = instruction[-1]
				mapping.append(changed_region)
				p[changed_index] = (instruction[2], p[changed_index][1])
			else:
				continue
		elif instruction[1] == '>':
			changed_index = categories.index(instruction[0])
			changed_region = [x if (i != changed_index) else 0 for i, x in enumerate(p)]
			if p[changed_index][1] > instruction[2]:
				changed_region[changed_index] = (instruction[2] + 1, p[changed_index][1])
				changed_region[-1] = instruction[-1]
				mapping.append(changed_region)
				p[changed_index] = (p[changed_index][0], instruction[2])
			else:
				continue
	return(mapping)

if __name__ == "__main__":
	start_time = time.time()
	print(f" Part 1 solution: {main_part_1()}")
	print("Part 1 finished --- %s seconds ---" % (time.time() - start_time))
	mid_time = time.time()
	print(f" Part 2 solution: {main_part_2()}")
	print("Part 2 finished --- %s seconds ---" % (time.time() - mid_time))
