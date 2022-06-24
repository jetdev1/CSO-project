# variable condition algorithm?
# Create classes that are able to link to one another to form a whole flow chart.

# basically what we want to do here is to be able to create flowObjects that indicate its master object.
# Each flowObject, apart from other details specific to the program, should have its own objID so that
# each flowObject can be tracked and should make debugging easier. 

# The flowMaster object will be the handler of the array of flowObjects and is responsible for the
# creation of flowObjects, assigning the objID at the point of creation, keeping track of them
# and retrieving data from the flowObjects to display to the end user.

# Store the existing flow chart as an array, flowObjectsArr, populated with flowObjects. 
# The other option is to unpack the array of flowObjects into a plain text file and loading the 
# file to memory on startup. This way , we don't have to store the entire array of objects
# in memory and can be yielded on demand.


from FlowOption import flowOption


class flowObject:

    # make upper an optional argument, so that the master (first) flowObject can be created
    def __init__(self, objID):
        self.objProperties = objID.split(sep='9')
        self.parentID = self.objProperties[0]
        self.objID = self.objProperties[1]
        self.optionID = self.objProperties[2]
        self.optionArr = []
        
    def createOption(self, optionID, label):
        self.optionObj = flowOption(optionID, label)
        self.optionArr.append(self.optionArr)

    def changeOption(self, optionID, newLabel):
        pass

    def removeOption(self, optionID):
        pass
