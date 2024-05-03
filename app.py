import json
import time
import pickle
import joblib
import datetime
import pandas as pd
import altair as alt

import hopsworks 
import streamlit as st
import csv
import os

import plotly.express as px
import folium
from streamlit_folium import st_folium

# Now we import the functions from the features folder
# This is the functions we have created to generate features for electricity prices and weather measures
from features import electricity_prices, weather_measures, calendar 

def print_fancy_header(text, font_size=22, color="#ff5f27"):
    res = f'<span style="color:{color}; font-size: {font_size}px;">{text}</span>'
    st.markdown(res, unsafe_allow_html=True)  

# I want to cache this so streamlit would run much faster after restart (it restarts a lot)
@st.cache_data()
def get_feature_view():
    st.write("Getting the Feature View...")
    feature_view = fs.get_feature_view(
        name = 'electricity_training_feature_view',
        version = 1
    )
    st.write("✅ Success!")

    return feature_view


@st.cache_data()
def download_model(name="electricity_price_prediction_model",
                   version=4):
    mr = project.get_model_registry()
    retrieved_model = mr.get_model(
        name="electricity_price_prediction_model",
        version=4
    )
    saved_model_dir = retrieved_model.download()
    return saved_model_dir



def plot_price(df):
    # create figure with plotly express
    fig = px.line(df, x='date', y='dk1_spotpricedkk_kwh', color='type')

    # customize line colors and styles
    fig.update_traces(mode='lines+markers')
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        'legend_title': 'type',
        'legend_font': {'size': 12},
        'legend_bgcolor': 'rgba(0, 0, 0, 0)',
        'xaxis': {'title': 'Date'},
        'yaxis': {'title': 'dk1_spotpricedkk_kwh'},
        'shapes': [{
            'type': 'line',
            'x0': datetime.datetime.now().strftime('%Y-%m-%d'),
            'y0': 0,
            'x1': datetime.datetime.now().strftime('%Y-%m-%d'),
            'y1': df['dk1_spotpricedkk_kwh'].max(),
            'line': {'color': 'red', 'width': 2, 'dash': 'dashdot'}
        }]
    })

    # show plot
    st.plotly_chart(fig, use_container_width=True)

with open('data/calendar_incl_holiday.csv') as csv_file:
    target_days = csv.reader(csv_file)

#########################
st.title('🌫 Electricity Price Prediction 🌦')

st.write(3 * "-")
print_fancy_header('\n📡 Connecting to Hopsworks Feature Store...')

st.write("Logging... ")
# (Attention! If the app has stopped at this step,
# please enter your Hopsworks API Key in the commmand prompt.)
project = hopsworks.login(project = "camillah", api_key_value=os.environ['HOPSWORKS_API_KEY'])
fs = project.get_feature_store()
st.write("✅ Logged in successfully!")

# Retrieve the model registry
mr = project.get_model_registry()

# Retrieving the model from the Model Registry
retrieved_model = mr.get_model(
    name="electricity_price_prediction_model", 
    version=1,
)

# Downloading the saved model to a local directory
saved_model_dir = retrieved_model.download()

# Loading the saved XGB model
retrieved_xgboost_model = joblib.load(saved_model_dir + "/dk_electricity_model.pkl")

st.write("✅ Model successfully loaded!")

# I am going to load data for of last 60 days (for feature engineering)
today = datetime.date.today()
date_threshold = today - datetime.timedelta(days=60)

st.write(3 * "-")
print_fancy_header('\n☁️ Retriving batch data from Feature Store...')
# Fetching weather forecast measures for the next 5 days
weather_forecast_df = weather_measures.forecast_weather_measures(
    forecast_length=5
)

# Fetching danish calendar
calendar_df = calendar.get_calendar()

# Merging the weather forecast and calendar dataframes
new_data = pd.merge(weather_forecast_df, calendar_df, how='inner', left_on='date', right_on='date')

st.write("New data:")
st.write(new_data.sample(5))            

# Drop columns 'date', 'datetime', 'timestamp' from the DataFrame 'new_data'
data = new_data.drop(columns=['date', 'datetime', 'timestamp'])

predictions = retrieved_xgboost_model.predict(data)

predictions_data = {
    'prediction': predictions,
    'time': new_data["datetime"],
}

# Create a DataFrame from the predictions data
predictions_df = pd.DataFrame(predictions_data)
predictions_df = predictions_df.sort_values(by='time')

st.write("predictions_df:")
st.write(predictions_df.sample(5))       


#########################
st.write(3 * '-')
st.write("\n")

print_fancy_header('\n📈 Predictions Table for today and 4 days ahead')

# Reshape the predictions data to a Table format, where each row represents a hour and each column a day
table_df = predictions_df['prediction'].values.reshape(-1, 24)
table_df = pd.DataFrame(table_df, columns=[f'{i}:00' for i in range(24)], index = [f'Day {i}' for i in range(table_df.shape[0])])

st.write(table_df.T.style.set_properties(**{'width': '100%', 'max-width': 'none'}))

#########################
st.write(3 * '-')
st.write("\n")

# Create a slider for selecting the number of days to display
num_hours = st.slider("Select number of hours to display", min_value=1, max_value=120, value=48)

# Filter the predictions dataframe based on the selected number of days
filtered_predictions_df = predictions_df.head(num_hours)

# Create Altair chart with line and dots
chart = alt.Chart(filtered_predictions_df).mark_line(point=True).encode(
    x='time:T',
    y='prediction:Q',
    tooltip=[alt.Tooltip('time:T', title='Date', format='%d-%m-%Y'), 
             alt.Tooltip('time:T', title='Time', format='%H:%M'), 
             alt.Tooltip('prediction:Q', title='Spot Price (DKK)', format='.2f')
            ]
)

# Display the chart
st.altair_chart(chart, use_container_width=True)

