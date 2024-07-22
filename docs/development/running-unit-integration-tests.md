---
parent: Development
title: Running unit and integration tests
nav_order: 7
---

# Running ruleset unit and integration tests

Various components of Yoda have unit and integration tests. They run automatically using Github Actions.
This page explains how to run them locally.

## Running ruleset unit tests

The ruleset uses the [unittest framework](https://docs.python.org/2.7/library/unittest.html) for the unit tests.
The test suites can be found in the `unit-tests` subdirectory of the ruleset. Run them using Python 2.7. Example:

```bash
$ cd unit-tests
$ python2 -m unittest unit_tests
.............................................
----------------------------------------------------------------------
Ran 45 tests in 0.021s

OK
```

## Running ruleset integration tests

The ruleset has a custom rule for running the integration tests. These tests verify that various functions work in combination
with iRODS. You need to run the tests on either the [Docker setup](docker-setup.md) or on a development VM that has the test dataset. Please consult the
[API and UI tests manual page](running-api-ui-tests.md) for instructions on how to install test data on a development VM.

You can then run the integration tests from the `irods` account using the integration test script.

```
$ /etc/irods/yoda-ruleset/tools/run-integration-tests.sh
[... output omitted]
util.collection.exists.yes VERDICT_OK
util.collection.exists.no VERDICT_OK
util.collection.owner VERDICT_OK
util.collection.to_from_id VERDICT_OK
util.data_object.exists.yes VERDICT_OK
util.data_object.exists.no VERDICT_OK
util.data_object.owner VERDICT_OK
util.data_object.size VERDICT_OK
[... output omitted]
```

In order to run only a single test, add the test name as a parameter, like this:

```
$ /etc/irods/yoda-ruleset/tools/run-integration-tests.sh util.collection.owner
util.collection.owner VERDICT_OK

```

In order to run all integration tests with a particular prefix, add a * after the prefix. For example:

```
$ /etc/irods/yoda-ruleset/tools/run-integration-tests.sh util.collection.*
util.collection.exists.yes VERDICT_OK
util.collection.exists.no VERDICT_OK
util.collection.owner VERDICT_OK
util.collection.to_from_id VERDICT_OK

```

# Running Yoda portal unit tests

The Yoda portal uses the [unittest framework](https://docs.python.org/3/library/unittest.html) for the unit tests.
The test suites can be found in the `unit-tests` subdirectory of the portal repository. Run them using Python 3:

```bash
$ cd unit-tests
$ python3 -m unittest
......
----------------------------------------------------------------------
Ran 6 tests in 0.001s

OK
```

# Running external user service unit and integration tests

The external user service (EUS) uses [pytest](https://pytest.org) for unit and integration tests.

In order to run them, install the EUS package in a Python 3 virtual environment,
go to `yoda_eus/tests` and run the test suites using `pytest`. Example:

```bash
(venv) $ cd yoda_eus/tests
(venv) $ python3 -m pytest
===================================================================================== test session starts ======================================================================================
platform linux -- Python 3.10.12, pytest-7.4.2, pluggy-1.3.0
rootdir: /data/source/yoda-external-user-service
collected 33 items

test_integration.py .......................                                                                                                                                              [ 69%]
test_unit.py ..........                                                                                                                                                                  [100%]

===================================================================================== 33 passed in 10.02s ======================================================================================
```

# Running MOAI unit and integration tests

MOAI uses the [unittest framework](https://docs.python.org/3/library/unittest.html) for the unit and integration tests.

In order to run them you need to install apxs (`sudo apt install apache2-dev` on Ubuntu)
and SQLite3 libraries (`sudo apt install libsqlite3-dev` on Ubuntu). Then install MOAI in a Python 3 virtual environment
and run the tests using `unittest`:

```bash
(venv) $ cd moai
(venv) $ python3 -m unittest
......................
----------------------------------------------------------------------
Ran 22 tests in 0.192s

OK
```
