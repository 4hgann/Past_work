#imports
import numpy as np
import pandas as pd
import folium
from sklearn.cluster import KMeans
import itertools as it
import os
from pulp import *
from matplotlib import pyplot as plt
import openrouteservice as ors

#-- DATA GENERATION -----------------------------------------------------------------------
def generate_data():
    ''' 
    Generate all store, demand, distance, duration, and location data.

    Parameters:
    -----------
    -
    Returns:
    --------
    demand_data_A : array-like
        Average demand data for all stores (NL & TW).
    demand_data_M : array-like
        Maximum demand data for all stores (NL & TW).
    demands : array-like
        Dataframe of daily store demand
    distances : array-like
        Dataframe of every distance combination.
    durations : array-like
        Dataframe of every duration combination.
    '''
    #sets the data imports to be global variables for easier data accessibility.
    global demand_data_A, demand_data_M, demands, distances, durations, locations
    

    #Demand Data
    #demand_data_A = pd.read_csv('Data' + os.sep + 'DOW_Demand_Averages.csv',header=0)
    demand_data_A = pd.read_csv('Data' + os.sep + 'weekday_weekend_averages.csv',header=0)
    demand_data_M = pd.read_csv('Data' + os.sep + 'weekday_weekend_maximums.csv',header=0)
    demands = pd.read_csv('Data' + os.sep + 'demandDataUpdated.csv', header = 0, index_col=0)

    #Warehouse Distance Matrix
    distances = pd.read_csv('Data' + os.sep + 'WarehouseDistances.csv',header=0,index_col=0)

    #Warehouse Duration Matrix
    durations = pd.read_csv('Data' + os.sep + 'WarehouseDurations.csv',header=0,index_col=0)

    #Warehouse Location Dataframe
    locations = pd.read_csv('Data' + os.sep + 'WarehouseLocations.csv')
    
    return demand_data_A, demand_data_M, demands, distances, durations, locations

def sample_demand(nsamples):
    '''
    Generate a random demand sample for the weekday or weekend (whichever specified)

    Parameters:
    -----------
    nsamples: integer
        number of times data is bootstrapped.
    Returns:
    ------------
    store_sample: list
        List with a demand value for every store
    
    '''
    global weekday_boot, weekend_boot

    #collect the demand for each weekday
    weekday_data = np.zeros([demands.values.shape[0], 20]) #make a 40 x 20 array (40 stores, 20 weekdays in 28 days)
    for i in range(demands.values.shape[0]):
        count = 0
        for j in range(demands.values.shape[1]):
            #pick the demand value if it is the 1st - 5th dow (mon - fri)
            if(j % 7 != 5 and j % 7 != 6):
                weekday_data[i][count] = demands.values[i][j] 
                count += 1

    #collect the demand for each weekend/saturday
    weekend_data = np.zeros([demands.values.shape[0], 4]) #make a 40 x 4 array (40 stores, 4 weekend days in 28 days (no Sundays))
    for i in range(demands.values.shape[0]):
        count = 0
        for j in range(demands.values.shape[1]):
            #pick the demand value if it is the 6th dow (saturday)
            if(j % 7 == 5):
                weekend_data[i][count] = demands.values[i][j] 
                count += 1

    #bootstrap the data
    weekday_boot = np.zeros([demands.values.shape[0], nsamples])
    weekend_boot = np.zeros([demands.values.shape[0], nsamples])
    for i in range(demands.values.shape[0]):
        for j in range(nsamples):
            weekday_boot[i,j] = np.random.choice(weekday_data[i,:], replace = True)
            weekend_boot[i,j] = np.random.choice(weekend_data[i,:], replace = True)

    return weekday_boot, weekend_boot

