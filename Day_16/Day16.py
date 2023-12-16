import os
import time
import copy

def main(part):
	input = []
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		while(len(line := f.readline()) != 0):
			input.append([set() if (x == '.') else set(x) for x in line.strip().replace("\\", "S")])

	directions = {(-1, 0) : (0, 1), 
				 (0, 1) : (-1, 0), 
				 (1, 0) : (0, -1), 
				 (0, -1) : (1, 0)}

	directions_s = {(-1, 0) : (0, -1), 
				 (0, 1) : (1, 0), 
				 (1, 0) : (0, 1), 
				 (0, -1) : (-1, 0)}

	if part == 1:
		# For the test:
		#beams = [(0, 0, (0, 1))]

		beams = [(0, 0, (1, 0))]
		solution = find_energized_tiles(beams, input, directions, directions_s)
		return(solution)
	else:
		d_rot = {'/' : directions, 'S' : directions_s}
		l_beams = [y for y in range(0, len(input)) if (input[y][0] != {'|'})]
		starting_beams = [(y, 0, d_rot[next(iter(input[y][0]))][(0,1)]) if (input[y][0].intersection({'/', 'S'})) else (y, 0, (0,1)) for y in l_beams]

		t_beams = [x for x in range(0, len(input[0])) if (input[0][x] != {'-'})]
		starting_beams += [(0, x, d_rot[next(iter(input[0][x]))][(1,0)]) if (input[0][x].intersection({'/', 'S'})) else (0, x, (1,0)) for x in t_beams]

		r_beams = [y for y in range(0, len(input)) if (input[y][-1] != {'|'})]
		starting_beams += [(y, len(input[0])-1, d_rot[next(iter(input[y][-1]))][(0,-1)]) if (input[y][-1].intersection({'/', 'S'})) else (y, len(input[0])-1, (0,-1)) for y in r_beams]

		b_beams = [x for x in range(0, len(input[0])) if (input[-1][x] != {'-'})]
		starting_beams += [(len(input)-1, x, d_rot[next(iter(input[-1][x]))][(-1,0)]) if (input[-1][x].intersection({'/', 'S'})) else (len(input)-1, x, (-1,0)) for x in b_beams]

		energized_count = 0
		for start in starting_beams:
			data = copy.deepcopy(input)
			beams = [start]
			energized_count = max(energized_count, find_energized_tiles(beams, data, directions, directions_s))
		return(energized_count)
	


def find_energized_tiles(beams, data, directions, directions_s):
	data[beams[0][0]][beams[0][1]].add(beams[0][2])
	while beams:
		curr_pos = beams.pop(0)
		next_y = curr_pos[0] + curr_pos[2][0]
		next_x = curr_pos[1] + curr_pos[2][1]
		curr_d = curr_pos[2]
		if (0 <= next_y < len(data)) and (0 <= next_x < len(data[0])):
			next_vals = data[next_y][next_x]

			if ('|' in next_vals):
				if (curr_d in {(0, 1), (0, -1)}):
					if (-1, 0) not in next_vals:
						data[next_y][next_x].add((-1, 0))
						beams.append((next_y, next_x, (-1, 0)))
					if (1, 0) not in next_vals:
						data[next_y][next_x].add((1, 0))
						beams.append((next_y, next_x, (1, 0)))
				elif curr_d not in next_vals:
					data[next_y][next_x].add(curr_d)
					beams.append((next_y, next_x, curr_d))
						
			elif ('-' in next_vals):
				if (curr_d in {(-1, 0), (1, 0)}):
					if (0, -1) not in next_vals:
						data[next_y][next_x].add((0, -1))
						beams.append((next_y, next_x, (0, -1)))
					if (0, 1) not in next_vals:
						data[next_y][next_x].add((0, 1))
						beams.append((next_y, next_x, (0, 1)))
				elif curr_d not in next_vals:
					data[next_y][next_x].add(curr_d)
					beams.append((next_y, next_x, curr_d))

			elif ('/' in next_vals):
				new_direction = directions[curr_d]
				if new_direction not in next_vals:
					data[next_y][next_x].add(new_direction)
					beams.append((next_y, next_x, new_direction))

			elif ('S' in next_vals):
				new_direction = directions_s[curr_d]
				if new_direction not in next_vals:
					data[next_y][next_x].add(new_direction)
					beams.append((next_y, next_x, new_direction))
			
			else:
				data[next_y][next_x].add(curr_d)
				beams.append((next_y, next_x, curr_d))

	solution = 0
	for line in data:
		p_line = ''
		for point in line:
			if point.intersection(set(k for k in directions.keys())):
				p_line += '#'
				solution += 1
			else:
				p_line += '.'
	return(solution)



if __name__ == "__main__":
	start_time = time.time()
	print(f" Part 1 solution: {main(1)}")
	print("Part 1 finished --- %s seconds ---" % (time.time() - start_time))
	mid_time = time.time()
	print(f" Part 2 solution: {main(2)}")
	print("Part 2 finished --- %s seconds ---" % (time.time() - mid_time))
