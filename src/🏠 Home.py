import streamlit as st
from pathlib import Path
from Tree import Tree, Node
import pickle


def genTree():
    try:
        with open(Path(__file__).with_name('savedata.pickle'), 'rb') as outfile:
            t = pickle.load(outfile)

    except FileNotFoundError:
        t = Tree()

    return t

def section(name: str, t: Tree):
    node = t[name]
    if list(node.options.keys()) != []:
        selection = st.radio(
            node.label,
            node.options.keys()
        )
        if selection:
            section(t[node.options[selection]].NAME, t)
    else:
        st.subheader(name)

# Set sidebar width
st.markdown(f'''
    <style>
    section[data-testid="stSidebar"] .css-ng1t4o {{width: 14rem;}}
    </style>
''', unsafe_allow_html=True)

st.title('Home')
t = genTree()
section(t.getroot(), t)
