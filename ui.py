import os
from tkinter import Tk, Label, Button, filedialog, messagebox
from errors import DateBeforeDataDates
from tkcalendar import DateEntry
import pandas as pd
import fake_api

file_selected = False
folder_path = None


def on_click():
    if not file_selected:
        messagebox.showinfo("Info", "Please select a file first.")
        return
    if not folder_path:
        messagebox.showinfo("Info", "Please select a folder first.")
        return
    dates = []
    for entry in date_entries:
        date = entry.get_date()
        if date:
            dates.append(date)
        else:
            messagebox.showerror("Error", "Invalid date format. Please use the date picker to select a date.")
            return []

    # Verify the order of dates
    for i in range(len(dates) - 1):
        if dates[i] >= dates[i + 1]:
            messagebox.showerror("Error", "Dates are not in the correct order.")
            return []

    try:
        graphs = fake_api.get_graph_by_dates(dates, folder_path)
    except DateBeforeDataDates:
        messagebox.showerror("Error", "The provided dates are before the dates provided in the file")


def open_file():
    global file_selected

    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xls *.xlsx"), ("CSV files", "*.csv")])
    if file_path:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xls') or file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)

        if 'StartDate' in df.columns:
            messagebox.showinfo("Success", "File loaded successfully.")
            file_selected = True
            fake_api.memories_df = df
        else:
            messagebox.showerror("Error", "The file does not contain a 'StartDate' column.")


def select_folder():
    global folder_path
    folder_path = filedialog.askdirectory()
    if folder_path:
        messagebox.showinfo("Success", "Folder selected successfully.")
    else:
        messagebox.showerror("Error", "No folder selected.")


# Create the main window
window = Tk()
window.title("Inputs")
window.geometry("400x300")  # Set the size of the window

# Customize the appearance
window.configure(bg="white")  # Set the background color

# Define custom font
font_label = ("Arial", 12, "bold")
font_button = ("Arial", 10)

select_file_label = Label(window, text="Select a data file:")
select_file_label.pack()

select_file_button = Button(window, text="Browse", command=open_file)
select_file_button.pack()

select_folder_button = Button(window, text="Select Folder", command=select_folder)
select_folder_button.pack()

date_labels = []
date_entries = []
for i in range(1, 6):
    label = Label(window, text=f"Treatment session {i} date:")
    label.pack()
    date_labels.append(label)

    entry = DateEntry(window, date_pattern="dd/mm/yyyy")
    entry.pack()
    date_entries.append(entry)

get_dates_button = Button(window, text="Analyze", command=on_click)
get_dates_button.pack()

# Start the GUI event loop
window.mainloop()
