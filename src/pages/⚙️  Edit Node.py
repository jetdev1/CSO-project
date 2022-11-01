import streamlit as st 
import Tree


class EditNode:
    def __init__(self) -> None:
        self.tree = Tree.getTree()
        
        st.title('Edit')
        node = st.selectbox('Node', self.tree._tree.keys())
        
        if node:
            self.value = st.text_input('Description', self.tree[node].label)

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
                self.tree[node].label = self.value
                Tree.save(self.tree)
                st.info(f"Edited node '{node}'")

        with col2:
            if st.button('Delete') and node:
                del self.tree[node]
                Tree.save(self.tree)
                st.info(f"Deleted node '{node}'")

if __name__ == '__main__':
    EditNode()

