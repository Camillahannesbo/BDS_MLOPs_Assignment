from datetime import datetime, date
import numpy as np
import pandas as pd


def dk_calendar() -> pd.DataFrame:
    """
    Fetches calendar for Denmark.

    Parameters:
    - ....

    Returns:
    - pd.DataFrame: DataFrame with danish calendar.
    """

    df = pd.read_csv('https://raw.githubusercontent.com/Camillahannesbo/MLOPs-Assignment-/main/data/calendar_incl_holiday.csv', delimiter=';', usecols=['date', 'type'])

    # Formatting the date column to 'YYYY-MM-DD' dateformat
    df["date"] = df["date"].map(lambda x: datetime.strptime(x, '%d/%m/%Y').strftime("%Y-%m-%d"))

    # Add features to the calender dataframe
    df['date_'] = pd.to_datetime(df['date'])
    df['dayofweek'] = df['date_'].dt.dayofweek
    df['day'] = df['date_'].dt.day
    df['month'] = df['date_'].dt.month
    df['year'] = df['date_'].dt.year
    df['workday'] = np.where(df['type'] == 'Not a Workday', 0, 1)

    # Drop the columns 'type' and 'date_' to finalize the calender dataframe
    calendar = df.drop(['type','date_'], axis=1)

    # Return the DataFrame with weather data
    return calendar