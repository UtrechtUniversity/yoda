---
parent: Administration Tasks
title: Using the python-irodsclient API
nav_order: 10
---

# Using the python-irodsclient API

iRODS has a Python API named [python-irodsclient](https://github.com/irods/python-irodsclient). It can
be used to automate operations on iRODS entities such as data objects, collections, users and groups,
as well as associated metadata. It is also commonly used to query iRODS using the *GenQuery* functionality.

This page shows how to run a demo Python script that connects to iRODS using python-irodsclient and performs
a GenQuery.

For further information about python-irodsclient, see the
[python-irodsclient README](https://github.com/irods/python-irodsclient). The test
cases in the python-irodsclient repository also can be used to see examples of how functionality can
be used.

# Prerequisites

In order to use the Python-irodsclient you would need to have Python installed on your PC/laptop (preferably version
3.6 or higher, although some older versions can also be made to work), as well as `pip`. Use of `virtualenv` is
recommended, in order to isolate python-irodsclient's dependencies from those of other Python software on
your system.

You also need a CA bundle. A common choice is to either use your system's CA bundle or to
download [the curl CA bundle](https://curl.se/docs/caextract.html).

Finally, you need an account on a Yoda environment and a `yoda_environment.json` file containing the
environment configuration.

Python-irodsclient is most commonly used on Linux, but works on Windows and macOS as well.

# Preparation

* Download the [example script](example-code/demo-python-api.py) and put it in a local directory.
* Adjust the `ca_file` (or equivalent) parameters to point to your OS CA Bundle. Alternatively,
  download [the curl CA bundle](https://curl.se/docs/caextract.html) and put the `cacert.pem` file
  in the same directory as the script.
* Put the `irods_environment.json` file of the environment in the same directory as the script.
* Create and activate a virtualenv for the script that has `python-irodsclient` (on Windows, replace `source venv/bin/activate` with `venv\scripts\Activate`):

```
virtualenv venv
source venv/bin/activate
python -m pip install python-irodsclient==1.1.5
```

* If you are on Linux or MacOS, ensure the script is executable:

```
chmod +x demo-python-api.py
```

* The example script is configured for Yoda 1.8 and higher. If you still use Yoda 1.7, set `require_ssl`
  to `False` in the script.

# Running the script

You can now run the script. It will first prompt for your password. If you have
enabled [data access passwords](configuring-data-access-passwords.md),
enter a valid data access password here. Otherwise enter your account password.

After entering the password, the script should perform a GenQuery to retrieve a list
of group collections that you have access to and show the results, for example:


```
/testZone/home/research-test
/testZone/home/vault-test
```
