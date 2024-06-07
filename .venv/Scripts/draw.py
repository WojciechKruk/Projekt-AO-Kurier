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

    num_vehicles = simpledialog.askinteger("Liczba pojazdów", "Wpisz liczbę pojazdów:", initialvalue=4)
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

    button = tk.Button(root, text="Save to Excel", command=save_points)
    button.pack()

    root.mainloop()

# select_points_to_excel()  # To służy do testowania funkcji bez konieczności importowania
