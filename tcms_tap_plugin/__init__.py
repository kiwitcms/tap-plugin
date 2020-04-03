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

        test_execution_id = None
        trace_back = []
        for line in Parser().parse_file(tap_file):
            if isinstance(line, Result):
                # before parsing the 'next' result line add
                # traceback as comment to the previous TE
                if test_execution_id and trace_back:
                    self.backend.add_comment(test_execution_id,
                                             "\n" + "\n".join(trace_back))
                trace_back = []
            elif isinstance(line, Diagnostic):
                trace_back.append(line.text[2:])
                continue
            else:
                continue

            test_case, _ = self.backend.test_case_get_or_create(
                line.description)
            test_case_id = test_case['id']

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

        self.backend.finish_test_run()


def main(argv):
    if len(argv) < 2:
        raise Exception("USAGE: %s results.tap" % argv[0])

    plugin = Plugin()
    plugin.parse(argv[1])