#-- MAP GENERATION ------------------------------------------------------------------------
def generate_map(day):
    '''
    Generate a map with plots of average demand for each store for each days of the week.

    Parameters:
    -----------
    day : String
        Days of the week

    Returns:
    --------
    None
    '''

    # Import a map of Auckland
    m = folium.Map(location=[-36.906636, 174.787650], tiles="Stamen Terrain", zoom_start=11)
    merged = locations.merge(demand_data_A, left_on='Store', right_on='Name')
    
    # Adding markers on the map
    for i in range(0,len(locations['Long'])):
        # For distribution centres
        if (locations['Type'][i] == 'Distribution'):
            folium.Circle(
            location=[locations['Lat'][i], locations['Long'][i]], # Store location
            popup= locations['Store'][i], # Store name
            radius = 300,
            color='black',
            fill=True,
            ).add_to(m)

    # Adding markers on the map
    for i in range(0,len(merged['Long'])):
        # For The Warehouse
        if (merged['Type'][i] == 'The Warehouse'):
            folium.Circle(
            location=[merged['Lat'][i], merged['Long'][i]], # Store location
            popup= merged['Store'][i], # Store name
            radius = merged [day][i] * 100, # Need to modify
            color='red',
            fill=True,
            ).add_to(m)

        elif (merged['Type'][i] == 'Noel Leeming'):
            folium.Circle(
            location=[merged['Lat'][i], merged['Long'][i]], # Store location
            popup = merged['Store'][i], # Store name
            radius = merged [day][i] * 100, # Need to modify
            color='blue',
            fill=True,
            ).add_to(m)

    # Save it as html
    m.save('General_Maps' + os.sep + day + '_demand_map.html')

def generate_cluster_map(n):
    '''
    Generate a map of n clustered stores for a given group of stores

    Parameters:
    -----------
    n : Integer
        number of clusters 
    Returns:
    --------
    None
    '''
    colours = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']
    # Import a map of Auckland
    m = folium.Map(location=[-36.906636, 174.787650], tiles="Stamen Terrain", zoom_start=11)
    
    #Adding markers on the map
    #Distribution Centers
    for i in range(2):
        folium.Marker(
        location = [locations['Lat'][i], locations['Long'][i]], 
        popup = locations['Store'][i], 
        icon=folium.Icon(color='black')
        ).add_to(m)

    #Stores
    for cluster in range(0,n):
        #Filter for the given cluster
        is_cluster = locations['cluster'] == cluster
        temp = locations[is_cluster].reset_index()

        for i in range(0,len(temp['Long'])):
            folium.Marker(
            location = [temp['Lat'][i], temp['Long'][i]], # Store location
            popup = temp['Store'][i], # Store name
            icon=folium.Icon(color=colours[cluster])
            ).add_to(m)

    # Save it as html
    m.save('General_Maps' + os.sep + 'Clusters.html')

#-- MISC FUNCTIONS ------------------------------------------------------------------------
def location_clustering(n, closed):
    '''
    Cluster locations using their longitude and latitude in a kmeans algorithm. 
    Then find the closest distribution centre using the average travel time to the cluster.

    Parameters:
    -----------
    n : Integer
        number of clusters 
    closed : Boolean
        True, if the North Distribution is closed
        False, otherwise
    Returns:
    --------
    '''
    #collect the long and lat values for each store
    Long_Lat = np.array(locations[['Long','Lat']])[2:,:]
    
    #use kmeans clustering to find an appropriate cluster for each store
    clusters = KMeans(n_clusters = n, init = 'k-means++', n_init = 20).fit(Long_Lat)

    #add new column to the locations dataframe
    distribution_clusters = [np.nan,np.nan]
    locations['cluster'] = np.concatenate((distribution_clusters,clusters.labels_))
    #print(locations.head(20))
    
    # Find the nearest distribution center to each cluster
    global cluster_source

    # If 'Distribution North' is closed
    if (closed == True):
        cluster_source = ['Distribution South'] * len(locations)
        return cluster_source

    cluster_source = []
    store_source = []
    for cluster in range(0,n):
        #filter locations for a specific cluster
        is_cluster = locations['cluster'] == cluster
        temp = locations[is_cluster].reset_index()

        #reset variables
        averages = np.zeros(2)
        times = np.zeros(len(temp['cluster']))

        #find the average time from each cluster to each distribution center
        distribution = ['Distribution South','Distribution North']
        stores = np.array(temp['Store'])
        for i in range(len(distribution)):
            for j in range(0,len(temp['Store'])):
                times[j] = durations[distribution[i]][stores[j]]
            averages[i] = np.mean(times)
        
        #record the closest distribution center to a cluster
        cluster_source.append(distribution[np.argmin(averages)])

    #create array of distribution centers for each store in the location df.
    for i in range(0,len(locations['Store'])-2):
        store_source.append(cluster_source[int(np.array(locations['cluster'])[i+2])])

    #add new column to the locations dataframe
    locations['nearest_distribution'] = np.concatenate((distribution_clusters,store_source))
    #print(locations.head(50))
    
    return cluster_source

