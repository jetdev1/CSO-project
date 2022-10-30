import streamlit as st

from Tree import getTree, save


def editnode():
    global t
    t = getTree()
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


if __name__ == '__main__':
    editnode()
