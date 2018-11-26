# Setting up development environment
Setting up a Yoda development environment is easy, you only need the following:

* [VirtualBox](https://www.virtualbox.org/manual/ch02.html) (>= 5.2)
* [Vagrant](https://www.vagrantup.com/docs/installation/) (>= 2.0)

On GNU/Linux or macOS you also need:
* [Ansible](https://docs.ansible.com/ansible/intro_installation.html) (>= 2.7)

The guide below will deploy an 'allinone' instance (all functional roles in one virtual machine) with the default [configuration](CONFIGURATION.md).

1. Configure the virtual machines for development:
```bash
vagrant --instance=allinone up
```

2. On a Windows host first SSH into the Ansible controller virtual machine (skip this step on GNU/Linux or macOS):
```bash
vagrant ssh controller
cd ~/yoda-ansible
```

3. Deploy Yoda to the virtual machines:
```bash
ansible-playbook -i environments/development/allinone/ playbook.yml
```

4. Provision Yoda with test data:
```bash
ansible-playbook -i environments/development/allinone/ test.yml
```

5. Add following hosts to /etc/hosts (GNU/Linux or macOS) or  %SystemRoot%\System32\drivers\etc\hosts (Windows):
```
192.168.50.10 portal.yoda.test
192.168.50.10 data.yoda.test
192.168.50.10 public.data.yoda.test
192.168.50.10 public.yoda.test
```

## Upgrading your Yoda development environment
Upgrading the Yoda development environment to the latest version can be done by running the Ansible playbooks again.

1. On a Windows host first SSH into the Ansible controller virtual machine (skip this step on GNU/Linux or macOS):
```bash
vagrant ssh controller
cd ~/yoda-ansible
```

2. Upgrade Ansible scripts:
```bash
git pull
```

3. Upgrade Yoda development environment:
```bash
ansible-playbook -i environments/development/allinone/ playbook.yml
```
