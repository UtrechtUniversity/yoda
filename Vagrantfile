# -*- mode: ruby -*-
# vi: set ft=ruby :

# Configuration variables.

VAGRANTFILE_API_VERSION = "2"

BOX = 'centos/7'
GUI = false
CPU = 1
RAM = 512

DOMAIN  = ".yoda.dev"
NETWORK = "192.168.50."
NETMASK = "255.255.255.0"

HOSTS = {
   "portal"   => [NETWORK+"10", CPU, RAM, GUI, BOX],
   "database" => [NETWORK+"11", CPU, RAM, GUI, BOX],
   "icat"     => [NETWORK+"12", CPU, RAM, GUI, BOX],
   "resource" => [NETWORK+"13", CPU, RAM, GUI, BOX],
}


Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.ssh.insert_key = false

  HOSTS.each do | (name, cfg) |
    ipaddr, cpu, ram, gui, box = cfg

    config.vm.define name do |machine|
      machine.vm.box = box

      machine.vm.provider "virtualbox" do |vbox|
        vbox.gui    = gui
        vbox.cpus   = cpu
        vbox.memory = ram
        vbox.name   = name
      end

      machine.vm.hostname = name + DOMAIN
      machine.vm.network 'private_network', ip: ipaddr, netmask: NETMASK
    end
  end
end
