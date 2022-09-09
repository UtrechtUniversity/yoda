# Running API and UI tests

Yoda uses [pytest](https://pytest.org) for API and UI tests.

## Running tests on the allinone VM

In order to run the tests on the Vagrant-based development environment, the allinone (default) Vagrant
configuration automatically mounts the `/etc/irods/yoda-ruleset` directory in the VM on the ./test
directory.

To run the tests on the Vagrant VM:
1. Ensure that you have [Geckodriver](https://github.com/mozilla/geckodriver) installed for running the UI tests.
2. Deploy the VM, for example:

```bash
vagrant box update && vagrant up && ansible-playbook -DK -i environments/development/allinone playbook.yml
```

3. Deploy the test data on the VM:

```
ansible-playbook -DK -i environments/development/allinone test.yml
```

4. Install the test dependencies

```bash
virtualenv ~/yoda-test-venv
source ~/yoda-test-venv/bin/activate
cd yoda/test/tests
python3 -m pip install selenium
python3 -m pip install -r requirements.yml
```

4. Run the tests (in the `yoda/test/tests` directory)

```bash
test -d /tmp/cache || mkdir -p /tmp/cache
python3 -m pytest -o cache_dir=/tmp/cache
```

## Alternative way of mounting the ruleset folder on Linux systems

Mount vagrant guest folder on host (e.g. `/etc/irods/yoda-ruleset/` so you can run `pytest` on the local machine):

```bash
# Mount
sshfs -o IdentityFile=/home/dev/.vagrant.d/insecure_private_key -p 2222 vagrant@127.0.0.1:/etc/irods/yoda-ruleset yoda-ruleset

# Umount
fusermount -u yoda-ruleset
```
