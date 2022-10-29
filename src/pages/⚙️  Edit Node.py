from Tree import Tree
from pathlib import Path
import pickle
import streamlit as st 


def genTree() -> Tree:
    try:
        with open(Path(__file__).with_name('savedata.pickle'), 'rb') as outfile:
            t = pickle.load(outfile)

    except FileNotFoundError:
        t = Tree()

    return t


def editnode():
    global t
    t = genTree()
    st.title('Edit')
    node = st.selectbox('Node', t._tree.keys())
    if node:
        value = st.text_input('Description', t[node].label)

    st.markdown("""
    <style>
        .stButton>button {
            color: #4F8BF9;
            width: 21em;
        }
    </style>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Confirm') and node:
            t[node].label = value
            st.info(f"Edited node {node}")

    with col2:
        if st.button('Delete'):
            st.info(f"Deleted node {node}")
            del(t, node)

def savedata():
    global t
    with open(Path(__file__).with_name('savedata.pickle'), 'wb+') as outfile:
        pickle.dump(t, outfile)

if __name__ == '__main__':
    editnode()
