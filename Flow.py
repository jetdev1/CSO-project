from dataclasses import dataclass, field
from pprint import pprint
import dataclasses
import pickle
import uuid
import inspect
import logging 


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
    __flowNodes: dict

    def __init__(self) -> None:
        try:
            with open('saveData.pickle', 'rb') as outfile:
                saveData = pickle.load(outfile)

            for key, value in saveData.items():
                setattr(self, key, value)

        except FileNotFoundError:
            # maybe log this to a separate file?
            print('No save file found.')
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

            return 'Data successfully saved at ~/saveData.pickle'

        except Exception as e:
            return f'An error occurred.\n\n{e}'

    
    def addNode(self, node) -> None:
        self.__flowNodes[node.nodeID] = node
        returnStatus = self.saveSession()
        print(returnStatus)

    def deleteNode(self, nodeID) -> None:
        try:
            del self.__flowNodes[nodeID]

        except KeyError:
            print(f'Delete unsuccessful, node {nodeID} not found.')

    def editNode(self, nodeID, **kwargs):
        self.keysFound = False

        # Check the unpacking of kwargs
        for key, value in kwargs:
            if key not in dir(self.__flowNodes[nodeID]):
                self.keysFound = False
                print(f'Property {key} does not exist in flowNode object.')
            else:
                self.keysFound = True

        if self.keysFound:
            dataclasses.replace(self.__flowNodes[nodeID], **kwargs)


if __name__ == '__main__':
    a = FlowNode(str(uuid.uuid4()), str(uuid.uuid4()), 'Hello World!', {})
    pprint(inspect.getmembers(FlowNode, inspect.isfunction))
    pprint(a)