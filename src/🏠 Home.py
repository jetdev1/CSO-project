import streamlit as st

from Tree import Tree, getTree


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


if __name__ == '__main__':
    # Set sidebar width
    st.markdown(f"""
        <style>
        section[data-testid="stSidebar"] .css-ng1t4o {{width: 14rem;}}
        </style>
    """, unsafe_allow_html=True)

    st.title('Home')
    t = getTree()
    root = t.getroot()
    if root != 'Untitled':
        section(root, t)
    else:
        st.header('There are no root nodes.')
        st.markdown('> Create a node and check the "root" checkbox')
