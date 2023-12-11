# pylint: disable=no-self-use

import unittest
from unittest.mock import patch
from tcms_tap_plugin import main


class MainFuncTestCase(unittest.TestCase):
    def test_when_calling_main_with_arguments_then_parse(self):
        with patch("tcms_tap_plugin.Plugin.parse") as parse:
            main([__file__, "output.tap"])
            parse.assert_called_with(["output.tap"])

    def test_when_calling_main_without_arguments_then_usage(self):
        with self.assertRaisesRegex(SystemExit, "2"):
            main([__file__])

    @unittest.expectedFailure
    def test_expected_traceback_for_te_comment(self):
        raise RuntimeError("This is expected")
