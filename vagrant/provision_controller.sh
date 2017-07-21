#!/bin/bash
# copyright Utrecht University

# Install Ansible if not present.
if ! command -v ansible >/dev/null; then
    echo "Installing Ansible."
    sudo yum install epel-release -y
    sudo yum install ansible -y
fi

# Run YoDa playbook.
cd /vagrant
ansible-playbook playbook.yml
