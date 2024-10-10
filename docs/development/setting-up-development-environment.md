---
parent: Development
title: Setting up development environment
nav_order: 0
---
# Setting up development environment
Setting up a Yoda development environment is easy, you only need the following:

* [VirtualBox](https://www.virtualbox.org/manual/ch02.html) or [libvirt](https://libvirt.org/)
* [Vagrant](https://www.vagrantup.com/docs/installation/) (>= 2.0)

On GNU/Linux or macOS you also need:
* [Ansible](https://docs.ansible.com/ansible/intro_installation.html) (>= 2.11)

The guide below will deploy an 'allinone' instance (all functional roles in one virtual machine) with the default configuration.

1. Clone the Yoda repository and checkout the development branch:
```bash
git clone https://github.com/UtrechtUniversity/yoda.git
cd yoda
git checkout development
```

2. Configure the virtual machines for development:

If you are using VirtualBox, open the `Vagrantfile` in an editor and change the `DEFAULT_VAGRANT_PROVIDER` line near
the top of the file so that it uses VirtualBox:

```bash
ENV['VAGRANT_DEFAULT_PROVIDER'] = "virtualbox"
```

Then use Vagrant to create the virtual machine (this applies to both VirtualBox and Libvirt):

```bash
vagrant up
```

3. On a Windows host first SSH into the Ansible controller virtual machine (skip this step on GNU/Linux or macOS):
```bash
vagrant ssh controller
cd ~/yoda
```
On a GNU/Linux or macOS host make sure the SSH keys have the right permissions (skip this step on Windows):
```bash
chmod 0600 ~/yoda/vagrant/ssh/vagrant
```

4. Deploy Yoda to the virtual machines:
```bash
ansible-galaxy collection install -r requirements.yml
ansible-playbook -i environments/development/allinone/ playbook.yml
```

5. Add following hosts to `/etc/hosts` (GNU/Linux or macOS) or  `%SystemRoot%\System32\drivers\etc\hosts` (Windows):
```
192.168.56.10 portal.yoda.test
192.168.56.10 data.yoda.test
192.168.56.10 public.data.yoda.test
192.168.56.10 public.yoda.test
192.168.56.10 eus.yoda.test
192.168.56.10 datacite-mock.yoda.test
192.168.56.10 sram-mock.yoda.test
```

6. Provision Yoda with test data:
```bash
ansible-playbook -i environments/development/allinone/ test.yml
```

7. [OPTIONAL] Provision Yoda with [Zabbix](https://www.zabbix.com/) agent and monitoring scripts:

    Configure Zabbix server in `environments/development/allinone/group_vars/allinone.yml` and make sure a Zabbix server is running on this address, you could use a [Zabbix appliance](https://www.zabbix.com/download_appliance) in Virtualbox.
    ```yaml
    zabbix_server: 192.168.56.20
    ```
    Run the Zabbix playbook
    ```
    ansible-playbook -i environments/development/allinone/ zabbix.yml
    ```

## Upgrading your Yoda development environment
Upgrading the Yoda development environment to the latest version can be done by running the Ansible playbooks again.

1. On a Windows host first SSH into the Ansible controller virtual machine (skip this step on GNU/Linux or macOS):
```bash
vagrant ssh controller
cd ~/yoda
```

2. Upgrade Ansible scripts:
```bash
git pull
```

3. Upgrade Yoda development environment:
```bash
ansible-playbook -i environments/development/allinone/ playbook.yml
```

## Development environment test users and data
When you have set up an Yoda development environment and provisioned it with test data the following users are created:

User                | Role
--------------------|----------
viewer              | Viewer with read only access to research groups
researcher          | Researcher with read / write access to research groups
groupmanager        | Groupmanager  with user management rights on research groups
datamanager         | Datamanager of the research groups
technicaladmin      | Technical administrator with rodsadmin access

Password for all test users is `test`.

In research group `research-initial` a folder `testdata` is created with some example data.

# Surf development environment

Surf uses the following setup:
- Portal server: runs Yoda portal, iRODS iCAT server (provider), iCAT database and EUS
- WebDAV server: runs DavRODS and public server, as well as iRODS resource server (consumer)
- Resource server: additional iRODS resource server

To deploy it on local VMs, add the following entries to your hosts file:

```
# Surf Yoda test
192.168.56.20 portal.surfyoda.test
192.168.56.21 data.surfyoda.test
192.168.56.21 public.data.surfyoda.test
192.168.56.21 public.surfyoda.test
192.168.56.20 eus.surfyoda.test
192.168.56.22 resource.surfyoda.test
```

And run the following commands in the root of the Yoda repository:

```
cp vagrant/environment/surf/Vagrantfile .
vagrant box update
vagrant up
ansible-playbook -DK -i environments/development/surf playbook.yml
```
