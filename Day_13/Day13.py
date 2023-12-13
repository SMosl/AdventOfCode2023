import os
import time
import copy

def main1():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		raw_input = f.read().split('\n\n')

	patterns_r = []
	patterns_c = []
	for pattern in raw_input:
		patterns_r.append([x for x in pattern.splitlines()])
		patterns_c.append([''.join([x[i] for x in pattern.splitlines()]) for i in range(len(pattern.splitlines()[0]))])
	
	solutions = [[],[]]
	for i, pattern in enumerate(patterns_c):
		c_reflective_i = find_reflective_i(pattern, -1, (-1,-1))
		if c_reflective_i:
			solutions[0].append(c_reflective_i)
		else:
			r_reflective_i = find_reflective_i(patterns_r[i], -1, (-1,-1))
			if r_reflective_i:
				solutions[1].append(r_reflective_i)
	
	return(sum(solutions[0]) + (100*sum(solutions[1])))



def main2():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		raw_input = f.read().split('\n\n')

	patterns = [[x for x in pattern.splitlines()] for pattern in raw_input]
	
	solutions = [[],[]]
	for pattern in patterns:
		c_reflective_i = find_reflective_i(pattern, -1, (-1,-1))
		if c_reflective_i:
			original_r_line = (c_reflective_i, 1)
		else:
			original_transposed = [''.join([x[i] for x in pattern]) for i in range(len(pattern[0]))]
			r_reflective_i = find_reflective_i(original_transposed, -1, (-1,-1))
			if r_reflective_i:
				original_r_line = (r_reflective_i, 0)

		fixed = fix_smudge(pattern, original_r_line)
		solutions[fixed[1]].append(fixed[0])

	return(sum(solutions[0]) + (100*sum(solutions[1])))



def fix_smudge(pattern, original_r_line):
	for r in range(len(pattern)):
		for c in range(len(pattern[0])):
			smudge_corrected = copy.deepcopy(pattern)
			val = smudge_corrected[r][c]
			if val == '.':
				smudge_corrected[r] = smudge_corrected[r][:c] + '#' + smudge_corrected[r][c+1:]
			else:
				smudge_corrected[r] = smudge_corrected[r][:c] + '.' + smudge_corrected[r][c+1:]
	
			c_reflective_i = find_reflective_i(smudge_corrected, 1, original_r_line)
			if c_reflective_i:
				return(c_reflective_i, 1)

			smudge_transposed = [''.join([x[i] for x in smudge_corrected]) for i in range(len(smudge_corrected[0]))]
			r_reflective_i = find_reflective_i(smudge_transposed, 0, original_r_line)
			if r_reflective_i:
				return(r_reflective_i, 0)



def find_reflective_i(pattern, orientation, original_sol):
	# orientation and original_sol are needed to ensure part 2 doesn't return the same line of reflection for a pattern as part 1
	c_counts = [pattern.index(x) for x in pattern]
	potential_reflections = [i for i in range(len(pattern) - 1) if [pattern.index(x) for x in pattern][i] == [pattern.index(x) for x in pattern][i+1]]
	for i in potential_reflections:
		after = [x for x in c_counts[i+1:]]
		before = [x for x in c_counts[:i+1]]
		if len(after) > len(before):
			if before[::-1] == after[:len(before)]:
				if ((i + 1) != original_sol[0]) or (orientation != original_sol[1]):
					return i + 1
		else:
			before = before[::-1]
			if after == before[:len(after)]:
				if ((i + 1) != original_sol[0]) or (orientation != original_sol[1]):
					return i + 1
	return False


if __name__ == "__main__":
	start_time = time.time()
	print(f" Part 1 solution: {main1()}")
	print("Part 1 finished --- %s seconds ---" % (time.time() - start_time))
	mid_time = time.time()
	print(f" Part 2 solution: {main2()}")
	print("Part 2 finished --- %s seconds ---" % (time.time() - mid_time))
