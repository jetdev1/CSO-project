# Figuring out nonw __name__ works
import nameTestSub

TESTCASE = 'a'

if TESTCASE == 'a':
    print(__name__)
    testobj = nameTestSub.Test()
    print(testobj.getName())


'''
Seems that the __name__ always reflects the name of the module __name__ is in.
__main__ reflects that the method is being called from the module itself, while anything
else suggests that the method was called from another module. This, however, does not 
reflect which module the method was called from
'''