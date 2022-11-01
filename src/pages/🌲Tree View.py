import streamlit as st
import Tree
import graphviz


def preorder(node: str):
    if node != 'Untitled':
        for key, val in tree[node].options.items():
            if val != 'Untitled':
                graph.edge(key, val)
            graph.edge(node, key)
            preorder(val)


if __name__ == '__main__':
    tree = Tree.getTree()
    root = tree.getroot()
    graph = graphviz.Digraph()
    if root != 'Untitled':
        preorder(root)
        st.graphviz_chart(graph)
    else:
        st.subheader('No root node found.')
