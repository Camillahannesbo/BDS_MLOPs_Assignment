import requests
from math import cos, asin, sqrt, pi
from datetime import datetime, date
from calendar import monthrange
import pandas as pd


def fetch_weater_measures(lat: float = 57.048, lon: float = 9.9187) -> pd.DataFrame:
    """
    Fetches weater measures from Open Meteo API.

    Parameters:
    - latitude and longitude: Default to coordinates to Aalborg

    Returns:
    - pd.DataFrame: DataFrame with electricity prices for different areas (DK1, DK2).
    """

    API_URL = 'https://archive-api.open-meteo.com/v1/archive'
    r = requests.get(API_URL , params={
                'latitude': lat,
                'longitude': lon,
                'start_date': '2022-01-01',
                'end_date': '2023-12-31',
                'hourly': 'temperature_2m,relative_humidity_2m,precipitation,rain,snowfall,weather_code,cloud_cover,wind_speed_10m,wind_gusts_10m'
            })

    data = r.json()['hourly']
    df = pd.DataFrame(data)
    df["date"] = df['time'].str[:10]
    df['time'] = pd.to_datetime(df['time'])

    weater = df[['date', 'time', 'temperature_2m', 'relative_humidity_2m', 'precipitation', 'rain', 'snowfall', 'weather_code', 'cloud_cover', 'wind_speed_10m', 'wind_gusts_10m']]

    return weater