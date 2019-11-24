import os
from typing import Sequence, Set

from anytree import NodeMixin, RenderTree, ContStyle, Node
from pubsub import pub

from LogViewer.source.config import APP_LONG_NAME
from LogViewer.source.gui import MainFrame

example_PNP = 'C:\\Users\\Jakab Gábor\\AppData\\Roaming\\LogViewer\\Logs\\PNP_trace.log'
example_VW = 'C:\\Users\\Jakab Gábor\\AppData\\Roaming\\LogViewer\\Logs\\VW_trace.log'

LOGPATH = 'C:\\Users\\Jakab Gábor\\AppData\\Roaming\\LogViewer\\Logs'


# logger = logging.getLogger('controller')


class Controller:

    def __init__(self):
        self.view = MainFrame(None, -1, APP_LONG_NAME, size=(1250, 690))  # the GUI
        # logger.debug('Created the view component')
        self.logs = self.detect_logs()
        # logger.debug('Detected {} logs'.format(len(self.logs.descendants)))
        self.view.treectrl.update_tree(treedata=self.logs)
        # logger.debug('Updated the view')
        self._active_log = None
        pub.subscribe(self.set_active_log, 'tree.selected')

    def detect_logs(self, logdir: os.path.abspath = LOGPATH):
        """
        Looks into the path provided and gets all files, then tries to parse them.
        Populates a tree based on the types of logs found

        :param logdir:
        :type logdir:
        :return:
        :rtype:
        """
        logs = Node(name='Logs')  # the tree holding the available logs
        # trying all known log descriptors
        for ld_class in WV_descriptor, PNP_descriptor:
            ld = ld_class(parent=logs)
            for filename in os.listdir(logdir):
                if ld.isValidFile(logfile=filename):
                    _log = Log(logfile=os.path.join(LOGPATH, filename), parent=ld)

        return logs

    def set_active_log(self, data):
        if isinstance(data, Log):
            self._active_log = data
            self.view.loglist.fill_list(self._active_log)

    def print_logtree(self):
        print(RenderTree(self.logs, style=ContStyle()))


class LogDescriptor(NodeMixin):
    entry_structure = None
    separator = None
    name = None

    def __init__(self, parent=None):
        """
        Holds basic information required to handle logs: structure, field separator, name etc
        """
        self.parent = parent

    @classmethod
    def isValidFile(cls, logfile: str = None):
        """Tells if the file provided is a valid file for self.descriptor"""

        first_line = Log.read_logfile(logfile=os.path.join(LOGPATH, logfile))[0]

        # trying, using the provided separator
        try:
            entry = Log.parse_entry(entry=first_line, separator=cls.separator)
        except ValueError:
            return False
        if cls.name not in entry:
            return False

        return True


class Log(NodeMixin):
    """A base class holding handling the logs: the descriptor hold the log entry structure, the class enables
    reading, parsing the log. To be subclassed.
    """

    def __init__(self, parent: LogDescriptor = None, logfile: os.path.abspath = None):
        self.parent = parent
        self.logfile = logfile

    @property
    def separator(self):
        """to avoid collision with the separator attribute of NodeMixin"""
        return self.descriptor.separator

    @property
    def name(self):
        return os.path.basename(self.logfile)

    @property
    def descriptor(self):
        return self.parent

    @classmethod
    def read_logfile(cls, logfile: str = None) -> Sequence[str]:
        """reads a file. This should be a logfile with an entry in each line"""
        with open(logfile, 'r') as f:
            lines = f.readlines()
        lines = tuple([x.strip() for x in lines])
        return lines

    @classmethod
    def parse_entry(cls, entry: str = None, separator: str = None) -> Sequence[str]:
        """Disassembles a log entry either using the provided separator or using the own"""

        if separator not in entry:
            raise ValueError('No sparator "{}" found in entry "{}"'.format(separator, entry))
        return tuple(entry.split(separator))

    def get_levels(self) -> Set[str]:
        """
        Returns a set with the level names in it, as found in the logfile provided.
        """
        # getting all lines, parsed
        parsed = [self.parse_entry(x) for x in self.read_logfile()]

        # finding the level
        structure = [x.lower() for x in self.descriptor.entry_structure]
        level_position = structure.index('level')

        # retreiving all unique values
        _ret = {x[level_position] for x in parsed}
        return _ret


class WV_descriptor(LogDescriptor):
    entry_structure = ('Timestamp', 'Session', 'Level', 'emitter', 'module', 'line', 'method', 'message')
    separator = ' ++ '
    name = 'VW'


class PNP_descriptor(LogDescriptor):
    entry_structure = ('Timestamp', 'Session', 'Level', 'emitter', 'module', 'line', 'method', 'message')
    separator = ' -- '
    name = 'PNP'
