# ISSUES

# FlowMaster.saveSession() may save unwanted variables and reinstate
# its value in the next session and cause glitches. Resolve by limtting
# the variables that are saved.


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
    label: str
    options: list[FlowOption]


# @dataclass(frozen=True)
class FlowMaster:
    flowObjects: dict
    flowOptions: dict

    def __init__(self) -> None:
        try:
            with open('saveData.pickle', 'rb') as outfile:
                saveData = pickle.load(outfile)

            for key, value in saveData.items():
                setattr(self, key, value)

        except FileNotFoundError:
            flowObjects = {}
            flowOptions = {}

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

