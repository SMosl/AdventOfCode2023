import os
import time
import re

def main(part):
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		raw_input = f.read().split(',')

	if part == 1:
		solution = 0
		for s in raw_input:
			solution += find_hash(s)
		return(solution)
	else:
		boxes = {}
		for s in raw_input:
			[label, eq, dash, lens] = re.split(r"(=)|(-)", s)
			box_number = find_hash(label)
			if dash:
				if (box_number in boxes) and (label in [x[0] for x in boxes[box_number]]):
					boxes[box_number] = [x for x in boxes[box_number] if x[0] != label]
			else:
				if box_number in boxes:
					if label in (indexes := [x[0] for x in boxes[box_number]]):
						i = indexes.index(label)
						boxes[box_number] = boxes[box_number][:i] + [[label, int(lens)]] + boxes[box_number][i+1:]
					else:
						boxes[box_number] = boxes[box_number] + [[label, int(lens)]]
				else:
					boxes[box_number] = [[label, int(lens)]]

		solution = 0
		for box in boxes:
			for i, lens in enumerate(boxes[box]):
				solution += (1 + box) * (i + 1) * lens[1]
		return(solution)

def find_hash(s):
	curr_val = 0
	for val in s:
		curr_val = (17 * (curr_val + ord(val))) % 256
	return(curr_val)

if __name__ == "__main__":
	start_time = time.time()
	print(f" Part 1 solution: {main(1)}")
	print("Part 1 finished --- %s seconds ---" % (time.time() - start_time))
	mid_time = time.time()
	print(f" Part 2 solution: {main(2)}")
	print("Part 2 finished --- %s seconds ---" % (time.time() - mid_time))
