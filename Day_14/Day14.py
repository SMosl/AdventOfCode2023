import os
import time
import numpy as np

def main(part):
	data = []
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		while(len(line := f.readline()) != 0):
			data.append(list(line.strip()))

	data = np.array(data)
	
	if part == 1:
		data = tilt(data, 0)
		return(sum(((len(data) - i) * val) for i, val in enumerate(list(np.count_nonzero(data == 'O', axis=1)))))
	else:
		cycled_solutions = [sum(((10 - i) * val) for i, val in enumerate(list(np.count_nonzero(data == 'O', axis=1))))]
		for _ in range(250):
			data = cycle(data)
			cycled_solutions.append(sum(((len(data) - i) * val) for i, val in enumerate(list(np.count_nonzero(data == 'O', axis=1)))))

		# Writing the loads into a file to then determine cycle length
		f2 = open(f"{dir_path}/solving.txt", "w")
		f2.write(', '.join(str(sol) for sol in cycled_solutions))
		f2.close()

		repeating_cycle = [89133, 89106, 89078, 89047, 89048, 89048, 89044, 89049, 89058, 89089, 89119, 89150, 89173, 89170, 89171, 89167, 89160]
		cycle_start = 151
		return(repeating_cycle[(1000000000 - cycle_start) % len(repeating_cycle)])



def cycle(data):
	data = tilt(data, 0)
	data = tilt(data, 3)
	data = tilt(data, 2)
	data = tilt(data, 1)
	return(data)

def tilt(data, N):
	data = np.rot90(data, N)
	for y, row in enumerate(data):
		for x, value in enumerate(row):
			if value == 'O':
				above = [[i, x, data[i, x]] for i in range(y)]
				moved_position = next(([u[0] + 1, u[1]] for u in above[::-1] if u[2] in {'O','#'}), [0,x])
				data[y, x] = '.'
				data[moved_position[0], moved_position[1]] = 'O'
	data = np.rot90(data, 4 - N)
	return data



if __name__ == "__main__":
	start_time = time.time()
	print(f" Part 1 solution: {main(1)}")
	print("Part 1 finished --- %s seconds ---" % (time.time() - start_time))
	mid_time = time.time()
	print(f" Part 2 solution: {main(2)}")
	print("Part 2 finished --- %s seconds ---" % (time.time() - mid_time))
