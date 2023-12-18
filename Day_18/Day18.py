import os
import time
import re

def main(part):
	input = []
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		while(len(line := f.readline()) != 0):
			b = re.match(r'(?P<direction>\w) (?P<distance>\d+) (?P<colour>\S+)', line)
			input.append((b['direction'], int(b['distance']), b['colour'][1:-1]))

	curr_vertex = (0,0, None)
	boundary_length = 0
	vertices = []
	
	directions = {'U' : (-1, 0),
				'D' : (1, 0),
				'L' : (0, -1),
				'R' : (0, 1),
				3 : (-1, 0),
				1 : (1, 0),
				2 : (0, -1),
				0 : (0, 1)}

	for instruction in input:
		if part == 1:
			direction = directions[instruction[0]]
			distance = instruction[1]
		else:
			direction = directions[int(instruction[2][-1])]
			distance = int(instruction[2][1:-1], 16)
		boundary_length += distance
		curr_vertex = (curr_vertex[0] + (direction[0] * distance), curr_vertex[1] + (direction[1] * distance))
		vertices.append((curr_vertex[1] + 1, curr_vertex[0] + 1))
	
	vertices.insert(0, vertices[-1])
	left_shoe = sum([vertices[i][0] * vertices[i + 1][1] for i in range(len(vertices) - 1)])
	right_shoe = sum([vertices[i][1] * vertices[i + 1][0] for i in range(len(vertices) - 1)])
	sole = 0.5 * abs(left_shoe - right_shoe)
	return(sole + boundary_length/2 + 1)


if __name__ == "__main__":
	start_time = time.time()
	print(f" Part 1 solution: {main(1)}")
	print("Part 1 finished --- %s seconds ---" % (time.time() - start_time))
	mid_time = time.time()
	print(f" Part 2 solution: {main(2)}")
	print("Part 2 finished --- %s seconds ---" % (time.time() - mid_time))
