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
print_fancy_header(text="🖍 Select the cities using the form below. \
                         Click the 'Submit' button at the bottom of the form to continue.",
                   font_size=22)
dict_for_streamlit = {}
# for workday in target_days:
#         for type in target_days[workday].items():
#             dict_for_streamlit[type] = type
selected_target_day_full_list = []

with st.form(key="user_inputs"):
    print_fancy_header(text='\n🗺 Here you can choose date from the drop-down menu',
                       font_size=20, color="#00FFFF")
    
    days_multiselect = st.multiselect(label='',
                                        options=dict_for_streamlit.keys())
    selected_target_day_full_list.extend(days_multiselect)
    st.write("_" * 3)
    
    print_fancy_header(text='\n🧮 How many days do you want me to predict?',
                 font_size=18, color="#00FFFF")
    options = [3, 7, 10, 14]
    
#     st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)

#     st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{padding-left:2px;}</style>',
#              unsafe_allow_html=True)

#     HOW_MANY_DAYS_PREDICT = st.radio("", options)

#     HOW_MANY_DAYS_PREDICT = int(HOW_MANY_DAYS_PREDICT)

#     submit_button = st.form_submit_button(label='Submit')

# if submit_button:
#     st.write('Selected work days days:', selected_target_day_full_list)

#     st.write(3*'-')

#     dataset = batch_data
  
#     dataset = dataset.drop_duplicates(subset=['type', 'date'])
#     dataset = dataset.sort_values(by=["type", "date"])

#     saved_model_dir = download_model(
#         name="electricity_price_prediction_model",
#         version=1
#     )

#     retrieved_xgboost_model = joblib.load(saved_model_dir + "/dk_electricity_model.pkl")

#     print_fancy_header("\n🧬 Modeling",
#                        font_size=22)
#     st.write("\n")
#     print_fancy_header(text='\n🤖 Getting the model...',
#                        font_size=18, color="#FDF4F5")


#     saved_model_dir = download_model(
#         name="electricity_price_prediction_model",
#         version=1
#     )
#     st.write("\n")
#     st.write("✅ Model was downloaded and cached.")
    
#     regressor = joblib.load(saved_model_dir + "/dk_electricity_model.pkl")

#     print_fancy_header(text='\n🧠 Predicting PM2.5 for selected cities...',
#                        font_size=18, color="#FDF4F5")

    
#     st.write("")
#     print_fancy_header(text="📈Results 📉",
#                        font_size=22)
#     plot_price(dataset[dataset['type'].isin(selected_target_day_full_list)])

    # st.write(3 * "-")
    # st.subheader('\n🎉 📈 🤝 App Finished Successfully 🤝 📈 🎉')
    # st.button("Re-run")