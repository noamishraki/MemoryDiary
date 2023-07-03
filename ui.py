from tkinter import Tk, Label, Button, filedialog, messagebox
from errors import DateBeforeDataDates
from tkcalendar import DateEntry
import pandas as pd
import fake_api

file_selected = False


def on_click():
    if not file_selected:
        messagebox.showinfo("Info", "Please select a file first.")
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
        fake_api.get_graph_by_dates(dates)
    except DateBeforeDataDates:
        messagebox.showerror("Error", "The provided dates are before the dates provided in the file")
    # except Exception as e:
    #     print(e)
    #     messagebox.showerror("Error", "Something went wrong, please try again")

    return dates


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

date_labels = []
date_entries = []
for i in range(1, 6):
    label = Label(window, text=f"Treatment session {i} date:")
    label.pack()
    date_labels.append(label)

    entry = DateEntry(window, date_pattern="dd/mm/yyyy")
    entry.pack()
    date_entries.append(entry)

get_dates_button = Button(window, text="Analyze", command=lambda: print("Dates:", on_click()))
get_dates_button.pack()

# Start the GUI event loop
window.mainloop()
