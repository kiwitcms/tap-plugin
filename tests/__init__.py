import unittest
from tap_plugin import Plugin


class PluginTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plugin = Plugin()
