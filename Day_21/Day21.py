import os
import time
import numpy as np

def main_part_1():
	
	data = []
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		while(len(line := f.readline()) != 0):
			line = list(line.strip())
			if 'S' in line:
				start = (len(data), line.index('S'))
			data.append(line)

	data = np.array(data)
	valid_plots = {start}
	for _ in range(64):
		valid_plots = next_step(valid_plots, data)
	return len(valid_plots)

def main_part_2():
	
	data = []
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		while(len(line := f.readline()) != 0):
			line = list(line.strip().replace('S','.') * 5)
			"""if 'S' in line:
				start = (len(data), line.index('S'))"""
			data.append(line)
		data = data * 5

	start = (327, 327)
	data = np.array(data)
	data[start[0], start[1]] = 'S'
	np.savetxt('5x5grid.txt', data, fmt='%s', delimiter='')

	"""
	The input consists of an empty central row and column (other than containing 'S') and empty diagonal lines of space
	from the centre of the top row to the centre of each side, then down to the centre of the bottom row, forming a diamond.

	'S' is 65 units away from each side of the input square, which has dimensions 131 x 131.
	After 65 steps, the outer limits of the visited space will be on the centre of each of the 4 sides due to the empty centre row and column.
	If the input is then repeated infinitely, after 131 + 65 steps, the visited space will be contained within, and reached the boundary of,
	a diamond made up of a 3 x 3 grid of the input, again due to the empty central line and column.
	After 131 + 131 + 65 steps, the visited space is contained within, and on, the boundary line of a diamond made up of a 5 x 5 grid of inputs.
	-------
	|D ^ A|
	| / \ |
	|< O >|
	| \ / |
	|C v B|
	-------
	After every cycle of 131 steps (after the initial 65), the number of valid points is the sum of 3 terms:
	The corners:
		The top most square, bottom most square, left most square and right most square are always included and are constant, don't depend on the step number,
		these are OCB, ODA, OAB, ODC respectively
	The edges:
		The top left edge of the diamond consists of (x * B) + (x-1 * (OABC)), the rop right (x * C) + (x-1 * (OBCD)), bottom right (x * D) + (x-1 * (OACD)),
		and bottom left (x * A) + (x-1 * (OABD)) where x is the number of full 131 length cycles. This term linearly depends on x.
	The centre:
		The centre of the diamond consists of full inputs where every other non-# is filled with O, note that this alternates between adjacent grids,
		ie if the starting coordinate S == '.', the central points of adjacent input grids will be 'O', whose adjacent grids will then have a central '.' etc.
	Part 2 requres the 26501365th step, note that  26501365 = 131*202300 + 65
	"""
	quadratic_cases_x = (65, 131 + 65, (131 * 2) + 65)
	quadratic_cases_y = [0, 0, 0]
	for i, val in enumerate(quadratic_cases_x):
		valid_plots = {start}
		for _ in range(val):
			valid_plots = next_step(valid_plots, data)
		quadratic_cases_y[i] = len(valid_plots)
	
	eqns = np.array([[1, 65, 65**2],[1, 131 + 65, (131 + 65)**2], [1, ((131 * 2) + 65), ((131 * 2) + 65)**2]])
	solns = np.array(quadratic_cases_y)
	coefficients = np.linalg.solve(eqns, solns)
	x = 26501365
	return(coefficients[0] + coefficients[1]*x + coefficients[2]*x*x)


def next_step(coords, garden):
	directions = {(-1, 0), (1, 0), (0, -1), (0, 1)}
	new_coords = set()
	for coord in coords:
		for d in directions:
			new_coord = (coord[0] + d[0], coord[1] + d[1])
			if (0 <= new_coord[0] <= (len(garden) - 1)) and (0 <= new_coord[1] <= (len(garden[0]) - 1)) and (garden[new_coord[0], new_coord[1]] != '#'):
				new_coords.add(new_coord)
	return new_coords

if __name__ == "__main__":
	start_time = time.time()
	print(f" Part 1 solution: {main_part_1()}")
	print("Part 1 finished --- %s seconds ---" % (time.time() - start_time))
	mid_time = time.time()
	print(f" Part 2 solution: {main_part_2()}")
	print("Part 2 finished --- %s seconds ---" % (time.time() - mid_time))
