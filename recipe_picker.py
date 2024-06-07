import tkinter as tk
from PIL import ImageTk, Image
import sqlite3
import random

bg_color = '#396a89'

# clear widgets in frame
def clear_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()

# fetch data from database
def fetch_db():
    connection = sqlite3.connect("data/recipes.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sqlite_schema WHERE type='table'")
    all_tables = cursor.fetchall()

    # generate a random number
    idx = random.randint(0, len(all_tables)-1)

    # fetch a random table and it's table_records
    table_name = all_tables[idx][1]
    cursor.execute("SELECT * FROM " + table_name + " ;")
    table_records = cursor.fetchall()
    
    connection.close()
    return table_name, table_records


def pre_process(table_name, table_records):
    title = table_name[:-6]
    title = "".join([char if char.islower() else f" {char}" for char in title])

    ingredients = []

    # extract ingredients
    for record in table_records:
        id, name, qty, unit = record
        if unit:
            ingredient = f"{qty} {unit} of {name}"
        else:
            ingredient = f"{qty} {name}"

        ingredients.append(ingredient)

    return title, ingredients


# populates frame 1
def load_frame1():
    clear_widgets(frame2)
    frame1.tkraise()
    # preventing the child widget from modifying parent
    frame1.pack_propagate(False)

    # create logo widget
    logo_img = ImageTk.PhotoImage(file='assets/RRecipe_logo.png')
    logo_widget = tk.Label(frame1, image=logo_img, bg=bg_color)
    logo_widget.image = logo_img
    logo_widget.pack()

    tk.Label(frame1, 
            text="Ready for a random recipe?", 
            bg=bg_color, 
            fg="white",
            font=("TKMenuFont", 14)).pack()

    tk.Button(frame1,
            text="SHUFFLE",
            bg="#28393A",
            font=("TkHeadingFont", 20),
            fg="white",
            cursor="hand2",
            activebackground="#BADEE2",
            activeforeground="black",
            command=lambda: load_frame2()).pack(pady=20)


# populates frame 2
def load_frame2():
    clear_widgets(frame1)
    frame2.tkraise()
    table_name, table_records = fetch_db()
    title, ingredients = pre_process(table_name, table_records)

    # create logo widget
    logo_img = ImageTk.PhotoImage(file='assets/RRecipe_logo_bottom.png')
    logo_widget = tk.Label(frame2, image=logo_img, bg=bg_color)
    logo_widget.image = logo_img
    logo_widget.pack(pady=20)

    # title
    tk.Label(frame2,
             text=title,
             bg=bg_color, 
             fg="white",
             font=("TKHeadingFont", 20)).pack(pady=25)
    
    # ingredients
    for ingredient in ingredients:
        tk.Label(frame2,
                 text=ingredient,
                 bg="#28393A",
                 fg="white",
                 font=("TKMenuFont", 12)).pack(fill="x")
        
    tk.Button(frame2,
        text="BACK",
        bg="#28393A",
        font=("TkHeadingFont", 17),
        fg="white",
        cursor="hand2",
        activebackground="#BADEE2",
        activeforeground="black",
        command=lambda: load_frame1()).pack(pady=20)



# initializing app
root = tk.Tk()
root.title("Recipe Picker")

# center on screen using Tcl language
root.eval("tk::PlaceWindow . center")

# frame gives the window shape
frame1 = tk.Frame(root, width=500, height=600, bg=bg_color)
frame1.grid(row=0, column=0, sticky="nsew")

frame2 = tk.Frame(root, bg=bg_color)
frame2.grid(row=0, column=0, sticky="nsew")

load_frame1()



# run
root.mainloop()