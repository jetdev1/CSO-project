import streamlit as st 
from pathlib import Path
import Tree


p = Path(__file__).parents[0].with_name('savedata.pickle')
print(p)
try:
    outfile = Tree.getfile()
    with open(p, 'rb') as f:
        st.download_button('Download data', f)

except FileNotFoundError:
    st.warning('No save data found.')
