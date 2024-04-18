import requests
from datetime import datetime, date, timedelta
import pandas as pd


def historical_weater_measures(historical: bool = False, lat: float = 57.048, lon: float = 9.9187, start: str = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"), end: str = (date.today()).strftime("%Y-%m-%d")) -> pd.DataFrame:
    """
    Fetches weater measures from Open Meteo API.

    Parameters:
    - historical (bool): If True, fetches historical data from start date to end date. If False, fetches data for the current day. Default is False.
    - latitude and longitude: Default to coordinates to Aalborg.
    - start and end date is default to 'Yesterday' - 'Today'.

    Returns:
    - pd.DataFrame: DataFrame with weater data for defined area.
    """

    API_URL = 'https://archive-api.open-meteo.com/v1/archive'
    r = requests.get(API_URL , params={
                'latitude': lat,
                'longitude': lon,
                'start_date': start,
                'end_date': end,
                'hourly': 'temperature_2m,relative_humidity_2m,precipitation,rain,snowfall,weather_code,cloud_cover,wind_speed_10m,wind_gusts_10m'
            })

    data = r.json()['hourly']
    df = pd.DataFrame(data)
    df["date"] = df['time'].str[:10]
    df['time'] = pd.to_datetime(df['time'])

    today = (date.today()).strftime("%Y-%m-%d")

    if historical:
        df = df[df.date != today]
    else:
        df = df[df.date == today]

    df["timestamp"] = df["time"].astype(int) // 10**6 * 1000

    weater = df[['timestamp', 'date', 'time', 'temperature_2m', 'relative_humidity_2m', 'precipitation', 'rain', 'snowfall', 'weather_code', 'cloud_cover', 'wind_speed_10m', 'wind_gusts_10m']]

    return weater

def forecast_weater_measures(lat: float = 57.048, lon: float = 9.9187, forecast_length : int = 1) -> pd.DataFrame:
    """
    Fetches weater forecast from Open Meteo API.

    Parameters:
    - latitude and longitude: Default to coordinates to Aalborg.

    Returns:
    - pd.DataFrame: DataFrame with weater forecast for defined area.
    """

    API_URL = 'https://api.open-meteo.com/v1/forecast'
    r = requests.get(API_URL , params={
                'latitude': lat,
                'longitude': lon,
                'hourly': 'temperature_2m,relative_humidity_2m,precipitation,rain,snowfall,weather_code,cloud_cover,wind_speed_10m,wind_gusts_10m',
                "forecast_days": forecast_length
            })

    data = r.json()['hourly']
    df = pd.DataFrame(data)
    df["date"] = df['time'].str[:10]
    df['time'] = pd.to_datetime(df['time'])

    df["timestamp"] = df["time"].astype(int) // 10**6 * 1000

    weater = df[['timestamp', 'date', 'time', 'temperature_2m', 'relative_humidity_2m', 'precipitation', 'rain', 'snowfall', 'weather_code', 'cloud_cover', 'wind_speed_10m', 'wind_gusts_10m']]

    return weater