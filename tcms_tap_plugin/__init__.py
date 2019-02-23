# Copyright (c) 2019 Alexander Todorov <atodorov@MrSenko.com>

# Licensed under the GPLv3: https://www.gnu.org/licenses/gpl.html

from tap.line import Result, Diagnostic
from tap.parser import Parser
from tcms_api.plugin_helpers import Backend


class Plugin:  # pylint: disable=too-few-public-methods
    def __init__(self):
        self.backend = Backend(prefix='[TAP] ')

    def parse(self, tap_file, progress_cb=None):
        self.backend.configure()

        before_first_test = True
        test_case_run_id = False
        status_id = False
        trace_back = []
        comment = ''
        for line in Parser().parse_file(tap_file):
            if isinstance(line, Result):
                # Before parse result line, we need to add
                # traceback as comment to the previous result
                if test_case_run_id and status_id and trace_back:
                    comment += '\n' + '\n'.join(trace_back)
                    self.backend.update_test_case_run(
                        test_case_run_id, status_id, comment)
                trace_back = []
                before_first_test = False
            elif isinstance(line, Diagnostic):
                if not before_first_test:
                    trace_back.append(line.text[2:])
            else:
                continue

            test_case = self.backend.test_case_get_or_create(line.description)
            test_case_id = test_case['case_id']

            self.backend.add_test_case_to_plan(test_case_id,
                                               self.backend.plan_id)
            test_case_run_id = self.backend.add_test_case_to_run(
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

            self.backend.update_test_case_run(
                test_case_run_id, status_id, comment)

            if progress_cb:
                progress_cb()


def main(argv):
    if len(argv) < 2:
        raise Exception("USAGE: %s results.tap" % argv[0])

    plugin = Plugin()
    plugin.parse(argv[1])
