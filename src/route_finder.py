# file used to be able to find the route between two points

def find_routes(start, end, route_graph):
    possible_routes = [] # list of all possible routes
    # iterate through all routes in the route graph
    for route_id, stops in route_graph.items():
        if start in stops and end in stops:
            possible_routes.append({
                "route_id": route_id,
                "origin": start,
                "destination": end,
                "stops":stops[stops.index(start):stops.index(end)+1],
                "bus_time": len(stops[stops.index(start):stops.index(end)+1]) * 3, # simulation
            })
    return possible_routes # return all possible routes between two points