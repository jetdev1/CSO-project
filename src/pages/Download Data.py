import streamlit as st 
from pathlib import Path
import Tree


p = Path(__file__).parents[1].with_name('savedata.pickle')
try:
    outfile = Tree.getfile()
    st.download_button('Download data', outfile)

except FileNotFoundError:
    st.warning('No save data found.')
