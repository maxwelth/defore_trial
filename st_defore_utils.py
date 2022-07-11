# -*- coding: utf-8 -*-
"""st_DeFore_Utils.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xJr06Ta68yEUYOKN-Xq90XhGPbhVMQw3
"""

import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

from datetime import datetime, date, timedelta
from hijri_converter import Hijri, Gregorian
from prophet import Prophet

def load_data(uploaded_data):

    uploaded_data_path = uploaded_data.name
    if '.csv' in str(uploaded_data_path):
        data = pd.read_csv(uploaded_data)
    elif '.xls' in str(uploaded_data_path):
        data = pd.read_excel(uploaded_data)
    else: 
        raise(ImportError("Invalid file extension for uploaded file - must be .csv or .xls or .xlsx"))
  
    return data

def twin_dates(date, month):
    date_month, date_day = date.month, date.day
    if (date_month == month) and (date_day == month):
      return 1
    else:
      return 0

tokopedia_wib = [25, 26, 27, 28, 29, 30, 31]
def is_tokopedia(date):
    month, day = date.month, date.day
    if (month == day) or (day in tokopedia_wib):
      return True
    else: 
      return False

shopee_payday = [25, 26, 27]
def is_shopee(date):
    month, day = date.month, date.day
    if (month == day) or (day in shopee_payday):
      return True
    else: 
      return False

def is_covid(date): 
    if date > datetime.strptime('2021-03-02', "%Y-%m-%d"):
      return 1
    else: 
      return 0

def is_payday(date):
    if date.day == 25:
      return True
    else: 
      return False

def is_ramadhan(date):
  year, month, day = date.year, date.month, date.day

  hijriah_date = Gregorian(year, month, day).to_hijri()
  hijriah_month = hijriah_date.month_name()

  if hijriah_month == 'Ramdhan':
    return True
  else:
    return False

def pre_format(df):
  df = df.rename(columns = {'date' : 'ds', 'total_order' : 'y'})
  df['ds'] = df['ds'].astype('datetime64[ns]') 
  return df

def add_twin_dates_feature(df):
  for month in [i + 1 for i in range(12)]:
    feature_name = 'twin_dates_' + str(month)
    df[feature_name] = df['ds'].apply(lambda x:twin_dates(x, month))
  return df

def add_main_feature(df):
  feature_name_str = ['is_covid','is_tokopedia','is_shopee','is_payday','is_ramadhan']
  feature_name = [is_covid,is_tokopedia,is_shopee,is_payday,is_ramadhan]
  for feature, name in enumerate(feature_name_str):
    df[name] = df['ds'].apply(feature_name[feature])
  return df

def create_prediction_range(df, pred_date):
  end_day = pd.to_datetime(pred_date) + timedelta(days=3)
  return pd.DataFrame({'ds': pd.date_range(start = df['ds'].values[-1], end = end_day)})

def prophet_model(df, future):
  m = Prophet(seasonality_mode = 'multiplicative')

  m.add_country_holidays('ID') # Add national holidays
  for regressor in ['is_covid','is_tokopedia','is_shopee','is_payday','is_ramadhan']:
    m.add_regressor(regressor)

  for month in [i + 1 for i in range(12)]:
    feature_name = 'twin_dates_' + str(month)
    m.add_regressor(feature_name)

  m.fit(df)
  forecast = m.predict(future)
  return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]