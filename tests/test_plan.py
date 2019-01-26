from unittest.mock import MagicMock

from . import PluginTestCase


class GivenRunExistsInDatabase(PluginTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.plugin._rpc = MagicMock()
        cls.plugin._rpc.TestRun.filter = MagicMock(
            return_value=[{'plan_id': 4}])
        cls.plugin._rpc.TestPlan.filter = MagicMock()
        cls.plugin._rpc.TestPlan.create = MagicMock()

    def test_when_get_plan_id_then_will_reuse_TestPlan(self):
        plan_id = self.plugin.get_plan_id(0)
        self.assertEqual(plan_id, 4)
        self.plugin._rpc.TestPlan.filter.assert_not_called()
        self.plugin._rpc.TestPlan.create.assert_not_called()


class GivenRunDoesntExistInDatabase(PluginTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.plugin._rpc = MagicMock()
        cls.plugin._rpc.TestRun.filter = MagicMock(return_value=[])
        cls.plugin.get_product_id = MagicMock(return_value=(4, 'p.Four'))
        cls.plugin.get_version_id = MagicMock(return_value=(44, 'v.Test'))
        cls.plugin.get_plan_type_id = MagicMock(return_value=10)

    def test_when_get_plan_id_with_existing_TestPlan_then_will_reuse_it(self):
        self.plugin._rpc.TestPlan.filter = MagicMock(
            return_value=[{'plan_id': 400}])
        self.plugin._rpc.TestPlan.create = MagicMock()

        plan_id = self.plugin.get_plan_id(0)
        self.assertEqual(plan_id, 400)
        self.plugin._rpc.TestPlan.create.assert_not_called()

    def test_when_get_plan_id_with_non_existing_TP_then_will_create_it(self):
        self.plugin._rpc.TestPlan.filter = MagicMock(return_value=[])
        self.plugin._rpc.TestPlan.create = MagicMock(
            return_value={'plan_id': 500})

        plan_id = self.plugin.get_plan_id(0)
        self.assertEqual(plan_id, 500)
        self.plugin._rpc.TestPlan.create.assert_called_with({
            'name': '[TAP] Plan for p.Four',
            'text': 'Created by Kiwi TCMS tap-plugin',
            'product': 4,
            'product_version': 44,
            'is_active': True,
            'type': 10,
        })


class GivenEmptyTestPlan(PluginTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.plugin._rpc = MagicMock()
        cls.plugin._rpc.TestCase.filter = MagicMock(return_value=[])
        cls.plugin._rpc.TestPlan.add_case = MagicMock()

    def test_when_add_test_case_to_plan_then_TestCase_is_added(self):
        self.plugin.add_test_case_to_plan(11, 22)
        self.plugin._rpc.TestPlan.add_case.assert_called_with(22, 11)


class GivenTestPlanWithTestCases(PluginTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.plugin._rpc = MagicMock()
        cls.plugin._rpc.TestCase.filter = MagicMock(return_value=[{}])
        cls.plugin._rpc.TestPlan.add_case = MagicMock()

    def test_when_add_test_case_to_plan_then_TestCase_is_not_added(self):
        self.plugin.add_test_case_to_plan(11, 22)
        self.plugin._rpc.TestPlan.add_case.assert_not_called()
