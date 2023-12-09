import os
import time
import re
import itertools

def main(part):
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		lines = f.readlines()
		sequences = [([int(d) for d in re.findall(r'-?\d+', line)]) for line in lines]

	next_values = []
	prev_values = []

	for raw_values in sequences:
		history = [raw_values]
		differences = [b - a for a, b in itertools.pairwise(raw_values)]
		history.insert(0, differences)
		while len(set(differences)) != 1:
			differences = [b - a for a, b in itertools.pairwise(differences)]
			history.insert(0, differences)
		
		history.insert(0, [0 for _ in range(len(differences) - 1)])

		for i in range(1, len(history)):
			history[i].append(history[i][-1] + history[i-1][-1])
			history[i].insert(0, history[i][0] - history[i-1][0])
		
		next_values.append(history[-1][-1])
		prev_values.append(history[-1][0])

	if part == 1:
		return(sum(next_values))
	else:
		return(sum(prev_values))

if __name__ == "__main__":
	start_time = time.time()
	print(f" Part 1 solution: {main(1)}")
	print("Part 1 finished --- %s seconds ---" % (time.time() - start_time))
	mid_time = time.time()
	print(f" Part 2 solution: {main(2)}")
	print("Part 2 finished --- %s seconds ---" % (time.time() - mid_time))
