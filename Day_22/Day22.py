import os
import time
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

def main(part):

	dims = [set(), set(), set()]
	bricks = []
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		while(len(line := f.readline().strip()) != 0):
			brick = [list(map(int, x.split(','))) for x in line.split('~')]
			if brick[0][0] != brick[1][0]:
				bricks.append([(min(brick[0][0], brick[1][0]) + i, brick[0][1], brick[0][2]) for i in range(abs(brick[0][0] - brick[1][0]) + 1)])
			elif brick[0][1] != brick[1][1]:
				bricks.append([(brick[0][0], min(brick[0][1], brick[1][1]) + i, brick[0][2]) for i in range(abs(brick[0][1] - brick[1][1]) + 1)])
			elif brick[0][2] != brick[1][2]:
				bricks.append([(brick[0][0], brick[0][1], min(brick[0][2], brick[1][2]) + i) for i in range(abs(brick[0][2] - brick[1][2]) + 1)])
			else:
				bricks.append([(brick[0])])
	dims = (max(set(max(set(a[2] for a in b)) for b in bricks)) + 1, max(set(max(set(a[1] for a in b)) for b in bricks)) + 1, max(set(max(set(a[0] for a in b)) for b in bricks)) + 1)
	after_moves = np.zeros(dims)
	after_moves[0] = [[-1 * dims[1]] * dims[2]]

	supported_by = {} # in form of X : {Y, Z} which means X is being supported by Y and Z
	supporting = {}	# in form of X : {Y, Z} which means X is supporting Y and Z
	moved_bricks = []

	bricks.sort(key=lambda brick: min([brick[i][2] for i in range(len(brick))]))
	for i, brick in enumerate(bricks):
		new_z = 0
		for coord in brick:
			above = [[i, coord[1], coord[0], after_moves[i, coord[1], coord[0]]] for i in range(coord[2])]
			new_z = max((next(([u[0] + 1, u[1], u[2]] for u in above[::-1] if u[3] != 0), coord))[0], new_z)
		distance_moved = min(k[2] for k in brick) - new_z
		moved_brick = []
		for coord in brick:
			after_moves[coord[2] - distance_moved, coord[1], coord[0]] = i + 1
			moved_brick.append((coord[2] - distance_moved, coord[1], coord[0]))
		supported_by[i+1] = set(int(after_moves[new_z - 1, x[1], x[0]]) for x in brick if (after_moves[new_z - 1, x[1], x[0]] != 0))
		moved_bricks.append(moved_brick)
	
	for i, brick in enumerate(moved_bricks):
		max_z = max([x[0] for x in brick])
		supporting[i+1] = set(int(after_moves[max_z + 1, x[1], x[2]]) for x in brick if (after_moves[max_z + 1, x[1], x[2]] != 0))
	
	safely_removed = set()
	for b in supporting:
		if supporting[b] == set():
			safely_removed.add(b)
		if len([supported_by_b for supported_by_b in supporting[b] if (len(supported_by[supported_by_b]) > 1)]) == len(supporting[b]):
			safely_removed.add(b)


	if part == 1:
		return(len(safely_removed))
	else:
		G = nx.Graph()
		for brick_a in supporting.keys():
			for brick_b in supporting[brick_a]:
				G.add_edge(brick_a, brick_b)
		#nx.draw(G, with_labels=True)
		#plt.show()

		answer = 0
		for base_brick in supporting.keys():
			falling = set()
			new_falling = {base_brick}
			while len(new_falling) > len(falling):
				falling = falling.union(new_falling)
				for connected_block in supporting.keys():					
					if supported_by[connected_block].issubset(falling):
						new_falling.add(connected_block)
			answer += len(falling) - 1

		return(answer)

if __name__ == "__main__":
	start_time = time.time()
	print(f" Part 1 solution: {main(1)}")
	print("Part 1 finished --- %s seconds ---" % (time.time() - start_time))
	mid_time = time.time()
	print(f" Part 2 solution: {main(2)}")
	print("Part 2 finished --- %s seconds ---" % (time.time() - mid_time))
