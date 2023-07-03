from typing import List

import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.linear_model import LinearRegression
import numpy as np


def plot_graph(df: pd.DataFrame, treatment_dates: List, count_of_interest: str):
    # Assuming you have imported necessary libraries and loaded the data frame (df)
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
    plt.show()


def average_per_week(df: pd.DataFrame, dates:List, count_of_interest: str):
    #treatment_dates=pd.read_excel('dates139.xlsx')
    #dates=treatment_dates
    dates=pd.DataFrame(dates)
    #treatment_dates=treatment_dates.dt.strftime('%y/%m/%d')

    file_name='139_Daily_Diary_Summary.xlsx'
    count_of_interest = 'Count_Target'
    df = pd.read_excel(file_name)
    #date_list = pd.Series(df['Date'])


    # Calculate the start date as one week before the first date in the series
    start_date = dates.iloc[0] - pd.DateOffset(weeks=1)
    end_date = dates.iloc[-1] + pd.DateOffset(weeks=1)

    print(start_date)
    first_row=df['Date'][df['Date']==start_date[0]].index.astype(int)[0]
    if df['Date'].any==end_date[0]:
        last_row=df['Date'][df['Date']==end_date[0]].index.astype(int)[0]
    else:
        last_row=df['Date'].index[-1]

    narrowed_df=df[first_row:last_row+1]


    narrowed_df.set_index(narrowed_df['Date'], inplace=True)
    # Resample the data by week and calculate the mean
    weekly_average = narrowed_df[count_of_interest].resample('W').mean()



    #Reset the index to make 'Date' a column again
    weekly_average = weekly_average.reset_index()
    dates = weekly_average['Date'].tolist()
    weeks = weekly_average['Date']
    averages = weekly_average[count_of_interest].tolist()
    print(averages)

    #Create the bar plot
    plt.bar(weekly_average['Date'], weekly_average[count_of_interest], width=6.5)
    plt.xticks(weeks, rotation=90)
    plt.xlabel('Week')
    plt.ylabel(f'Average {count_of_interest}')
    plt.title(f'Weekly Average {count_of_interest}')
    plt.show()
