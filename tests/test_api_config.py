import unittest


class GivenConfigurationFileExists(unittest.TestCase):
    def test_when_plugin_initializes_then_uses_config(self):
        self.fail('not implemented')


class GivenConfigurationFileDoesntExist(unittest.TestCase):
    def test_when_plugin_initializes_then_uses_environment(self):
        self.fail('not implemented')

    def test_when_TCMS_API_URL_is_not_configured_then_fails(self):
        self.fail('not implemented')

    def test_when_TCMS_USERNAME_is_not_configured_then_fails(self):
        self.fail('not implemented')

    def test_when_TCMS_PASSWORD_is_not_configured_then_fails(self):
        self.fail('not implemented')
