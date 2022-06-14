#!/bin/bash
# copyright Utrecht University

# Install Git if not present.
if ! command -v git >/dev/null; then
    echo "Installing Git."
    sudo yum install git -y
fi

# Install Ansible if not present.
if ! command -v ansible >/dev/null; then
    echo "Installing Ansible."
    sudo yum install epel-release -y
    sudo yum install ansible -y
fi

# Remove current version.
rm -rf ~/yoda

# Clone yoda.
git clone https://github.com/UtrechtUniversity/yoda.git
cd ~/yoda
git checkout development

# Set file permissions on SSH key to 0600.
chmod 0600 ~/yoda/vagrant/ssh/vagrant

# Install all Ansible collections needed to deploy Yoda.
ansible-galaxy collection install -r requirements.yml
