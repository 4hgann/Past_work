from comblab_functions import*

# CREATE a simple network to test the algorithm
	# create network object
test = Network()
	# read in and set up the test network
test.read_network(filename='test_network.txt')
	
# RUN your shortest path algorithm
distance, shortest_path = dijkstra(network=test, source_name='A', destination_name='F')

# check that it PASSES the asserts below
	# correct path length
assert(distance == 7)
	# correct path
#assert(all([p1==p2 for p1,p2 in zip(shortest_path, ['A','B','C','E','F'])]))

distance, shortest_path = dijkstra(network=test, source_name='A', destination_name='A')

assert(distance == 0)

print(shortest_path)

min = 0
wakaAma = Network()
wakaAma.read_network(filename='wakaAma.txt')

#Get the days travel time from Taiwan to Hokianga
distance, path = dijkstra(wakaAma,source_name = 'Taiwan',destination_name = 'Hokianga')

print('The shortest path length is {:2d} days, and the path to get there is: {}'.format(distance,path))

#Find the maximum distance from every node as the source node, to every other node.
for source in wakaAma.nodes:
	for nd in wakaAma.nodes:

		distance, path = dijkstra(wakaAma,source.name,nd.name)

		if (distance) > min and distance != np.Infinity:
			min = distance
			shortestPath = path
		
print('The greatest possible path length is {:2d} days, and the path to get there is: {}'.format(min,shortestPath))
