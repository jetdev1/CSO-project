import pickle
import os
from dataclasses import dataclass, field
from typing import NamedTuple
import logging


@dataclass(frozen=True)
class Node:
    """
    Represents a node in the decision tree.

    Attributes:
        name (str): The name of the node. Used to refer back to the node.
        label(str): The question that the node asks.
        parent (tuple): (name of parent node, option to reach this node)
        options (list): List of options the user can choose from.
        others (namedTuple): Stores miscellaneous fields of the node.
    """
    name: str
    label: str
    parent: tuple[str, str]
    options: list = field(default_factory=list)
    others: NamedTuple = field(default_factory=NamedTuple)


@dataclass(frozen=True)
class Option:
    """
    Represents an option in the decision tree.

    Attributes:
        label (str): Label of option
        child (str): Name of child node
    """
    label: str
    child: Node | str | None = None


class Tree:
    """
    Collection of nodes to form a decision tree.

    Attributes:
        saveFile (str): Path to save existing tree to.
        loadFile (str): Path to load existing tree from.
        logging (bool): True enables logging.
    """
    def __init__(self, saveFile: str= None, loadfile: str = None, 
        logfile: str = None, logging: bool= True) -> None:
        # Logging setup
        LOGPATH = os.path.realpath(__file__) + r'/programLogs.log'

        self.__logger = logging.getself.__logger(__name__)
        self.__logger.setLevel(logging.DEBUG)

        fHandler = logging.FileHandler(LOGPATH, 'a', 'utf-8')
        fHandler.setLevel(logging.DEBUG)

        sHandler = logging.StreamHandler()
        sHandler.setLevel(logging.WARNING)

        fileFormatter = logging.Formatter('%(asctime)-23s | %(filename)-8s \
                                            | %(lineno)-3s | %(levelname)-8s | %(message)s')

        streamFormatter = logging.Formatter('%(module)-7s | %(levelname)-8s | %(message)s')
        fHandler.setFormatter(fileFormatter)
        sHandler.setFormatter(streamFormatter)

        self.__logger.addHandler(fHandler)
        self.__logger.addHandler(sHandler)

        if saveFile:
            try:
                with open(saveFile, 'rb') as f:
                    self.tree = pickle.load(f)
                    self.__logger.info("Loaded tree from file")

            except FileNotFoundError:
                self.tree = {}
                self.__logger.info("No save file found, starting new tree")

        else:
            self.tree = {}
            self.__logger.info("No save file given, starting new tree")

    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        pass

    def __len__(self) -> int:
        return len(self.tree)

    def __getitem__(self, name: str) -> Node:
        if name in self.tree:
            return self.tree[name]
        else:
            raise KeyError("Node not found")

    def __setitem__(self, node: Node, value: tuple = None) -> None:
        if node in self.tree:
            c = {
                "name": node.name, 
                "label": node.label,
                "options": node.options,
                "others": node.others
            }
            if value[0] in c:
                c[value[0]] = value[1]
                self.tree[node.name] = Node(**c)
                self.__logger.info("Changed node {}".format(node.name))
            else:
                raise KeyError(f"Invalid key: key {value[0]} not found.")
        else:
            self.__logger.debug("Node not found, creating new node.")
            self.tree[node.name] = node

            __parent = node.parent[0]

        self.save()

    def __delitem__(self, name: str) -> None:
        del self.tree[name]

    def __contains__(self, name: str) -> bool:
       return name in self.tree 

    def save(self) -> None:
        with open('saveData.pickle', 'wb+') as outfile:
            pickle.dump(self.tree, outfile)
        self.__logger.info("Saved tree to file")

    # def setOption(self, node: Node, option: Option) -> None:
    #     pass

    # def getOption(self, node: Node, option: Option) -> None:
    #     pass

    # def deleteOption(self, node: Node, option: str) -> None:
    #     pass
 