def feasible_stores(day):
    '''
    Determine all the possible combinations of the stores to help with route generation later. This occurs in layers
    Parameters:
    -----------
    day : string
        Day of the week 
    Returns:
    --------
    combinations: List
        A list of all possible combinations of the stores in all clusters
    '''
    clusters = locations['cluster'].unique()
    
    clusters.sort()
    clusters = np.delete(clusters, len(clusters)-1)
    combinations = []

    for i in clusters:
        array = []
        all_combinations = []
        filtered = []
        
        # Identify stores in each cluster
        for j in range (len(demand_data_M)):
            if (locations['cluster'][j+2] == i and demand_data_M[day][j] != 0):
                #if demand for a day is 0, don't add that node to the array
                array.append(locations['Store'][j+2])

        # Find all combinations of feasible stores
        for k in range(1,len(array) + 1):
            # Will generate all possible combinations with k elements in the combination and add these
            # As a list to all the possible combinations
            combinations_object = it.combinations(array, k)
            combinations_list = list(combinations_object)
            all_combinations+=combinations_list


        # Filter the combinations to meet constraints
        for node_list in all_combinations:
            #The demand for the routes must be less than 20 due to truck capacity
            if (find_route_demand(node_list, day, np.nan) <= 20):
                filtered.append(node_list)
  
        combinations.append(filtered)
    return combinations

def find_route_distance(node_list, day, iteration):
    '''
    Based on the name of locations provided, find the total distance travelled between all the locations
    -----------
    node_list : List
        Name of locations in that route 
    Returns:
    --------
    total_distance: Float
        The total distance travelled between all locations
    '''

    total_distance = 0.
    #Find the distance travelled between each node and the one after it, until you reach the last node
    for i in range(len(node_list)-1):
        #Sum the distance travelled
        total_distance += durations[node_list[i]][node_list[i+1]]/3600

    total_distance += find_route_demand(node_list, day, iteration) * (10/60)  #10 mins unload time at each store

    return total_distance

def find_route_demand(node_list,day,iteration):
    '''
    Base on the name of locations provided and the day, find the total demand requested from all the relevant locations
    -----------
    node_list : List
        The names of the locations in that route
    day: string
        The name of the day 
    Returns:
    --------
    total_distance: Float
        The total distance travelled between all locations
    '''
    #find the initial route set
    if np.isnan(iteration):
        total_demand = 0.
        for i in range (0, len(node_list)):
            for j in range (0, len(demand_data_M)):
                #Finds the location that matches the current location and adds the demand found on that day to a counter
                if (demand_data_M['Name'][j] == node_list[i]):
                    total_demand += demand_data_M[day][j]
    else:
        #decide which demand dataset to use
        if day == "Weekday":
            demand_used = weekday_boot
        else:
            demand_used = weekend_boot

        total_demand = 0.
        for i in range (0, len(node_list)):
            for j in range (0, len(demand_used)):
                #Finds the location that matches the current location and adds the demand found on that day to a counter
                if (demand_data_M['Name'][j] == node_list[i]):
                    total_demand += demand_used[j][iteration]

    return total_demand

