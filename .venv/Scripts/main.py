from math import factorial
import time
import random
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from functions import *
from visualization import *
from tabu_search import *
from draw import select_points_to_excel, get_number_of_vehicles

select_points_to_excel()

# DATASET1
starting_point = 0
# number_of_vehicles = 4
number_of_vehicles = get_number_of_vehicles()
max_capacity = 1000
max_distance = 1600
iterations = 200
tabu_list_size = 10
excel_file = 'dane_uzytkownika.xlsx'
# excel_file = 'dane.xlsx'

df = pd.read_excel(excel_file, usecols=['X', 'Y', 'masa'])
number_of_points = len(df)
number_of_combinations, estimated_time_seconds = estimate_brute_force_time(number_of_points)
print(f"Liczba możliwych kombinacji: {number_of_combinations}, Oszacowany czas (s): {estimated_time_seconds}")

(best_solution, best_solution_cost, load_exceeded, distance_exceeded) = tabu_search(df, number_of_vehicles, max_capacity, max_distance, iterations, tabu_list_size)

if best_solution is not None:
    print("Best found solution:")
    for nr, route in enumerate(best_solution):
        full_route = [0] + route + [0]
        print(f"Vehicle {nr + 1}: Route - {full_route}")
    print(f"Total cost of the best solution: {best_solution_cost}")

    if load_exceeded:
        print("Exceeded maximum load.")
    if distance_exceeded:
        print("Exceeded maximum route distance.")

    fig = draw_routes(df, best_solution, best_solution_cost, show=True)
else:
    print("No feasible solution found.")
