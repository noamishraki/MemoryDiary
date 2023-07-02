from typing import List

import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import seaborn as sns
import numpy as np


file_name =r'139_Daily_Diary_Summary.xlsx'
treatment_dates = r'dates139.xlsx'

def plot_graph(df:pd.DataFrame, treatment_dates: List, count_of_interest: str):
    df = df.drop(df.index[0])
    # Assuming you have imported necessary libraries and loaded the data frame (df)
    colors = ['green' if date in treatment_dates else 'blue' for date in df['Date']]

    plt.bar(df['Date'], df[count_of_interest], color=colors)
    i=1
    for date, treatment in zip(df['Date'], df[count_of_interest]):
        if date in treatment_dates:
            plt.text(date, treatment, i, ha='center', va='bottom')
            i+=1
        
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


    plt.xticks(rotation=90)
    # Add labels and legends
    plt.xlabel('Date')
    plt.ylabel(count_of_interest)
    plt.legend()

    # Display the plot
    plt.show()

# plot_graph(file_name, treatment_dates,'Count_Target')
# plot_graph(file_name, treatment_dates,'Count_Nontarget')
# plot_graph(file_name, treatment_dates,'Count_Total')