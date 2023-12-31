from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

from logics.utils import get_unique


def plot_graph(df: pd.DataFrame, treatment_dates: List, count_of_interest: str):
    colors = ["green" if date in treatment_dates else "blue" for date in df["Date"]]

    plt.bar(df["Date"], df[count_of_interest], color=colors)
    i = 1
    for date, treatment in zip(df["Date"], df[count_of_interest]):
        if date in treatment_dates:
            plt.text(date, treatment, i, ha="center", va="bottom")
            i += 1

    # Convert the date column to numeric values for regression
    date_values = np.arange(len(df["Date"]))

    # Reshape the date values to fit the input requirements of LinearRegression
    x1 = date_values.reshape(-1, 1)
    y1 = df[count_of_interest]

    # Perform linear regression
    regressor = LinearRegression()
    regressor.fit(x1, y1)

    # Predict the trend line values
    trend_y1 = regressor.predict(x1)

    # Plot the trend line
    plt.plot(df["Date"], trend_y1, color="red", label="Trend Line")

    plt.ylim(0, None)
    plt.xticks(rotation=90)
    # Add labels and legends
    plt.xlabel("Date")
    plt.ylabel(count_of_interest)
    plt.title(f"{count_of_interest} Per day")
    plt.legend()

    # Display the plot
    return plt


def average_per_week(df: pd.DataFrame, treatment_dates: List, count_of_interest: str):
    """
    Plot a bar graph showing the average value for each period defined by the treatment_dates list.

    Args:
        df (pd.DataFrame): The input DataFrame containing the data.
        treatment_dates (List): List of treatment dates.
        count_of_interest (str): The column in the DataFrame to plot.

    Returns:
        plt.figure: The matplotlib figure object with the plot.
    """
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index(df["Date"], inplace=True)

    # Calculate averages for each period defined by treatment_dates
    averages = []
    labels = []

    # Week before the first treatment date
    start_date = min(treatment_dates) - pd.Timedelta(days=7)
    end_date = treatment_dates[0]
    filtered_df = df.loc[start_date:end_date]
    average = filtered_df[count_of_interest].mean()
    averages.append(average)
    labels.append(start_date.strftime('%Y-%m-%d'))

    # Between each pair of consecutive treatment dates
    for i in range(len(treatment_dates) - 1):
        start_date = treatment_dates[i]
        end_date = treatment_dates[i + 1] - pd.Timedelta(days=1)  # Exclude the last date
        filtered_df = df.loc[start_date:end_date]
        average = filtered_df[count_of_interest].mean()
        averages.append(average)

    # Week after the last treatment date
    start_date = treatment_dates[-1]
    end_date = max(treatment_dates) + pd.Timedelta(days=7)
    filtered_df = df.loc[start_date:end_date]
    average = filtered_df[count_of_interest].mean()
    averages.append(average)

    for date in treatment_dates:
        labels.append(date)
    # Create the bar plot
    plt.bar(range(1, len(averages) + 1), averages)
    plt.xticks(range(1, len(averages) + 1), labels, rotation=45)
    plt.xlabel("Period")
    plt.ylabel(f"Average {count_of_interest}")
    plt.title(f"Weekly Average {count_of_interest}")
    return plt


def plot_all_graphs(
    df: pd.DataFrame, treatment_dates: List, count_of_interest: List, saving_folder
):
    """
    Plot all graphs in a 2x3 grid of subplots and save them to a specific folder.

    Args:
        df (pd.DataFrame): The input DataFrame containing the data.
        treatment_dates (List): List of treatment dates.
        count_of_interest (List): List of columns in the DataFrame to plot.
        saving_folder (str): The path of the folder where the graphs will be saved.

    Returns:
        None
    """
    # Create a 2x3 grid of subplots
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    # Call each function and plot the graphs
    graph_funcs = [plot_graph, average_per_week]

    for i, func in enumerate(graph_funcs):
        for j, coi in enumerate(count_of_interest):
            plt.sca(axes[i, j])
            func(df, treatment_dates, coi)

    # Display the plot
    plt.tight_layout()
    plt.savefig(f"{saving_folder}/visualizations-{get_unique()}.pdf")
    plt.show()