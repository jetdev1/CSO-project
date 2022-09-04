import logging
import os
import pickle
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Node:
     """
     Represents a node in the decision tree.
 
     Attributes:
         tree (Tree): Tree to automatically attach this node to.
         name (str): The name of the node. Used to refer back to the node.
         label (str): The question that the node asks.
         parent (tuple): (name of parent node, option to reach this node)
         options (list): List of options the user can choose from.
         fields (dict): Additional fields to store in node.
     """
     TREE: Any 
     PARENT: tuple[str, str]
     NAME: str
     options: list = field(default_factory=list)
     fields: dict = field(default_factory=dict)

     def __post_init__(self):
         self.TREE._addnode(self)


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
        # Logging setup
        if logPath != '':
            __LOGPATH = os.path.realpath(__file__) + r'/programLogs.log'
        else:
            __LOGPATH = logPath

        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(logging.DEBUG)

        fHandler = logging.FileHandler(__LOGPATH, 'a', 'utf-8')
        fHandler.setLevel(logging.DEBUG)

        sHandler = logging.StreamHandler()
        sHandler.setLevel(logging.WARNING)

        fileFormatter = logging.Formatter('%(asctime)-23s | %(filename)-8s \
                                            | %(lineno)-3s | %(levelname)-8s | %(message)s')

        streamFormatter = logging.Formatter('%(module)-7s | %(levelname)-8s | %(message)s')
        fHandler.setFormatter(fileFormatter)
        sHandler.setFormatter(streamFormatter)

        if enable_logging:
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
        pass

    def __repr__(self) -> str:
        pass

    def __len__(self) -> int:
        return len(self._tree)

    def __getitem__(self, name: str) -> Node:
        if name in self._tree:
            return self._tree[name]
        else:
            raise KeyError("Node not found")

    # TODO: remove __setitem__ method and create addnode, editnode methods.
    def _addnode(self, node: Node) -> None:
        """
        Add node to tree.
        """
        if node.NAME not in self._tree:
            self._tree[node.NAME] = node
        else:
            raise ValueError(f"Node with name {node.NAME} exists in tree.")

    def _setnode(self, node: str | Node, field: str, value: Any) -> None:
        """
        Edit field(s) of a node in the tree.
        Arguments:
            node (str | Node): Name of node to edit
            field (str | tuple): Field(s) to set 
            value (Any): New value of field
        """
        nd = self._tree[node] if type(node) is str else node
        if field == 'options':
            pass
            
    def __setitem__(self, name: str, node: Node | tuple) -> None:
        if name in self._tree:
            c = {
                "name": name, 
                "label": self._tree[name].label,
                "options": self._tree[name].options,
            }
            if node[0] in c:
                c[node[0]] = node[1]
                self._tree[name] = Node(**c)
                self.__logger.info("Changed node {}".format(name))
            else:
                raise KeyError(f"Invalid key: key {node[0]} not found.")
        else:
            self.__logger.debug("Node not found, creating new node.")
            self._tree[name] = name

            __parent = self._tree[name].parent[0]

        self.save()

    # Not sure if there's a way to delete without disconnecting a whole part.
    def __delitem__(self, name: str) -> None:
        del self._tree[name]

    def __contains__(self, name: str) -> bool:
       return name in self._tree 

    def save(self) -> None:
        with open('saveData.pickle', 'wb+') as outfile:
            pickle.dump(self._tree, outfile)
        self.__logger.info("Saved tree to file")

    def getTree(self) -> dict:
        """
        Returns the tree as a list of Nodes.
        """
        return self._tree

    # def setOption(self, node: Node, option: Option) -> None:
    #     pass

    # def getOption(self, node: Node, option: Option) -> None:
    #     pass

    # def deleteOption(self, node: Node, option: str) -> None:
    #     pass
 
