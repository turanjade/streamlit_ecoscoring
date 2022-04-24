from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
from gsheetsdb import connect
from google.oauth2 import service_account

"""
#This is eco-score!
"""

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

query = 'SELECT orderid, vehid FROM "https://docs.google.com/spreadsheets/d/1JznNtYSlTlOwmFq8baTR4Ws0r7f865wyPe2NG4m45a0/edit#gid=0" WHERE orderid = "4da2cfjf443wB5eDp6b34honega1xx6n"'
result = conn.execute(f"""
    {query}
""", headers=1)

i = 1
for rows in result:
    st.write(type(rows))
    if i == 1:
        break

gs_id = "1JznNtYSlTlOwmFq8baTR4Ws0r7f865wyPe2NG4m45a0"
sheetname = "sampledata"
gs_url = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(gs_id, sheetname)
st.write(gs_url)
selected = pd.read_csv(gs_url)

st.write(selected.head())
#results = results.fetchall()
#st.write('fetch all')
selecteddata = pd.DataFrame(results, columns = ['orderid', 'vehid']) #, columns=['recordid', 'vehid', 'orderid', 'time', 'longitude', 'latitude', 'date'])
st.write(selecteddata.head())

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



