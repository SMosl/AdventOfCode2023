import os
import time
import re

def main(part):
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		lines = f.read().splitlines()

	total = 0
	num_cards = [1 for _ in range(len(lines))]
	for card_number, line in enumerate(lines):
		line = (line.split(':')[1]).split('|')
		values = [set(re.findall(r'\d+',line[x])) for x in (0,1)]
		my_winning_numbers = set.intersection(values[0], values[1])

		if part == 1:
			if (score := pow(2, len(my_winning_numbers) - 1)) >= 1:
				total += score
		else:
			for x in range(len(my_winning_numbers)):
				num_cards[card_number + x + 1] = num_cards[card_number + x + 1] + num_cards[card_number]

	if part == 1:
		return total
	else:
		return (sum(num_cards))

if __name__ == "__main__":
	start_time = time.time()
	print(f" Part 1 solution: {main(1)}")
	print("Part 1 finished --- %s seconds ---" % (time.time() - start_time))
	mid_time = time.time()
	print(f" Part 2 solution: {main(2)}")
	print("Part 2 finished --- %s seconds ---" % (time.time() - mid_time))
