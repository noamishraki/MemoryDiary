import pandas as pd

from logics.utils import get_unique


def weekly_sums(df: pd.DataFrame, dates: list, target_folder: str) -> None:
    """
    Calculate weekly sums and averages based on the provided DataFrame and dates.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the data to be analyzed.
        dates (list): A list of date strings in ascending order representing the weekly intervals.
        target_folder (str): The path to the target folder where the results will be saved.

    Returns:
        None: The function does not return any value, but it writes the results to an Excel file.

    The function calculates the sum of specific columns in the DataFrame over each weekly interval and
    calculates the average per day for each interval. The results are stored in a new DataFrame and
    saved to an Excel file in the specified target folder.

    Note: The DataFrame should have columns named 'Date', 'Count_Target', 'Count_Nontarget', and 'Count_Total'.
    """
    # Convert the first and last dates in the list to Timestamp objects
    last_date = pd.Timestamp(dates[-1])
    # Calculate the start and end dates of the desired range
    end_date = last_date + pd.Timedelta(days=7)
    # Filter the DataFrame based on the date range

    # Create a new DataFrame to store the results
    result_df = pd.DataFrame(
        columns=[
            "Start Date",
            "End Date",
            "Gap Between Sessions",
            "Average Per Day - Target",
            "Average Per Day - Nontarget",
            "Average Per Day - Total",
        ]
    )

    # Iterate over the dates in the list
    for i in range(len(dates) - 1):
        # Calculate the start and end dates for each gap
        start_date = pd.Timestamp(dates[i])
        end_date = pd.Timestamp(dates[i + 1])

        # Filter the DataFrame based on the start and end dates for each gap
        filtered_df = df[(df["Date"] >= start_date) & (df["Date"] < end_date)]

        # Calculate the number of days between the start and end dates for each gap
        num_days = (end_date - start_date).days

        # Calculate the average values for each week, normalized by the number of days
        average_target = filtered_df["Count_Target"].sum() / num_days
        average_nontarget = filtered_df["Count_Nontarget"].sum() / num_days
        average_total = filtered_df["Count_Total"].sum() / num_days

        # Append the results to the new DataFrame
        result_df = pd.concat(
            [
                result_df,
                pd.DataFrame(
                    {
                        "Start Date": [start_date],
                        "End Date": [end_date],
                        "Gap Between Sessions": [num_days],
                        "Average Per Day - Target": [average_target],
                        "Average Per Day - Nontarget": [average_nontarget],
                        "Average Per Day - Total": [average_total],
                    }
                ),
            ]
        )

    # Calculate the last gap between the last session date and the end date
    last_start_date = pd.Timestamp(dates[-1])
    last_end_date = end_date

    last_filtered_df = df[
        (df["Date"] >= last_start_date) & (df["Date"] <= last_end_date)
    ]
    last_num_days = (last_end_date - last_start_date).days

    # Check if last_num_days is not zero
    if last_num_days != 0:
        last_average_target = last_filtered_df["Count_Target"].sum() / last_num_days
        last_average_nontarget = (
            last_filtered_df["Count_Nontarget"].sum() / last_num_days
        )
        last_average_total = last_filtered_df["Count_Total"].sum() / last_num_days
    else:  # If last_num_days is zero
        last_average_target = None
        last_average_nontarget = None
        last_average_total = None

    result_df = pd.concat(
        [
            result_df,
            pd.DataFrame(
                {
                    "Start Date": [last_start_date],
                    "End Date": [last_end_date],
                    "Gap Between Sessions": [last_num_days],
                    "Average Per Day - Target": [last_average_target],
                    "Average Per Day - Nontarget": [last_average_nontarget],
                    "Average Per Day - Total": [last_average_total],
                }
            ),
        ]
    )

    # Reset the index of the result DataFrame
    result_df = result_df.reset_index(drop=True)

    # Write the new DataFrame to an Excel file
    result_df.to_excel(
        f"{target_folder}/Weekly_Diary_Summary-{get_unique()}.xlsx", index=False
    )


def weekly_count_zeros(df: pd.DataFrame, dates: list, target_folder: str) -> None:
    """
    Count the number of zero values for specific columns over weekly intervals.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the data to be analyzed.
        dates (list): A list of date strings in ascending order representing the weekly intervals.
        target_folder (str): The path to the target folder where the results will be saved.

    Returns:
        None: The function does not return any value, but it writes the results to an Excel file.

    The function counts the occurrences of zero values in specific columns of the DataFrame over each weekly interval.
    The results are stored in a new DataFrame and saved to an Excel file in the specified target folder.

    Note: The DataFrame should have columns named 'Date', 'Count_Target', 'Count_Nontarget', and 'Count_Total'.
    """
    # Convert the first and last dates in the list to Timestamp objects
    last_date = pd.Timestamp(dates[-1])
    # Calculate the start and end dates of the desired range
    end_date = last_date + pd.Timedelta(days=7)

    # Create a new DataFrame to store the results
    result_df = pd.DataFrame(
        columns=["Week", "Zero Days_Target", "Zero Days_Nontarget", "Zero Days_Total"]
    )

    # Iterate over the dates in the list
    for i in range(len(dates) - 1):
        # Calculate the start and end dates for each week
        start_date = pd.Timestamp(dates[i])
        end_date = pd.Timestamp(dates[i + 1])

        # Filter the DataFrame based on the start and end dates for each week
        filtered_df = df[(df["Date"] >= start_date) & (df["Date"] < end_date)]

        # Count the number of days with zero values for each variable
        zero_days_target = (filtered_df["Count_Target"] == 0).sum()
        zero_days_nontarget = (filtered_df["Count_Nontarget"] == 0).sum()
        zero_days_total = (filtered_df["Count_Total"] == 0).sum()

        # Create a temporary DataFrame for the current week
        week_df = pd.DataFrame(
            {
                "Week": [start_date],
                "Zero Days_Target": [zero_days_target],
                "Zero Days_Nontarget": [zero_days_nontarget],
                "Zero Days_Total": [zero_days_total],
            }
        )

        # Concatenate the temporary DataFrame with the result DataFrame
        result_df = pd.concat([result_df, week_df], ignore_index=True)

    # Calculate the last week between the last date and the end date
    last_start_date = pd.Timestamp(dates[-1])
    last_end_date = end_date

    last_filtered_df = df[
        (df["Date"] >= last_start_date) & (df["Date"] <= last_end_date)
    ]
    last_zero_days_target = (last_filtered_df["Count_Target"] == 0).sum()
    last_zero_days_nontarget = (last_filtered_df["Count_Nontarget"] == 0).sum()
    last_zero_days_total = (last_filtered_df["Count_Total"] == 0).sum()

    # Create a temporary DataFrame for the last week
    last_week_df = pd.DataFrame(
        {
            "Week": [last_start_date],
            "Zero Days_Target": [last_zero_days_target],
            "Zero Days_Nontarget": [last_zero_days_nontarget],
            "Zero Days_Total": [last_zero_days_total],
        }
    )

    # Concatenate the temporary DataFrame for the last week with the result DataFrame
    result_df = pd.concat([result_df, last_week_df], ignore_index=True)

    result_df.to_excel(
        f"{target_folder}/Weekly_Summary_zeros-{get_unique()}.xlsx", index=False
    )
