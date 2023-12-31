from typing import List

import pandas as pd

from logics import excel_outputs, filter_data, validators, visualizations

memories_df: pd.DataFrame = None
COUNT_OF_INTEREST = ["Count_Target", "Count_Nontarget", "Count_Total"]


def run_statistics_flow(treatment_dates: List, folder_path: str):
    """
    Run the statistics flow.

    Args:
        treatment_dates (List): A list of treatment dates in datetime.Date format.
        folder_path (str): The path where the generated output files will be saved.

    Returns:
        None
    """
    df = filter_data.run_filter_flow(memories_df)

    validators.validate_range(treatment_dates, df["Date"].min())
    visualizations.plot_all_graphs(df, treatment_dates, COUNT_OF_INTEREST, folder_path)
    excel_outputs.weekly_count_zeros(df, treatment_dates, folder_path)
    excel_outputs.weekly_sums(df, treatment_dates, folder_path)
