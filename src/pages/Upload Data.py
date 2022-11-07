import streamlit as st 
from pathlib import Path
import pickle
import Tree


uploaded = st.file_uploader('Upload .pickle data file')
if uploaded and st.button('Load'):
        t = pickle.load(uploaded)
        Tree.save(t)
        st.info('Data successfully loaded!')
