Test Anything Protocol (TAP) plugin for Kiwi TCMS
=================================================

.. image:: https://img.shields.io/pypi/v/kiwitcms-tap-plugin.svg
    :target: https://pypi.org/project/kiwitcms-tap-plugin
    :alt: PyPI version

.. image:: https://travis-ci.org/kiwitcms/tap-plugin.svg?branch=master
    :target: https://travis-ci.org/kiwitcms/tap-plugin
    :alt: Travis CI

.. image:: https://coveralls.io/repos/github/kiwitcms/tap-plugin/badge.svg?branch=master
    :target: https://coveralls.io/github/kiwitcms/tap-plugin?branch=master
    :alt: Code coverage

.. image:: https://pyup.io/repos/github/kiwitcms/tap-plugin/shield.svg
    :target: https://pyup.io/repos/github/kiwitcms/tap-plugin/
    :alt: Python updates

.. image:: https://img.shields.io/badge/kiwi%20tcms-results-9ab451.svg
    :target: https://tcms.kiwitcms.org/plan/6/
    :alt: TP for kiwitcms/tap-plugin (master)

.. image:: https://tidelift.com/badges/package/pypi/kiwitcms-tap-plugin
    :target: https://tidelift.com/subscription/pkg/pypi-kiwitcms-tap-plugin?utm_source=pypi-kiwitcms-tap-plugin&utm_medium=github&utm_campaign=readme
    :alt: Tidelift

.. image:: https://opencollective.com/kiwitcms/tiers/sponsor/badge.svg?label=sponsors&color=brightgreen
   :target: https://opencollective.com/kiwitcms#contributors
   :alt: Become a sponsor

.. image:: https://img.shields.io/twitter/follow/KiwiTCMS.svg
    :target: https://twitter.com/KiwiTCMS
    :alt: Kiwi TCMS on Twitter

This package allows you to read Test Anything Protocol (TAP) files and
send the results to `Kiwi TCMS <http://kiwitcms.org>`_.


Installation
------------

::

    pip install kiwitcms-tap-plugin


Note: this plugin should be installed on the system executing your automated tests
or a separate system whose task is to parse the results and import them into Kiwi TCMS.
This is usually not your Kiwi TCMS container!


Configuration and environment
-----------------------------

Minimal config file `~/.tcms.conf`::

    [tcms]
    url = https://tcms.server/xml-rpc/
    username = your-username
    password = your-password


For more info see `tcms-api docs <https://tcms-api.readthedocs.io>`_.

This plugin is only concerned with parsing the TAP format and executing
``tcms-api`` functions which will create/reuse test cases, test plans and test runs.
``tcms-api`` behavior is controlled via environment variables.

For example inside
`.github/workflows/testing.yml <https://github.com/kiwitcms/tap-plugin/blob/master/.github/workflows/testing.yml>`_
this looks like::

    export TCMS_PRODUCT=$GITHUB_REPOSITORY
    export TCMS_PRODUCT_VERSION=$(echo $GITHUB_REF | sed "s|refs/heads/||" | sed "s|refs/||" | sed "s|/merge||")
    export TCMS_BUILD=$(echo $GITHUB_SHA | cut -c1-7)


Further documentation and behavior specification can be found
`here <https://tcms-api.readthedocs.io/en/latest/modules/tcms_api.plugin_helpers.html>`_.

The above configuration creates a separate TestPlan for each branch, for example
`TP-6: [TAP] Plan for kiwitcms/tap-plugin (master) <https://tcms.kiwitcms.org/plan/6/>`_,
a separate TestPlan for each pull request (recording possible multiple test runs) and
separate TestPlan and TestRun for each tag on GitHub! ``tcms-api`` has default behavior
for Travis CI and Jenkins and allows endless configuration via environment variables.


Usage
-----

::

    # define environment variables
    tcms-tap-plugin /path/to/results.tap


Changelog
---------

v12.7 (11 Dec 2023)
~~~~~~~~~~~~~~~~~~~

