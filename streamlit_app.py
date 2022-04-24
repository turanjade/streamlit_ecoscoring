from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import pandas
from gsheetsdb import connect
from google.oauth2 import service_account
from shillelagh.backends.apsw.db import connect

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

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials)
st.write('connection created')

result = conn.execute("""
    SELECT
        country
      , SUM(cnt)
    FROM
        "https://docs.google.com/spreadsheets/d/1_rN3lm0R_bU3NemO0s9pbFkY5LQPcuy1pscv8ZXPtg8/"
    GROUP BY
        country
""", headers=1)
for row in result:
    print(row)


# Print results.
#st.write(rows)

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



