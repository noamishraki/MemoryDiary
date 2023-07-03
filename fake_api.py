from typing import List
import pandas as pd

from logics import filter_data, validators, visualizations

memories_df: pd.DataFrame = None


def get_graph_by_dates(treatment_dates: List):
    df = filter_data.run_filter_flow(memories_df)

    validators.validate_range(treatment_dates, df['Date'].min())
    count_of_interest_list = ['Count_Target', 'Count_Nontarget', 'Count_Total']
    visualizations.plot_all_graphs(df, treatment_dates, count_of_interest_list)