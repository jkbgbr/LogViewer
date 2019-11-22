
from .gui import MainFrame
from .config import APP_LONG_NAME


class Controller:

    def __init__(self):
        self.view = MainFrame(None, -1, APP_LONG_NAME, size=(1250, 690))