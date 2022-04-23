from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import pandas
from gsheetsdb import connect

#"""
# Welcome to Streamlit!

#Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

#If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
#forums](https://discuss.streamlit.io).

#In the meantime, below is an example of what you can do with just a few lines of code:
#"""
# Using object notation
#add_selectbox = st.sidebar.selectbox(
#    "How would you like to be contacted?",
#    ("Email", "Home phone", "Mobile phone")
#)

st.sidebar.subheader('Upload your GPS trajectory data')
uploaded_file = st.sidebar.file_uploader(" ")
if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    df = pd.read_csv(uploaded_file, encoding = 'utf-8')
    #st.write(df.head())


#select a specific vehicle
st.subheader('Choose one vehicle to visualize')
vehoption = st.selectbox(' ', df.vehid.unique())
vehselected = df[df.vehid == vehoption]

#select a spcific trip of that vehicle
st.write('This vehicle has in total ', str(len(vehselected.orderid.unique())), ' trips')

st.subheader('Choose one trip to visualize')
tripoption = st.selectbox(' ', vehselected.orderid.unique())
tripselected = vehselected[vehselected.orderid == tripoption]

map_data = pd.DataFrame(columns = ['lat', 'lon'])
map_data['lat'] = tripselected.latitude
map_data['lon'] = tripselected.longitude
st.map(map_data)




# Create a connection object.
#conn = connect()
# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
#@st.cache(ttl=600)
#def run_query(query):
#    rows = conn.execute(query, headers=1)
#    rows = rows.fetchall()
#    return rows

#sheet_url = st.secrets['public_gsheets_url']
#rows = run_query(f'SELECT * FROM "{sheet_url}"')

# Print results.
#for row in rows:
#    st.write(row)
#    #st.write(f"{row.name} has a :{row.pet}:")
