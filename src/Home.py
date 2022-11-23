import streamlit as st
import validators
import Tree


def section(name: str, t: Tree.Tree):
    node = t[name]
    if list(node.options.keys()) != []:
        st.subheader(name)
        selection = st.radio(
            node.label,
            list(node.options.keys())
        )
        st.markdown('---')
        if selection:
            section(t[node.options[selection]].NAME, t)
    else:
        if validators.url(node.label):
            st.markdown(f"<p style='font:sans-serif; background-color:darkslategray;\
                        font-size:35px; border: 10px solid darkslategray;\
                        border-radius:10px;'>\
                        <b>{name}</b> <br> <a style='font-size:24px;'href={node.label}>{node.label}</a></p>",
                        unsafe_allow_html=True)
        else:
            st.markdown(f"<p style='font:sans-serif; background-color:dimgray;\
                        font-size:35px; border: 10px solid dimgray;\
                        border-radius:10px;'>\
                        <b>{name}</b> <br> {node.label}</p>",
                        unsafe_allow_html=True)



if __name__ == '__main__':
    # Set sidebar width
    st.markdown(f"""
        <style>
        section[data-testid="stSidebar"] .css-ng1t4o {{width: 14rem;}}
        </style>
    """, unsafe_allow_html=True)

    st.title('Home')
    
    tree = Tree.getTree()
    root = tree.getroot()
    if root != 'Untitled':
        section(root, tree)

    else:
        st.header('There are no root nodes.')
        st.markdown('Create a node and check the "root" checkbox')

