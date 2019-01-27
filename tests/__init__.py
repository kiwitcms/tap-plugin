import unittest
from tcms_tap_plugin import Plugin


class PluginTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plugin = Plugin()
