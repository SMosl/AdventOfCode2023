import os
import time

def main(part):
	grid = []
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		grid = f.read().splitlines()
	
	for i, line in enumerate(grid):
		if 'S' in line:
			start = (i,line.find('S'), 'S')
			break

	loop = [start]
	next_pos = find_first_direction(grid, start)
	while next_pos not in loop:
		loop.append(next_pos)
		next_pos = find_next_direction(grid, loop[-1], loop)
	
	if part ==1:
		return(len(loop) / 2)
	else:
		# Count the number of points to the left of each non-loop value that are both part of the loop and connected to north (ie '|', 'L', or 'J')
		# If this is even, the value is outside the loop, if it's odd, the value is enclosed
		internal_points = 0
		loop_points = [(x[0], x[1]) for x in loop]
		for point in loop:
			if point[2] in '|LJ':
				grid[point[0]] = grid[point[0]][:point[1]] + '*' + grid[point[0]][point[1] + 1:]

		for y, line in enumerate(grid):
			for x in range(len(line)):
				if (y, x) not in loop_points:
					if line[:x].count('*') % 2 != 0:
						internal_points += 1
		
		return(internal_points)



def find_next_direction(grid, position, loop):
	
	if (position[2] in '|LJ') and (grid[position[0] - 1][position[1]] in '|7F') and ((position[0] - 1, position[1], grid[position[0] - 1][position[1]]) not in loop):
		return (position[0] - 1, position[1], grid[position[0] - 1][position[1]])

	if (position[2] in '-LF') and (grid[position[0]][position[1] + 1] in '-J7') and ((position[0], position[1] + 1, grid[position[0]][position[1] + 1]) not in loop):
		return (position[0], position[1] + 1, grid[position[0]][position[1] + 1])

	if (position[2] in '|7F') and (grid[position[0] + 1][position[1]] in '|LJ') and ((position[0] + 1, position[1], grid[position[0] + 1][position[1]]) not in loop):
		return (position[0] + 1, position[1], grid[position[0] + 1][position[1]])

	if (position[2] in '-J7') and (grid[position[0]][position[1] - 1] in '-LF') and ((position[0], position[1] - 1, grid[position[0]][position[1] - 1]) not in loop):
		return (position[0], position[1] - 1, grid[position[0]][position[1] - 1])
	
	return loop[0]



def find_first_direction(grid, start):
	if grid[start[0] - 1][start[1]] in '|7F':
		return (start[0] - 1, start[1], grid[start[0] - 1][start[1]])
	elif grid[start[0]][start[1] + 1] in '-J7':
		return (start[0], start[1] + 1, grid[start[0]][start[1] + 1])
	elif grid[start[0] + 1][start[1]] in '|LJ':
		return (start[0] + 1, start[1], grid[start[0] + 1][start[1]])



if __name__ == "__main__":
	start_time = time.time()
	print(f" Part 1 solution: {main(1)}")
	print("Part 1 finished --- %s seconds ---" % (time.time() - start_time))
	mid_time = time.time()
	print(f" Part 2 solution: {main(2)}")
	print("Part 2 finished --- %s seconds ---" % (time.time() - mid_time))
