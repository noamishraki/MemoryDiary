from typing import List

import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from datetime import datetime
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
    plt.title(count_of_interest)
    plt.legend()

    # Display the plot
    return plt


def average_per_week(df: pd.DataFrame, treatment_dates: List, count_of_interest: str):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index(df['Date'], inplace=True)

    # # Resample the data by week and calculate the mean
    weekly_average = df[count_of_interest].resample('W').mean()

    # Reset the index to make 'Date' a column again
    weekly_average = weekly_average.reset_index()
    # dates = weekly_average['Date'].tolist()
    weeks = weekly_average['Date']
    averages = weekly_average[count_of_interest].tolist()

    # Create the bar plot
    plt.bar(weekly_average['Date'], weekly_average[count_of_interest], width=6.5)
    plt.xticks(weeks, rotation=90)
    plt.xlabel('Week')
    plt.ylabel(f'Average {count_of_interest}')
    plt.title(f'Weekly Average {count_of_interest}')
    return plt


def plot_all_graphs(df: pd.DataFrame, treatment_dates: List, count_of_interest):
    # Create a 2x3 grid of subplots
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    # Call each function and plot the graphs
    graph_funcs = [plot_graph, average_per_week]
    titles = ['Original Data', 'Weekly Average']

    for i, func in enumerate(graph_funcs):
        plt.sca(axes[i, 0])
        func(df, treatment_dates, count_of_interest)

        plt.sca(axes[i, 1])
        func(df, treatment_dates, count_of_interest)

        plt.sca(axes[i, 2])
        func(df, treatment_dates, count_of_interest)

        plt.subplots_adjust(wspace=0.4)

    # Set common title for each row
    axes[0, 0].set_title('Treatment Dates')
    axes[0, 1].set_title('Non-Treatment Dates')
    axes[0, 2].set_title('All Dates')

    # Display the plot
    plt.show()
