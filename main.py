import requests
import streamlit as st
from streamlit_lottie import st_lottie
import pandas as pd
import plotly.express as px

# TO DEPLOY: https://www.youtube.com/watch?v=nJHrSvYxzjE

# ~~~~~~~~~~~~~~~~~~~~ MAIN ~~~~~~~~~~~~~~~~~~~~
def main():
    setup()

    # WEBPAGE START
    st.title("Welcome!")
    st.subheader("This is a site to manage sales & inventory.")
    st.write("Created by Daniel Wood.")


# ~~~~~~~~~~~~~~~~~~~~ SETUP FUNCTION ~~~~~~~~~~~~~~~~~~~~
def setup():
    # PAGE CONFIG
    st.set_page_config(
        page_title="Sales Management Site",
        initial_sidebar_state="auto",
        page_icon=":abacus:",
        layout="wide"
    )

    # CS SSETUP
    with open("C:/Users/WDXDAN004/Desktop/python-projects/sales/style/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ~~~~~~~~~~~~~~~~~~~~ LOTTIE SETUP FUNCTION, takes lottie URL to display graphics ~~~~~~~~~~~~~~~~~~~~
def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# ~~~~~~~~~~~~~~~~~~~~ CALL TO MAIN FUNCTION ~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    main()