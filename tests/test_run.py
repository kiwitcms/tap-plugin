import unittest


class Given_TCMS_RUN_ID_IsPresent(unittest.TestCase):
    def test_when_plugin_initializes_then_will_reuse_TestRun(self):
        self.fail('not implemented')


class Given_TCMS_RUN_ID_IsNotPresent(unittest.TestCase):
    def test_when_plugin_initializes_then_will_create_TestRun(self):
        self.fail('not implemented')


class TestCaseRunMixin:
    def test_when_parsing_results_are_updated(self):
        self.fail('not implemented')


class GivenEmptyTestRun(unittest.TestCase, TestCaseRunMixin):
    def test_when_parsing_then_TestCase_is_added(self):
        self.fail('not implemented')


class GivenTestRunWithTestCases(unittest.TestCase, TestCaseRunMixin):
    def test_when_parsing_then_existing_TestCase_is_not_added(self):
        self.fail('not implemented')
