from unittest.mock import MagicMock

from . import PluginTestCase


class GivenStatusCache(PluginTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.plugin._statuses = {'PASSED': 1}
        cls.plugin._rpc = MagicMock()
        cls.plugin._rpc.TestCaseRunStatus.filter = MagicMock()

    def test_when_status_in_cache_then_return_from_cache(self):
        self.plugin.get_status_id('PASSED')
        self.plugin._rpc.TestCaseRunStatus.filter.assert_not_called()

    def test_when_status_not_in_cache_then_return_from_cache(self):
        self.plugin.get_status_id('FAILED')
        self.plugin._rpc.TestCaseRunStatus.filter.assert_called_with({
            'name': 'FAILED',
        })
