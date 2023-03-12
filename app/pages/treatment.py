import pandas as pd

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Div
from bokeh.models.tools import HoverTool
import streamlit as st


@st.cache_data
def fetch_and_clean_data():
   cached_df = pd.read_csv('data/thor_wwii.csv')
   return cached_df

df = fetch_and_clean_data()
sample_df = df.sample(50)
source = ColumnDataSource(sample_df)

col1, col2 = st.columns(2)
with col1:
   st.write("Column 1 - Hover over data enabled")
   p = figure()
   p.circle(x='TOTAL_TONS', y='AC_ATTACKING',
            source=source,
            size=10, color='green')
   p.title.text = 'Attacking Aircraft and Munitions Dropped'
   p.xaxis.axis_label = 'Tons of Munitions Dropped'
   p.yaxis.axis_label = 'Number of Attacking Aircraft'
   hover = HoverTool()
   hover.tooltips = [
      ('Attack Date', '@MSNDATE'),
      ('Attacking Aircraft', '@AC_ATTACKING'),
      ('Tons of Munitions', '@TOTAL_TONS'),
      ('Type of Aircraft', '@AIRCRAFT_NAME')
   ]
   p.add_tools(hover)
   st.bokeh_chart(p, use_container_width=True)
with col2:
   st.write("Column 2 - HTML Components")
   #https://docs.bokeh.org/en/latest/docs/user_guide/interaction/widgets.html#div
   template = ("""
         <div class='content'>
          <div class='name'> {info_title} </div>
           <span class='percentage' style='color: {colour};background-color:{bcolor}; font-size:70px;'> {percentage}<small>%</small> </span>
         </div>
         """)
   # initial text
   text = template.format(info_title="Change Year over Year",
                          percentage=32,
                          colour='Violet',
                          bcolor = 'LightGray')
   div = Div(text=text, height=300)
   st.bokeh_chart(div, use_container_width=True)


st.write("This is outside the container")