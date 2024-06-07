from math import factorial
import time
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def draw_routes(data_frame, solution, cost, show=False):
    fig, ax = plt.subplots()

    colors = ['c', 'm', 'y', 'k', 'r', 'g', 'b']
    start_marker = 's'  # Square marker for start/end point
    normal_marker = 'o'  # Circular marker for other points

    # Draw routes for each vehicle
    for i, route in enumerate(solution):
        points_x = data_frame.iloc[route]['X'].tolist()
        points_y = data_frame.iloc[route]['Y'].tolist()

        # Insert start and end point at the beginning and end of the list
        points_x.insert(0, data_frame.iloc[0]['X'])
        points_y.insert(0, data_frame.iloc[0]['Y'])
        points_x.append(data_frame.iloc[0]['X'])
        points_y.append(data_frame.iloc[0]['Y'])

        # Draw the route with the appropriate color and marker
        ax.plot(points_x, points_y, marker=normal_marker, color=colors[i % len(colors)], label=f'Vehicle {i + 1}')
        # Mark the start/end point with a different color and marker
        ax.plot(data_frame.iloc[0]['X'], data_frame.iloc[0]['Y'], marker=start_marker, color='black')

    # Add legend and title with the cost
    ax.legend()
    ax.set_title(f'Visualization of vehicle routes (Total cost: {cost})')
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_aspect('equal', adjustable='datalim')  # Ensures equal axis scale

    # Optionally show the plot
    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig