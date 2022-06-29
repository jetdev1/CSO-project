from dataclasses import dataclass, field
from pprint import pprint
import dataclasses
import pickle
import uuid
import inspect
import logging 
import os


# Things to do 
# 1. implement logging
#   a. Either find the working directory of the script and create the log in the same location or
#   b. Let user specify log file location in the logger config file
# 2. Write __str__ func 
# 3. Write docstrings

# CONSTANTS
LOGPATH = os.path.realpath(__file__) + r'/testLog.log'


# Logging setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

fHandler = logging.FileHandler(LOGPATH, 'a', 'utf-8')
fHandler.setLevel(logging.DEBUG)

sHandler = logging.StreamHandler()
sHandler.setLevel(logging.WARNING)

fileFormatter = logging.Formatter('%(asctime)-23s | %(filename)-8s \
                                  | %(lineno)-3s | %(levelname)-8s | %(message)s')
streamFormatter = logging.Formatter('%(module)-7s | %(levelname)-8s | %(message)s')
fHandler.setFormatter(fileFormatter)
sHandler.setFormatter(streamFormatter)

logger.addHandler(fHandler)
logger.addHandler(sHandler)


@dataclass(frozen=True)
class FlowOption:
    optionID: str
    label: str
    childNodeID: str


@dataclass(frozen=True, order=True)
class FlowNode:
    parentID: str
    parentOptionID: str
    label: str
    options: dict
    nodeID: str = str(uuid.uuid4())


@dataclass(frozen=True)
class TopNode:
    label: str
    options: dict 
    nodeID: str = str(uuid.uuid4())


class Flow:
    def __init__(self) -> None:
        try:
            with open('saveData.pickle', 'rb') as outfile:
                saveData = pickle.load(outfile)

            for key, value in saveData.items():
                setattr(self, key, value)

        except FileNotFoundError:
            # maybe log this to a separate file?
            logger.debug('No save file found.')
            # Create first node
            # self.topID = uuid.uuid4()
            # self.topNode = TopNode(str(input('Enter the label of the top node: ')), {})
            self.__flowNodes = {}

    def __str__(self) -> str:
        # construct and print entire flowchart
        pass

    def saveSession(self) -> str:
        try:
            # Retrive names and values of all properties
            saveDataKeys = [e for e in dir(self) if e[0:2] != '__']
            saveDataValues = [getattr(self, e) for e in saveDataKeys]
            saveData = {}

            for key, value in zip(saveDataKeys, saveDataValues):
                saveData[key] = value

            with open('saveData.pickle', 'ab') as file:
                pickle.dump(saveData, file)

            logger.info('Data successfully saved at ~/saveData.pickle')

        except Exception as e:
            logger.exception('Error occurred in saveSession()')

    
    def addNode(self, node) -> None:
        self.__flowNodes[node.nodeID] = node
        self.saveSession()

    def deleteNode(self, nodeID) -> None:
        try:
            del self.__flowNodes[nodeID]

        except KeyError:
            logger.exception(f'Delete unsuccessful, node {nodeID} not found.')

    def editNode(self, nodeID, **kwargs):
        self.keysFound = False

        # Check the unpacking of kwargs
        for key, value in kwargs:
            if key not in dir(self.__flowNodes[nodeID]):
                self.keysFound = False
                print(f'Property {key} does not exist in flowNode object.')
                logger.error(f'Property {key} does not exist in flowNode object.')
            else:
                self.keysFound = True

        if self.keysFound:
            dataclasses.replace(self.__flowNodes[nodeID], **kwargs)
            logger.debug(f'Property has been added.\n{self.__flowNodes[nodeID]}')


if __name__ == '__main__':
    a = FlowNode(str(uuid.uuid4()), str(uuid.uuid4()), 'Hello World!', {})
    pprint(inspect.getmembers(FlowNode, inspect.isfunction))
    pprint(a)