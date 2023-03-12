from datetime import datetime
import re
import pandas as pd
from bokeh.plotting import figure
from bokeh.models.tickers import CategoricalTicker
import streamlit as st


@st.cache_data
def fetch_and_clean_data():
    cached_df = pd.read_csv('data/thor_wwii.csv')
    return cached_df


df = fetch_and_clean_data()
df['MSNDATE'] = pd.to_datetime(df['MSNDATE'], format='%m/%d/%Y')
df['MSNDATE'] = df['MSNDATE'].dt.date
sample = df.head(2000)


def df_filter(main_df):
    start_date = st.date_input('Start date', main_df['MSNDATE'].min())
    end_date = st.date_input('End date', main_df['MSNDATE'].max())

    if start_date > end_date:
        st.error('Error: End date must fall after start date.')

    filtered_df = main_df[(main_df['MSNDATE'] >= start_date)
                          & (main_df['MSNDATE'] <= end_date)]
    grouped_df = filtered_df.groupby('COUNTRY_FLYING_MISSION')[
        ['AC_ATTACKING']].sum().reset_index()
    return grouped_df


st.title('Datetime Filter')
grouped_df = df_filter(sample)

x = grouped_df['COUNTRY_FLYING_MISSION']
y = grouped_df['AC_ATTACKING']
p = figure(
    y_range=x.values,
    x_axis_label='AC_ATTACKING',
    y_axis_label='')

p.yaxis.ticker = CategoricalTicker()
p.hbar(right=y, y=x, height=0.5)

st.bokeh_chart(p)
