import streamlit as st
from Tree import Tree, Node
from pathlib import Path
import pickle


def genTree():
    try:
        with open(Path(__file__).with_name('savedata.pickle'), 'rb') as outfile:
            t = pickle.load(outfile)

    except FileNotFoundError:
        t = Tree()

    return t

def createnode() -> None:
    global parentopt

    st.header('New Node')
    name = st.text_input('Name', key='name')
    label = st.text_input('Description', key='label')
    parent = st.selectbox('Parent', t._tree.keys(), key='parent')
    if parent:
        parentopt = st.selectbox('Parent Option',
                                 t[parent].options.keys(), key='parentopt')
        opts = st.text_area('List of Options: Place each option on separate lines',
                            key='opts')
        submitted = st.button('Create', on_click=__cleartext)
        if submitted and parentopt:
            t._addnode(
                Node(NAME=name, PARENT=(parent, parentopt), label=label,
                     opts=opts.split('\n'))
            )
            st.info(f"Created node with name \"{name}\"")

def __cleartext() -> None:
    global parentopt

    fields = ('name', 'label', 'opts')
    for f in fields:
        st.session_state[f] = ''
    if not parentopt:
        st.warning('A parent option is required.')
            
if __name__ == '__main__':
    t = genTree()
    createnode()

