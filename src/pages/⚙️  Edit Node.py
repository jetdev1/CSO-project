import streamlit as st 
import Tree


class EditNode:
    def __init__(self) -> None:
        self.tree = Tree.getTree()
        
        st.title('Edit')
        node = st.selectbox('Node', self.tree.keys())
        if node:
            self.value = st.text_input('Description', self.tree[node].label)
            self.opts = st.text_area('Options', value='\n'.join(self.tree[node].options))
            self.newopts = self.opts.split('\n')

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
                self.node = self.tree[node]
                self.node.label = self.value
                for s in self.newopts:
                    if s not in self.node.options:
                        self.node.options[s] = 'Untitled'
                for s in [e for e in self.node.options.keys() if e not in self.newopts]:
                    del self.tree[s]
                Tree.save(self.tree)
                st.info(f"Edited node '{node}'")
        with col2:
            if st.button('Delete') and node:
                if node != 'Untitled':
                    del self.tree[node]
                    Tree.save(self.tree)
                    st.info(f"Deleted node '{node}'")
                else:
                    st.info('The node Untitled cannot be deleted.')


        st.markdown('---')
        st.markdown('<h1 style="color: red;">Danger Zone</h1>', unsafe_allow_html=True)
        st.subheader('Override parent node - select node in above section')
        if node:
            parent = self.tree[node].PARENT
            if len(parent) != 0:
                self.newparent = st.selectbox('Parent Node', self.tree.keys(),
                                              index=self.tree.keys().index(self.tree[node].PARENT[0]))
                if self.newparent:
                    self.newparentopt = st.selectbox('Parent Option', list(self.tree[self.newparent].options.keys()),
                                                     index=list(self.tree[self.newparent].options.keys()).index(self.tree[node].PARENT[1]))
                cnode = self.tree[node]
                if st.button('Override parent node') and self.newparent and self.newparentopt:
                    self.tree._addnode(Tree.Node(
                        NAME=cnode.NAME,
                        PARENT=(self.newparent, self.newparentopt),
                        label=cnode.label,
                        options=cnode.options
                    ))
                    del self.tree[node]
        else:
            st.write('No valid node selected.')

        st.markdown('<br>', unsafe_allow_html=True)
        st.subheader('Override root node')
        n = st.selectbox('New root node', list(self.tree._tree.keys()))

        if n and st.button('Override'):
            self.tree._setroot(self.tree[n])
            Tree.save(self.tree)
            st.info('Root has been updated!')

if __name__ == '__main__':
    EditNode()