def cheapest_insertion(source, node_list, day):
    '''
    Implements the cheapest insertion method to find a near-optimal route between a list of nodes

    Parameters
    -----------
    source: string
        The distribution node
    node_list : array-like
        Array of strings of possible route combinations
    durations: array-like
        Contains time length between nodes

    Returns:
    --------
    route_list: List
    '''
    
    route_list = [source, source]

    while(len(node_list) != 0):
        min_distance = np.inf

        #Find the cheapest insertion for any node in any position
        for node in node_list:
            
            #Based on all the places that a node could be inserted, check which has the cheapest insertion cost
            for i in range(1,len(route_list)):
                temp = route_list.copy()
                temp.insert(i, node)
                total_distance = find_route_distance(temp, day, np.nan)
                #If a cheaper node is found, record the cost, the current route and the current cheapest node
                if(total_distance < min_distance):
                    min_list = temp
                    min_node = node
                    min_distance = total_distance
        
        #Update the route_list and remove the minimum node from the nodes that we can now add to the network
        route_list = min_list.copy()
        node_list.pop(node_list.index(min_node))

    return route_list

def best_routes(all_combinations, day):
    '''
    Iterates over all the combinations of locations we have to implement the cheapest insertion method on each of them

    Parameters
    -----------
    source: string
        The distribution node
    node_list : array-like
        Array of strings of possible route combinations
    durations: array-like
        Contains time length between nodes

    Returns:
    --------
    route_list: List
    '''

    # Uses cheapest insertion to determine the best routes
    best_routes_list = []
    for i in range(len(all_combinations)):
        temp = []
        for j in range(len(all_combinations[i])):
            route_list = cheapest_insertion(cluster_source[i], list(all_combinations[i][j]), day)
            temp.append(route_list)
        best_routes_list.append(temp)

    #if a better route found using two arc interchange, change route in best_routes_list
    for i in range(len(best_routes_list)):
        for j in range(len(best_routes_list[i])):
            old = best_routes_list[i][j]
            new = two_arc_interchange(best_routes_list[i][j], day)
            if(old != new):
                best_routes_list[i][j] = new 

    return best_routes_list

def two_arc_interchange(route_list, day):
    '''
    Parameters
    -----------
    route_list: array-like
        An ordered list of nodes 

    Returns:
    ------------
    improved_routes: array-like
        An improved list of nodes (by time).
    '''

    #for two arc interchange to occur, length of route_list >= 4
    if(len(route_list) < 4):
        return route_list
    
    #create a copy of the route list for alteration
    improved_routes = route_list.copy()

    #Say route_list is OABCDEO
    #The considered routes are: OBACDEO, OACBDEO, OABDCEO, OABCEDO. This is covered in for loop below
    for i in range(1, len(route_list)-2):
        temp = route_list.copy()
        temp[i], temp[i+1] = temp[i+1], temp[i]

        if(find_route_distance(temp, day, np.nan) < find_route_distance(improved_routes, day, np.nan)):
            improved_routes = temp.copy()
    
    #The route OBCDEAO (putting the first element to the 2nd to last element) is covered below
    temp = route_list.copy()
    first_element = temp.pop(1)
    temp.insert(len(temp)-1, first_element)

    if(find_route_distance(temp, day, np.nan) < find_route_distance(improved_routes, day, np.nan)):
        improved_routes = temp.copy()
    
    #The route OEABCDO (putting the 2nd to last element) into the 1st position is covered below
    
    temp = route_list.copy()
    last_element = temp.pop(len(temp)-2)
    temp.insert(1, last_element)

    if(find_route_distance(temp, day, np.nan) < find_route_distance(improved_routes, day, np.nan)):
        improved_routes = temp.copy()

    return improved_routes

