from dataclasses import dataclass, field
from Tree.Tree import Tree


@dataclass
class Node:
    """
    Node in tree data structure

    Attributes:
        TREE (Tree): Tree to automatically attach this node to.
        NAME (str): The name of the node. Used to refer back to the node.
        PARENT (tuple): (name of parent node, option to reach this node)
        ROOT (bool): Pass True if this is the root node.
        options (list): List of options the user can choose from.
        fields (dict): Additional fields to store in node.
    """
    TREE: Tree
    NAME: str
    PARENT: tuple[str, str] = field(default_factory=tuple)
    ROOT: bool = False
    label: str = ''
    opts: list[str] = field(default_factory=list)
    fields: dict = field(default_factory=dict)

    def __post_init__(self):
        if not self.ROOT:
            self.TREE[self.PARENT[0]]._setchild(self.PARENT[1], self.NAME)
        else:
            self.TREE._setroot(self.NAME)

        self.TREE._addnode(self)
        self.options = {k: '' for k in self.opts}

    def _setchild(self, option: str, child: str):
        if option in self.options:
            self.options[option] = child
            if self.ROOT:
                self.TREE._setroot(self.NAME)
        else:
            raise KeyError(f"Option '{option}' does not exist in node '{self.NAME}")

