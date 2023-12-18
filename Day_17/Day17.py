import os
import time
import heapq
import sys

def main(part):
	# part 1 has max range 3, part 2 has max range 10
	max_range = (7 * (part - 1)) + 3
	# part 1 has min range 1, part 2 has min range 4
	min_range = (3 * (part - 1)) + 1
	
	heat_costs = []
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		for line in f.read().splitlines():
			heat_costs.append([int(point) for point in line])
	
	start = (0, 0)
	end = (len(heat_costs) - 1, len(heat_costs[0]) - 1)
	paths = [(0, start[0], start[1], (-1, -1))]
	visited = set()
	path_costs = {}
	directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

	while paths:
		heat_cost, y, x, prev_dir = heapq.heappop(paths)
		# if we're at the end, return the total cost
		if y == end[0] and x == end[1]:
			return heat_cost
		# if we've already visited this point, continue
		if (y, x, prev_dir) in visited:
			continue
		# add this point (x, y, prev_dir) to the visited set
		visited.add((y, x, prev_dir))
		# for each of the 4 directions, d:
		for d in directions:
			# if it's prev_dir, continue
			if d == prev_dir:
				continue
			# if the direction has turned around, continue, ie if the previous direction was right, we can't go left
			if (prev_dir == (-1, 0) and d == (1, 0)) or \
				(prev_dir == (0, 1) and d == (0, -1)) or \
				(prev_dir == (1, 0) and d == (-1, 0)) or \
				(prev_dir == (0, -1) and d == (0, 1)):
				continue
			# set the cost to move to the next point to 0
			tot_cost = 0
			# for travel length from 1 to the maximum distance allowed in a straight line
			# note not range(min, max + 1) as we are summing the heat costs along the way
			for travel_length in range(1, max_range + 1):
				new_y = y + (d[1] * travel_length)
				new_x = x + (d[0] * travel_length)
				# if this new coord is within the bounds of the map:
				if (0 <= new_y <= len(heat_costs) - 1) and (0 <= new_x <= len(heat_costs[0]) - 1):
					# increase the total cost to travel to this new point by the heat value at new_y, new_x
					tot_cost += heat_costs[new_y][new_x]
					# for part 2, need to take into account the minimum range as well
					if travel_length < min_range:
						continue
					# set the new heat cost to get to this new point
					new_cost = heat_cost + tot_cost
					# if the new cost to get to this point is more than the current cost to get here, continue
					if path_costs.get((new_y, new_x, d), sys.maxsize) <= new_cost:
						continue
					path_costs[(new_y, new_x, d)] = new_cost
					heapq.heappush(paths, (new_cost, new_y, new_x, d))


if __name__ == "__main__":
	start_time = time.time()
	print(f" Part 1 solution: {main(1)}")
	print("Part 1 finished --- %s seconds ---" % (time.time() - start_time))
	mid_time = time.time()
	print(f" Part 2 solution: {main(2)}")
	print("Part 2 finished --- %s seconds ---" % (time.time() - mid_time))
