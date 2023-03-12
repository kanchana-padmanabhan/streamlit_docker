from datetime import datetime
import re

import numpy as np
import pandas as pd

from bokeh.layouts import column
from bokeh.models import ColumnDataSource, RangeTool
from bokeh.models.tickers import DatetimeTicker
from bokeh.plotting import figure
import streamlit as st


@st.cache_data
def fetch_and_clean_data():
    cached_df = pd.read_csv('data/thor_wwii.csv')
    return cached_df


df = fetch_and_clean_data()
df['MSNDATE'] = pd.to_datetime(df['MSNDATE'], format='%m/%d/%Y')
df['MSNDATE'] = df['MSNDATE'].dt.date

sample = df.head(2000)
sample_grouped = sample.groupby(['COUNTRY_FLYING_MISSION', 'MSNDATE'])[
    ['AC_ATTACKING']].sum().reset_index()
country_list = sample_grouped['COUNTRY_FLYING_MISSION'].unique()


def df_filter(main_df):
    options = st.multiselect(
        'COUNTRY',
        country_list,
        country_list)
    filtered_df = main_df[main_df['COUNTRY_FLYING_MISSION'].isin(options)]
    return filtered_df


st.title('Column Filter')
filtered_df = df_filter(sample_grouped)

dates = np.array(filtered_df['MSNDATE'], dtype=np.datetime64)
source = ColumnDataSource(data=filtered_df)

p = figure(height=300, width=800, tools="xpan", toolbar_location=None,
           x_axis_type="datetime", x_axis_location="above",
           background_fill_color="#efefef", x_range=(dates[200], dates[300]))
#

p.line('MSNDATE', 'AC_ATTACKING', source=source)
p.yaxis.axis_label = 'AC_ATTACKING'

select = figure(
    title="Drag the middle and edges of the selection box to change the range above",
    height=130,
    width=800,
    y_range=p.y_range,
    x_axis_type="datetime",
    y_axis_type=None,
    tools="",
    toolbar_location=None,
    background_fill_color="#efefef")

range_tool = RangeTool(x_range=p.x_range)
range_tool.overlay.fill_color = "navy"
range_tool.overlay.fill_alpha = 0.2

select.line('MSNDATE', 'AC_ATTACKING', source=source)
select.ygrid.grid_line_color = None
select.add_tools(range_tool)

st.bokeh_chart(column(p, select))
