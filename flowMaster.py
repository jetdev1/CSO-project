# Handles ID assignment, ID creation, loading objects and saving objects

class flowMaster:
    def __init__(self) -> None:
        # Find startup file
        # Load file information into memory
        # optional: parse plaintext file data?
        # if using plaintext format: recreate all the objects
        # Create ui
        pass

    def createFlowObj(self):
        pass

    def createFlow(self):
        pass

    def generateObjID(self):
        # objID format: [parent_ID]9[objID]9[optionID]
        # Use '9' as split char. Ensure that all parent and child IDs do not contain '9'
        # Format each ID such that the IDs are of the same length, using leading zeros
        # Look up the existing list of objID and determine the next ID. Skip any number
        # containing '9'.
        # Give the first flowObject an id of 000090000900
        pass