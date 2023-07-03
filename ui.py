from tkinter import Button, Label, Tk, filedialog, messagebox

import pandas as pd
from tkcalendar import DateEntry

import fake_api
from errors import DateBeforeDataDates

file_selected = False
folder_path = None


def on_click():
    """
    Event handler for the 'Analyze' button click.

    This function is called when the 'Analyze' button is clicked. It reads the selected dates from the date entries,
    validates the dates, and runs the statistics flow to generate statistics and save them to the selected folder.

    Returns:
        None
    """
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
            messagebox.showerror(
                "Error",
                "Invalid date format. Please use the date picker to select a date.",
            )
            return []

    # Verify the order of dates
    for i in range(len(dates) - 1):
        if dates[i] >= dates[i + 1]:
            messagebox.showerror("Error", "Dates are not in the correct order.")
            return []

    try:
        graphs = fake_api.run_statistics_flow(dates, folder_path)
    except DateBeforeDataDates:
        messagebox.showerror(
            "Error", "The provided dates are before the dates provided in the file"
        )
    except PermissionError:
        messagebox.showerror(
            "Error", "No permission to folder, please choose different one"
        )
    except:
        messagebox.showerror("Error", "Something went wrong")


def open_file():
    """
    Event handler for the 'Browse' button click to open a data file.

    This function is called when the 'Browse' button is clicked. It opens a file dialog to select a data file (Excel or CSV).
    If the file contains a 'StartDate' column, it loads the data and sets the 'file_selected' flag to True.

    Returns:
        None
    """
    global file_selected

    file_path = filedialog.askopenfilename(
        filetypes=[("Excel files", "*.xls *.xlsx"), ("CSV files", "*.csv")]
    )
    if file_path:
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_path.endswith(".xls") or file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)

        if "StartDate" in df.columns:
            messagebox.showinfo("Success", "File loaded successfully.")
            file_selected = True
            fake_api.memories_df = df
        else:
            messagebox.showerror(
                "Error", "The file does not contain a 'StartDate' column."
            )


def select_folder():
    """
    Event handler for the 'Select Folder' button click.

    This function is called when the 'Select Folder' button is clicked. It opens a folder dialog to select a folder
    where the generated graphs will be saved. The selected folder path is stored in the 'folder_path' variable.

    Returns:
        None
    """
    global folder_path
    folder_path = filedialog.askdirectory()
    if folder_path:
        messagebox.showinfo("Success", "Folder selected successfully.")
    else:
        messagebox.showerror("Error", "No folder selected.")


# Create the main window
window = Tk()
window.title("Inputs")
window.geometry("600x400")  # Set the size of the window

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

