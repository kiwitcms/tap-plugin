# pylint: disable=no-self-use

import unittest
from unittest.mock import patch
from tcms_tap_plugin import main


class MainFuncTestCase(unittest.TestCase):
    def test_when_calling_main_with_arguments_then_parse(self):
        with patch('tcms_tap_plugin.Plugin.parse') as parse:
            main([__file__, 'output.tap'])
            parse.assert_called_with('output.tap')

    def test_when_calling_main_without_arguments_then_usage(self):
        with self.assertRaisesRegex(Exception,
                                    'USAGE: %s results.tap' % __file__):
            main([__file__])

    @unittest.expectedFailure
    def test_produce_traceback_output(self):
        """Add traceback on TAP ouput"""
        main([__file__])

    def test_parse_file_with_traceback(self):
        """Parse file with traceback"""
        with patch('tcms_tap_plugin.Plugin.parse') as parse:
            main([__file__, 'traceback.taptest'])
            parse.assert_called_with('traceback.taptest')
