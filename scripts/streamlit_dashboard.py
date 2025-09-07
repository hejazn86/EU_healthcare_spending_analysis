# Main_Dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ====================== Load Data ======================
fitted_data = pd.read_csv("data/fitted_data.csv", index_col=0)
metrics_df = pd.read_csv("reports/model_metrics.csv")
ols_coefs = pd.read_csv("reports/ols_coefficients.csv")
glm_coefs = pd.read_csv("reports/glm_coefficients.csv")
mix_coefs = pd.read_csv("reports/mixedlm_coefficients.csv")
rand_eff_df = pd.read_csv("reports/rand_eff.csv", index_col=0)
pred_data = pd.read_csv("reports/pred_data.csv", index_col=0)


# ===================== clean the data ==========================

fitted_data.drop(columns=["age_year"], inplace=True)
preview_data = fitted_data.head(200)
# Strip whitespace from column names and entries
metrics_df.columns = metrics_df.columns.str.strip()
metrics_df["Model"] = metrics_df["Model"].str.strip()

# Ensure numeric columns are numeric (force NaN where empty)
for col in ["R2", "Adj_R2", "AIC", "BIC", "Pseudo_R2", "LogLikelihood"]:
    metrics_df[col] = pd.to_numeric(metrics_df[col], errors="coerce")
    metrics_df_display = metrics_df.fillna("—")
    metrics_df_display = metrics_df_display.round(2)

# replace NAN with readable labels
metrics_df_display = metrics_df.fillna("—")


# ====================== Dashboard Layout ======================
st.set_page_config(page_title="Life Expectancy & Mortality Analysis", layout="wide")

st.title("📊 Life Expectancy & Mortality Analysis")
st.markdown("This dashboard summarizes the analysis of factors influencing **Life expectancy** and **Mortality rates** across countries, genders, and years. It is based on regression models and mixed-effects models for cross-country comparisons.")

# Tabs for storytelling
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview",
    "Model Metrics",
    "Coefficients",
    "Random Effects",
    "Predicted Effects"
])

# ====================== Tab 1: Overview ======================

with tab1:
    st.subheader("Project Overview")
    st.markdown("""
    - **Goal**: Investigate how **spending, gender, and time** affect life expectancy and mortality.
    - **Methods**:
        - Ordinary Least Squares (OLS) for **life expectancy**.
        - Generalized Linear Model (GLM) for **log mortality rate**.
        - Mixed Effects Model for country-specific variations.
    - **Outcome**: Provides insights into which factors consistently explain variation in health outcomes.
    """)

    styled_df = preview_data.style.set_properties(
        **{"color": "green", "font-weight": "bold"}, subset=["life_expectancy"]
        ).set_properties(
            **{"color": "red", "font-weight": "bold"}, subset=["mortality_rate"]
            )


    col3, col4 = st.columns(2)

    with col3:
        st.write("### Data Preview")
        st.dataframe(styled_df)
        
    with col4:
        st.write("### Statistics Summary")    
        st.write(fitted_data[["Spending", "Year","gender_encoded", "life_expectancy", "mortality_rate"]].rename(columns={
            "Spending": "Healthcare Spending",
            "gender_encoded": "Gender", 
            "life_expectancy": "Life Expectancy", 
            "mortality_rate": "Mortality Rate"
        }).describe())



    # --- EDA Plots ---
        
    st.subheader("Exploratory Data Analysis")
        
    col1, col2 = st.columns(2)
        
    # Distribution of Life Expectancy
    fig1 = px.histogram(
        fitted_data,
        x="life_expectancy",
        nbins=40,
        title="Distribution of Life Expectancy",
        color_discrete_sequence=["green"]
    )

    # Distribution of Mortality Rate
    fig2 = px.histogram(
        fitted_data,
        x="mortality_rate",
        nbins=40,
        title="Distribution of Mortality Rate",
        color_discrete_sequence=["red"]
    )

        

    # Scatterplot Spending vs Life Expectancy
    fig3 = px.scatter(
        fitted_data.sample(5000),  # sample for speed
        x="Spending",
        y="life_expectancy",
        color="Country",
        opacity=0.5,
        title="Spending vs Life Expectancy (sample)"
    )



    # Scatterplot Spending vs Mortality Rate
    fig4 = px.scatter(
        fitted_data.sample(5000),
        x="Spending",
        y="mortality_rate",
        color="Country",
        opacity=0.5,
        title="Spending vs Mortality Rate (sample)"
    )
    

    with col1:
        st.plotly_chart(fig1, use_container_width=True)
        st.plotly_chart(fig3, use_container_width=True)


    with col2:  
        st.plotly_chart(fig2, use_container_width=True)
        st.plotly_chart(fig4, use_container_width=True)

    
    # col5, col6 = st.columns(2)

    # with col5:
    # Compute correlation
    corr = fitted_data[["Spending", "Year","gender_encoded", "life_expectancy", "mortality_rate"]].rename(columns={
            "Spending": "Healthcare Spending",
            "gender_encoded": "Gender", 
            "life_expectancy": "Life Expectancy", 
            "mortality_rate": "Mortality Rate"
        }).corr(numeric_only=True).round(2)

    # Convert to long format for Plotly
    fig = px.imshow(
    corr,
    text_auto=True,       
    color_continuous_scale="RdBu_r",
    aspect="auto",
    title="Correlation Heatmap"
    )

