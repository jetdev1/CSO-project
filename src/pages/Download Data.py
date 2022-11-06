import streamlit as st 
from pathlib import Path


p = Path(__file__).parents[1].with_name('savedata.pickle')
try:
    with open(p, 'rb') as outfile:
        st.download_button('Download data', outfile)

except FileNotFoundError:
    st.warning('No save data found.')
