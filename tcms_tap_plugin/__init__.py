# Copyright (c) 2019 Alexander Todorov <atodorov@MrSenko.com>

# Licensed under the GPLv3: https://www.gnu.org/licenses/gpl.html

import os

import tcms_api
from tap.line import Result
from tap.parser import Parser


class Plugin:
    _statuses = {}
    _cases_in_test_run = {}

    def __init__(self):
        self._rpc = tcms_api.TCMS().exec
        self.run_id = None
        self.plan_id = None
        self.product_id = None
        self.category_id = None
        self.priority_id = None
        self.confirmed_id = None

    def configure(self):
        self.run_id = self.get_run_id()
        self.plan_id = self.get_plan_id(self.run_id)
        self.product_id, _ = self.get_product_id(self.plan_id)

        self.category_id = self._rpc.Category.filter({
            'product': self.product_id
        })[0]['id']
        self.priority_id = self._rpc.Priority.filter({})[0]['id']
        self.confirmed_id = self._rpc.TestCaseStatus.filter({
            'name': 'CONFIRMED'
        })[0]['id']

    def get_status_id(self, name):
        if name not in self._statuses:
            self._statuses[name] = self._rpc.TestCaseRunStatus.filter({
                'name': name
            })[0]['id']

        return self._statuses[name]

    def get_product_id(self, plan_id):
        product_id = None
        product_name = None

        test_plan = self._rpc.TestPlan.filter({'pk': plan_id})
        if test_plan:
            product_id = test_plan[0]['product_id']
            product_name = test_plan[0]['product']
        else:
            product_name = os.environ.get('TCMS_PRODUCT',
                                          os.environ.get('TRAVIS_REPO_SLUG',
                                                         os.environ.get(
                                                             'JOB_NAME')))
            if not product_name:
                raise Exception('Product name not defined, '
                                'missing one of TCMS_PRODUCT, '
                                'TRAVIS_REPO_SLUG or JOB_NAME')

            product = self._rpc.Product.filter({'name': product_name})
            if not product:
                class_id = self._rpc.Classification.filter({})[0]['id']
                product = [self._rpc.Product.create({
                    'name': product_name,
                    'classification_id': class_id
                })]
            product_id = product[0]['id']

        return product_id, product_name

    def get_version_id(self, product_id):
        version_val = os.environ.get(
            'TCMS_PRODUCT_VERSION',
            os.environ.get('TRAVIS_COMMIT',
                           os.environ.get('TRAVIS_PULL_REQUEST_SHA',
                                          os.environ.get('GIT_COMMIT'))))
        if not version_val:
            raise Exception('Version value not defined, '
                            'missing one of TCMS_PRODUCT_VERSION, '
                            'TRAVIS_COMMIT, TRAVIS_PULL_REQUEST_SHA '
                            'or GIT_COMMIT')

        version = self._rpc.Version.filter({'product': product_id,
                                            'value': version_val})
        if not version:
            version = [self._rpc.Version.create({'product': product_id,
                                                 'value': version_val})]

        return version[0]['id'], version_val

    def get_build_id(self, product_id, _version_id):
        # for _version_id see https://github.com/kiwitcms/Kiwi/issues/246
        build_number = os.environ.get('TCMS_BUILD',
                                      os.environ.get('TRAVIS_BUILD_NUMBER',
                                                     os.environ.get(
                                                         'BUILD_NUMBER')))
        if not build_number:
            raise Exception('Build number not defined, '
                            'missing one of TCMS_BUILD, '
                            'TRAVIS_BUILD_NUMBER or BUILD_NUMBER')

        build = self._rpc.Build.filter({'name': build_number,
                                        'product': product_id})
        if not build:
            build = [self._rpc.Build.create({'name': build_number,
                                             'product': product_id})]

        return build[0]['build_id'], build_number

    def get_plan_type_id(self):
        plan_type = self._rpc.PlanType.filter({'name': 'Integration'})
        if not plan_type:
            plan_type = [self._rpc.PlanType.create({'name': 'Integration'})]

        return plan_type[0]['id']

    def get_plan_id(self, run_id):
        result = self._rpc.TestRun.filter({'pk': run_id})
        if not result:
            product_id, product_name = self.get_product_id(0)
            version_id, version_name = self.get_version_id(product_id)

            name = '[TAP] Plan for %s (%s)' % (product_name, version_name)

            result = self._rpc.TestPlan.filter({'name': name,
                                                'product': product_id,
                                                'product_version': version_id})

            if not result:
                plan_type_id = self.get_plan_type_id()

                result = [self._rpc.TestPlan.create({
                    'name': name,
                    'text': 'Created by Kiwi TCMS tap-plugin',
                    'product': product_id,
                    'product_version': version_id,
                    'is_active': True,
                    'type': plan_type_id,
                })]

        return result[0]['plan_id']

    def get_run_id(self):
        run_id = os.environ.get('TCMS_RUN_ID')

        if not run_id:
            product_id, product_name = self.get_product_id(0)
            version_id, version_val = self.get_version_id(product_id)
            build_id, build_number = self.get_build_id(product_id, version_id)
            plan_id = self.get_plan_id(0)
            # the user issuing the request
            user_id = self._rpc.User.filter()[0]['id']

            testrun = self._rpc.TestRun.create({
                'summary': '[TAP] Results for %s, %s, %s' % (
                    product_name, version_val, build_number
                ),
                'manager': user_id,
                'plan': plan_id,
                'build': build_id,
            })
            run_id = testrun['run_id']

        # fetch pre-existing test cases in this TestRun
        # used to avoid adding existing TC to TR later
        for case in self._rpc.TestRun.get_cases(run_id):
            self._cases_in_test_run[case['case_id']] = case['case_run_id']

        return int(run_id)

    def test_case_get_or_create(self, summary):
        test_case = self._rpc.TestCase.filter({
            'summary': summary,
            'category__product': self.product_id,
        })

        if not test_case:
            test_case = [self._rpc.TestCase.create({
                'summary': summary,
                'category': self.category_id,
                'product': self.product_id,
                'priority': self.priority_id,
                'case_status': self.confirmed_id,
                'notes': 'Created by Kiwi TCMS tap-plugin',
            })]

        return test_case[0]

    def add_test_case_to_plan(self, case_id, plan_id):
        if not self._rpc.TestCase.filter({'pk': case_id, 'plan': plan_id}):
            self._rpc.TestPlan.add_case(plan_id, case_id)

    def add_test_case_to_run(self, case_id, run_id):
        if case_id in self._cases_in_test_run.keys():
            return self._cases_in_test_run[case_id]

        return self._rpc.TestRun.add_case(run_id, case_id)['case_run_id']

    def parse(self, tap_file, progress_cb=None):
        self.configure()

        for line in Parser().parse_file(tap_file):
            if not isinstance(line, Result):
                continue

            test_case_id = self.test_case_get_or_create(
                line.description)['case_id']
            self.add_test_case_to_plan(test_case_id, self.plan_id)
            test_case_run_id = self.add_test_case_to_run(test_case_id,
                                                         self.run_id)
            comment = 'Result recorded via Kiwi TCMS tap-plugin'

            if line.ok:
                status_id = self.get_status_id('PASSED')
            else:
                status_id = self.get_status_id('FAILED')

            if line.skip:
                status_id = self.get_status_id('WAIVED')
                comment = line.directive.text

            if line.todo:
                status_id = self.get_status_id('PAUSED')
                comment = line.directive.text

            self._rpc.TestCaseRun.update(test_case_run_id,
                                         {'status': status_id})

            self._rpc.TestCaseRun.add_comment(test_case_run_id, comment)

            if progress_cb:
                progress_cb()


def main(argv):
    if len(argv) < 2:
        raise Exception("USAGE: %s results.tap" % argv[0])

    plugin = Plugin()
    plugin.parse(argv[1])
