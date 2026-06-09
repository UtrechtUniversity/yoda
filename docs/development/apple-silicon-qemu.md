---
parent: Development
title: Running the Vagrant VM on Apple Silicon (QEMU)
nav_order: 2
---
# Running the Vagrant VM on Apple Silicon (QEMU)

The default Yoda development VM uses VirtualBox or libvirt/KVM. Neither runs
on Apple Silicon (arm64) Macs: VirtualBox is x86-only on macOS and libvirt/KVM
is Linux-only. This page describes an alternative environment that runs the
**same Ansible-provisioned VM** on Apple Silicon using
[QEMU](https://www.qemu.org/) and the
[vagrant-qemu](https://github.com/ppggff/vagrant-qemu) plugin.

## Why the guest is emulated (x86_64), not native (arm64)

Yoda's core dependency, iRODS, is only published for x86_64. The iRODS package
repositories contain no arm64/aarch64 builds:

- APT: `https://packages.irods.org/apt/dists/noble/main/` provides only
  `binary-amd64` and `binary-i386`.
- YUM: `https://packages.irods.org/yum/pool/el9/` provides only `x86_64`.

Every Yoda server role (iCAT, resource, icommands, runtime, microservices,
davrods) installs iRODS from these repositories, so a native arm64 guest
cannot be provisioned. This environment therefore runs an **x86_64 guest under
QEMU's TCG emulation**. Provisioning works, but because the CPU is emulated
rather than virtualised it is **considerably slower** than a native VM. If you
only want to *use* Yoda on a Mac (rather than exercise the Ansible roles),
the [Docker Compose setup](docker-setup.md), which runs the prebuilt
`linux/amd64` images under Rosetta 2, is usually the faster option.

## Prerequisites

```sh
brew install qemu
vagrant plugin install vagrant-qemu
```

## Bringing up the VM

From the repository root:

```sh
cp vagrant/environments/qemu/Vagrantfile .
vagrant up
```

The box defaults to `cloud-image/ubuntu-24.04` (a libvirt-format amd64 box,
which is the format vagrant-qemu consumes). The first `vagrant up` downloads
the box and resizes its disk; expect this to take a while under emulation.

### Tunables

All of the following can be overridden as environment variables before
`vagrant up`:

| Variable | Default | Purpose |
|---|---|---|
| `YODA_QEMU_BOX` | `cloud-image/ubuntu-24.04` | amd64 libvirt/qemu box |
| `YODA_QEMU_SMP` | `2` | emulated vCPUs |
| `YODA_QEMU_RAM` | `4096` | guest memory (MB) |
| `YODA_QEMU_DISK` | `32G` | resized guest disk |
| `YODA_QEMU_SSH_PORT` | `50022` | host port forwarded to guest SSH |
| `YODA_QEMU_HTTP_PORT` | `8080` | host port forwarded to guest port 80 |
| `YODA_QEMU_HTTPS_PORT` | `8443` | host port forwarded to guest port 443 |

OpenSearch is memory-hungry; if the VM is short on RAM either raise
`YODA_QEMU_RAM` or set `enable_open_search: false` in the environment's
`group_vars`.

## Networking model

QEMU user-mode networking does not support the static private-network IP
(`192.168.56.10`) the other environments rely on. Instead, host ports are
forwarded to the guest:

- SSH: host `50022` → guest `22`
- HTTP: host `8080` → guest `80`
- HTTPS: host `8443` → guest `443`

Inside the guest, all Yoda FQDNs are mapped to `127.0.0.1` (every service of
the all-in-one instance runs on this single host).

To reach the portal from your Mac's browser, add the FQDNs to the **host**
`/etc/hosts`, pointing at loopback:

```
127.0.0.1 combined.yoda.test portal.yoda.test data.yoda.test \
          public.data.yoda.test public.yoda.test eus.yoda.test \
          api.eus.yoda.test datacite-mock.yoda.test sram-mock.yoda.test
```

Then browse to `https://portal.yoda.test:8443`.

> Caveat: because HTTPS is forwarded to the unprivileged port `8443`, any
> absolute redirect Yoda emits to `https://portal.yoda.test/` (port 443) will
> not resolve on the host. If you hit this, forward the privileged ports
> directly by setting `YODA_QEMU_HTTPS_PORT=443` and `YODA_QEMU_HTTP_PORT=80`
> (binding ports below 1024 on macOS requires running `vagrant up` with
> sufficient privileges) and drop the `:8443` from the URL.

## Provisioning with Ansible

The control node is your Mac. Because the VM is reached over the forwarded SSH
port rather than a routable IP, pass the connection details on the command
line (the all-in-one inventory is a single host, so this applies cleanly to
it):

```sh
chmod 0600 vagrant/ssh/vagrant
ansible-playbook -i environments/development/allinone/ \
  -e ansible_host=127.0.0.1 -e ansible_port=50022 \
  playbook.yml
```

The `ansible_user`, private key and Python interpreter come from the
`allinone` group variables as usual; `host_key_checking` is already disabled
in `ansible.cfg`. To load the test data afterwards, run `test.yml` the same
way.

## Limitations

- Emulated x86_64 is slow; a full provisioning run takes substantially longer
  than on a native (Intel/Linux) host.
- Only the all-in-one topology is provided. The multi-host environments
  (`full`, `surf`) assume routable private-network IPs and are not adapted to
  QEMU user-mode networking.
- Native arm64 is not possible while iRODS ships x86_64 only; revisit if the
  iRODS Consortium publishes aarch64 packages.
