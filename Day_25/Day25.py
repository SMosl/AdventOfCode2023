import os
import time
import matplotlib.pyplot as plt
import networkx as nx

def main():
	relations = {}
	components = set()
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		while(len(line := f.readline().strip()) != 0):
			head, tail = line.split(': ')
			components.add(head)
			relations[head] = set()
			for c in tail.split(' '):
				relations[head].add(c)
				components.add(c)
	
	G = nx.Graph()
	for node_a in relations.keys():
		for node_b in relations[node_a]:
			G.add_edge(node_a, node_b)
		
	#nx.draw(G, with_labels=True)
	#plt.show()

	G.remove_edge('sgc', 'xvk')
	G.remove_edge('cvx', 'dph')
	G.remove_edge('pzc', 'vps')

	#nx.draw(G, with_labels=True)
	#plt.show()

	sizes = []
	for disconnected_graph in list(nx.connected_components(G)):
		print(len(disconnected_graph))
		sizes.append(len(disconnected_graph))
	return(sizes[0] * sizes[1])

if __name__ == "__main__":
	start_time = time.time()
	print(f" Part 1 solution: {main(1)}")
	print("Part 1 finished --- %s seconds ---" % (time.time() - start_time))
