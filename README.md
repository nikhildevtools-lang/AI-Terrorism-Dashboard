# AI Terrorism Intelligence Dashboard

This is a Streamlit dashboard for exploring terrorism incident data from CSV files. It helps users view key statistics, maps, country-level analysis, forecasts, predictions, reports, and raw data tables in one place.

## What This Project Does

- Shows important totals like incidents, countries, fatalities, injuries, groups, and attack types.
- Displays charts for yearly trends, affected countries, attack types, weapon types, groups, and regions.
- Includes an interactive global threat map.
- Lets users analyze one country in detail.
- Provides basic machine learning pages for prediction and forecasting.
- Includes a data explorer for searching and filtering records.
- Supports both offline CSV files from the `data/` folder and CSV files uploaded from the app sidebar.

## Dataset Options

You can use data in two ways:

1. Offline data folder CSV
   Place a CSV file inside the `data/` folder. The app will show available CSV files in the sidebar so you can choose one.

2. Uploaded CSV
   Upload a CSV file from the sidebar. After uploading, choose `Uploaded CSV` as the data source. The dashboard updates automatically with the uploaded data.

The app is designed for the Global Terrorism Database format, but it can also work with similar CSV files that contain columns such as year, country, region, attack type, group name, weapon type, fatalities, and injuries.

## How To Run

Install the required packages:

```bash
pip install -r requirements.txt
```

Start the dashboard:

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

## Project Structure

```text
AI_Terrorism_Dashboard/
|-- app.py                  # Main Streamlit app and sidebar navigation
|-- requirements.txt        # Python packages needed to run the app
|-- README.md               # Project explanation
|-- assets/
|   `-- style.css           # Dashboard styling
|-- data/
|   `-- *.csv               # Offline CSV datasets
|-- pages/
|   |-- Home.py             # Main dashboard page
|   |-- Global_Threat_Map.py
|   |-- Country_Analysis.py
|   |-- Attack_Prediction.py
|   |-- Forecasting.py
|   |-- AI_Report.py
|   |-- Data_Explorer.py
|   `-- About.py
`-- utils/
    |-- data_loader.py      # Loads and cleans CSV data
    |-- preprocessing.py    # ML helper logic
    |-- helper.py           # Utility functions
    `-- charts.py           # Plotly chart helpers
```

## Notes

The dashboard uses Streamlit, Pandas, Plotly, NumPy, and Scikit-learn. It is intended for learning, research, and data analysis purposes.
