#!/bin/bash
# copyright Utrecht University

# Install Ansible if not present.
if ! command -v ansible >/dev/null; then
    echo "Installing Ansible."
    sudo yum install epel-release -y
    sudo yum install ansible -y
fi

# Copy SSH key from Samba share to home directory.
cp /vagrant/vagrant/ssh/vagrant ~/vagrant

# Set file permissions on SSH key to 0600.
chmod 0600 ~/vagrant

# Remove key on Samba share.
sudo rm /vagrant/vagrant/ssh/vagrant

# Create hardlink to SSH key.
ln ~/vagrant /vagrant/vagrant/ssh/vagrant

# Run YoDa playbook.
cd /vagrant
ansible-playbook playbook.yml
