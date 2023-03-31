#!/bin/bash
# copyright Utrecht University
set -e
set -x

# Install Git if not present.
if ! command -v git >/dev/null; then
    echo "Installing Git."
    sudo apt install git -y
fi

# Install Ansible if not present.
if ! command -v ansible >/dev/null; then
    echo "Installing Ansible."
    sudo add-apt-repository ppa:ansible/ansible
    sudo apt update
    sudo apt install ansible -y
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
