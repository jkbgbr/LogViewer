import logging
import os
import random
import unittest

from LogViewer.source.controller import LogDescriptor, Log

LEVELS = {'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}
NUM_TEST_ENTRIES = 50


class TestLogHandling(unittest.TestCase):

    # def cleanup(self) -> None:
    #     try:
    #         os.remove('testlog.log')
    #     except:
    #         with open('testlog.log', 'w') as f:
    #             f.write('')

    def setUp(self) -> None:

        self.logger = logging.getLogger('test_logger')

        # logging to stream, file
        self.logger.setLevel(logging.DEBUG)

        filehandler = logging.FileHandler(filename='testlog.log')
        file_formatter = logging.Formatter(fmt='%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s',
                                           datefmt='%d-%m-%Y. %H:%M:%S')
        filehandler.setFormatter(file_formatter)
        filehandler.setLevel(logging.DEBUG)
        self.logger.addHandler(filehandler)

        pnp = {'entry_structure': ('Timestamp', 'emitter', 'Level', 'message'),
               'separator': ' -- ',
               'section_start': 'Program start',
               'name': 'Test',
               'logdir_path': 'E:\modules\LogViewer\LogViewer\tests'}

        self.ld = LogDescriptor(parent=None, **pnp)
        self.log = Log(parent=self.ld, logfile='testlog.log')
        for i in range(NUM_TEST_ENTRIES):
            lvl = random.choice((self.logger.debug, self.logger.info, self.logger.warning, self.logger.error, self.logger.critical))
            lvl('mivan')

    def tearDown(self) -> None:
        try:
            os.remove('testlog.log')
        except:
            with open('testlog.log', 'w') as f:
                f.write('')

    def test_is_valid(self):
        """tests the validity of the log file"""
        self.assertTrue(self.ld.isValidFile(logfile=self.log.logfile, separator=self.ld.separator,
                                            expected_length=self.ld.expected_length,
                                            level_position=self.ld.level_position,
                                            file_extension=self.ld.file_extension))

    def test_list_levels(self):
        """tests if levels are found"""
        self.assertSetEqual(LEVELS, set(self.log.get_levels()))

    def test_emitters(self):
        """tests if emitters are found"""
        self.assertSetEqual({'test_logger'}, set(self.log.get_emitters()))

    def test_log_summary(self):
        """tests if the summary is OK"""
        logsum = self.log.get_log_summary()['messages_per_level']
        self.assertSetEqual(set(logsum.keys()), LEVELS)


if __name__ == '__main__':
    unittest.main()
