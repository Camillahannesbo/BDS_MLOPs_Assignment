import requests
from datetime import datetime, date
import pandas as pd


def fetch_electricity_prices(historical: bool = False, start: str = '2022-01-01', end: str = (date.today()).strftime("%Y-%m-%d")) -> pd.DataFrame:
    """
    Fetches electricity prices from Energinet (Dataservice API).

    Parameters:
    - historical (bool): If True, fetches historical data from start date to end date. If False, fetches data for the current day. Default is False.
    - start (str): Define a start date for the API call. Defaul is 2022-01-01.
    - end (str): Define a end date for the API call. Default is today.
    
    Returns:
    - pd.DataFrame: DataFrame with electricity prices for different areas in Denmark (DK1, DK2).
    """

    API_URL = 'https://api.energidataservice.dk/dataset/Elspotprices'
    r = requests.get(API_URL , params={
                'offset': 0,
                'start': start+'T00:00',
                'end': end+'T23:59',
                'filter': '{"PriceArea":["DK1", "DK2"]}',
                'sort': 'HourUTC DESC'
            })

    areas = ['DK1', 'DK2']
    areas_data = {}
    areas_data[areas[0]] = {}

    data = r.json()['records']

    area_price_list = []
    for r in data:
            if r['PriceArea'] in areas:
                area_price_list.append({"time": r["HourDK"], "PriceArea": r["PriceArea"], "SpotPriceDKK": r['SpotPriceDKK']})
    df = pd.DataFrame(area_price_list)
    df["date"] = df["time"].map(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S').strftime("%Y-%m-%d"))
    df['SpotPriceDKK_KWH'] = df['SpotPriceDKK'] / 1000
    df['time'] = pd.to_datetime(df['time'])
    df.drop('SpotPriceDKK', axis=1, inplace=True)
    if not historical:
        today = (date.today()).strftime("%Y-%m-%d")
        df = df[df.date == today]

    electricity_prices = df[['date', 'time', 'PriceArea', 'SpotPriceDKK_KWH']]

    return electricity_prices