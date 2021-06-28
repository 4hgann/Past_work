from Functions import *

demand_data_A, demand_data_M, demand, distances, durations, locations = generate_data()
cluster_source = location_clustering(5,closed = False)

assert(find_route_demand(['Distribution North','The Warehouse Glenfield Mall','Noel Leeming Wairau Park',
'The Warehouse Milford','Distribution North'],'Tuesday') == 19.25)

assert(find_route_distance(['Distribution South','Distribution North',
'The Warehouse Atrium','The Warehouse Newmarket'],'Tuesday') == 2516.03 + 1031.38 + 604.61)

assert(two_arc_interchange(['Noel Leeming Papatoetoe','The Warehouse Takanini',
'Noel Leeming Ormiston','The Warehouse Clendon'],'Tuesday') ==
['Noel Leeming Papatoetoe','Noel Leeming Ormiston','The Warehouse Takanini','The Warehouse Clendon'])

