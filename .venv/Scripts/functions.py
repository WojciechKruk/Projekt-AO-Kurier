from math import factorial
import time
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def optimize_2opt(route, data_frame):
    """2-opt Optimization for a single route."""
    best_route = route
    best_distance = calculate_distance(route, data_frame)
    improved = True

    while improved:
        improved = False
        for i in range(1, len(route) - 1):
            for j in range(i + 1, len(route)):
                new_route = route[:i] + route[i:j][::-1] + route[j:]
                new_distance = calculate_distance(new_route, data_frame)
                if new_distance < best_distance:
                    best_route = new_route
                    best_distance = new_distance
                    improved = True
        route = best_route

    return best_route


def optimize_3opt(route, data_frame):
    """3-opt Optimization for a single route."""
    best_route = route
    best_distance = calculate_distance(route, data_frame)
    improved = True

    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route) - 1):
                for k in range(j + 1, len(route)):
                    new_routes = [
                        route[:i] + route[i:j][::-1] + route[j:k][::-1] + route[k:],
                        route[:i] + route[j:k] + route[i:j] + route[k:],
                        route[:i] + route[j:k][::-1] + route[i:j][::-1] + route[k:],
                    ]
                    for new_route in new_routes:
                        new_distance = calculate_distance(new_route, data_frame)
                        if new_distance < best_distance:
                            best_route = new_route
                            best_distance = new_distance
                            improved = True
        route = best_route

    return best_route


def check_constraints(solution, data_frame, max_capacity, max_distance):
    load_exceeded = False
    distance_exceeded = False

    for route in solution:
        distance_route = 0
        load_route = 0

        for i in range(len(route)):
            if i == 0:
                distance_route += np.sqrt(
                    (data_frame.iloc[route[i]]['X'] - data_frame.iloc[0]['X']) ** 2 + (
                            data_frame.iloc[route[i]]['Y'] - data_frame.iloc[0]['Y']) ** 2)
            else:
                distance_route += np.sqrt((data_frame.iloc[route[i]]['X'] - data_frame.iloc[route[i - 1]]['X']) ** 2 + (
                            data_frame.iloc[route[i]]['Y'] - data_frame.iloc[route[i - 1]]['Y']) ** 2)

            load_route += data_frame.iloc[route[i]]['masa']

        distance_route += np.sqrt(
            (data_frame.iloc[route[-1]]['X'] - data_frame.iloc[0]['X']) ** 2 + (
                    data_frame.iloc[route[-1]]['Y'] - data_frame.iloc[0]['Y']) ** 2)

        if load_route > max_capacity:
            load_exceeded = True

        if distance_route > max_distance:
            distance_exceeded = True

    return load_exceeded, distance_exceeded


def calculate_distance(route, data_frame):
    """Calculates the total distance for a given route."""
    distance = 0
    # Calculate distance between consecutive points
    for i in range(1, len(route)):
        distance += np.sqrt((data_frame.iloc[route[i]]['X'] - data_frame.iloc[route[i - 1]]['X']) ** 2 + (
                data_frame.iloc[route[i]]['Y'] - data_frame.iloc[route[i - 1]]['Y']) ** 2)
    # Add return distance to the starting point
    distance += np.sqrt((data_frame.iloc[route[-1]]['X'] - data_frame.iloc[route[0]]['X']) ** 2 + (
                data_frame.iloc[route[-1]]['Y'] - data_frame.iloc[route[0]]['Y']) ** 2)
    return distance

def evaluate_solution(solution, data_frame, max_capacity, max_distance):
    total_cost = 0
    penalty_for_exceeding_capacity = 100000
    penalty_for_exceeding_distance = 50000
    total_weight = sum(data_frame['masa'])  # Sum of all weights
    expected_capacity = total_weight / len(solution)  # Theoretical equal capacity for each vehicle

    for route in solution:
        if not route:
            continue

        distance_route = 0
        load_route = 0

        for i in range(len(route)):
            if i == 0:  # Distance from base to the first point in the route
                distance_route += np.sqrt(
                    (data_frame.iloc[route[i]]['X'] - data_frame.iloc[0]['X']) ** 2 + (
                            data_frame.iloc[route[i]]['Y'] - data_frame.iloc[0]['Y']) ** 2)
            else:  # Distance between consecutive points in the route
                distance_route += np.sqrt((data_frame.iloc[route[i]]['X'] - data_frame.iloc[route[i - 1]]['X']) ** 2 + (
                            data_frame.iloc[route[i]]['Y'] - data_frame.iloc[route[i - 1]]['Y']) ** 2)

            load_route += data_frame.iloc[route[i]]['masa']

        # Add return to base
        distance_route += np.sqrt(
            (data_frame.iloc[route[-1]]['X'] - data_frame.iloc[0]['X']) ** 2 + (
                    data_frame.iloc[route[-1]]['Y'] - data_frame.iloc[0]['Y']) ** 2)

        # Penalty for exceeding maximum load
        if load_route > max_capacity:
            total_cost += penalty_for_exceeding_capacity

        # Penalty for exceeding maximum route distance
        if distance_route > max_distance:
            total_cost += penalty_for_exceeding_distance

        # Penalty for uneven distribution of loads
        total_cost += (load_route - expected_capacity) ** 2

        total_cost += distance_route

    return total_cost

def estimate_brute_force_time(number_of_points):
    number_of_combinations = factorial(number_of_points - 1)
    time_in_seconds = number_of_combinations * 1e-6
    return number_of_combinations, time_in_seconds
