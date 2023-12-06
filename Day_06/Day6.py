import os
import time
import numpy as np

def main(part):
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		input_data = f.read().splitlines()
	times = [[int(x) for x in input_data[0].split()[1:]], [int(''.join([x for x in input_data[0].split()[1:]]))]]
	distances = [[int(x) for x in input_data[1].split()[1:]], [int(''.join([x for x in input_data[1].split()[1:]]))]]

	total_ways = []
	for i, t in enumerate(times[part - 1]):
		x = ((-t + np.sqrt(t**2 - (4 * distances[part - 1][i]))) / -2, 
	   		(-t - np.sqrt(t**2 - (4 * distances[part - 1][i]))) / -2)
		if np.ceil(min(x)) == min(x):
			lb = min(x) + 1
		else:
			lb = np.ceil(min(x))

		if np.floor(max(x)) == max(x):
			ub = max(x) - 1
		else:
			ub = np.floor(max(x))
		total_ways.append(ub - lb + 1)
	return(np.product(total_ways))

if __name__ == "__main__":
	start_time = time.time()
	print(f" Part 1 solution: {main(1)}")
	print("Part 1 finished --- %s seconds ---" % (time.time() - start_time))
	mid_time = time.time()
	print(f" Part 2 solution: {main(2)}")
	print("Part 2 finished --- %s seconds ---" % (time.time() - mid_time))
