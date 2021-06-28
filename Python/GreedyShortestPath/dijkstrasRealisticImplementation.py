import numpy as np
import networkx as nx
from matplotlib import pyplot as plt

def script():
    '''
    This is the script, which calls all of the function in the order to calculate and display the shortest courier paths.
    '''
    #Read the data, setup the network and split the rest homes into 4 groups
    auckland = read_network('network.graphml')
    rest_homes = get_rest_homes('rest_homes.txt')
    courierLocations = splitHomes(auckland,rest_homes)

    courierPath = [[],[],[],[]]
    distanceTravelled = [[],[],[],[]]
    order = [[],[],[],[]]

    #Loop over the different couriers and display the path when the route has been calculated
    for i in range(0,4):
        courierPath[i],distanceTravelled[i],order[i] = solvePath(auckland, courierLocations[i])
        plot_path(auckland, courierPath[i], save= False)

        #Uncomment the lines below to save the maps and order of the locations
        #plot_path(auckland, courierPath[i], save='Path_{:1d}.png'.format(i + 1))
        #np.savetxt('Path_{:1d}.txt'.format(i+1),order[i], delimiter = "", newline = "\n", fmt="%s")



def read_network(filename):
    """ Reads in a file to a nketowrkx.Graph object

    Parameters
    ----------
    filename : str
        Path to the file to read. File should be in graphml format

    Returns
    -------
    network : networkx.Graph
        representation of the file as a graph/network

    """

    network = nx.read_graphml(filename)
    # relabel all integer nodes if possible
    def relabeller(x):
        try:
            return int(x)
        except ValueError:
            return x
    nx.relabel_nodes(network, relabeller, copy=False)
    return network


def get_rest_homes(filename):
    """ Reads in the list of rest home names

    Parameters
    ----------
    filename : str
        Path to the file to read

    Returns
    -------
    rest_homes : list of strings
        list of all rest homes
    """

    rest_homes = []
    with open(filename, 'r') as fp:
        for line in fp:
            rest_homes.append(line.strip())
    return rest_homes

def plot_path(network, path, save=None):
    """ Plots a given path of the Auckland network

    Parameters
    ----------
    network : networkx.Graph
        The graph that contains the node and edge information
    path : list
        A list of node names
    save: str or None
        If a string is provided, then saves the figure to the path given by the string
        If None, then displays the figure to the screen
    """
    lats = [network.nodes[p]['lat'] for p in path]
    lngs = [network.nodes[p]['lng'] for p in path]
    plt.figure(figsize=(8,6))
    ext = [174.48866, 175.001869, -37.09336, -36.69258]
    plt.imshow(plt.imread("akl_zoom.png"), extent=ext)
    plt.plot(lngs, lats, 'r.-')
    if save:
        plt.savefig(save, dpi=300)
    else:
        plt.show()

def splitHomes(network,places):
    """
    Splits all of the locations into 4 different sectors based on their position

    inputs:
    -------

    network : networkx.Graph
              The graph that contains the node and edge information
    
    places: list
            A list of all the locations names

    returns:
    --------

    pathList: List
              A 1x4 list where each index contains all the locations within that quadrant.

    """

    #Establishes the airports longitude as a reference
    lngRef = network.nodes['Auckland Airport']['lng']
    courier1 = []
    courier2 = []
    courier3 = []
    courier4 = []

    #Loops over every location and assigns the location to a courier based on its latitude and longitude values
    for location in places:
        lat = network.nodes[location]['lat']
        lng = network.nodes[location]['lng']

        if(lng>lngRef):
            if(lat > -36.9):
                courier1.append(location)
            else:
                courier2.append(location)
        else:
            if(lat > -36.85):
                courier3.append(location)
            else:
                courier4.append(location)

    return [courier1,courier2,courier3,courier4]