def make_route_matrix(best_routes_list):
    '''
    Create a generalised format for possible routes to be fed into the linear program. Each column
    is a route and each row is a store.

    Parameters
    -----------
    route_list: array-like
        An ordered list of nodes 

    Returns:
    ------------
    route_matrix: array
        matrix of all routes and the pallets delivered to stores in each route
    '''

    #determine the total number of possible routes for all clusters
    array = [0]
    for i in range(len(best_routes_list)):
        array.append(array[i] + len(best_routes_list[i])) 

    #preallocate the route matrix
    route_matrix = np.zeros((len(locations['Store']),array[-1]))

    #input demand values according to route nodes
    for i in range (len(best_routes_list)):
        for j in range (len(best_routes_list[i])):
            for k in range (len(locations)):
                if (locations['Store'][k] in best_routes_list[i][j]):
                    route_matrix[k][array[i]+j] = 1
                
    #remove the first two rows of distribution centers
    route_matrix = route_matrix[2:]

    #Create a list of all unused routes
    delete_list = []
    for i in range(route_matrix.shape[0]):
        boolean = all(elements == 0 for elements in route_matrix[i])
        if boolean:
            delete_list.append(i)
    
    #Remove all unused routes
    route_matrix = np.delete(route_matrix, delete_list, 0)

    return route_matrix

def make_cost_matrix(best_routes_list, day, iteration, time):
    '''
    Makes a cost vector of all routes in best_routes_list

    Parameters:
    ----------
    best_routes_list: array
        A 3d array of all routes found, layered by cluster
    
    Returns:
    ----------
    cost_matrix: array
        a 1d array of the cost of all routes

    '''
    #initialisations:
    cost_list = []

    for i in range(len(best_routes_list)):
        for j in range(len(best_routes_list[i])):
            
            #$175 per hour to use a truck (we assume that if a truck is used for half an hour, it will cost $87.5)
            duration = find_route_distance(best_routes_list[i][j], day, iteration)
            
            #apply traffic factor to the duration
            if time == "Morning":
                duration = duration * 1.15  #morning
            else:
                duration = duration * 1.35  #afternoon

            cost = 175 * duration 

            #if duration exceeds 4 hours, extra $250 per hour to use
            if(duration > 4):
                cost += 250 * (duration - 4)

            cost_list.append(cost)

    return cost_list

