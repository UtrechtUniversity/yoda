#!/bin/bash
# copyright Utrecht University

# Install Ansible if not present.
if ! command -v ansible >/dev/null; then
    echo "Installing Ansible."
    sudo yum install epel-release -y
    sudo yum install ansible -y
fi

# Remove current version.
rm -rf ~/yoda-ansible

# Copy repository to home directory.
cp -R /tmp/yoda-ansible ~

# Remove temporary directory.
rm -rf /tmp/yoda-ansible

# Set file permissions on SSH key to 0600.
chmod 0600 ~/yoda-ansible/vagrant/ssh/vagrant

# Run YoDa playbook.
cd ~/yoda-ansible
ansible-playbook playbook.yml --limit=$1
