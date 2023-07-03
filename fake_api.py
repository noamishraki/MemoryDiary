from typing import List
import pandas as pd

from logics import filter_data, validators, visualizations, excel_outputs

memories_df: pd.DataFrame = None
COUNT_OF_INTEREST = ['Count_Target', 'Count_Nontarget', 'Count_Total']


def get_graph_by_dates(treatment_dates: List, folder_path):
    df = filter_data.run_filter_flow(memories_df)

    validators.validate_range(treatment_dates, df['Date'].min())
    visualizations.plot_all_graphs(df, treatment_dates, COUNT_OF_INTEREST, folder_path)
    # excel_outputs.weekly_count_zeros(df, treatment_dates)
    # excel_outputs.weekly_sums(df,treatment_dates)
