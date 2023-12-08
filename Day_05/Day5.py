import os
import time

def main1():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		maps = f.read().split('\n\n')
	
	seeds = [int(x) for x in maps[0].split()[1:]]
	maps.pop(0)
	for i, m in enumerate(maps):
		maps[i] = [list(map(int, x.split())) for x in m.split('\n')[1:]]

	for category in maps:
		for i, seed in enumerate(seeds):
			changed = False
			for mapping in category:
				if (changed == False) & (mapping[1] <= seed <= mapping[1] + mapping[2] - 1):
					seeds[i] = mapping[0] + (seed - mapping[1])
					changed = True
	return(min(seeds))

def main2():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		maps = f.read().split('\n\n')
	
	seeds = [int(x) for x in maps[0].split()[1:]]
	seeds = [[seeds[2*x], seeds[2*x + 1]] for x in range(int(len(seeds) / 2))]

	maps.pop(0)
	for i, m in enumerate(maps):
		maps[i] = [list(map(int, x.split())) for x in m.split('\n')[1:]]
	
	location_ranges = []
	for seed in seeds:
		# iterate over each pair of seed values in the input, applying each map until all the final location ranges are found
		intervals = [[seed[0], seed[0] + seed[1] - 1]]
		new_intervals = []
		for _map in maps:
			while intervals:
				seed_bounds = intervals.pop()
				for mapping in _map:
					source_end = mapping[1] + mapping[2]
					difference = mapping[0] - mapping[1]
					# consider 3 cases:
					# (source start, source end)	[seed start, seed end]	(source start, source end)
					# [seed start 		(source start,  	seed end] 		source end)
					# (source start 	[seed start, 		source end) 	seed end]
					if (source_end <= seed_bounds[0]) or (seed_bounds[1] <= mapping[1]):
						continue
					if seed_bounds[0] < mapping[1]:
						intervals.append([seed_bounds[0], mapping[1]])
						seed_bounds[0] = mapping[1]
					if source_end < seed_bounds[1]:
						intervals.append([source_end, seed_bounds[1]])
						seed_bounds[1] = source_end
					
					new_intervals.append([seed_bounds[0] + difference, seed_bounds[1] + difference])
					break
				else:
					# occurs if the seed bounds don't intersect the source bounds
					new_intervals.append([seed_bounds[0], seed_bounds[1]])
			intervals = new_intervals
			new_intervals = []
		location_ranges += intervals

	return(min(x[0] for x in location_ranges))

if __name__ == "__main__":
	start_time = time.time()
	print(f" Part 1 solution: {main1()}")
	print("Part 1 finished --- %s seconds ---" % (time.time() - start_time))
	mid_time = time.time()
	print(f" Part 2 solution: {main2()}")
	print("Part 2 finished --- %s seconds ---" % (time.time() - mid_time))
