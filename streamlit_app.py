from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import pandas
from gsheetsdb import connect
from google.oauth2 import service_account

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

sheet_url = st.secrets["private_gsheets_url"]
st.markdown(sheet_url)

result = conn.execute("""
    SELECT * FROM "https://docs.google.com/spreadsheets/d/1JznNtYSlTlOwmFq8baTR4Ws0r7f865wyPe2NG4m45a0/edit#gid=0" WHERE vehid = '9j22fi9gb62rB4luAgce49ahegf_qBbg'
""", headers=1)
for rows in result:
    st.write(rows)

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



