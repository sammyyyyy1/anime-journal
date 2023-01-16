# Imports
from tkinter import ttk
import tkinter as tk
import pandas as pd

# Create window
root = tk.Tk()
root.title("ANIME JOURNAL")
root.geometry("550x400")
root.resizable(False,True)

# Upon selection in dropdown menu
def on_select(*args):
    movie_name = movie_var.get()
    df = pd.read_csv("anime.csv")
    selected_movie = df[df["Name"] == movie_name]
    rating_label = tk.Label(root, anchor='w')
    rating_label.grid(row=1, column=3)
    rating_label.config(background="grey", width=20)
    # If there is no selected movie, show error message instead of rating
    if selected_movie.empty:
        rating_label.config(text="Movie not found")
    else:
        rating = selected_movie["Rating"].values[0]
        rating_label.config(text=f"Rating: {rating}")
    refresh_table()

# Upon pressing add button, make a new window to input values and pass as parameters
def on_add():
    add_window = tk.Toplevel(root)
    add_window.title("Add Movie")
    title_label = tk.Label(add_window, text="Enter anime title:")
    title_label.grid(row=0, column=0)
    title_entry = tk.Entry(add_window)
    title_entry.grid(row=0, column=1)
    rating_label = tk.Label(add_window, text="Enter rating:")
    rating_label.grid(row=1, column=0)
    rating_spinbox = tk.Spinbox(add_window, from_=0, to=10)
    rating_spinbox.grid(row=1, column=1)
    submit_button = tk.Button(add_window, text="Submit", command=lambda: on_add_submit(add_window, title_entry, rating_spinbox))
    submit_button.grid(row=2, column=1)

# Read and write on file according to provided parameters, then refresh main window
def on_add_submit(add_window, title_entry, rating_spinbox):
    movie_title = title_entry.get()
    movie_rating = rating_spinbox.get()
    df = pd.read_csv("anime.csv")
    df = df.append({"Name": movie_title, "Rating": movie_rating}, ignore_index=True)
    df.to_csv("anime.csv", index=False)
    add_window.destroy()
    choose_movie()
    on_select()
    movie_var.set(movie_title)

# Upon pressing change button, make a new window to input values and pass as parameters
def on_change():
    change_window = tk.Toplevel(root)
    change_window.title("")
    rating_label = tk.Label(change_window, text=f"Change rating for {movie_var.get()}")
    rating_label.grid(row=0, column=0)
    new_rating_label = tk.Label(change_window, text="Enter new rating:")
    new_rating_label.grid(row=1, column=0)
    rating_spinbox = tk.Spinbox(change_window, from_=0, to=10)
    rating_spinbox.grid(row=1, column=1)
    submit_button = tk.Button(change_window, text="Submit", command=lambda: on_change_submit(new_rating_label, rating_spinbox, change_window))
    submit_button.grid(row=2, column=1)

# Read and write on file according to provided parameters, then refresh main window
def on_change_submit(rating_label, rating_spinbox, change_window):
    movie_name = movie_var.get()
    new_rating = rating_spinbox.get()
    df = pd.read_csv("anime.csv")
    df.loc[df["Name"] == movie_name, "Rating"] = new_rating
    df.to_csv("anime.csv", index=False)
    rating_label.config(text=f"Rating: {new_rating}")
    choose_movie()
    on_select()
    change_window.destroy()

# Remove selected movie
def on_remove():
    movie_name = movie_var.get()
    df = pd.read_csv("anime.csv")
    df = df[df["Name"] != movie_name]
    df.to_csv("anime.csv", index=False)
    # Refresh dropdown table
    choose_movie()
    movie_var.set('')
    on_select()

# When a movie is chosen in the dropdown list or an action was completed on a movie
def choose_movie():
    df = pd.read_csv("anime.csv")
    movie_list = df['Name'].tolist()
    # If selected movie is not in the list, change the selected movie to an empty string
    menu = movie_dropdown.children['menu']
    menu.delete(0, 'end')
    for movie in movie_list:
        menu.add_command(label=movie, command=lambda value=movie: movie_var.set(value))
    if len(movie_list) > 0:
        movie_var.set(movie_list[0])
    else:
        movie_var.set('')


# Read csv file
df = pd.read_csv("anime.csv")
movie_list = df['Name'].tolist()
movie_var = tk.StringVar()

# Create dropdown list
movie_dropdown = tk.OptionMenu(root, movie_var, *movie_list, command=on_select)
movie_dropdown.config(width=80)
movie_dropdown.grid(row=0,columnspan=4)
choose_movie()

# Create add button
add_button = tk.Button(root, text="Add", command=on_add)
add_button.grid(row=1, column=0)
add_button.config(width=15)

# Create remove button
remove_button = tk.Button(root, text="Remove", command=on_remove)
remove_button.grid(row=1, column=1)
remove_button.config(width=15)

# Create change button
change_button = tk.Button(root, text="Change", command=on_change)
change_button.grid(row=1, column=2)
change_button.config(width=15)

movie_var.set(movie_list[0])
movie_var.trace("w", on_select)

# Create a Treeview table
table = ttk.Treeview(root)
table["columns"] = ("Name", "Rating")
table.column("#0", width=0, stretch=False)
table.column("Name", width=480, stretch=False)
table.column("Rating", width=50, stretch=False)
table.heading("Name", text="Name")
table.heading("Rating", text="Rating")

# Insert data from the CSV file into the table
df = pd.read_csv("anime.csv")
for index, row in df.iterrows():
    table.insert("", "end", text=index, values=(row["Name"], row["Rating"]))

# Add the table to the main window
table.grid(columnspan=4)
table.configure(height=500)

def refresh_table():
    # Read the csv file with new data
    df = pd.read_csv("anime.csv")
    # delete all existing rows
    for i in table.get_children():
        table.delete(i)
    # insert new data
    for index, row in df.iterrows():
        table.insert("", "end", text=index, values=(row["Name"], row["Rating"]))

root.mainloop()