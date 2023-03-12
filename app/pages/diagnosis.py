import pandas as pd
import streamlit as st
from bokeh.palettes import Spectral3
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource


@st.cache_data
def fetch_and_clean_data():
   cached_df = pd.read_csv('data/thor_wwii.csv')
   return cached_df

df = fetch_and_clean_data()

tab1, tab2= st.tabs(["Variation 1", "Variation 2"])

with tab1:
    df['MSNDATE'] = pd.to_datetime(df['MSNDATE'], format='%m/%d/%Y')

    grouped = df.groupby('MSNDATE')[['TOTAL_TONS', 'TONS_IC', 'TONS_FRAG']].sum()
    grouped = grouped / 1000

    source = ColumnDataSource(grouped)

    p = figure(x_axis_type='datetime')

    p.line(x='MSNDATE', y='TOTAL_TONS', line_width=2, source=source, legend_label='All Munitions')
    p.line(x='MSNDATE', y='TONS_FRAG', line_width=2, source=source, color=Spectral3[1],legend_label='Fragmentation')
    p.line(x='MSNDATE', y='TONS_IC', line_width=2, source=source, color=Spectral3[2], legend_label='Incendiary')

    p.yaxis.axis_label = 'Kilotons of Munitions Dropped'
    st.bokeh_chart(p)

with tab2:
    grouped = df.groupby('COUNTRY_FLYING_MISSION')[['TONS_IC', 'TONS_FRAG', 'TONS_HE']].sum()

    # convert tons to kilotons again
    grouped = grouped / 1000
    source = ColumnDataSource(grouped)
    countries = source.data['COUNTRY_FLYING_MISSION'].tolist()
    p = figure(x_range=countries)
    p.vbar_stack(stackers=['TONS_HE', 'TONS_FRAG', 'TONS_IC'],
                 x='COUNTRY_FLYING_MISSION', source=source,
                 legend_label=['High Explosive', 'Fragmentation', 'Incendiary'],
                 width=0.5, color=Spectral3)
    p.title.text = 'Types of Munitions Dropped by Allied Country'
    p.legend.location = 'top_left'

    p.xaxis.axis_label = 'Country'
    p.xgrid.grid_line_color = None  # remove the x grid lines

    p.yaxis.axis_label = 'Kilotons of Munitions'

    st.bokeh_chart(p)

