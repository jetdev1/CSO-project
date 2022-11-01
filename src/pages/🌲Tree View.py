import streamlit as st
import Tree
import graphviz


def preorder(node: str):
    if node != 'Untitled':
        for key, val in tree[node].options.items():
            graph.node(key, shape='box')
            if val != 'Untitled':
                graph.edge(key, val)
                graph.node(val, shape='box')
            graph.edge(node, key)
            preorder(val)


if __name__ == '__main__':
    tree = Tree.getTree()
    root = tree.getroot()
    graph = graphviz.Digraph()
    graph.edge_attr.update(arrowhead='vee', arrowsize='1')
    graph.graph_attr.update(splines='ortho')
    if root != 'Untitled':
        preorder(root)
        st.graphviz_chart(graph)
    else:
        st.subheader('No root node found.')
