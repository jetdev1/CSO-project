import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict
import pickle


@dataclass
class Node:
    """
    Node in tree data structure

    Attributes:
        NAME (str): The name of the node. Used to refer back to the node.
        PARENT (tuple): (name of parent node, option to reach this node)
        ROOT (bool): Pass True if this is the root node.
        label (str): Description of node.
        opts (list): List of options the user can choose from.
        fields (dict): Additional fields to store in node.
    """
    NAME: str
    PARENT: tuple[str, str] = field(default_factory=tuple)
    ROOT: bool = False
    label: str = ''
    opts: list[str] = field(default_factory=list)
    fields: Dict[str, Any] = field(default_factory=dict)
    options: Dict[str, str] = field(default_factory=dict)

    def __post_init__(self):
        if self.options == {}:
            self.options = {k: 'Untitled' for k in self.opts}

    def _setchild(self, option: str, child: str):
        if option in self.options:
            self.options[option] = child
        else:
            raise KeyError(f"Option '{option}' does not exist in node '{self.NAME}")


class Tree:
    """
    Collection of nodes to form a Tree structure.
    """

    def __init__(self) -> None:
        self.root = 'Untitled'
        self._tree = {'Untitled': Node(NAME='Untitled')}
        
        # Logging setup
        self.__logger = self.__createlogger()

    def __createlogger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        fhandler = logging.FileHandler(str(Path(__file__).with_name('log.txt')), 'a+')
        fhandler.setLevel(logging.INFO)
        shandler = logging.StreamHandler()
        shandler.setLevel(logging.WARNING)
        fileFormatter = logging.Formatter('%(asctime)-23s | %(filename)-8s \
                                            | %(lineno)-3s | %(levelname)-8s | %(message)s')
        streamFormatter = logging.Formatter('%(module)-7s | %(levelname)-8s | %(message)s')
        fhandler.setFormatter(fileFormatter)
        shandler.setFormatter(streamFormatter)

        logger.addHandler(fhandler)
        logger.addHandler(shandler)

        return logger

    def keys(self) -> list:
        """
        Returns the keys of the tree as a list.
        """
        return list(self._tree.keys())

    def __str__(self) -> str:
        self.__CHARS = {
            'vert': '│  ',
            't-joint': '├──',
            'corner': '└──',
            'space': ' ' * 3
        }

        if self.root == '':
            raise KeyError('No root node found in tree.')
        elif self._tree == {}:
            raise KeyError('Tree is empty and has no nodes attached.')
        else:
            __ret = self.__preorder(self.root)
        
        return "\n".join(__ret)

    def __preorder(self, node: str, arr: list = list(), indent: int = 0,
                   space: int = 0, last: bool = False) -> list:
        """
        Traverse through the tree using the preorder method
        Arguments:
            node (str): name of node to visit
            arr (list): accumulates output
            indent (int): indent level 
            space (int): indent without verticle char 
            last (bool): True if current node is last branch of parent

        Returns:
            list: contains lines of a visual representation of the tree
        """
        __opts = self._tree[node].options.keys()
        __joint = self.__CHARS['corner'] if last else self.__CHARS['t-joint']
        s = [
            self.__CHARS['vert'] * (indent - 1 if indent > 0 else 0),
            self.__CHARS['space'] * space,
            __joint if (indent+space) > 0 else '',
            node
        ]
        
        arr.append("".join(s))

        for n, opt in enumerate(__opts):
            arr = self.__preorder(
                node=self._tree[node].options[opt],
                arr=arr,
                indent=indent if last else indent + 1,
                space=space + 1 if last else space,
                last=(n == (len(__opts) - 1))
            )

        return arr

    def __repr__(self) -> str:
        return str(self._tree)

    def __len__(self) -> int:
        return len(self._tree)

    def __getitem__(self, name: str) -> Node:
        if name in self._tree:
            return self._tree[name]
        else:
            raise KeyError(f"Node {name} not found")

    def __delitem__(self, name: str) -> None:
        if name == self.root:
            self.root = 'Untitled'

        del self._tree[name]

    def __contains__(self, name: str) -> bool:
       return name in self._tree 

    def pop(self, node: str) -> Node:
        return self._tree.pop(node)

    def _setroot(self, node: Node):
        """
        Assign node as root node.

        Arguments:
            node: Name of root node.
        """

        self.root = node.NAME
        self._tree[node.NAME] = node

    def _addnode(self, node: Node | list[Node]) -> None:
        """
        Add node to tree.
        
        Attributes:
            node (Node | list[node]): Node(s) to add to tree
            root (bool): Defaults to False. Pass True if node is root node,
        """

        if type(node) is list:
            for n in node:
                self._tree[n.NAME] = n
                self._tree[n.PARENT[0]]._setchild(n.PARENT[1], n.NAME)
        elif type(node) is Node:
            self._tree[node.NAME] = node
            self._tree[node.PARENT[0]]._setchild(node.PARENT[1], node.NAME)

    def getroot(self):
        return self.root

    def setfield(self, node: str, field: Any, value: Any) -> None:
        """
        Edit or add a field to a node in the tree.
        Arguments:
            node (str): Name of node
            field (Any): field to chagne
            value (Any): value of field 
        """
        if node in self._tree:
            self._tree[node].fields[field] = value
        else:
            raise KeyError(f'Node {node} does not exist.')
    
    def delfield(self, node: str, field: Any) -> None:
        if node in self._tree and node in self._tree[node].fields:
            del self._tree[node].fields[field]
        else:
            raise KeyError('Node/field combination does not exist.')

    def setoption(self, node: str, label: str, child: str = '') -> None:
        if node in self._tree:
            self._tree[node].options[label] = child
        else:
            raise KeyError(f'Node {node} does not exist.')

    def deloption(self, node: str, option: str) -> None:
        if node in self._tree and option in self._tree[node].options:
            del self._tree[node].options[option]

        else:
            raise KeyError('node/option combination does not exist.')


def getTree() -> Tree:
    try:
        with open(Path(__file__).with_name('savedata.pickle'), 'rb') as outfile:
            t = pickle.load(outfile)
    except FileNotFoundError:
        t = Tree()

    return t

def save(t: Tree):
    if 'Untitled' not in t:
        t._addnode(Node('Untitled'))
    # Saves to data file in src directory
    p = Path(__file__).with_name('savedata.pickle')
    with open(p, 'wb+') as infile:
        pickle.dump(t, infile)

def getfile():
    with open(Path(__file__).with_name('savedata.pickle'), 'rb') as outfile:
        return outfile

