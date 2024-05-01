import datetime

import hopsworks
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px

import streamlit as st

import json
import time
import pickle
import joblib
import datetime

import hopsworks 
import streamlit as st
import csv

import plotly.express as px
import folium
from streamlit_folium import st_folium

def print_fancy_header(text, font_size=22, color="#ff5f27"):
    res = f'<span style="color:{color}; font-size: {font_size}px;">{text}</span>'
    st.markdown(res, unsafe_allow_html=True)  

# I want to cache this so streamlit would run much faster after restart (it restarts a lot)
@st.cache_data()
def get_feature_view():
    st.write("Getting the Feature View...")
    feature_view = fs.get_feature_view(
        name = 'electricity_feature_view',
        version = 1
    )
    st.write("✅ Success!")

    return feature_view


@st.cache_data()
def get_batch_data_from_fs(td_version, date_threshold):
    st.write(f"Retrieving the Batch data since {date_threshold}")
    feature_view.init_batch_scoring(training_dataset_version=td_version)

    batch_data = feature_view.get_batch_data(start_time=date_threshold)
    return batch_data


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

############

st.title('🌫 Electricity Price Prediction 🌦')

st.markdown(
    """Predictions of daily average energy prices (before taxes and fees) in Stockholm/SE3 for the upcoming 7 days."""
)

#########################
st.title('🌫 Electricity Price Prediction 🌦')

st.write(3 * "-")
print_fancy_header('\n📡 Connecting to Hopsworks Feature Store...')

st.write("Logging... ")
# (Attention! If the app has stopped at this step,
# please enter your Hopsworks API Key in the commmand prompt.)
project = hopsworks.login()
fs = project.get_feature_store()
st.write("✅ Logged in successfully!")

feature_view = get_feature_view()

# I am going to load data for of last 60 days (for feature engineering)
today = datetime.date.today()
date_threshold = today - datetime.timedelta(days=60)

st.write(3 * "-")
print_fancy_header('\n☁️ Retriving batch data from Feature Store...')
batch_data = get_batch_data_from_fs(td_version=1,
                                    date_threshold=date_threshold)

st.write("Batch data:")
st.write(batch_data.sample(5))            

st.write(3 * '-')
st.write("\n")

progressBar = st.progress(0)
progressBar.progress(20)


def get_price():

    project = hopsworks.login()
    fs = project.get_feature_store()

    price_pred_fg = fs.get_feature_group(name="price_predictions", version=1).read()

    dates = [
        (datetime.datetime.now() + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range(1, 8)
    ]
    days_ahead = list(range(1, 8))

    prices = [
        price_pred_fg.loc[
            (price_pred_fg["date"] == dates[i])
            & (price_pred_fg["days_ahead"] == days_ahead[i])
        ]["predicted_price"].values[0]
        for i in range(0, 7)
    ]
    price_predictions = pd.DataFrame()
    price_predictions["date"] = dates
    price_predictions["predicted price (SEK öre)"] = prices

    return price_predictions


prices = get_price()
progressBar.progress(70)

fig = px.line(prices, x="date", y="predicted price (SEK öre)")
fig.update_yaxes(rangemode="tozero")

prices = prices.set_index("date")
prices = prices.reset_index()
prices.index = np.arange(1, len(prices) + 1)

st.write(fig)
st.dataframe(data=prices.style.background_gradient(cmap="YlOrRd"))
progressBar.progress(100)