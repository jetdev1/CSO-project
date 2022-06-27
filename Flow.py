from dataclasses import dataclass, field
import dataclasses
import pickle
import uuid


@dataclass(frozen=True)
class FlowOption:
    optionID: str
    label: str
    childNodeID: str


@dataclass(frozen=True, order=True)
class FlowNode:
    objID: str = field(init=False)
    parentID: str
    parentOptionID: str
    label: str
    options: dict


class FlowMaster:
    __flowNodes: dict

    def __init__(self) -> None:
        try:
            with open('saveData.pickle', 'rb') as outfile:
                saveData = pickle.load(outfile)

            for key, value in saveData.items():
                setattr(self, key, value)

        except FileNotFoundError:
            self.__flowNodes = {}

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
            return f'An error occurred.\n{e}'

    def generateID(self) -> str:
        return str(uuid.uuid4())
    
    def addNode(self, node, nodeID) -> None:
        # Shorten the process of creating and adding nodes. Instead of having
        # to generate a UUID, create an instance of FlowNode then passing it
        # to addNode to be tracked and saved, make these processes internal to Flow.py

        # However, making FlowMaster.addNode take the properties of the new Node
        # then pass it to the Node class seems verbose and unnecessary. One option
        # is to make the UUID creation internal to FlowNode, so the creation of the 
        # node becomes a 2-step process.

        self.__flowNodes[nodeID] = node
        print(self.saveSession())

    def delNode(self, nodeID) -> None:
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
            dataclasses.replace(self.__flowNodes[nodeID], kwargs)

    def constructFlow(self) -> None:
        pass