def linear_program(route_matrix, cost_matrix, best_routes_list, day, closed):
    '''
    Generates the best routes to use so that each store is visited each day

    Parameters:
    -----------
    route_matrix: Array
        An array where the rows correspond to stores, columns to possible routes, 1 indicates a route visits that store, 0 otherwise
    cost_matrix: List
        A list of the trucking costs in NZD for every route
    best_routes_list: List
        A 3D list of all possible routes, layered by cluster

    Returns:
    ------------
    optimal_routes_list: List
        List of all routes used so that cost is minimised
    solution_cost: Float
        minimised solution cost
    '''

    #initialisations:
    all_routes = []
    route_list = []
    optimal_route_list = []
    optimal_route_printout = []
    count = 0

    #Create a dictionary of the route name and the corresponding route list e.g. 'Route0': [O,A,O]
    for rep in range(2):
        for i in range(len(best_routes_list)):
            for j in range(len(best_routes_list[i])):

                if count < (len(cost_matrix)/2):
                    all_routes.append("Route_{}_Morning".format(count)) 
                else:
                    all_routes.append("Route_{}_Afternoon".format(count)) 

                count += 1
                route_list.append(best_routes_list[i][j]) 
        routes_dict = dict(zip(all_routes, route_list)) 

    #Create variables for the LP 
    route_variables = LpVariable.dicts("Routes", all_routes, 0, 1, LpInteger) #Create binary variables
    Cost = pd.Series(cost_matrix, index = all_routes) #pandas dict with cost for every route

    #Create the LP minimisation problem
    prob = LpProblem("Vehicle Routing Problem", LpMinimize)
    prob += lpSum(Cost[i] * route_variables[all_routes[i]] for i in range(len(cost_matrix))), "objective Function"

    #Apply constraints:
    #truck maximum limit of 25 per day
    prob += lpSum(route_variables[all_routes[i]] for i in range(int(len(cost_matrix)/2))) <= 25, "truck number constraint in morning"
    prob += lpSum(route_variables[all_routes[i]] for i in range(int(len(cost_matrix)/2), len(cost_matrix))) <= 25, "truck number constraint in afternoon"
    
    #Number of times a store visited by all routes = 1
    for i in range(route_matrix.shape[0]):
        prob += lpSum(route_variables[all_routes[j]] * route_matrix[i][j] for j in range(len(route_matrix[0]))) == 1

    #write and solve the LP
    prob.writeLP("VRP.lp")
    prob.solve(PULP_CBC_CMD(msg=0)) #get rid of annoying print outs
    solution_cost = value(prob.objective)

    #collating all the routes with value = 1 (this means they are chosen by the LP) into a list
    for i in range(len(route_variables)):
        if(route_variables[all_routes[i]].varValue != 0):
            #print('{}, {}'.format(all_routes[i], routes_dict[all_routes[i]]))
            optimal_route_list.append(routes_dict[all_routes[i]])
            optimal_route_printout.append('{}, {}'.format(all_routes[i], routes_dict[all_routes[i]]))
 
    return optimal_route_list, optimal_route_printout, solution_cost

def plot_solutions(weekday_open_costs, weekday_closed_costs, weekend_open_costs, weekend_closed_costs):
    '''
    Plot the cost solutions for all four models

    Parameters
    -----------
    weekday_open_costs: array-like
        List of all costs on weekdays with North distribution open (only length 1 if simulation == false)
    weekday_closed_costs: array-like
        List of all costs on weekdays with North distribution closed (only length 1 if simulation == false)
    weekend_open_costs: array-like
        List of all costs on weekends with North distribution open (only length 1 if simulation == false)
    weekend_closed_costs: array-like
        List of all costs on weekends with North distribution closed (only length 1 if simulation == false)

    Returns:
    ------------
    None
    '''
    #plot the simulated results
    n_bins = 15

    plt.figure(figsize=(8,6))
    plt.hist(weekday_open_costs, n_bins, alpha=0.5, label="Northern Distribution open")
    plt.hist(weekday_closed_costs, n_bins, alpha=0.5, label="Northern Distribution closed")
    plt.xlabel("Optimal Cost (NZD)")
    plt.ylabel("Freqency")
    plt.title("Weekday Simulations")
    plt.legend(loc='upper right')
    plt.savefig("Plots" + os.sep + "Weekday hists")

    plt.figure(figsize=(8,6))
    plt.hist(weekend_open_costs, n_bins, alpha=0.5, label="Northern Distribution open")
    plt.hist(weekend_closed_costs, n_bins, alpha=0.5, label="Northern Distribution closed")
    plt.xlabel("Optimal Cost (NZD)")
    plt.ylabel("Freqency")
    plt.title("Weekend Simulations")
    plt.legend(loc='upper right')
    plt.savefig("Plots" + os.sep + "Weekend hists")


    weekday = [weekday_open_costs, weekday_closed_costs]
    weekend = [weekend_open_costs, weekend_closed_costs]
    fig, ax = plt.subplots(2,1)
    
    ax1, ax2 = ax.flatten()
    ax1.boxplot(weekday_open_costs, positions = [0])
    ax1.boxplot(weekday_closed_costs, positions = [1])
    ax1.set_title("Weekday Routes")
    plt.xticks([0,1], ["North Open", "North Closed"])
    ax1.set_ylabel("Cost for 1 day (NZD)")

    ax2.boxplot(weekend_open_costs, positions = [0])
    ax2.boxplot(weekend_closed_costs, positions = [1])
    plt.xticks([0,1], ["North Open", "North Closed"])
    ax2.set_title("Weekend Routes")
    ax2.set_ylabel("Cost for 1 day (NZD)")

    fig.tight_layout()
    plt.savefig("Plots" + os.sep + "simulation_boxplot.png", dpi=300)

    return


