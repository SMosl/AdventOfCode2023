import os
import time
import numpy as np

def main(part):

	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		input_data = f.read().splitlines()
	times_1 = [int(x) for x in input_data[0].split()[1:]]
	distances_1 = [int(x) for x in input_data[1].split()[1:]]
	times_2 = int(''.join([x for x in input_data[0].split()[1:]]))
	distances_2 = int(''.join([x for x in input_data[1].split()[1:]]))
	
	if part == 1:
		total_ways = []
		for i in range(len(times_1)):
			ways = 0
			for j in range(times_1[i]):
				if (times_1[i] - j) * j > distances_1[i]:
					ways += 1
			total_ways.append(ways)
		return(np.product(total_ways))
	else:
		ways = 0
		for i in range(times_2):
			if (times_2 - i) * i > distances_2:
				ways += 1
		return(ways)

if __name__ == "__main__":
	start_time = time.time()
	print(f" Part 1 solution: {main(1)}")
	print("Part 1 finished --- %s seconds ---" % (time.time() - start_time))
	mid_time = time.time()
	print(f" Part 2 solution: {main(2)}")
	print("Part 2 finished --- %s seconds ---" % (time.time() - mid_time))
