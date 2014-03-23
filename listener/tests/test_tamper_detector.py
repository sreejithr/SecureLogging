import os
import unittest

from ..tamper_detector import TamperDetector
from ..settings import SNAPSHOT_PREFIX


class TestTamperDetector(unittest.TestCase):
    def setUp(self):
        self._path_prefix = os.path.join(SNAPSHOT_PREFIX, 'TEST')
        self._list_of_files = [os.path.join(self._path_prefix, 'daily.out_added'),
                               os.path.join(self._path_prefix,
                                            'daily.out_tampered')]

    def test_is_valid(self):
        self.td = TamperDetector()
        for path in self._list_of_files:
            print self.td.tamper_detect(path, os.path.join(self._path_prefix,
                                                           'SNAPSHOT/daily.out'))

