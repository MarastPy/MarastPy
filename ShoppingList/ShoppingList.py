# Documentation https://docs.streamlit.io/get-started

import streamlit as st
from io import StringIO
import functions
import pandas as pd
import numpy as np
import time

def add_list():
    list = st.session_state["new_list"] + "\n"
    lists.append(list)
    functions.write_lists(lists,"ShoppingList/list.txt")

# Chosse your shop
selected_shop = st.sidebar.selectbox(
    'Which shop are you going to?',
    ('Albert', 'Tesco', 'BILLA')
)
st.title(f"Hi this is preparation for my shopping list you are going to: {selected_shop}")
st.write("You selected:", selected_shop)


# List of items with check boxes
lists = functions.get_list("ShoppingList/list.txt")

st.text_input(label="Here is an exmaple for adding new items into the shopping list", placeholder="Add new to list...", on_change=add_list, key="new_list")

for index, list in enumerate(lists):
    # vygeneruje checkbox a zapise do Session Dictionery jako zde: {"ping-pong":false, "new_todo":""}, key je prvni, druhy "false" je stav checkboxu, zaskrtnuty nebo ne
    checkbox = st.checkbox(list, key=list)
    # When its in FrontEndu then its beeing executed
    if checkbox is True:
        lists.pop(index)    # it delets list
        functions.write_lists(lists, "lists.txt")
        del st.session_state[list] # deleted record from session session
        st.rerun()

# Active session of selected
#st.session_state


#Sharing file
uploaded_file = st.file_uploader("C:\Marek\Programming\Python\IDC\Task_1.xlsx")
if uploaded_file:
    # Read the Excel file into a Pandas dataframe
    df = pd.read_excel(uploaded_file)
    # Display the dataframe as a table in Streamlit
    st.dataframe(df)

# streamlit run ShoppingList/ShoppingList.py