def distance_from_origin(point):
    '''
    return the distance between the origin and a given point

    inputs:
    -------

    point: np.array
        Should only contain the coordinates

    Outputs:
    --------

    distance: float
            The distance between the two points
    '''

    return (point[0]**2 + point[1]**2)**(0.5)

def insertion_sort(A):
	''' Sort array A into ascending order using insertion sort.
		
		Parameters
		----------
		A : array
		    Array of values to be sorted in-place.
			
		Returns
		-------
		index : array
			An index table for A.
		
		Notes
		-----
		Index table for sort constructed by applying the same sort operations
		to INDS that are applied to A.
		
	'''

    #Generate the initial index array
	index = np.arange(0,len(A),1)

    #Loop over the length of the array
	for j in range (1, len(A)):
		key = A[j]
		i = j-1

        #Stop the loop only when the previous value is smaller than the current value or if we are at the zeroth index
		while i>-1:
			if not (A[i] > key):
				break
            #If the value is smaller than the one in the previous index, swap the values
			A[i+1] = A[i]
			i = i-1
			A[i+1] = key
            
            #Swap the corresponding index positions
			index[[i+2,i+1]] = index[[i+1,i+2]]
	

	return index

def solvePath(network,courierLocations):
    '''
    Applies the greedy algorithm to solve for the shortest route between the nearest location

    Inputs:
    -------
    network : networkx.Graph
              The graph that contains the node and edge information

    courierLocations: list
                      All of the locations that must be visited by the courier

    Outputs:
    --------
    path: list
          The specific route travelled, including all roads taken between the locations

    distanceTotal: np.array
                   The total distance travelled from the origin to the final location and then back to the origin

    courierPaths: list
                  The rest homes in the order that they are visited
    '''

    #Sets up the starting location as Auckland Airport
    distanceTotal = 0
    closestLocation = 'Auckland Airport'
    courierPaths = [closestLocation]
    distances = []
    path = []

    #Keeps looping until there are no more locations left to visit
    while(len(courierLocations) > 0):

        #Get the coordinates of the current location
        origin = np.array([float(network.nodes[closestLocation]['lat']),float(network.nodes[closestLocation]['lng'])])

        #Loop over every unvisited location and get the straight-line distance from the current location
        for location in courierLocations:
            
            #The straight-line distance from the current location to each unvisited location is recorded in an array
            coords = np.array([float(network.nodes[location]['lat']),float(network.nodes[location]['lng'])])
            distance = distance_from_origin(coords-origin)
            distances.append(distance)

        #Get the index table of the distances
        inds = insertion_sort(distances)    

        #Uses the index table to find the nearest location and move it from the unvisited to the visited list
        start = closestLocation
        closestLocation = courierLocations[inds[0]]
        courierLocations.remove(closestLocation)
        courierPaths.append(closestLocation)

        #Creates a single list of the exact path travelled from start to finish
        shortestPath = nx.shortest_path(network, start, closestLocation, weight = 'weight', method = 'dijkstra')
        path[len(path) - 1:len(path) + len(shortestPath) - 2] = shortestPath

        #Gets the shortest distance to the closest location and adds that to the distance already travelled.
        distance = nx.shortest_path_length(network, start, closestLocation, weight = 'weight', method = 'dijkstra')
        distanceTotal += distance

        #Clear out all of the recorded distances for the next loop
        distances = []

    #From the final location, the distance back to the starting point, as well as the path, is recorded
    distance = nx.shortest_path_length(network, courierPaths[len(courierPaths) - 1], 'Auckland Airport', weight = 'weight', method = 'dijkstra')
    shortestPath = nx.shortest_path(network, courierPaths[len(courierPaths) - 1], 'Auckland Airport', weight = 'weight', method = 'dijkstra')
    
    path[len(path) - 1:len(path) + len(shortestPath) - 2] = shortestPath
    courierPaths.append('Auckland Airport')
    distanceTotal += distance

    return path, distanceTotal, courierPaths

#Run the script
if __name__ == "__main__":
    script()