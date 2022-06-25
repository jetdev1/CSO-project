# CSO-project
Project to recreate the flowchart of the KKFSC organisation

# Developer notes
## Flow.py
Flow.py houses the data container classes for nodes in the flowchart. Each FlowOption contains its own ID and label, while each node, FlowObject, contains its own ID, the ID of its parent, the ID of its parent option and an array of the IDs of the options it contains.

The FlowMaster is used for the handling of FlowOption and FlowObject objects. This file does not have any external dependencies and runs entirely on the built in python library.

## Known Issues/Potential Issues
### FlowMaster.saveData: saves all variables of instance
FlowMaster.saveData is currently configured to save all the properties of a given instance of FlowMaster, which can result in unintended variables being restored in the next session and causing unforseen glitches. 

### Trash Files: Old files no longer in use
- flowMaster.py
- flowObject.py
- flowOption.py
- test.py