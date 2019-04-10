# Copyright (c) 2019 Alexander Todorov <atodorov@MrSenko.com>

# Licensed under the GPLv3: https://www.gnu.org/licenses/gpl.html

from tap.line import Result
from tap.parser import Parser
from tcms_api.plugin_helpers import Backend


class Plugin:  # pylint: disable=too-few-public-methods
    def __init__(self):
        self.backend = Backend(prefix='[TAP] ')

    def parse(self, tap_file, progress_cb=None):
        self.backend.configure()

        for line in Parser().parse_file(tap_file):
            if not isinstance(line, Result):
                continue

            test_case = self.backend.test_case_get_or_create(line.description)
            test_case_id = test_case['case_id']

            self.backend.add_test_case_to_plan(test_case_id,
                                               self.backend.plan_id)
            test_execution_id = self.backend.add_test_case_to_run(
                test_case_id,
                self.backend.run_id)
            comment = 'Result recorded via Kiwi TCMS tap-plugin'

            if line.ok:
                status_id = self.backend.get_status_id('PASSED')
            else:
                status_id = self.backend.get_status_id('FAILED')

            if line.skip:
                status_id = self.backend.get_status_id('WAIVED')
                comment = line.directive.text

            if line.todo:
                status_id = self.backend.get_status_id('PAUSED')
                comment = line.directive.text

            self.backend.update_test_execution(test_execution_id,
                                               status_id,
                                               comment)

            if progress_cb:
                progress_cb()


def main(argv):
    if len(argv) < 2:
        raise Exception("USAGE: %s results.tap" % argv[0])

    plugin = Plugin()
    plugin.parse(argv[1])
