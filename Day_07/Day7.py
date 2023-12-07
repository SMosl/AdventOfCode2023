import os
import time
from collections import Counter
import itertools

def main(part):
	values = []
	conversion = {
		'A' : 'A',
		'K' : 'B',
		'Q' : 'C',
		'J' : 'D',
		'T' : 'E',
		'9' : 'F',
		'8' : 'G',
		'7' : 'H',
		'6' : 'I',
		'5' : 'L',
		'4' : 'M',
		'3' : 'N',
		'2' : 'O'
	}

	if part == 2:
		conversion['J'] = 'P'	# J is the new lowest valued card

	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		while(len(line := f.readline()) != 0):
			easier_to_sort = line.split()[0]
			for x in easier_to_sort:
				easier_to_sort = easier_to_sort.replace(x, conversion[x])
			values.append([easier_to_sort, int(line.split()[1].strip())])

	sorted_by_type = [[] for _ in range(7)]
	for i, hand in enumerate(values):
		num_jokers = hand[0].count('P')
		counts = Counter(hand[0]).most_common()
		if num_jokers == 5:
			sorted_by_type[0].append(values[i])
		else:
			counts = [x for x in counts if x[0] != 'P']
			counts[0] = (counts[0][0], counts[0][1] + num_jokers)
			if counts[0][1] == 5:
				sorted_by_type[0].append(values[i])
			elif counts[0][1] == 4:
				sorted_by_type[1].append(values[i])
			elif (counts[0][1] == 3) & (counts[1][1] == 2):
				sorted_by_type[2].append(values[i])
			elif counts[0][1] == 3:
				sorted_by_type[3].append(values[i])
			elif (counts[0][1] == 2) & (counts[1][1] == 2):
				sorted_by_type[4].append(values[i])
			elif counts[0][1] == 2:
				sorted_by_type[5].append(values[i])
			else:
				sorted_by_type[6].append(values[i])

	# Sort the hands of each type alphabetically
	for type in sorted_by_type:
		type.sort(key=lambda x: x[0])
	# Expand the list of hands into a singl fully ordered list to then sum 
	sorted_hands = list(itertools.chain.from_iterable(sorted_by_type))

	return(sum((x[1] * (i + 1)) for i, x in enumerate(reversed(sorted_hands))))

if __name__ == "__main__":
	start_time = time.time()
	print(f" Part 1 solution: {main(1)}")
	print("Part 1 finished --- %s seconds ---" % (time.time() - start_time))
	mid_time = time.time()
	print(f" Part 2 solution: {main(2)}")
	print("Part 2 finished --- %s seconds ---" % (time.time() - mid_time))