- Update tcms-api from 11.3 to 12.7
- Update README to avoid confusions where to install this package. Closes
  `Issue #62 <https://github.com/kiwitcms/tap-plugin/issues/62>`_
- Build and test with Python 3.11
- Reformat source code with Black
- Enable CodeQL for code scanning
- Small refactoring internally


v11.3 (17 May 2022)
~~~~~~~~~~~~~~~~~~~

- Update tcms-api from 11.2 to 11.3
- Print information about created recrods if ``-v`` or ``--verbose``
  is specified on the command line
- Allow multiple TAP files to be specified on the command line. Fixes
  `Issue #57 <https://github.com/kiwitcms/tap-plugin/issues/57>`_


v11.2 (15 May 2022)
~~~~~~~~~~~~~~~~~~~

- Update tap.py from 3.0 to 3.1
- Update tcms-api from 11.0 to 11.2. Closes
  `Issue #5 <https://github.com/kiwitcms/tap-plugin/issues/5>`_ and
  `Issue #13 <https://github.com/kiwitcms/tap-plugin/issues/13>`_
- Fix bug with traceback not being posted as comment.
  `Issue #48 <https://github.com/kiwitcms/tap-plugin/issues/48>`_


v11.0 (05 Dec 2021)
~~~~~~~~~~~~~~~~~~~

- Future compatible with upcoming Kiwi TCMS v11.0
- Update tcms-api from 10.0 to 11.0
- Pylint fixes


v10.0 (02 Mar 2021)
~~~~~~~~~~~~~~~~~~~

- Compatible with Kiwi TCMS v10.0
- Update tcms-api to 10.0


v9.0 (13 Jan 2021)
~~~~~~~~~~~~~~~~~~

- Compatible with Kiwi TCMS v9.0
- Update tcms-api to 9.0
- Resolve a dependency issue in tests


v8.4 (28 Oct 2020)
~~~~~~~~~~~~~~~~~~

- Update tcms-api to 8.6.0


v8.3 (10 Apr 2020)
~~~~~~~~~~~~~~~~~~

- Update to
  `tcms-api v8.3.0 <https://github.com/kiwitcms/tcms-api/#v830-10-april-2020>`_
  which uses ``gssapi`` for Kerberos
- Requires MIT Kerberos for Windows if installed on Windows


v8.2 (03 Apr 2020)
~~~~~~~~~~~~~~~~~~

This version works only with Kiwi TCMS v8.2 or later!

- Update to tcms-api==8.2.0
- Patch for changed return value in
  ``plugin_helpers.Backend.test_case_get_or_create()``
- Call ``plugin_helpers.backend.finish_test_run()`` when done. Fixes
  `Issue #9 <https://github.com/kiwitcms/tap-plugin/issues/9>`_


v8.0.1 (10 February 2020)
~~~~~~~~~~~~~~~~~~~~~~~~~

This version works only with Kiwi TCMS v8.0 or later!

- Update to tcms-api==8.0.1


v8.0 (09 February 2020)
~~~~~~~~~~~~~~~~~~~~~~~

This version works only with Kiwi TCMS v8.0 or later!

- Adjust plugin due to API changes in Kiwi TCMS v8.0
- Update ``tap.py`` from 2.6.2 to 3.0
- Require ``tcms-api>=8.0``


v0.5 (07 January 2020)
~~~~~~~~~~~~~~~~~~~~~~

- Update ``tap.py`` dependency from 2.6.1 to 2.6.2


v0.4 (23 September 2019)
~~~~~~~~~~~~~~~~~~~~~~~~

- Include traceback from TAP file as TE comment. Fixes
  `Issue #7 <https://github.com/kiwitcms/tap-plugin/issues/7>`_
  (Christophe CHAUVET)


v0.3 (10 April 2019)
~~~~~~~~~~~~~~~~~~~~

- Works with Kiwi TCMS v6.7 or newer
- Uses new names of API methods
