import os
import time
from functools import cache

def main_part_1():
	data = []
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		while(len(line := f.readline()) != 0):
			data.append([line.strip().split(' ')[0], [int(x) for x in line.strip().split(' ')[1].split(',')]])

	answer = 0
	for d in data:
		str = d[0]
		pattern = d[1]
		
		min_case = sum(pattern) + len(pattern) - 1
		additional_dots = len(str) - min_case
		
		for index in range(len(pattern) - 1, 0, -1):
			pattern[index:index] = [0]
		
		full_solutions = [pattern]
		while additional_dots > 0:
			new_solutions = []
			for p in full_solutions:
				new_solutions += [p[:i] + [0] + p[i:] for i in range(len(p)) if p[i] != 0]
				new_solutions.append(p + [0])
			additional_dots += -1
			full_solutions = new_solutions

		new_strings = set()
		for solution in full_solutions:
			new_solution = ''
			for c in solution:
				if c == 0:
					new_solution += '.'
				else:
					new_solution += '#' * c
			new_strings.add(new_solution)

		q_indexes = [x for x in range(len(str)) if str[x] == '?']

		for s in new_strings:
			new_s = ''
			for i in range(len(s)):
				if i in q_indexes:
					new_s += '?'
				else:
					new_s += s[i]
			if new_s == str:
				answer += 1
	return(answer)


def main_part_2():
	data = []
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		while(len(line := f.readline()) != 0):
			data.append([line.strip().split(' ')[0], tuple(int(x) for x in line.strip().split(' ')[1].split(','))])

	answer = 0
	for record, groups in data:
		record = record + '?' + record + '?' + record + '?' + record + '?' + record
		groups = groups * 5
		new_answer = find_arrangement(record, groups)
		answer += new_answer

	return answer

@cache
def find_arrangement(record, groups):
	if len(record) < (sum([x for x in groups]) + len(groups) - 1):
		return 0
	
	if len(record) == 0:
		if len(groups) > 0:
			return 0
		else:
			return 1
	
	if len(groups) == 0:
		if '#' in set(record):
			return 0
		else:
			return 1

	answer = 0
	if record[0] == '.':
		answer += find_arrangement(record[1:], groups)
	
	if record[0] == '?':
		answer += find_arrangement(record[1:], groups)
		answer += find_arrangement('#' + record[1:], groups)

	if record[0] == '#':
		if len(record) >= groups[0]:
			if set(x for x in record[:groups[0]]).issubset({'#', '?'}):
				if len(record) == groups[0]:
					return 1
				elif record[groups[0]] == '#':
					return 0
				else:
					answer += find_arrangement('.' + record[groups[0] + 1:], groups[1:])
		else:
			return 0

	return answer


if __name__ == "__main__":
	start_time = time.time()
	print(f" Part 1 solution: {main_part_1()}")
	print("Part 1 finished --- %s seconds ---" % (time.time() - start_time))
	mid_time = time.time()
	print(f" Part 2 solution: {main_part_2()}")
	print("Part 2 finished --- %s seconds ---" % (time.time() - mid_time))
