import pandas as pd
import streamlit as st
from difflib import get_close_matches

df_ratings = pd.read_csv(r'Keggle downloads/Ratings.csv', encoding='cp1251', sep=',')

print(df_ratings.mean())