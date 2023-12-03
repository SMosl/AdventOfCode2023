import os
import time
import re

def main(part):

	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		data = f.read().splitlines()

		# find the coordinates of the start of each number in form [y, x, value] and each symbol in coordinate form [y, x]
		part_starts = []
		symbols = []
		for y, line in enumerate(data):
			line_poss_parts = [(y, m.start(), m[1]) for m in re.finditer('(\d+)', line)]
			if len(line_poss_parts) > 0:
				part_starts = [*part_starts, *line_poss_parts]
			for x, value in enumerate(line):
				if (value != '.') & (value.isdigit() == False):
					symbols.append([y, x])

		# identify all the coords of each part
		part_complete_coords = []
		for number in part_starts:
			coords = [int(number[2])]
			for i in range(len(number[2])):
				coords.append([number[0], number[1] + i])
			part_complete_coords.append(coords)

		# for part 1, if any of the coords are next to a symbol, add it to the list of parts and sum their values
		directions = ((0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1))
		if part == 1:
			valid_parts = []
			for possibility in part_complete_coords:
				for index in possibility[1:]:
					for d in directions:
						if ([index[0] + d[0], index[1] + d[1]] in symbols) & (possibility not in valid_parts):
							valid_parts.append(possibility)

			return sum([x[0] for x in valid_parts])
		# for part 2, for each symbol representing a gear '*', sum the product of the values of the adjacent parts if there are exactly 2 adjacent parts
		else:
			ratios = 0
			for gear in symbols:
				if data[gear[0]][gear[1]] == '*':
					adjacent_to_gear = [[gear[0] + d[0], gear[1] + d[1]] for d in directions]
					adjacent_parts = []
					for part in part_complete_coords:
						for coord in part[1:]:
							if (coord in adjacent_to_gear) and (part not in adjacent_parts):
								adjacent_parts.append(part)
					if len(adjacent_parts) == 2:
						ratios += adjacent_parts[0][0] * adjacent_parts[1][0]
			return ratios

if __name__ == "__main__":
	start_time = time.time()
	print(f" Part 1 solution: {main(1)}")
	print("Part 1 finished --- %s seconds ---" % (time.time() - start_time))
	mid_time = time.time()
	print(f" Part 2 solution: {main(2)}")
	print("Part 2 finished --- %s seconds ---" % (time.time() - mid_time))
