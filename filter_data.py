from typing import List, Union

import pandas as pd


def count_values(df: pd.DataFrame, number_of_first_cols: int, value: Union[int, float]) -> int:
    return df.iloc[:, :number_of_first_cols].eq(value).sum(axis=1)


def get_filtered_pd(df: pd.DataFrame, cols_names: List) -> pd.DataFrame:
    return df[cols_names].copy()


def run_filter_flow(memories_df: pd.DataFrame) -> pd.DataFrame:
    memories_df = memories_df.drop(0)
    max_ideas = max(memories_df["Amount"])
    new_column_names = [f"{i}_Content" for i in range(1, max_ideas + 1)]
    new_column_names.extend(["Amount", "StartDate"])

    filtered_df = get_filtered_pd(memories_df, new_column_names)

    new_df = pd.DataFrame()

    new_df['Count_Target'] = count_values(filtered_df, max_ideas, 1)
    new_df['Count_Nontarget'] = count_values(filtered_df, max_ideas, 2)
    new_df["Count_Total"] = filtered_df["Amount"]
    new_df["Date"] = pd.to_datetime(filtered_df["StartDate"]).dt.date

    # Group by the 'Date' column and sum the values in each group
    grouped_mat = new_df.groupby('Date').agg({
        'Count_Total': 'sum',
        'Count_Target': 'sum',
        'Count_Nontarget': 'sum'
    }).reset_index()

    grouped_mat.to_excel("memories_count.xlsx", index=False)
    return grouped_mat
