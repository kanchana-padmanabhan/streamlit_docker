import streamlit as st
from bokeh.plotting import figure
from st_pages import Page, show_pages

st.set_page_config(
    page_title="PAG Administrative Dashboard",
)

show_pages(
    [
        Page("dashboard_app.py", "Home", ""),
        Page("pages/treatment.py", "Treatment", ""),
        Page("pages/diagnosis.py", "Diagnosis", ""),
        Page("pages/datetime_filter.py", "DateTime Filter", ""),
        Page("pages/column_filter.py", "Column Filter", ""),
    ]
)

st.write("# Welcome to PAG Administrative Dashboard 👋")


st.markdown("""
            ## Summary Statistics

            ### Number of Hospitals in Federation: 20
            ### Number of User Accounts in Federation: 10

            ### Hospitals
            * #### Total Invitations: 50
            * #### Acceptance: 30
            * #### Completed: 20
            * #### In Progress: 5

            ### Researchers
            * #### Total Invitations: 60
            * #### Acceptance: 20
            * #### Completed: 10
            * #### In Progress: 10

            ### Compute
            * #### Total Queries Executed till date: 3230
            * #### Total Queries Executed in last week: 100
            * #### Total logged in users per week: 50
"""
            )