def mapClusterRoutes(day, cluster, routeList):
    '''
    Displays each of the routes we intend to use on a map

    Parameters:
    -----------

    cluster: Int
        The cluster that we are interested in
    routeList: List
        Contains all of the routes that we intend to use
    day: string
        The name of the day 

    Returns:
    --------
    None
    '''

    #This key may become invalid and need to be replaced by generating a new token from https://openrouteservice.org/dev/#/home
    ORSkey ='5b3ce3597851110001cf62488d4aec96835845a8af28e0f1b7e13f03'

    #Set up the map
    m = folium.Map(location=[-36.906636, 174.787650], tiles="Stamen Terrain", zoom_start=11)
        
    client = ors.Client(key = ORSkey)

    colours = ['red', 'blue', 'green', 'purple', 'orange','yellow']

    for i in range(0, len(routeList)):
        # Plotting distribution centre(s)
        if (i == 0):
            if (routeList[0] == "Distribution North"):
                folium.Marker(location = [-36.802192,174.758981],
                popup = "Distribution North", icon = folium.Icon(color = 'black')
                ).add_to(m)
            else:
                folium.Marker(location = [-37.011888,174.865463],
                popup = "Distribution South", icon = folium.Icon(color = 'black')
                ).add_to(m)

        count = 0

        # ONLY plotting the stores that are in the routes
        for j in range(2,len(locations['Store'])):
            if (locations['Store'][j] in routeList[i]):
                folium.Marker(location = [locations['Lat'][j],locations['Long'][j]],
                popup = "("+ str(count) + ") " + locations['Store'][j],
                icon = folium.Icon(color = colours[i])
                ).add_to(m)

                count+=1
                
        coordList = getCoordinates(routeList[i])

        #Generates a complete route between all the locations
        currentRoute = client.directions(
        coordinates = coordList,
        profile = 'driving-hgv',
        format = 'geojson',
        validate = False
        )

        folium.PolyLine(locations = [list(reversed(coord))
        for coord in currentRoute['features'][0]['geometry']['coordinates']], color = colours[i], opacity = 0.75, weight = 4).add_to(m)

    m.save(day + 'Cluster ' + str(cluster) + ' routes.html')

def getCoordinates(stores):
    '''
    This will return an array of all the coordinates of the locations within an array

    Parameters:
    -----------
    stores: List
        The names of all the locations
    
    Returns:
    --------
    coords: Array-like
        Contains all of the coordinates of the locations
    '''

    #Preallocate the list of coordinates for each route
    coordList = list()
    
    #Add all of the coordinates into an array for the route mapping
    for j in range(0,len(stores)):
        for k in range(0,len(locations)):
            if(locations['Store'][k] == stores[j]):
                coordList.append([locations['Long'][k],locations['Lat'][k]])
                break

    return coordList

def getClusterRoutes(cluster,routes):
    '''
    Will filter out all of the routes in a particular cluster

    Parameters:
    -----------
    cluster: Int
        The cluster number that we are interested in

    routes: List
        All of the routes that will be taken
    
    Returns:
    --------
    clusterRoutes: List
        The routes in a specified cluster
    '''

    clusterRoutes = list()
    for i in range(0,len(routes)):
        #Gets the index of the store location and uses it to check what cluster that store belongs to
        index = locations[locations['Store'] == routes[i][1]].index[0]
        if(locations['cluster'][index]==cluster):
            clusterRoutes.append(routes[i])
    return clusterRoutes

