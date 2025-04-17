# file used to be able to find the route between two points

def find_routes(start, end, route_graph):
    posible_routes = [] # list of all possible routes
        for route_id, stops in route_graph.items():
            if start in stops and end in stops:
                possible_routes.append({
                    "route_id": route_id,
                    ""

                })