from math import factorial
import time
import random
import pandas as pd
import numpy as np
import matplotlib
from functions import *

def generate_initial_solution(data_frame, number_of_vehicles, max_capacity):
    solution = [[] for _ in range(number_of_vehicles)]
    vehicle_capacities = [0] * number_of_vehicles
    to_visit = set(data_frame.index[1:])  # Assuming point 0 is the depot

    while to_visit:
        for current_vehicle in range(number_of_vehicles):
            if not to_visit:
                break
            current_point = 0 if not solution[current_vehicle] else solution[current_vehicle][-1]
            nearest = None
            min_distance = float('inf')
            for point in to_visit:
                distance = np.sqrt((data_frame.loc[point, 'X'] - data_frame.loc[current_point, 'X']) ** 2 + (
                            data_frame.loc[point, 'Y'] - data_frame.loc[current_point, 'Y']) ** 2)
                if distance < min_distance and vehicle_capacities[current_vehicle] + data_frame.loc[
                    point, 'masa'] <= max_capacity:
                    min_distance = distance
                    nearest = point

            if nearest is None:
                continue

            solution[current_vehicle].append(nearest)
            vehicle_capacities[current_vehicle] += data_frame.loc[nearest, 'masa']
            to_visit.remove(nearest)

    return solution

def generate_neighborhood(current_solution, data_frame, max_capacity, max_distance, current_cost):
    """Generates a list of neighboring solutions by swapping two random points and performing local 2-opt and 3-opt optimizations."""
    neighborhood = []
    number_of_vehicles = len(current_solution)

    # Swapping points between routes
    for _ in range(20):  # Increasing the number of neighboring solutions
        solution_copy = [route[:] for route in current_solution if isinstance(route, list) and len(route) > 0]
        if len(solution_copy) < 2:
            continue  # Skip iteration if less than two routes are suitable for swapping

        vehicle1, vehicle2 = random.sample(range(len(solution_copy)), 2)
        route1, route2 = solution_copy[vehicle1], solution_copy[vehicle2]

        index1, index2 = random.randint(0, len(route1) - 1), random.randint(0, len(route2) - 1)
        # Swapping points
        route1[index1], route2[index2] = route2[index2], route1[index1]

        neighborhood.append(solution_copy)

    # Swapping points within routes
    for route in current_solution:
        if len(route) < 2:
            continue
        for _ in range(10):  # Adding several swaps within routes
            solution_copy = [r[:] for r in current_solution]
            route_copy = route[:]
            i, j = random.sample(range(len(route_copy)), 2)
            route_copy[i], route_copy[j] = route_copy[j], route_copy[i]
            solution_copy[current_solution.index(route)] = route_copy
            neighborhood.append(solution_copy)

    # Local 2-opt and 3-opt optimization for each route in each solution
    for solution in current_solution:
        for idx, route in enumerate(solution):
            if isinstance(route, list) and len(route) > 2:
                new_route = optimize_2opt(route[:], data_frame)
                new_solution = [r[:] for r in current_solution]
                new_solution[idx] = new_route
                neighborhood.append(new_solution)

                # Adding 3-opt
                if len(route) > 3:
                    new_route_3opt = optimize_3opt(route[:], data_frame)
                    new_solution_3opt = [r[:] for r in current_solution]
                    new_solution_3opt[idx] = new_route_3opt
                    neighborhood.append(new_solution_3opt)

    return neighborhood
