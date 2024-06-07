from math import factorial
import time
import random
import pandas as pd
import numpy as np
import matplotlib
from functions import *
from generate import *

def tabu_search(data_frame, number_of_vehicles, max_capacity, max_distance, iterations, tabu_list_size):
    best_solution = None
    best_cost = float('inf')
    tabu_list = []
    current_solution = generate_initial_solution(data_frame, number_of_vehicles, max_capacity)
    current_cost = evaluate_solution(current_solution, data_frame, max_capacity, max_distance)
    no_improvement_iterations = 0
    max_no_improvement_iterations = 100

    for iteration in range(iterations):
        neighborhood = generate_neighborhood(current_solution, data_frame, max_capacity, max_distance, current_cost)
        neighborhood = [r for r in neighborhood if r not in tabu_list]

        best_neighborhood = None
        best_neighborhood_cost = float('inf')

        for candidate in neighborhood:
            candidate_cost = evaluate_solution(candidate, data_frame, max_capacity, max_distance)
            if candidate_cost < best_neighborhood_cost:
                best_neighborhood = candidate
                best_neighborhood_cost = candidate_cost

        if best_neighborhood is not None and best_neighborhood_cost < best_cost:
            best_solution = best_neighborhood
            best_cost = best_neighborhood_cost
            current_solution = best_neighborhood
            current_cost = best_neighborhood_cost
            update_tabu_list(tabu_list, best_neighborhood, tabu_list_size)
            no_improvement_iterations = 0
        else:
            no_improvement_iterations += 1

        if no_improvement_iterations > max_no_improvement_iterations:
            current_solution = generate_initial_solution(data_frame, number_of_vehicles, max_capacity)
            current_cost = evaluate_solution(current_solution, data_frame, max_capacity, max_distance)
            no_improvement_iterations = 0

    load_exceeded, distance_exceeded = check_constraints(best_solution, data_frame, max_capacity, max_distance)
    return best_solution, best_cost, load_exceeded, distance_exceeded

def update_tabu_list(tabu_list, new_element, tabu_list_size):
    tabu_list.append(new_element)
    while len(tabu_list) > tabu_list_size:
        tabu_list.pop(0)