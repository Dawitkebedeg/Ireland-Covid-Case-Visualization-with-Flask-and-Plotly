# pip install flask_bootstrap
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import pandas as pd
import plotly.express as px
from covid_data import get_table_data
from covid_data import get_tidy_data


app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.get("/")
def index():
    table_data = get_table_data()
    return render_template(
        "index.html",
        table_data=table_data.to_html(
            classes=["table", "table-striped", "table-bordered"], index=False
        ),
        page_title="Home",
        card_title="Covid Data",
    )


@app.route("/visuals", methods=["GET", "POST"])
def visuals():
    if request.method == "POST":
        tidy_data = get_tidy_data()

        graph_type = request.form.get("graph_type")
        if graph_type == "confirmed_death":
            fig = px.histogram(
                tidy_data,
                x="Date",
                y="ConfirmedCovidDeaths",
                histfunc="avg",
                title="Confirmed Covid Deaths",
                labels={"Date": "Date", "ConfirmedCovidDeaths": "Number of Deaths"},
                color_discrete_sequence=["blue"],
            )
            fig.update_traces(xbins_size="M1")

            confirmed_death = fig.to_html(full_html=False)
            return confirmed_death

        elif graph_type == "case_by_gender":
            fig = px.line(
                tidy_data,
                x="StatisticsProfileDate",
                y="CasebyGender",
                color="Gender",
                labels={"StatisticsProfileDate": "Profile Date"},
                title="Covid Case by Gender",
                category_orders={"Gender": ["Male", "Female", "Unknown"]},
            )
            fig = fig.update_traces(line=dict(width=3))
            case_by_gender = fig.to_html(full_html=False)
            return case_by_gender

        elif graph_type == "hospilization_by_age_group":
            fig = px.line(
                tidy_data,
                x="StatisticsProfileDate",
                y="HospitalisedCases",
                color="HospitalisedAgeGroup",
                labels={
                    "StatisticsProfileDate": "Profile Date",
                    "HospitalisedCases": "Hospitalised Cases",
                },
                title="Hospitalization by Age Group",
                category_orders={
                    "HospitalisedAgeGroup": [
                        "1to4",
                        "5to14",
                        "15to24",
                        "25to34",
                        "35to44",
                        "45to54",
                        "55to64",
                        "65to74",
                        "75to84",
                        "85up",
                    ]
                },
            )

            fig = fig.update_traces(line=dict(width=3))
            hospilization_by_age_group = fig.to_html(full_html=False)
            return hospilization_by_age_group

        elif graph_type == "covid_cases_by_median_age":
            fig = px.scatter(
                tidy_data,
                x="StatisticsProfileDate",
                y="Median_Age",
                color="Median_Age",
                title="Covid Cases by Median Age",
                labels={
                    "StatisticsProfileDate": "Profile Date",
                    "Median_Age": "Median Age",
                },
            )
            covid_cases_by_median_age = fig.to_html(full_html=False)
            return covid_cases_by_median_age

        elif graph_type == "icu_hospitalized_ratio":
            # Get the maximum values for the HospitalisedCovidCases and RequiringICUCovidCases columns
            # Since the data is in cumulative sums, this is the overall ratio since covid came
            hospitalized_cases_max = tidy_data["HospitalisedCovidCases"].max()
            icu_cases_max = tidy_data["RequiringICUCovidCases"].max()

            fig = px.pie(
                [hospitalized_cases_max, icu_cases_max],
                values=[hospitalized_cases_max, icu_cases_max],
                names=["Hospitalized Cases", "ICU Cases"],
                title="ICU Ratio",
            )
            icu_hospitalized_ratio = fig.to_html(full_html=False)
            return icu_hospitalized_ratio

        else:
            return "Please Select graph type!"

    elif request.method == "GET":
        return render_template(
            "visuals.html",
            page_title="visualizations",
            card_title="Please, select the visualization you want!",
        )


if __name__ == "__main__":
    app.run(debug=True)
