import pandas as pd


def get_table_data():
    table_data = pd.read_csv("static/covid_data.csv")
    table_data.StatisticsProfileDate = pd.to_datetime(
        table_data.StatisticsProfileDate
    ).dt.tz_localize(None)
    table_data.CovidCasesConfirmed = table_data.CovidCasesConfirmed.astype(int)
    table_data.HospitalisedCovidCases = table_data.HospitalisedCovidCases.astype(int)
    table_data.RequiringICUCovidCases = table_data.RequiringICUCovidCases.astype(int)
    table_data.DeathsCumulative_DOD = table_data.DeathsCumulative_DOD.astype(int)
    column_names = [
        "StatisticsProfileDate",
        "CovidCasesConfirmed",
        "HospitalisedCovidCases",
        "RequiringICUCovidCases",
        "DeathsCumulative_DOD",
    ]

    table_data = table_data[column_names]

    return table_data


def get_tidy_data():
    tidy_data = pd.read_csv("static/covid_tidy_data.csv")
    tidy_data.Date = pd.to_datetime(tidy_data.Date, errors="coerce")
    tidy_data.StatisticsProfileDate = pd.to_datetime(
        tidy_data.StatisticsProfileDate, errors="coerce"
    )

    return tidy_data
