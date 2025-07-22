# EU_healthcare_spending_analysis
A data analytics project exploring the relationship between healthcare spending and health outcomes in Europe (2012–2022)

## project structure
health_dashboard_project/
│
├── data/
│   ├── raw                 
│   │   ├── eu_health_expending.csv
│   │   ├── life_expectancy.csv
│   │   └── mortality_rate.csv
│   └── cleaned                 
│       ├── Cleaned_health_spending.csv
│       ├── Cleaned_life_expectancy.csv
│       ├── Cleaned_mortality_rate.csv
│       └── merged_eu_health_data.csv  
│
├── Scripts/
│   ├── main.py                 # Streamlit app
│   └── requirements.txt        # Python dependencies  
│
├── notebooks
│   └── explore_and_analyse_data.ipynb         
│
│
└── README.md              


## Health Outcomes Dashboard (EU Public Data)

This dashboard allows interactive exploration of:
- Health spending by country over time
- Life expectancy trends
- Preventable mortality rates

### 🚀 Technologies
- Streamlit
- Plotly
- Pandas
- Public EU datasets

### 📊 Dashboard Features
- Line plots of trends over time by country
- Trendlines per country
- Interactive filtering

### ▶️ How to Run
```bash
streamlit run dashboard.py

