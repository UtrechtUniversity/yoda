---
parent: Development
title: Running API and UI tests
nav_order: 2
---

# Running API and UI tests

Yoda uses [pytest](https://pytest.org) for API and UI tests.

## Running tests on the allinone VM

In order to run the tests on the Vagrant-based development environment, the allinone (default) Vagrant
configuration automatically mounts the `/etc/irods/yoda-ruleset` directory in the VM on the ./test
directory.

1. To run the UI tests you need Firefox 102 ESR or later.
2. Ensure that you have [geckodriver 0.33.0](https://github.com/mozilla/geckodriver/releases/tag/v0.33.0) installed for running the UI tests.
   On Ubuntu 22.04 LTS, Geckodriver does not work with the default Firefox snap package when using default settings. One workaround
   is to remove the Firefox snap package, and replace it with the Firefox deb package from the Mozilla PPA (`ppa:mozillateam/ppa`).
3. Create the development VM using Vagrant:
```bash
vagrant box update && vagrant up
```

4. Deploy the VM.

```bash
ansible-playbook -i environments/development/allinone playbook.yml -D
```
    On a Windows host first SSH into the Ansible controller virtual machine (skip this step on GNU/Linux or macOS):
```bash
vagrant ssh controller
cd ~/yoda
```

5. Deploy the test data on the VM:
```bash
ansible-playbook -i environments/development/allinone test.yml -D
```

6. Clone the yoda-ruleset repository and install the test dependencies
```bash
git clone https://github.com/UtrechtUniversity/yoda-ruleset.git
cd yoda-ruleset/tests
python3 -m pip install -r requirements.txt
```

7. Run the tests (in the `yoda-ruleset/tests` directory)
```bash
test -d /tmp/cache || mkdir -p /tmp/cache
python3 -m pytest -o cache_dir=/tmp/cache
```

### Custom test options

The test suite accepts the following custom options:

```
  --datarequest         Run datarequest tests
  --deposit             Run deposit tests
  --intake              Run intake tests
  --archive             Run vault archive tests
  --sram                Run group SRAM tests
  --skip-ui             Skip UI tests
  --skip-api            Skip API tests
  --all                 Run all tests
  --environment=ENVIRONMENT
                        Specify configuration file
  --verbose-test        Print additional information for troubleshooting purposes
```

The default configuration files are located in directory `tests/environments`.

Option `--all` is incompatible with the `--skip-ui` and `--skip-api` options.

### Testing against Datacite

By default, the development VM uses an internal mock Datacite service. If you want to test against a real Datacite environment,
you will need to provide the Datacite server name and credentials when deploying the VM (step 4). For example:

```bash
ansible-playbook -i environments/development/allinone playbook.yml --extra-vars 'datacite_server=api.test.datacite.org datacite_username=MYUSERNAME datacite_password=MYPASSWORD' -D
```

## Development
- Tests are written with Pytest-BDD: https://pytest-bdd.readthedocs.io/en/latest/
- UI tests use Splinter to automate browser actions: https://splinter.readthedocs.io/en/latest/index.html
