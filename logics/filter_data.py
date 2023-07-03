from typing import Union

import numpy as np
import pandas as pd


def count_occurrences(df: pd.DataFrame, value: Union[int, float]) -> pd.Series:
    """
    Count the occurrences of a specific value in each row of the DataFrame.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        value (Union[int, float]): The value to count occurrences of.

    Returns:
        pd.Series: A Pandas Series containing the count of occurrences of the specified value for each row.
    """
    return df.eq(value).sum(axis=1)


def remove_type_3(df: pd.DataFrame, max_ideas: int) -> pd.DataFrame:
    """
    Remove data from the DataFrame where the 'Type' column is equal to 3.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        max_ideas (int): The maximum number of ideas.

    Returns:
        pd.DataFrame: The DataFrame with data removed where 'Type' column is equal to 3.
    """
    for i in range(1, max_ideas + 1):
        type_column_name = f"{i}_Type"
        if type_column_name not in df.columns:
            continue
        mask = df[type_column_name] == 3
        for suffix in ["_When", "_Type", "_Content", "_Distress", "_Vividness"]:
            column_name = f"{i}{suffix}"
            if column_name in df.columns:
                df.loc[mask, column_name] = np.nan
    return df


def run_filter_flow(memories_df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform a series of data transformations and calculations on the DataFrame.

    Parameters:
        memories_df (pd.DataFrame): The DataFrame containing the data.

    Returns:
        pd.DataFrame: The resulting DataFrame after transformations and calculations.
    """
    memories_df = memories_df.drop(0)
    max_ideas = max(memories_df["Amount"])
    memories_df = remove_type_3(memories_df, max_ideas)

    new_df = pd.DataFrame()
    new_df["Count_Target"] = count_occurrences(memories_df.filter(like="_Content"), 1)
    new_df["Count_Nontarget"] = count_occurrences(
        memories_df.filter(like="_Content"), 2
    )
    new_df["Count_Total"] = new_df["Count_Target"] + new_df["Count_Nontarget"]
    new_df["Date"] = pd.to_datetime(memories_df["StartDate"]).dt.date

    grouped_mat = (
        new_df.groupby("Date")
        .agg({"Count_Total": "sum", "Count_Target": "sum", "Count_Nontarget": "sum"})
        .reset_index()
    )

    grouped_mat.to_excel("memories_count.xlsx", index=False)

    return grouped_mat
