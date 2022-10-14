import pytest
from Tree.Tree import Tree, Node


@pytest.fixture
def bTree():
    t = Tree()
    Node(
        TREE=t,
        NAME='Root',
        options=['finance', 'housing', 'healthcare'],
        fields={'label': 'Select the category of assistance the client requires.'}
    )

