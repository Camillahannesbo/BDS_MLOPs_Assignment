import gradio as gr
import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar as calendar

import hopsworks
import joblib
import datetime
import os
import requests