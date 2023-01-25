import requests
import streamlit as st
from streamlit_lottie import st_lottie
import pandas as pd


# ~~~~~ LOTTIE SETUP ~~~~~
def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# ~~~~~ WRITE DATA TO EXCEL ~~~~~
def write_excel(condition):
    if condition == "main":
        df.to_excel('data/inventory.xlsx', sheet_name="Inventory")
    elif condition == "backup":
        df.to_excel('data/backup/inventory_backup.xlsx', sheet_name="Inventory")
        st.success("Successfully pushed current table to backup.")


# ~~~~~~~~~~~~~~~~~~~~ PAGE START ~~~~~~~~~~~~~~~~~~~~

# READ CSV FILE
df = pd.read_excel(io='data/inventory.xlsx', engine='openpyxl', sheet_name='Inventory', usecols='B:K')

col1, col2, col3 = st.columns([1, 3, 1])


# MIDDLE COLUMN, TO ALIGN IMAGE MIDDLE
with col2:
    st_lottie(load_lottie("https://assets9.lottiefiles.com/packages/lf20_1n2cvwnt.json"), height=300, key="coding")
    st.markdown("<h1 style='text-align: center;'>Manage Inventory</h1>", unsafe_allow_html=True)
    st.write("---")


# CREATE NEW STOCK TYPE
with st.expander(label="Create New Stock", expanded=False):
    with st.form(key="create_new_stock", clear_on_submit=True):
        item_name = st.text_input("Name of new stock:")
        price = st.number_input("Enter cost per unit:", min_value=100, max_value=1500, step=1)
        sell_price = st.number_input("Enter selling price per unit:", min_value=100, max_value=1500, step=1)
        submitted = st.form_submit_button()

        if submitted:
            if item_name.strip() != "":
                df.loc[len(df.index)] = [item_name, 0, 0, price, 0, sell_price, "", "", "", ""]  # add new row to dataframe
                df.to_excel('data/inventory.xlsx', sheet_name="Inventory")  # commit changes to the excel file
                st.success("Successfully created new stock type: " + item_name + ".")
            else:
                st.error("Please enter a valid name.")



# FORM - BUY/SELL INVENTORY
with st.expander(label="Buy/Sell Stock", expanded=True):
    with st.form(key="add_inventory", clear_on_submit=True):

        items = df['Name'].tolist()
        selected_item = st.selectbox("Select Stock Item:", items)
        amount = st.number_input("Enter Stock Amount:", min_value=1, max_value=10, step=1)
        status = st.radio("Purchasing or Selling Stock?", index=0, options=('Purchasing','Selling'))
        submitted = st.form_submit_button("Submit Stock Changes")

        if submitted:

            x = 0
            i = -1
            for item in items:
                if item == selected_item:
                    i = x
                    break
                x = x+1

            if status == "Purchasing":
                if df.loc[0, 'Balance'] >= (df.loc[i, 'Cost per Unit'] * amount):  # IF BALANCE GREATER THAN STOCK'S COST, proceed
                    df.loc[i, 'Total Cost'] = (df.loc[i, 'Cost per Unit'] * amount) + df.loc[i, 'Total Cost'] # updates TOTAL COST
                    df.loc[i, 'Total Stock'] = df.loc[i, 'Total Stock'] + amount # updates TOTAL STOCK
                    df.loc[i, 'Total Sell Price'] = df.loc[i, 'Total Sell Price'] + (amount * df.loc[i, 'Sell Price per Unit'])  # update total sell price of all stock
                    df.loc[0, 'Balance'] = df.loc[0, 'Balance'] - (df.loc[i, 'Cost per Unit'] * amount)  # update TOTAL BALANCE (detract purchase price)
                    df.loc[0, 'Items Purchased'] = df.loc[0, 'Items Purchased'] + amount  # add amount to units purchased
                    df.loc[0, 'Total Profit'] = df.loc[0, 'Total Profit'] - (df.loc[i, 'Cost per Unit'] * amount)  # detract from total profit
                    st.success("Successfully purchased " + str(amount) + " " + selected_item + "s for R" + str(df.loc[i, 'Cost per Unit'] * amount) + ".")
                    write_excel("main")
                else:  # else show error.
                    st.error("Insufficient balance for this purchase.")
            elif status == "Selling":
                if df.loc[i, 'Total Stock'] >= amount:   # if amount selling DOES NOT exceed current stock, proceed.
                    df.loc[i, 'Total Cost'] = df.loc[i, 'Total Cost'] - (df.loc[i, 'Cost per Unit'] * amount)  # updates TOTAL COST
                    df.loc[i, 'Total Stock'] = df.loc[i, 'Total Stock'] - amount  # updates TOTAL STOCK
                    df.loc[i, 'Total Sell Price'] = df.loc[i, 'Total Sell Price'] - (amount * df.loc[i, 'Sell Price per Unit'])  # update total sell price of all stock
                    df.loc[0, 'Balance'] = df.loc[0, 'Balance'] + (df.loc[i, 'Sell Price per Unit'] * amount)  # update TOTAL BALANCE (add selling price)
                    df.loc[0, 'Items Sold'] = df.loc[0, 'Items Sold'] + amount  # add amount to units purchased
                    df.loc[0, 'Total Profit'] = df.loc[0, 'Total Profit'] + (df.loc[i, 'Sell Price per Unit'] * amount)  # increase total profit
                    st.success("Successfully sold " + str(amount) + " " + selected_item + "s for R" + str(df.loc[i, 'Sell Price per Unit'] * amount) + ".")
                    write_excel("main")
                else:
                    st.error("Can't sell more stock than exists in inventory.")

        with col2:
            st.markdown("<h2 style='text-align: center;'>Balance ~ R" + str("{:.2f}".format(df.loc[0, 'Balance'])) + "</h1>",unsafe_allow_html=True)
            st.write("##")


# Expand table (View)
with st.expander(label="Expand Table", expanded=True):
    dfShow = pd.read_excel(io='data/inventory.xlsx', engine='openpyxl', sheet_name='Inventory', usecols='B:G')
    st.dataframe(dfShow, use_container_width=True)
    if st.button("Push main table to backup"):
        write_excel("backup")





