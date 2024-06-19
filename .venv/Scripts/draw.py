import tkinter as tk
from tkinter import simpledialog
import pandas as pd
import os
import random

def save_to_excel(data, filename):
    df = pd.DataFrame(data, columns=['NR', 'X', 'Y', 'masa'])
    df.to_excel(filename, index=False)

def on_click(event):
    x = event.x
    y = event.y

    # Get the width and height of the canvas to draw axes
    width = canvas.winfo_width()
    height = canvas.winfo_height()

    # # Draw the coordinate system if it's the first click
    # if not points:
    #     # Draw X-axis with labels
    #     canvas.create_line(0, height - 20, width, height - 20, fill="black")
    #     for i in range(0, width, 50):
    #         canvas.create_text(i, height - 10, text=str(i), anchor=tk.S)
    #
    #     # Draw Y-axis with labels
    #     canvas.create_line(20, 0, 20, height, fill="black")
    #     for i in range(height, 0, -50):
    #         canvas.create_text(10, height - i, text=str(height - i), anchor=tk.E)


    if not points:
        point = [1, x, y, random.randint(1, 10)]
        canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="blue")
    else:
        point = [len(points) + 1, x, y, random.randint(1, 10)]
        canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="red")
    points.append(point)

def get_number_of_vehicles():
    root = tk.Tk()
    root.withdraw()

    num_vehicles = simpledialog.askinteger("Number of vehicles", "Enter the number of vehicles:", initialvalue=4)
    return num_vehicles


def save_points():
    if points:
        filename = "dane_uzytkownika.xlsx"
        script_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(script_dir, filename)
        save_to_excel(points, file_path)
        root.quit()

def select_points_to_excel():
    global points, canvas, root

    points = []

    root = tk.Tk()
    root.title("Click points and save to Excel (first point is a hub)")

    canvas = tk.Canvas(root, width=400, height=400, bg='white')
    canvas.pack()
    canvas.bind("<Button-1>", on_click)

    button = tk.Button(root, text="Save to Excel", command=lambda: [save_points(), root.destroy()])
    button.pack()

    root.mainloop()

# select_points_to_excel()  # To służy do testowania funkcji bez konieczności importowania
