import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="European Public Health Dashboard", layout="wide")

# Load data
exp_clean = pd.read_csv("data/cleaned/Cleaned_health_spending.csv")
life_clean = pd.read_csv("data/cleaned/Cleaned_life_expectancy.csv")
mort_clean = pd.read_csv("data/cleaned/Cleaned_mortality_rate.csv")

# Colour map
colours = {
    'Netherlands': 'Orange', 
    'Sweden': 'Yellow', 
    'Belgium': 'Black',
    'Norway': 'Red', 
    'France': 'Blue', 
    'Italy': 'Green'
}

# Title
st.title("European Public Health Dashboard")
st.markdown("### Select countries to compare:")

# Sidebar country selection
selected_countries = st.multiselect(
    label="Select Countries",
    options=sorted(life_clean["Country Name"].unique()),
    default=["Netherlands", "Sweden", "Belgium", "Norway", "France", "Italy"]
)

# --- LIFE EXPECTANCY ---
filtered_life = life_clean[life_clean["Country Name"].isin(selected_countries)]
fig1 = px.line(
    filtered_life,
    x="Year",
    y="Life Expectancy",
    color="Country Name",
    color_discrete_map=colours,
    facet_col="Country Name",
    facet_col_wrap=3,
    line_group="Gender",
    labels={"Year": "Year", "Life Expectancy": "Life Expectancy"},
    title="🧬 Life Expectancy Trends by Country and Gender"
)
fig1.update_layout(
    title_font_size=24,
    xaxis_title="Year",
    yaxis_title="Life Expectancy",
    xaxis=dict(title_font=dict(size=18), tickfont=dict(size=14)),
    yaxis=dict(title_font=dict(size=18), tickfont=dict(size=14)),
    legend_title_font_size=16,
    legend_font_size=14,
    height=600
)
fig1.update_traces(marker=dict(size=8), line=dict(width=2))

st.plotly_chart(fig1, use_container_width=True)

# --- HEALTH SPENDING ---
filtered_spending = exp_clean[exp_clean["Country Name"].isin(selected_countries)]
fig2 = px.line(
    filtered_spending,
    x="Year",
    y="Spending",
    color="Country Name",
    color_discrete_map=colours,
    facet_col="Country Name",
    facet_col_wrap=3,
    labels={"Year": "Year", "Spending": "Spending per Capita (USD)"},
    title="💶 Health Spending per Capita"
)
fig2.update_layout(
    title_font_size=24,
    xaxis_title="Year",
    yaxis_title="Spending per Capita (USD)",
    xaxis=dict(title_font=dict(size=18), tickfont=dict(size=14)),
    yaxis=dict(title_font=dict(size=18), tickfont=dict(size=14)),
    legend_title_font_size=16,
    legend_font_size=14,
    height=600
)
fig2.update_traces(marker=dict(size=8), line=dict(width=2))

st.plotly_chart(fig2, use_container_width=True)

# --- MORTALITY RATE ---
filtered_mortality = mort_clean[mort_clean["Country Name"].isin(selected_countries)]
fig3 = px.line(
    filtered_mortality,
    x="Year",
    y="Mortality Rate",
    color="Country Name",
    color_discrete_map=colours,
    facet_col="Country Name",
    facet_col_wrap=3,
    labels={"Year": "Year", "Mortality Rate": "Preventable Mortality Rate"},
    title="⚰️ Preventable Mortality Rate by Gender"
)
fig3.update_layout(
    title_font_size=24,
    xaxis_title="Year",
    yaxis_title="Mortality Rate (per 1000 people)",
    xaxis=dict(title_font=dict(size=18), tickfont=dict(size=14)),
    yaxis=dict(title_font=dict(size=18), tickfont=dict(size=14)),
    legend_title_font_size=16,
    legend_font_size=14,
    height=600
)
fig3.update_traces(marker=dict(size=8), line=dict(width=2))

st.plotly_chart(fig3, use_container_width=True)
