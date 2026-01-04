import math
from typing import List, Tuple
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

class LocalVRPSolver:
    """
    Solves the Vehicle Routing Problem (VRP) locally using Google OR-Tools.
    Calculates distance/cost using the Haversine formula (Great Circle distance).
    """

    def __init__(self, vehicles: int = 1, depot: int = 0):
        self.num_vehicles = vehicles
        self.depot_index = depot

    def solve(self, locations: List[Tuple[float, float]]) -> dict:
        """
        Solves the VRP for the given List of (Lat, Lng) tuples.
        Returns a dict with 'route': [index0, index3, index1...], 'distance': km
        """
        if not locations:
            return {"route": [], "distance": 0.0}

        # 1. Create the Distance Matrix
        distance_matrix = self._compute_distance_matrix(locations)

        # 2. Create the Routing Index Manager
        manager = pywrapcp.RoutingIndexManager(
            len(locations),
            self.num_vehicles,
            self.depot_index
        )

        # 3. Create Routing Model
        routing = pywrapcp.RoutingModel(manager)

        # 4. Create and Register Transit Callback
        def distance_callback(from_index, to_index):
            # Convert from routing variable Index to distance matrix NodeIndex
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            # OR-Tools expects integers. We multiply km by 1000 to work in meters.
            return int(distance_matrix[from_node][to_node] * 1000)

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        # 5. Define Cost of each Arc
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        # 6. Add Distance Dimension (Optional but good for tracking)
        dimension_name = 'Distance'
        routing.AddDimension(
            transit_callback_index,
            0,  # no slack
            3000000,  # max distance per vehicle (3000 km hard limit)
            True,  # start cumul to zero
            dimension_name
        )
        distance_dimension = routing.GetDimensionOrDie(dimension_name)
        distance_dimension.SetGlobalSpanCostCoefficient(100)

        # 7. Setting Search Parameters
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )
        # Optional: Local Search Metaheuristic (Guided Local Search) for better results if time permits
        # search_parameters.local_search_metaheuristic = (
        #    routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
        # )
        # search_parameters.time_limit.seconds = 1

        # 8. Solve
        solution = routing.SolveWithParameters(search_parameters)

        # 9. Extract Solution
        if solution:
            return self._extract_solution(manager, routing, solution, locations)
        else:
            return {"status": "no_solution", "route": [], "distance": 0.0}

    def _extract_solution(self, manager, routing, solution, locations):
        """Extracts the route for vehicle 0 (since we assume 1 vehicle)."""
        index = routing.Start(0)
        route_indices = []
        route_distance = 0

        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_indices.append(node_index)
            
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            
            # Add distance
            route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)

        # Add the last node (Depot End)
        node_index = manager.IndexToNode(index)
        route_indices.append(node_index)

        return {
            "status": "optimized",
            "route_indices": route_indices, # List of indices in input array
            "total_distance_km": route_distance / 1000.0, # Convert back to km
            "coordinates_ordered": [locations[i] for i in route_indices]
        }

    def _compute_distance_matrix(self, locations):
        """Builds a NxN matrix of distances."""
        size = len(locations)
        matrix = [[0.0] * size for _ in range(size)]
        
        for i in range(size):
            for j in range(size):
                if i == j:
                    matrix[i][j] = 0.0
                else:
                    matrix[i][j] = self._haversine(locations[i], locations[j])
        return matrix

    def _haversine(self, coord1, coord2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        lat1, lon1 = coord1
        lat2, lon2 = coord2
        
        R = 6371  # Radius of earth in km
        dLat = math.radians(lat2 - lat1)
        dLon = math.radians(lon2 - lon1)
        
        a = (math.sin(dLat / 2) * math.sin(dLat / 2) +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dLon / 2) * math.sin(dLon / 2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = R * c
        return d
