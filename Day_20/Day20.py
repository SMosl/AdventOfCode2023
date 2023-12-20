import os
import time

def main(part):
	
	types = {}
	flip_flops = {}
	con_mem = {}
	con_links = {}
	outputs = set()

	""" For the first example:
	broadcaster = {'a', 'b', 'c'}
	types = {
		'a' : 0,
		'b' : 0,
		'c' : 0,
		'inv' : 1
	}
	flip_flops = {
		'a' : {'b'},
		'b' : {'c'},
		'c' : {'inv'}
	}
	con_mem = {
		'inv' : {'c' : 0}
	}
	con_links = {
		'inv' : {'a'}
	}
	"""

	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		raw_input = f.read().splitlines()
		for line in raw_input:
			if line[0] == '%':
				line = line.split(' -> ')
				types[line[0][1:]] = ('ff', 0)
				flip_flops[line[0][1:]] = set()
				outputs = outputs.union(set(line[1].split(', ')))
				for output in line[1].split(', '):
					flip_flops[line[0][1:]].add(output)
			elif line[0] == '&':
				line = line.split(' -> ')
				types[line[0][1:]] = 'c'
				con_mem[line[0][1:]] = {}
				outputs = outputs.union(set(line[1].split(', ')))
				con_links[line[0][1:]] = set(x for x in line[1].split(', '))
			else:
				line = line.split(' -> ')[1].split(', ')
				outputs = outputs.union(set(line))
				broadcaster = set(x for x in line)
	
	for con in con_mem:
		for ff in flip_flops:
			if con in flip_flops[ff]:
				con_mem[con][ff] = 0

	# taking into account outputs
	for module in outputs:
		if module not in types:
			types[module] = 'o'

	if part == 1:
		i = 1000
	else:
		# run part 2 for an aribitrarily large amount of time in order to determine cycle length
		i = 100000

	pulses = []
	pulse_counts = [0, 0]
	button_presses = 0
	for _ in range(i):
		pulse_counts[0] = pulse_counts[0] + 1
		pulses.append(['button', 'broadcaster', 0])
		button_presses += 1
		while pulses:
			p = pulses.pop(0)
			if part == 2:
				if (p[0] == 'tr') and (p[2] == 1):
					print(button_presses, 'tr')
				elif (p[0] == 'xm') and (p[2] == 1):
					print(button_presses, 'xm')
				elif (p[0] == 'dr') and (p[2] == 1):
					print(button_presses, 'dr')
				elif (p[0] == 'nh') and (p[2] == 1):
					print(button_presses, 'nh')
				# find the cycle between each of the connectors to rx being 1
				# rx has 1 inputs, &dh
				# &dh has 4 inputs, {&tr, &xm, &dr, &nh}
				# for rx to receive a single low pulse,
				# dh must receive a high pulse from each of tr, xm, dr, nh
				# find the first time these output a high pulse and calculate the lcm of the 4 values
			if p[1] == 'broadcaster':
				new_pulses = [['broadcaster', x, 0] for x in broadcaster]
				pulses += new_pulses
				pulse_counts[0] = pulse_counts[0] + len(new_pulses)
			elif (types[p[1]][0] == 'ff') and (p[2] == 0):
				if types[p[1]][1] == 0:
					types[p[1]] = ('ff', 1)
					new_pulses = [[p[1], x, 1] for x in flip_flops[p[1]]]
					pulses += new_pulses
					pulse_counts[1] = pulse_counts[1] + len(new_pulses)
				elif types[p[1]][1] == 1:
					types[p[1]] = ('ff', 0)
					new_pulses = [[p[1], x, 0] for x in flip_flops[p[1]]]
					pulses += new_pulses
					pulse_counts[0] = pulse_counts[0] + len(new_pulses)
			elif types[p[1]][0] == 'c':
				con_mem[p[1]][p[0]] = p[2]
				v = [x for x in con_mem[p[1]].values()]
				if sum(v) == len(v):
					new_pulses = [[p[1], x, 0] for x in con_links[p[1]]]
					pulses += new_pulses
					pulse_counts[0] = pulse_counts[0] + len(new_pulses)
				else:
					new_pulses = [[p[1], x, 1] for x in con_links[p[1]]]
					pulses += new_pulses
					pulse_counts[1] = pulse_counts[1] + len(new_pulses)

	return(pulse_counts[0] * pulse_counts[1])

if __name__ == "__main__":
	start_time = time.time()
	print(f" Part 1 solution: {main(1)}")
	print("Part 1 finished --- %s seconds ---" % (time.time() - start_time))
	mid_time = time.time()
	print(f" Part 2 solution: {main(2)}")
	print("Part 2 finished --- %s seconds ---" % (time.time() - mid_time))
