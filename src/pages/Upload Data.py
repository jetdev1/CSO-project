import streamlit as st 
from pathlib import Path
import pickle


uploaded = st.file_uploader('Upload .pickle data file')
if uploaded:
        t = pickle.load(uploaded)
        st.info('Data successfully loaded!')