def mapRoutes(closed, day, final_routes):
    '''
    Displays each of the routes we intend to use on a map

    WARNING : MAX 5 clusters

    Parameters:
    -----------
    final_routes: List
        Contains all of the routes that we intend to use
    day: string
        The name of the day 

    Returns:
    --------
    None
    '''

    #This key may become invalid and need to be replaced by generating a new token from https://openrouteservice.org/dev/#/home
    ORSkey ='5b3ce3597851110001cf62488d4aec96835845a8af28e0f1b7e13f03'

    #Set up the map
    m = folium.Map(location=[-36.906636, 174.787650], tiles="Stamen Terrain", zoom_start=11)
        
    client = ors.Client(key = ORSkey)

    colours = ['red', 'blue', 'green', 'purple', 'orange']

    # Plotting distribution centre(s)
    folium.Marker(location = [-37.011888,174.865463],popup = "Distribution South", icon = folium.Icon(color = 'black')).add_to(m)
    if (closed == False):
        folium.Marker(location = [-36.802192,174.758981],popup = "Distribution North", icon = folium.Icon(color = 'black')).add_to(m)
    
    for i in range(len(final_routes)):
        for j in range (len(final_routes[i])):
            count = 1
            # ONLY plotting the stores that are in the routes
            for k in range(2,len(locations['Store'])):
                if (locations['Store'][k] in final_routes[i][j]):
                    folium.Marker(location = [locations['Lat'][k],locations['Long'][k]],
                    popup = 'Cluster: {}, Route: {}, Stop: {}, Location: {}'.format(i, j, count, locations['Store'][k]),
                    #popup = "Cluster " +str(i) + " Route "+str(j)+" ("+ str(count) + ") " + locations['Store'][k],
                    icon = folium.Icon(color = colours[i])
                    ).add_to(m)

                    count+=1

            #Get the first location in a route and check what cluster it's in, then use that as an index for the colours array
            #index = locations.get_loc(locations[routeList[i][0]])
            #clusterColour = colours[np.int(locations.iloc[index])]

            coordList = getCoordinates(final_routes[i][j])

            #Generates a complete route between all the locations
            currentRoute = client.directions(
            coordinates = coordList,
            profile = 'driving-hgv',
            format = 'geojson',
            validate = False
            )

            folium.PolyLine(locations = [list(reversed(coord))
            for coord in currentRoute['features'][0]['geometry']['coordinates']], color = colours[i], opacity = 0.75, weight = 4).add_to(m)

    if (closed == True):
        m.save('Route_Maps' + os.sep + day +'_routes_without_northern.html')
    else:
        m.save('Route_Maps' + os.sep + day +'_routes_with_northern.html')
    
    return

def plot_differences(average_weekday_open, average_weekday_closed, average_weekend_open, average_weekend_closed):

    NDclosed = []
    closed_sum = 0
    NDopen = []
    open_sum = 0
    days = range(28)

    #create a cost timeline for one month/4 weeks
    for weeks in range(4):
        for weekdays in range(5):
            closed_sum += average_weekday_closed
            NDclosed.append(closed_sum)

            open_sum += average_weekday_open
            NDopen.append(open_sum)
        
        closed_sum += average_weekend_closed
        NDclosed.append(closed_sum)
        NDclosed.append(closed_sum)

        open_sum += average_weekend_open
        NDopen.append(open_sum)
        NDopen.append(open_sum)

    #plot the difference timeline
    fig, ax = plt.subplots()
    ax.plot(days, NDclosed,'r-', label = "Northern Distribution Closed")
    ax.plot(days, NDopen,'b-', label = "Northern Distribution Open")
    ax.set_title('Comparison of Scenarios Over One Month/Four Weeks')
    ax.set_xlabel('Days')
    ax.set_ylabel('Cumulative Cost (NZD)')
    ax.legend(loc='upper left')
    fig.tight_layout()
    plt.savefig('Plots' + os.sep + 'Scenario_Cost_Comparison.png')