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
2. Ensure that you have [geckodriver 0.32.0](https://github.com/mozilla/geckodriver/releases/tag/v0.32.0) installed for running the UI tests.
3. Create the development VM using Vagrant:
```bash
vagrant box update && vagrant up
```

4. Deploy the VM. In order to be able to complete the vault publication tests, you will need to pass Datacite test credentials when
   deploying the playbook. For example:
```bash
ansible-playbook -i environments/development/allinone playbook.yml --extra-vars 'datacite_username=MYUSERNAME datacite_password=MYPASSWORD' -D
```
   If no Datacite test credentials are available, it is also possible to deploy the allinone VM without providing values for the Datacite parameters.
   In that case, the vault publication tests will fail. For example:
```bash
ansible-playbook -i environments/development/allinone playbook.yml -D
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
