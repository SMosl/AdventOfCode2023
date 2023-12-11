import os
import time
from itertools import combinations

def main(part):

	# Part 1 increases the size of empty rows and columns by 1, part 2 increases them by 999999
	multiplier = (999998 * (part - 1)) + 1

	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		lines = f.read().splitlines()

	empty_rows = set()
	empty_cols = set()
	galaxies = []
	for y in range(len(lines)):
		if len(set(lines[y])) == 1:
			empty_rows.add(y)
		for x in range(len(lines[0])):
			if len(set([lines[i][x] for i in range(len(lines))])) == 1:
				empty_cols.add(x)
			if lines[y][x] == '#':
				galaxies.append((y,x))

	for i, galaxy in enumerate(galaxies):
		galaxies[i] = (galaxy[0] + multiplier * len([x for x in empty_rows if x < galaxy[0]]), galaxy[1] + multiplier * len([x for x in empty_cols if x < galaxy[1]]))

	total_shortest_paths = 0
	for pair in combinations(galaxies, 2):
		total_shortest_paths += abs(pair[0][0] - pair[1][0]) + abs(pair[0][1] - pair[1][1])

	return(total_shortest_paths)

if __name__ == "__main__":
	start_time = time.time()
	print(f" Part 1 solution: {main(1)}")
	print("Part 1 finished --- %s seconds ---" % (time.time() - start_time))
	mid_time = time.time()
	print(f" Part 2 solution: {main(2)}")
	print("Part 2 finished --- %s seconds ---" % (time.time() - mid_time))
