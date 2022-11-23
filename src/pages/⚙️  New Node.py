import streamlit as st 
from pathlib import Path
import Tree


class CreateNode:
    def __init__(self) -> None:
        # Constants and variables
        self.tree = Tree.getTree()
        self.PATH = Path(__file__).parents[0].with_name('savedata.pickle')

        self.name = st.text_input('Name', key='name')
        self.label = st.text_input('Description', key='label')
        self.isroot = st.checkbox('Root')
        self.parent = st.selectbox('Parent', self.tree.keys(),
                                   disabled=self.isroot)
        if self.parent:
            self.parentOption = st.selectbox(
                'Parent Option',
                self.tree[self.parent].options.keys()
            )
        self.options = st.text_area(
            'Type each option on a new line',
            key='options'
        )
        st.button(
            'Create',
            on_click=self.submit
        )

    def submit(self) -> None:
        if self.name == '':
            st.warning('A name is required.')

        elif self.name == 'Untitled':
            st.warning('The name "Untitled" cannot be used.')

        elif self.isroot:
            self.tree._setroot(
                Tree.Node(
                    NAME=self.name,
                    label=self.label,
                    opts=self.options.split('\n')
                )
            )
            Tree.save(self.tree)
            st.info(f"Node '{self.name}' successfully created.")
            self.clearfields()

        elif self.parent and self.parentOption:
            if self.options != '':
                self.tree._addnode(
                    Tree.Node(
                        NAME=self.name.strip(),
                        PARENT=(self.parent, self.parentOption),
                        label=self.label.strip(),
                        opts=self.options.strip().split('\n')
                    )
                )
            else:
                self.tree._addnode(
                    Tree.Node(
                        NAME=self.name.strip(),
                        label=self.label.strip(),
                        PARENT=(self.parent, self.parentOption),
                    )
                )

            Tree.save(self.tree)
            self.clearfields()

        else:
            st.warning('Node not created.')

    def clearfields(self) -> None:
        fields = ('name', 'label', 'options')
        for f in fields:
            st.session_state[f] = ''

if __name__ == '__main__':
    CreateNode()
        
