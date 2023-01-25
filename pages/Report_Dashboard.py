import requests
import streamlit as st
from streamlit_lottie import st_lottie
import pandas as pd
import plotly.express as px


# ~~~~~ LOTTIE SETUP ~~~~~
def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# ~~~~~~~~~~~~~~~~~~~~ PAGE START ~~~~~~~~~~~~~~~~~~~~

# READ CSV FILE
df = pd.read_excel(io='data/inventory.xlsx', engine='openpyxl', sheet_name='Inventory', usecols='B:K')

col1, col2, col3 = st.columns([1, 3, 1])


# MIDDLE COLUMN, TO ALIGN IMAGE MIDDLE
with col2:
    st_lottie(load_lottie("https://assets8.lottiefiles.com/packages/lf20_qpsnmykx.json"), height=300, key="coding")
    st.markdown("<h1 style='text-align: center;'>Dashboard</h1>", unsafe_allow_html=True)

st.write("---")

with st.container():
    col1, col2, col3 = st.columns([1, 1, 1])

    name = st.multiselect(
        "Select by item:",
        options=df["Name"].unique(),
        default=df["Name"].unique()
    )

    df_name = df.query("Name==@name")

    with col2:
        st.markdown("<h3 style='text-align: center;'>Current Stock</h3>", unsafe_allow_html=True)

    with col1:
        st.write("##")
        st.plotly_chart(px.pie(
            df_name,
            values="Total Stock",
            names="Name",
            #x="Name",
            #y="Total Stock",
            #orientation="v",
            template="plotly_dark"
        ))

