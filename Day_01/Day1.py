import os
import time

def main(part):
	conversion = {
		'one' : '1',
		'two' : '2',
		'three' : '3',
		'four' : '4',
		'five' : '5',
		'six' : '6',
		'seven' : '7',
		'eight' : '8',
		'nine' : '9'
	}

	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		sum = 0
		while(len(line := f.readline()) != 0):
			values = []
			for i, x in enumerate(line):
				if x.isdigit():
					values.append(x)
				elif part == 2:
					for word in conversion:
						if line[i:].startswith(word):
							values.append(conversion[word])
			if values:
				sum += int(values[0] + values[-1])
	return sum

if __name__ == "__main__":
	start_time = time.time()
	print(f" Part 1 solution: {main(1)}")
	print("Part 1 finished --- %s seconds ---" % (time.time() - start_time))
	mid_time = time.time()
	print(f" Part 2 solution: {main(2)}")
	print("Part 2 finished --- %s seconds ---" % (time.time() - mid_time))
