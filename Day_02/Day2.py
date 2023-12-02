import os
import time
import re

def main(part):

	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		output = [0,0]
		while(len(line := f.readline().strip()) != 0):
			ID = int(re.search(r'Game (\d+):', line).group(1))
			line_data = line.split(':')[1]

			blue = max([int(x) for x in re.findall(r'(\d+) blue', line_data)])
			red = max([int(x) for x in re.findall(r'(\d+) red', line_data)])
			green = max([int(x) for x in re.findall(r'(\d+) green', line_data)])

			if (red <= 12) & (green <= 13) & (blue <= 14):
				output[0] += ID

			output[1] += red * green * blue

	if part == 1:
		return output[0]
	else:
		return output[1]

if __name__ == "__main__":
	start_time = time.time()
	print(f" Part 1 solution: {main(1)}")
	print("Part 1 finished --- %s seconds ---" % (time.time() - start_time))
	mid_time = time.time()
	print(f" Part 2 solution: {main(2)}")
	print("Part 2 finished --- %s seconds ---" % (time.time() - mid_time))
