import streamlit as st

import Tree


class CreateNode:
    def __init__(self) -> None:
        self.t = Tree.getTree()

        st.header('New Node')
        self.name = st.text_input('Name', key='name')
        self.label = st.text_input('Description', key='label')
        self.isroot = st.checkbox('Root')
        self.parent = st.selectbox('Parent', self.t.keys())

        if self.parent:
            self.parentopt = st.selectbox('Parent Option',
                                     self.t[self.parent].options.keys())
            self.opts = st.text_area('Type each option on a new line.', key='opts')
            st.button('Create', on_click=self.submit)


    def submit(self) -> None:
        fields = ('name', 'label', 'opts')
        for f in fields:
            st.session_state[f] = ''

        if self.name == '':
            st.warning('Name is required.')

        elif self.name == 'Untitled':
            st.warning('Name of node cannot be "Untitled"')

        else:
            # All pass, create node.
            if self.isroot and self.parent and self.parentopt:
                self.t._addnode(
                    Tree.Node(NAME=self.name, ROOT=self.isroot,
                              label=self.label,
                              opts=self.opts.split('\n')
                    )
                )
                st.info(f"Node '{self.name}' successfully created.")
                Tree.save(self.t)

            elif self.parent and self.parentopt:
                self.t._addnode(
                    Tree.Node(NAME=self.name,
                              PARENT=(self.parent, self.parentopt),
                              label=self.label,
                              opts=self.opts.split('\n')
                    )
                )
            st.info(f"Node '{self.name}' successfully created.")
            Tree.save(self.t)

if __name__ == '__main__':
    CreateNode()

