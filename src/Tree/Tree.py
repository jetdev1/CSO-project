import logging
import os
import pickle
from dataclasses import dataclass, field
from typing import Any


# TODO: add rootnode class
@dataclass
class Node:
    """
    Represents a node in the decision tree.

    Attributes:
        TREE (Tree): Tree to automatically attach this node to.
        NAME (str): The name of the node. Used to refer back to the node.
        PARENT (tuple): (name of parent node, option to reach this node)
        options (list): List of options the user can choose from.
        fields (dict): Additional fields to store in node.
    """
    TREE: Any 
    NAME: str
    PARENT: tuple[str, str] = field(default_factory=tuple)
    options: list[Any] = field(default_factory=list)
    fields: dict = field(default_factory=dict)

    def __post_init__(self):
        self.TREE._addnode(self)
        self.TREE[self.PARENT[0]]._setchild(self.PARENT[0], self.PARENT[1])
        self.opts = {k: '' for k in self.options}

    def _setchild(self, option: str, child: str):
        if option in self.options:
            self.opts[option] = child
        else:
            raise KeyError(f'Option {option} does not exist in node {self.NAME}')


class Tree:
    """
    Collection of nodes to form a decision tree.

    Attributes:
        savePath (str): Path to save existing tree to.
        loadPath (str): Path to load existing tree from.
        logPath(str): Path to log file.
        enable_logging (bool): True enables logging.
    """

    def __init__(self, savePath: str = '', loadPath: str = '', 
        logPath: str = '', enable_logging: bool = False) -> None:
        self.SAVEPATH = savePath

        # Logging setup
        if logPath == '':
            __arr = os.path.abspath(__file__).split('/')[:-1]
            __arr.append(r'programlogs.log')
            __LOGPATH = "/".join(__arr)
        else:
            __LOGPATH = logPath

        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(logging.DEBUG)

        if enable_logging:
            fHandler = logging.FileHandler(__LOGPATH, 'a+')
            fHandler.setLevel(logging.INFO)

            sHandler = logging.StreamHandler()
            sHandler.setLevel(logging.WARNING)

            fileFormatter = logging.Formatter('%(asctime)-23s | %(filename)-8s \
                                                | %(lineno)-3s | %(levelname)-8s | %(message)s')

            streamFormatter = logging.Formatter('%(module)-7s | %(levelname)-8s | %(message)s')
            fHandler.setFormatter(fileFormatter)
            sHandler.setFormatter(streamFormatter)
            self.__logger.addHandler(fHandler)
            self.__logger.addHandler(sHandler)

        if loadPath:
            try:
                with open(loadPath, 'rb') as f:
                    self.__filedata = pickle.load(f)
                    if type(self.__filedata) == dict:
                        self._tree = self.__filedata
                        self.__logger.info("Loaded tree from file")
                    else:
                        self._tree = {}
                        self.__logger.error("Invalid file data.")

            except FileNotFoundError:
                self._tree = {}
                self.__logger.info("No save file found, starting new tree")

        else:
            self._tree = {}
            self.__logger.info("No save file given, starting new tree")

    def __str__(self) -> str:
        self.__CHARS = {
            'vert': '│  ',
            't-joint': '├──',
            'corner': '└──',
            'space': ' ' * 3
        }

        if 'root' not in self._tree:
            raise KeyError('No root node found in tree.')
        elif self._tree == {}:
            raise KeyError('Tree is empty and has no nodes attached.')
        else:
            __ret = self.__preorder('root')
        
        return "".join(__ret)

    def __preorder(self, node: str, __arr: list = [], indent: int = 0,
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
            __joint if (indent+space)> 0 else '',
            node
        ]
        
        __arr.append("".join(s))

        for n, opt in enumerate(__opts):
            __arr = self.__preorder(
                node=opt,
                __arr=__arr,
                indent=indent if last else indent + 1,
                space=space + 1 if last else space,
                last=(n == (len(__opts) - 1))
            )

        return __arr

    def __repr__(self) -> str:
        return str(self._tree)

    def __len__(self) -> int:
        return len(self._tree)

    def __getitem__(self, name: str) -> Node:
        if name in self._tree:
            return self._tree[name]
        else:
            raise KeyError("Node not found")

    def __delitem__(self, name: str) -> None:
        del self._tree[name]

    def __contains__(self, name: str) -> bool:
       return name in self._tree 

    def pop(self, node: str) -> Node:
        return self._tree.pop(node)

    def _addnode(self, node: Node) -> None:
        """
        Add node to tree.
        """
        if node.NAME not in self._tree:
            self._tree[node.NAME] = node
        else:
            raise ValueError(f"Node with name {node.NAME} exists in tree.")

    def setfield(self, node: str, field: Any, value: Any):
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
    
    def delfield(self, node: str, field: Any):
        if node in self._tree and node in self._tree[node].fields:
            del self._tree[node].fields[field]
        else:
            raise KeyError('Node/field combination does not exist.')

    def setoption(self, node: str, label: str, child: str = ''):
        if node in self._tree:
            self._tree[node].options[label] = child
        else:
            raise KeyError(f'Node {node} does not exist.')

    def deloption(self, node: str, option: str):
        if node in self._tree and option in self._tree[node].options:
            del self._tree[node].options[option]

        else:
            raise KeyError('node/option combination does not exist.')

    def save(self) -> None:
        with open('saveData.pickle', 'wb+') as outfile:
            pickle.dump(self._tree, outfile)
        self.__logger.info("Saved tree to file")

 
