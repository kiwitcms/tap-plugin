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

.. image:: https://opencollective.com/kiwitcms/tiers/sponsor/badge.svg?label=sponsors&color=brightgreen
   :target: https://opencollective.com/kiwitcms#contributors
   :alt: Become a sponsor

.. image:: https://img.shields.io/badge/kiwi%20tcms-results-9ab451.svg
    :target: https://tcms.kiwitcms.org/plan/6/
    :alt: TP for kiwitcms/tap-plugin (master)

This package allows you to read Test Anything Protocol (TAP) files and
send the results to `Kiwi TCMS <http://kiwitcms.org>`_.


Installation
------------

::

    pip install kiwitcms-tap-plugin


Configuration and environment
-----------------------------

Minimal config file `~/.tcms.conf`::

    [tcms]
    url = https://tcms.server/xml-rpc/
    username = your-username
    password = your-password


For more info see `tcms-api docs <https://tcms-api.readthedocs.io>`_.

This plugin is only concerned with parsing the TAP format and executing
`tcms-api` functions which will create/reuse test cases, test plans and test runs.
`tcms-api` behavior is controlled via environment variables.

For example this is how our own environment looks like::

    #!/bin/bash
    
    if [ "$TRAVIS_EVENT_TYPE" == "push" ]; then
        # same as $TRAVIS_TAG when building tags
        export TCMS_PRODUCT_VERSION=$TRAVIS_BRANCH
    fi
    
    if [ "$TRAVIS_EVENT_TYPE" == "pull_request" ]; then
        export TCMS_PRODUCT_VERSION="PR-$TRAVIS_PULL_REQUEST"
    fi
    
    export TCMS_BUILD="$TRAVIS_BUILD_NUMBER-$(echo $TRAVIS_COMMIT | cut -c1-7)"

Further documentation and behavior specification can be found
`here <https://tcms-api.readthedocs.io/en/latest/modules/tcms_api.plugin_helpers.html>`_.

The above configuration creates a separate TestPlan for each branch, see
`TP-6: [TAP] Plan for kiwitcms/tap-plugin (master) <https://tcms.kiwitcms.org/plan/6/>`_,
a separate TestPlan for each pull request (recording possible multiple test runs) and
separate TestPlan and TestRun for each tag on GitHub! `tcms-api` has default behavior
for Travis CI and Jenkins and allows endless configuration via environment variables.

Changelog
---------

v0.3 (10 April 2019)
~~~~~~~~~~~~~~~~~~~~

- Works with Kiwi TCMS v6.7 or newer
- Uses new names of API methods

Usage
-----

::

    # define environment variables
    tcms-tap-plugin /path/to/results.tap
