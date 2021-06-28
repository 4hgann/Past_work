#imports
from Functions import *
import time
import scipy.stats as st
import statistics
import os

def main():
    #initialisations:
    t0 = time.time()
    t1 = t0
    Northern_dist = [False, True]
    days = ['Weekday','Weekend']
    weekday_closed_costs = []
    weekday_open_costs = []  
    weekend_closed_costs = []
    weekend_open_costs = []

    n = 5   #set number of location clusters
    nsamples = 200   #set the number of simulations

    #-------------------------------------------------------------------------------------------
    # 1.) Generate Data
    #------------------
    demand_data_A, demand_data_M, demands, distances, durations, locations = generate_data()
    weekday_boot, weekend_boot = sample_demand(nsamples)

    #solve the models:
    for closed in Northern_dist:
        for day in days:
            print("Start : {}, ND: {}".format(day,closed))
            print("Starting Location Clustering...")

            #-------------------------------------------------------------------------------------------
            # 2.) Generate a geographical map of the locations
            #-------------------------------------------------
            generate_map(day)

            #-------------------------------------------------------------------------------------------
            # 3.) Generate location clusters and a cluster map
            #-------------------------------------------------
            location_clustering(n,closed)
            generate_cluster_map(n)

            #-------------------------------------------------------------------------------------------
            #4.) Generate a list of all feasible routes for each cluster
            #-----------------------------------------------------------
            print("Finished Location Clustering. (time taken: {} s)".format(time.time()-t1))
            t1 = time.time()
            print("Starting Route Finding...")
            
            all_combinations = feasible_stores (day)

            #-------------------------------------------------------------------------------------------
            #5.) Optimise our route set for improved time efficiency
            #--------------------------------------------------------
            best_routes_list = best_routes(all_combinations, day)

            #-------------------------------------------------------------------------------------------
            #6.) Generalise the data formatting into appropriate matrices
            #------------------------------------------------------------
            route_matrix = make_route_matrix(best_routes_list)
            route_matrix = np.concatenate((route_matrix, route_matrix), axis=1)

            print("Finished Route Finding. (time taken: {} s)".format(time.time()-t1))
            t1 = time.time()
            print("Starting Simulation...")

            #-------------------------------------------------------------------------------------------
            #7.) Simulate many different possibilities using the LP
            #------------------------------------------------------
            for iteration in range(nsamples):
                print("iteration: {}".format(iteration))

                morning_cost_matrix = make_cost_matrix(best_routes_list, day, iteration, "Morning")
                afternoon_cost_matrix = make_cost_matrix(best_routes_list, day, iteration, "afternoon")
                cost_matrix = np.append(morning_cost_matrix, afternoon_cost_matrix)

                optimal_route_list, optimal_route_printout, solution_cost = linear_program(route_matrix, cost_matrix, best_routes_list, day, closed)

                #do not remove
                if day == "Weekday" and closed == True:
                    weekday_closed_costs.append(solution_cost)
                elif day == "Weekday" and closed == False:
                    weekday_open_costs.append(solution_cost)
                elif day == "Weekend" and closed == True:
                    weekend_closed_costs.append(solution_cost)
                else:
                    weekend_open_costs.append(solution_cost)
            
            #save the final iteration's chosen routes in a text file
            file_object = open("Route_Lists{}route_list_{}_NDopen({}).txt".format(os.sep,day,closed),"w")
            for i in range(len(optimal_route_printout)):
                file_object.write('{}\n'.format(optimal_route_printout[i]))
            file_object.close()

            # Plot the final iteration's chosen routes on a map (clusters combined)
            final_routes = []
            for i in range(n):
                clusterRoutes = getClusterRoutes(i,optimal_route_list)
                final_routes.append(clusterRoutes)
            mapRoutes(closed, day, final_routes)

            print("Finished Simulation. (time taken: {} s) \n".format(time.time()-t1))
            t1 = time.time()    

    #-------------------------------------------------------------------------
    #Optional.) Run linear program to solve a single run of non-simulated data
    #-------------------------------------------------------------------------
    if False:
        optimal_route_list, solution_cost = linear_program(route_matrix, cost_matrix, best_routes_list, day, closed)
        print(solution_cost)
        if day == "Weekday" and closed:
            weekday_closed = solution_cost

        elif day == "Weekday" and not closed:
            weekday_open = solution_cost
            
        elif day == "Weekend" and closed:
            weekend_closed = solution_cost
            
        else:
            weekend_open = solution_cost
    

    #-------------------------------------------------------------------------------------------
    #8.) Plot and compare the solution costs of the simulated data
    #-------------------------------------------------------------
    plot_solutions(weekday_open_costs, weekday_closed_costs, weekend_open_costs, weekend_closed_costs)

    #4 weekends and 20 weekdays, equivalent to 4 weeks or approx 1 month
    average_weekday_open = statistics.mean(weekday_open_costs)
    average_weekday_closed = statistics.mean(weekday_closed_costs)
    average_weekend_open = statistics.mean(weekend_open_costs)
    average_weekend_closed = statistics.mean(weekend_closed_costs)

    print('Estimated cost for a weekday when the Northern distribution centre is open = ${}'.format(average_weekday_open))
    print('Estimated cost for a weekday when the Northern distribution centre is closed = ${}'.format(average_weekday_closed))
    print('Estimated cost for a weekend when the Northern distribution centre is open = ${}'.format(average_weekend_open))
    print('Estimated cost for a weekend when the Northern distribution centre is closed = ${}'.format(average_weekend_closed))

    #find the percentiles (NOT CONFIDENCE INTERVALS)
    weekday_open_costs.sort()
    weekday_closed_costs.sort()
    weekend_open_costs.sort()
    weekend_closed_costs.sort()
    CI_weekday_open = (weekday_open_costs[int(0.05*len(weekday_open_costs))], weekday_open_costs[int(0.95*len(weekday_open_costs))])
    CI_weekday_closed = (weekday_closed_costs[int(0.05*len(weekday_closed_costs))], weekday_closed_costs[int(0.95*len(weekday_closed_costs))])
    CI_weekend_open = (weekend_open_costs[int(0.05*len(weekend_open_costs))], weekend_open_costs[int(0.95*len(weekend_open_costs))])
    CI_weekend_closed = (weekend_closed_costs[int(0.05*len(weekend_closed_costs))], weekend_closed_costs[int(0.95*len(weekend_closed_costs))])
    print('The 95 percentile interval for a weekday when the Northern distribution centre is open = ${}, ${}'.format(CI_weekday_open[0],CI_weekday_open[1]))
    print('The 95 percentile interval for a weekday when the Northern distribution centre is closed = ${}, ${}'.format(CI_weekday_closed[0],CI_weekday_closed[1]))
    print('The 95 percentile interval for a weekend when the Northern distribution centre is open = ${}, ${}'.format(CI_weekend_open[0],CI_weekend_open[1]))
    print('The 95 percentile interval for a weekend when the Northern distribution centre is closed = ${}, ${}'.format(CI_weekend_closed[0],CI_weekend_closed[1]))

    monthly_cost_difference = 4 * average_weekend_closed + 20 * average_weekday_closed - 4 * average_weekend_open - 20 * average_weekday_open
    print("Estimated difference in monthly cost to close Northern Distribution Centre: {}".format(monthly_cost_difference))
    plot_differences(average_weekday_open, average_weekday_closed, average_weekend_open, average_weekend_closed)
    
    #time keeping
    print("\n Total Computational Time : {} s".format(time.time()-t0))

if __name__ == "__main__":
    main()