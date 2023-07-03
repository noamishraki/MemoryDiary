from uuid import uuid4
from typing import List

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np


def plot_graph(df: pd.DataFrame, treatment_dates: List, count_of_interest: str):
    colors = ['green' if date in treatment_dates else 'blue' for date in df['Date']]

    plt.bar(df['Date'], df[count_of_interest], color=colors)
    i = 1
    for date, treatment in zip(df['Date'], df[count_of_interest]):
        if date in treatment_dates:
            plt.text(date, treatment, i, ha='center', va='bottom')
            i += 1

    # Convert the date column to numeric values for regression
    date_values = np.arange(len(df['Date']))

    # Reshape the date values to fit the input requirements of LinearRegression
    X1 = date_values.reshape(-1, 1)
    y1 = df[count_of_interest]

    # Perform linear regression
    regressor = LinearRegression()
    regressor.fit(X1, y1)

    # Predict the trend line values
    trend_y1 = regressor.predict(X1)

    # Plot the trend line
    plt.plot(df['Date'], trend_y1, color='red', label='Trend Line')

    plt.ylim(0, None)
    plt.xticks(rotation=90)
    # Add labels and legends
    plt.xlabel('Date')
    plt.ylabel(count_of_interest)
    plt.title(f"{count_of_interest} Per day")
    plt.legend()

    # Display the plot
    return plt

def average_per_week(df: pd.DataFrame, treatment_dates: List, count_of_interest: str):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index(df['Date'], inplace=True)

    # Filter data to include only weeks between (the week before the first date) and (the week after the last date)
    start_date = min(treatment_dates) - pd.Timedelta(days=7)
    end_date = max(treatment_dates) + pd.Timedelta(days=7)
    filtered_df = df.loc[start_date:end_date]

    # Resample the filtered data by week and calculate the mean
    weekly_average = filtered_df[count_of_interest].resample('W').mean()

    # Reset the index to make 'Date' a column again
    weekly_average = weekly_average.reset_index()

    # Create the bar plot
    plt.bar(weekly_average['Date'], weekly_average[count_of_interest], width=6.5)
    plt.xticks(weekly_average['Date'], rotation=90)
    plt.xlabel('Week')
    plt.ylabel(f'Average {count_of_interest}')
    plt.title(f'Weekly Average {count_of_interest}')
    return plt


def plot_all_graphs(df: pd.DataFrame, treatment_dates: List, count_of_interest: List, saving_folder):
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
    plt.savefig(f"{saving_folder}/visualizations-{str(uuid4()).split('-')[-1]}")
    plt.show()