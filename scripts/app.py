import dash
from dash import dcc, html, Input, Output
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Initialize the app
app = dash.Dash(__name__)
server = app.server  # for deployment


# Loading the data 
exp_clean = pd.read_csv("data/cleaned/Cleaned_health_spending.csv")
life_clean = pd.read_csv("data/cleaned/Cleaned_life_expectancy.csv")
mort_clean = pd.read_csv("data/cleaned/Cleaned_mortality_rate.csv")


# colour table
colours = {
  'Netherlands': 'Orange', 
  'Sweden': 'yellow', 
  'Belgium': 'black',
  'Norway': 'Red', 
  'France': 'Blue', 
  'Italy': 'green'  
}

# --- App layout ---
app.layout = html.Div([
    
    html.H1("European Public Health Dashboard"),

    html.Label("Select Countries:"),
    dcc.Dropdown(
        options=[{"label": c, "value": c} for c in sorted(life_clean["Country Name"].unique())],
        value=["Netherlands", "Sweden", "Belgium","Norway", "France", "Italy"],
        multi=True,
        id="country-dropdown"
    ),

    html.Br(),

    html.Div([
        dcc.Graph(id="life-plot", style={"width": "100%", "height": "400px"}),
        dcc.Graph(id="spending-plot", style={"width": "100%", "height": "400px"}),
        dcc.Graph(id="mortality-plot", style={"width": "100%", "height": "400px"})
    ])
])

# --- Callbacks to update graphs ---
@app.callback(
    Output("life-plot", "figure"),
    Output("spending-plot", "figure"),
    Output("mortality-plot", "figure"),
    Input("country-dropdown", "value")
)
def update_graphs(selected_countries):
    # Life Expectancy
    filtered_life = life_clean[life_clean["Country Name"].isin(selected_countries)]
    fig1 = px.line(
        filtered_life,
        x= "Year", y= "Life Expectancy",
        color='Country Name',
        color_discrete_map= colours,
        facet_col= 'Country Name',
        facet_col_wrap=3,
        labels= {'Year':'Year', 'Life Expectancy': 'Life Expectancy'},
        line_group="Gender",
        title="Life Expectancy Trends by Country and Gender"
    )

    fig1.update_layout(height=2000, width=6000)
    fig1.update_traces(marker=dict(size=50))

    # Health Spending
    filtered_spending = exp_clean[exp_clean["Country Name"].isin(selected_countries)]
    fig2 = px.line(
        filtered_spending,
        x='Year', y="Spending",
        color='Country Name',
        color_discrete_map= colours,
        facet_col= 'Country Name',
        facet_col_wrap=3,
        # trendline= 'ols',
        labels= {'Year':'Year', 'Spending': 'Spending'},
        title="Health Spending per Capita"
    )

    fig2.update_layout(height=2000, width=6000)
    fig2.update_traces(marker=dict(size=50))


    # Mortality
    filtered_mortality = mort_clean[mort_clean["Country Name"].isin(selected_countries)]
    fig3 = px.line(
        filtered_mortality,
        x="Year", y="Mortality Rate",
        color='Country Name',
        color_discrete_map= colours,
        facet_col= 'Country Name',
        facet_col_wrap=3,
        # trendline= 'ols',
        labels= {'Year':'Year', 'Mortality Rate': 'Mortality Rate'},
        title="Preventable Mortality Rate by Gender"
    )

    fig3.update_layout(height=2000, width=6000)
    fig3.update_traces(marker=dict(size=50))

    return fig1, fig2, fig3

# --- Run the app ---
if __name__ == "__main__":
    app.run(debug=True)
