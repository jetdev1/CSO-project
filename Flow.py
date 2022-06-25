# Handles ID assignment, ID creation, loading objects and saving objects
from dataclasses import dataclass, field
import pickle


@dataclass(frozen=True)
class FlowOption:
    optionID: int
    label: str


@dataclass(frozen=True, order=True)
class FlowObject:
    objID: int
    parentID: int
    parentOptionID: int
    options: list[FlowOption]


@dataclass(frozen=True)
class FlowMaster:
    flowObjects: list[dict]
    flowOptions: list[dict]

    def __init__(self) -> None:
        try:
            with open('saveData.pickle', 'rb') as outfile:
                saveData = pickle.load(outfile)

            for key, value in saveData.items():
                setattr(self, key, value)

        except FileNotFoundError:
            flowObjects = []
            flowOptions = []

    def saveSession(self) -> str:
        # Retrive names and values of all properties
        saveDataKeys = [e for e in dir(self) if e[0:2] != '__']
        saveDataValues = [getattr(self, e) for e in saveDataKeys]
        saveData = {}

        for key, value in zip(saveDataKeys, saveDataValues):
            saveData[key] = value

        with open('saveData.pickle', 'ab') as file:
            pickle.dump(saveData, file)

    def createFlowObj(self) -> None:
        pass

    def createFlow(self) -> None:
        pass

    def generateObjID(self):
        # objID format: [parent_ID].[objID].[optionID it is linked to in
        # parent object]
        # use parent ID 00 if no parent object is present
        pass

    def generateOptionID(self):
        pass

