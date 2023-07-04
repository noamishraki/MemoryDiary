import pandas as pd

from logics.filter_data import remove_type_3, run_filter_flow


def test_identical_keys():
    test_df = pd.read_excel("tests/memories_count.xlsx")
    df = run_filter_flow(pd.read_excel("tests/Intrusions.xlsx"))

    assert list(df) == list(test_df)


def test_df_values():
    test_df = pd.read_excel("tests/memories_count.xlsx")
    df = run_filter_flow(pd.read_excel("tests/Intrusions.xlsx"))
    test_df["Date"] = pd.to_datetime(test_df["Date"]).dt.date

    for key in list(test_df):
        assert list(df[key]) == list(test_df[key])


def test_remove_type_3():
    original_df = pd.read_excel("tests/Intrusions.xlsx")
    original_df = original_df.drop(0)
    max_ideas = max(original_df["Amount"])
    df = remove_type_3(original_df, max_ideas)

    for i in range(1, max_ideas + 1):
        assert not (df[f"{i}_Type"] == 3).any()