st.plotly_chart(fig, use_container_width=True)



# ====================== Tab 2: Model Metrics ======================

with tab2:
    st.subheader("Model Fit Metrics")
    st.markdown("Comparison of *OLS*, **GLM** and **Mixed Effects** models using AIC, BIC, and Log-Likelihood values.")

    st.dataframe(metrics_df_display)

    fig = px.bar(
        metrics_df_display,
        x="Model",
        y=["AIC", "BIC"],
        barmode="group",
        title="Model Comparison: AIC & BIC"
    )
    st.plotly_chart(fig, use_container_width=True)


# ====================== Tab 3: Coefficients ======================

with tab3:
    st.subheader("Model Coefficients")
    st.markdown("Estimated coefficients show the direction and strength of associations between covariates and outcomes.")

    colA1, colA2 = st.columns(2) 

    with colA1:
        st.write("### OLS Coefficients")
        st.dataframe(ols_coefs)
        
        st.write("### GLM Coefficients")
        st.dataframe(glm_coefs)
        
        st.write("### Mixed Effects Model Coefficients")
        st.dataframe(mix_coefs)
    
    # colB, colC = st.columns(2)

    with colA2:
        fig_ols = px.bar(ols_coefs, x="Variables", y="Coefficients", title="OLS Coefficients", color="Coefficients")
        st.plotly_chart(fig_ols, use_container_width=True)
        
        fig_glm = px.bar(glm_coefs, x="Variables", y="Coefficients", title="GLM Coefficients", color="Coefficients")
        st.plotly_chart(fig_glm, use_container_width=True)

        fig_mix = px.bar(mix_coefs, x="Variables", y="Coefficients", title="Mixe-Effects model Coefficients", color="Coefficients")
        st.plotly_chart(fig_mix, use_container_width=True)


# ====================== Tab 4: Random Effects ======================

with tab4:
    st.subheader("Country-specific Random Effects")
    st.markdown("Random intercepts capture country-level deviations in mortality rates.")
    # st.dataframe(rand_eff_df)


    fig_rand = px.bar(
        rand_eff_df.sort_values("Random Intercept", ascending=False),
        x="Country",
        y="Random Intercept",
        color="Random Intercept",
        color_continuous_scale="rdylgn",
        title="Random Intercepts by Country"
    )
    fig_rand.update_layout(xaxis_tickangle=90)
    st.plotly_chart(fig_rand, use_container_width=True)


# ====================== Tab 5: Predicted Effects ======================

with tab5:
    st.subheader("Predicted Effects")
    st.markdown("Predicted **log mortality rates** as a function of spending and gender.")

    colC1, colC2 = st.columns(2)
    with colC1:
        fig = px.line(
            pred_data,
            x="Spending_centered",
            y="Predicted",
            color="Gender",
            title="Predicted log Mortality Rate by Spending and Gender (GLM)"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("These lines show how predicted mortality rates change with spending, highlighting gender differences.")

