# Importing the necessary libraries
import streamlit as st
from streamlit_folium import st_folium
import pandas as pd
import hopsworks 

import joblib
import datetime

import altair as alt
import plotly.express as px

import os
import folium

# Now we import the functions from the features folder
# This is the functions we have created to generate features for electricity prices and weather measures
from features import electricity_prices, weather_measures, calendar 

def print_fancy_header(text, font_width="bold", font_size=22, color="#2656a3"):
    res = f'<span style="font-width:{font_width}; color:{color}; font-size:{font_size}px;">{text}</span>'
    st.markdown(res, unsafe_allow_html=True)  

def print_fancy_subheader(text, font_width="bold", font_size=22, color="#333"):
    res = f'<span style="font-width:{font_width}; color:{color}; font-size:{font_size}px;">{text}</span>'
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

# Function to load the dataset
@st.cache_data  # Cache the function to enhance performance
def load_data():
    # Fetching weather forecast measures for the next 5 days
    weather_forecast_df = weather_measures.forecast_weather_measures(
        forecast_length=5
    )

    # Fetching danish calendar
    calendar_df = calendar.dk_calendar()

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

    predictions_df = pd.DataFrame(predictions_data).sort_values(by='time')

    return predictions_df

#########################

progress_bar = st.sidebar.header('⚙️ Working Progress')
progress_bar = st.sidebar.progress(0)

# Title for the streamlit app
st.title('Electricity Price Prediction 🌦')

# Subtitle
st.markdown("""
            Welcome to the electricity price predicter for DK1.
""")

st.write(3 * "-")

with st.expander("📊 **Data Engineering and Machine Learning Operations in Business**"):
                 st.markdown("""
LEARNING OBJECTIVES
- Using our skills for designing, implementing, and managing data pipelines and ML systems.
- Focus on practical applications within a business context.
- Cover topics such as data ingestion, preprocessing, model deployment, monitoring, and maintenance.
- Emphasize industry best practices for effective operation of ML systems.
"""
)
                 
with st.expander("📊 **This assigment**"):
                 st.markdown("""
The objective of this assignment is to build a prediction system that predicts the electricity prices in Denmark (area DK1) based on weather conditions, previous prices, and the Danish holidays.
"""
)
                 
with st.sidebar:
    # st.write("This code will be printed to the sidebar.")

    print_fancy_header('\n📡 Connecting to Hopsworks Feature Store...')

    st.write("Logging... ")
    # please enter your Hopsworks API Key in the commmand prompt.)
    # project = hopsworks.login(project = "camillah", api_key_value=os.environ['HOPSWORKS_API_KEY'])
    project = hopsworks.login()
    fs = project.get_feature_store()
    progress_bar.progress(40)
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

    progress_bar.progress(80)

st.write(3 * "-")
print_fancy_header('\n☁️ Retriving batch data from Feature Store...')

predictions_df = load_data()

progress_bar.progress(100)

# Sidebar filter: Date range
min_value = 1
max_value = int(len(predictions_df['time'].unique()) / 24)
default = int(48 / 24)
date_range = st.sidebar.slider("Select Date Range", min_value=min_value, max_value=max_value, value=default)
filtered_predictions_df = predictions_df.head(date_range * 24)

visualization_option = st.selectbox(
    "Select Visualization 🎨", 
    ["Matrix", 
    "Linechart"]
)

# Visualizations based on user selection
if visualization_option == "Matrix":
    data = filtered_predictions_df
    data['date'] = data['time'].dt.strftime('%Y-%m-%d')
    data['time_of_day'] = data['time'].dt.strftime('%H:%M')
    data.drop(columns=['time'], inplace=True)

    # Pivot the DataFrame
    pivot_df = data.pivot(index='time_of_day', columns='date', values='prediction')

    st.write(pivot_df)  

elif visualization_option == "Linechart":
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

# #########################
# st.write(3 * '-')
# st.write("\n")

# print_fancy_header('\n📈 Predictions Table for today and 4 days ahead')

# #########################
# st.write(3 * '-')
# st.write("\n")





