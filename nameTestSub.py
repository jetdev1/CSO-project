# Finding out what __name__ is when called from another module
import logging


logger = logging.getLogger(__name__)


class Test:
    def __init__(self) -> None:
        self.name = __name__

    def getName(self) -> str:
        return self.name

    def testLog(self):
        pass