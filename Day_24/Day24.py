import os
import time
import sympy
from sympy.abc import x, y, z, a, b, c, r, s, t

def main(part):
	data = []
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		while(len(line := f.readline().strip()) != 0):
			data.append(tuple(int(x) for x in line.replace(' @', ',').split(', ')))

	if part == 1:
		successful_intersections = []
		for _ in range(len(data)):
			pxa, pya, pza, vxa, vya, vza = data.pop(0)
			for hail_b in data:
				pxb, pyb, pzb, vxb, vyb, vzb = hail_b
				p = find_intersection_point(pxa, pya, vxa, vya, pxb, pyb, vxb, vyb)
				if p and (200000000000000 <= p[0] <= 400000000000000) and (200000000000000 <= p[1] <= 400000000000000):
					successful_intersections.append(p)
		return(len(successful_intersections))
	else:
		answer = find_intersection_line(data)
		return(answer)


def find_intersection_line(data):
	pxa, pya, pza, vxa, vya, vza = data[0]
	pxb, pyb, pzb, vxb, vyb, vzb = data[1]
	pxc, pyc, pzc, vxc, vyc, vzc = data[2]
	# we want P(hail) + V(hail) * t = P(stone) + V(stone) * t for each of three hailstones
	# so variables we need to find are the 3 stone positions, the 3 stone velocities, and the 3 time values where the stone collides with each hailstone
	solutions = sympy.solve([pxa - x + (vxa - a) * t, pya - y + (vya - b) * t, pza - z + (vza - c) * t,
			pxb - x + (vxb - a) * s, pyb - y + (vyb - b) * s, pzb - z + (vzb - c) * s,
			pxc - x + (vxc - a) * r, pyc - y + (vyc - b) * r, pzc - z + (vzc - c) * r], [x, y, z, a, b, c, r, s, t], dict=True)
	return(solutions[0][x] + solutions[0][y] + solutions[0][z])

def find_intersection_point(pxa, pya, vxa, vya, pxb, pyb, vxb, vyb):
	ma = vya / vxa
	ca = pya - (ma * pxa)
	mb = vyb / vxb
	cb = pyb - (mb * pxb)

	if ma == mb:
		return None
	else:
		x_intersection = (cb - ca)/(ma - mb)
		y_intersection = (ma * x_intersection) + ca
		a_time_of_intersection = (x_intersection - pxa) / vxa
		b_time_of_intersection = (x_intersection - pxb) / vxb
		if (a_time_of_intersection < 0) or (b_time_of_intersection < 0):
			return None
		else:
			return((x_intersection, y_intersection))


if __name__ == "__main__":
	start_time = time.time()
	print(f" Part 1 solution: {main(1)}")
	print("Part 1 finished --- %s seconds ---" % (time.time() - start_time))
	mid_time = time.time()
	print(f" Part 2 solution: {main(2)}")
	print("Part 2 finished --- %s seconds ---" % (time.time() - mid_time))
