# -*- coding: utf-8 -*-
"""
the controller component
"""

import re
import os
from typing import Sequence, Set

from anytree import NodeMixin, RenderTree, ContStyle, Node
from pubsub import pub

from LogViewer.source.config import APP_LONG_NAME, UNDEFINED
from LogViewer.source.gui import MainFrame
from LogViewer.source.log_definition import logdefinitions


class Controller:

    def __init__(self):
        self.view = MainFrame(None, -1, APP_LONG_NAME, size=(1250, 690))  # the GUI
        self.logs = self.detect_logs()
        self.view.treectrl.update_tree(treedata=self.logs)
        self._active_log = None
        pub.subscribe(self.set_active_log, 'tree.selected')

    def detect_logs(self):
        """
        Looks into the path provided and gets all files, then tries to parse them.
        Populates a tree based on the types of logs found

        :return:
        :rtype:
        """
        logs = Node(name='Logs')  # the tree holding the available logs
        # trying all log descriptors found in log_definition.py
        for logdef in logdefinitions:
            ld = LogDescriptor(parent=logs, **logdef)
            for filename in os.listdir(ld.directory_path):
                fullpath = os.path.join(ld.directory_path, filename)
                try:
                    if ld.isValidFile(logfile=fullpath, separator=ld.separator):
                        _log = Log(logfile=fullpath, parent=ld)
                except (UnicodeDecodeError, PermissionError):
                    pass

        return logs

    def set_active_log(self, log):
        if isinstance(log, Log):
            self._active_log = log
            self.view.loglist.set_log(self._active_log)
            self.view.loglist.fill_list()

            pub.sendMessage('list.levels', levels=self._active_log.get_levels())
            pub.sendMessage('list.emitters', emitters=self._active_log.get_emitters())
            pub.sendMessage('list.filled')
        else:
            pub.sendMessage('clear.all')

    def print_logtree(self):
        print(RenderTree(self.logs, style=ContStyle()))


class LogDescriptor(NodeMixin):

    def __init__(self,
                 parent=None,
                 entry_structure: Sequence[str] = (),
                 separator: str = None,
                 name: str = None,
                 directory_path: str = None):
        """
        Holds basic information required to handle logs: structure, field separator, name etc
        """
        self.parent = parent
        self.entry_structure = entry_structure
        self.separator = separator
        self.name = name
        self.directory_path = directory_path

    @staticmethod
    def isValidFile(logfile: str = None, separator: str = None):
        """Tells if the file provided is a valid file for self.descriptor"""

        log = Log(logfile=logfile)
        first_line = log.read_logfile(logfile)[0]

        # trying, using the provided separator
        try:
            entry = log.parse_entry(entry=first_line, separator=separator)
        except ValueError:
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

    def parse_entry(self, entry: str = None, separator: str = None) -> Sequence[str]:
        """Disassembles a log entry either using the provided separator or using the own"""

        if separator not in entry:
            raise ValueError('No separator "{}" found in entry "{}"'.format(separator, entry))

        # if the last field - the message - is empty so the row to be parsed ends with a separator
        # if the separator is fully there
        fixed_flag = False
        if entry.endswith(separator):
            entry += UNDEFINED
            fixed_flag = True

        # if the separator is partially there we add a whitespace. Note: this does not heal the entry in all cases
        if entry.endswith(separator.strip()) and not fixed_flag:
            entry += ' '
            entry += UNDEFINED

        # splitting
        _ret = tuple(entry.split(separator))

        # checking for the result - the split tuple should the number of elements +1 as the number of separators
        expected_length = len([m.start() for m in re.finditer(separator, entry)]) + 1

        if len(_ret) < expected_length:
            print('is: {}, should be: {}'.format(len(_ret), expected_length))
            while len(_ret) < expected_length:
                _ret += (UNDEFINED, )

        elif len(_ret) > expected_length:
            print('is: {}, should be: {}'.format(len(_ret), expected_length))
            _ret = tuple(_ret[0:expected_length])

        else:
            pass

        return _ret

    def get_field_values(self, fieldname: str = None, lines: Sequence[str] = None) -> Set[str]:
        """
        Returns a set with the unique names found in the given field. If lines is provided, only those will be
        taken into account
        """
        # finding the level. If nothing found, an empty set is returned
        structure = [x.lower() for x in self.descriptor.entry_structure]
        try:
            level_position = structure.index(fieldname)
        except IndexError:  # there is a field called fieldname in the logs but currently none is found
            return set()
        except ValueError:  # no field called fieldname
            return set()

        if lines is None:
            lines = self.read_logfile(logfile=self.logfile)

        # getting all lines, parsed
        parsed = [self.parse_entry(x, separator=self.separator) for x in lines]

        # retreiving all unique values
        _ret = {x[level_position] for x in parsed}
        return _ret

    def get_levels(self) -> Set[str]:
        """
        Returns a set with the level names in it, as found in the logfile provided.
        """
        return self.get_field_values(fieldname='level')

    def get_emitters(self) -> Set[str]:
        """
        Returns a set with the emitter names in it, as found in the logfile provided.
        """
        return self.get_field_values(fieldname='emitter')
