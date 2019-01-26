import unittest


class Given_TCMS_PRODUCT_VERSION_IsPresent(unittest.TestCase):
    def test_when_adding_version_then_will_use_it(self):
        self.fail('not implemented')


class Given_TRAVIS_COMMIT_IsPresent(unittest.TestCase):
    def test_when_adding_version_then_will_use_it(self):
        self.fail('not implemented')


class Given_TRAVIS_PULL_REQUEST_SHA_IsPresent(unittest.TestCase):
    def test_when_adding_version_then_will_use_it(self):
        self.fail('not implemented')


class Given_GIT_COMMIT_IsPresent(unittest.TestCase):
    def test_when_adding_version_then_will_use_it(self):
        self.fail('not implemented')


class GivenVersionEnvironmentIsNotPresent(unittest.TestCase):
    def test_when_adding_version_then_will_raise(self):
        self.fail('not implemented')


class GivenVersionExistsInDatabase(unittest.TestCase):
    def test_when_adding_version_then_will_reuse_it(self):
        self.fail('not implemented')


class GivenVersionDoesntExistInDatabase(unittest.TestCase):
    def test_when_adding_version_then_will_add_it(self):
        self.fail('not implemented')
