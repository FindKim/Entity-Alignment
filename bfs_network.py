#!/usr/bin/env python

# bfs_network.py
#
# Kim Ngo
# June 28, 2015
# 
# Finds connected nodes with given seeds using breadth first search
# ** ID NEEDS TO BE CHANGED TO TWITTER_ID OR INSTAGRAM_ID DEPENDING ON DATA **
#
# usage: ./bfs_network.py [seed file] [edges file] [output file]
#

from pythonds.graphs import Graph, Vertex
from pythonds.basic import Queue
from progressbar import ProgressBar, Percentage, Bar
import sys
import os
import subprocess

SOURCE, TARGET = range(2)
TWITTER_NAME, TWITTER_ID, INSTAGRAM_NAME, INSTAGRAM_ID = range(4)
ID = TWITTER_ID


def parseSeedsFile(filename):
	""" Parses file of seeds and creates dictionary with seeds as key
	Args:
		filename (str): input file name of seed file
	Returns:
		dictionary (int(keys), []): source node with a list target nodes
	"""  
	seeds = []
	with open(filename, 'r') as f:
		for line in f:
			line = line.strip()
			line = line.split(',')
			seeds.append(int(line[ID]))
	return seeds


def buildGraph(filename):
	""" Parses edge file and builds graph
	Args:
		filename (str): input file name of edges file -- "source_id target_id"
	Returns:
		graph: edges (int(source), int(target))
	"""
	g = Graph()
	widgets = ['Building graph: ', Percentage(), ' ', Bar()]
	output = subprocess.check_output(["wc", "-l", filename]).split(' ')
	num_lines = int(output[0])
	pbar = ProgressBar(widgets=widgets, maxval=num_lines).start()
	with open(filename, 'r') as f:
		for i in range(num_lines):
			line = f.readline()
			line = line.strip()
			line = line.split(" ")
			g.addEdge(int(line[SOURCE]), int(line[TARGET]))
			pbar.update(i+1)
		pbar.finish()
	return g

def bfs(seed, graph):
	""" Finds connected nodes to seeds with given graph
	Args:
		seed (Vertex): vertex with seed ID
		graph (Graph): contains edges from source node to target node
	Returns:
		list(str(seed ID)): list of connected seeds
	"""
	seed.setDistance(0)
	seed.setPred(None)
	vertQueue = Queue()
	vertQueue.enqueue(seed)
	connected_nodes = []
	while (vertQueue.size() > 0):
		currentVert = vertQueue.dequeue()
		for nbr in currentVert.getConnections():
			if (nbr.getColor() == 'white'):
				nbr.setColor('gray')
				nbr.setDistance(currentVert.getDistance()+1)
				nbr.setPred(currentVert)
				vertQueue.enqueue(nbr)
				connected_nodes.append(nbr.getId())
		currentVert.setColor('black')
	return connected_nodes

def add_nodes_to_network(seeds, connected_nodes, filename):
	""" Writes list of known nodes in network to output file
	Args:
		seeds (list(int(ID))): list of given seeds
		connected_nodes (list(str(ID))): list of known nodes connected to seeds
		filename (str): name of output file that contains connected_nodes
	Returns:
	"""
	num_nodes = len(connected_nodes) + len(seeds)
	widgets = ['Writing to '+filename+": ", Percentage(), ' ', Bar()]
	pbar = ProgressBar(widgets=widgets, maxval=num_nodes).start()
	with open(filename, 'a') as f:
		for i,id in enumerate(seeds):
			f.write(str(id))
			f.write('\n')
			pbar.update(i+1)
		for j,id in enumerate(connected_nodes):
			f.write(str(id))
			f.write('\n')
			pbar.update(i+j+1)
		pbar.finish()
	return

def processSeeds(seeds, graph):
	""" For each seed, collect list of connected nodes
	Args:
		seeds (list(int(ID))): list of given seeds
		graph (Graph(int(sourceID), int(targetID))): list of edges that make up graph
	Returns:
		list(int(ID)): list of unique nodes connected to seeds
	"""
	unique_nodes = set()
	num_seeds = len(seeds)
	widgets = ['Processing seeds: ', Percentage(), ' ', Bar()]
	pbar = ProgressBar(widgets=widgets, maxval=num_seeds).start()
	for i in range(num_seeds):
		seed = graph.getVertex(seeds[i])
		if seed != None:
			nodes = bfs(seed, graph)
			if len(nodes) > 0:
				for node in nodes:
					unique_nodes.add(node)
		pbar.update(i+1)
	pbar.finish()
	return unique_nodes

def main():
	if len(sys.argv) < 4:
		print "usage:", sys.argv[0], "[seed file] [edge file] [output file]"
		sys.exit(0)


	seed_file = sys.argv[1]
	edge_file = sys.argv[2]
	output_file = sys.argv[3]
	if not os.path.isfile(seed_file):
		print "Cannot open", seed_file
		sys.exit(0)
	elif not os.path.isfile(edge_file):
		print "Cannot open", edge_file
		sys.exit(0)

	if os.path.isfile(output_file):
		print output_file, "already exists"
		sys.exit(0)
	else:
		cmd = 'touch ' + output_file
		os.system(cmd)

	seeds = parseSeedsFile(seed_file)
	graph = buildGraph(edge_file)
	unique_nodes = processSeeds(seeds, graph)
	add_nodes_to_network(seeds, unique_nodes, output_file)

if __name__ == "__main__":
	main()
