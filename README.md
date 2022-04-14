# Underground

A Cloud Platform developed and designed according to the Open Infrastructure
principles.

Underground is based on the most recent and stable version of OpenStack. It can
be expanded with additional resources and functionality based on need.

## Why Underground?

With Underground as the basis for a true open infrastructure, you won’t have to
worry about hardware or software constraints. Our Open Source Cloud Platform
is a solution without lock-ins, including from the point of view of
functionalities and services: each of them can be activated and deactivated
easily to radically change the scope and shape of the infrastructure. This is
something that can be defined as true infrastructure-as-code.

## Support Matrix

|                   |   Stein    |   Train    |   Ussuri   |  Victoria  |  Wallaby   |  Xena      |
| ----------------: | :--------: | :--------: | :--------: | :--------: | :--------: | :--------: |
|      Ubuntu 18.04 | Python 2.x | Python 3.x |            |            |            |            |
|      Ubuntu 20.04 |            | Python 3.x | Python 3.x | Python 3.x | Python 3.x | Python 3.x |
|        CentOS 7.x | Python 2.x | Python 3.x |            |            |            |            |
|        CentOS 8.x |            | Python 3.x | Python 3.x | Python 3.x |            |            |
| CentOS 8.x Stream |            |            |            | Python 3.x | Python 3.x |            |

## Deplyment Strategies

* **All-in-One [aio]**: small customers, dipartimental server, edge, demo, testing, and development environment
* **All-in-One [aio] + Baremetal**: baremetal management lifecycle
* **Hiper-Converged Infrastrure [hci]**: edge, fog,  or small/medium datacentre
* **Converged [converged]**: Contro/Network + Compute/Storage linear scalability for medium/large datacentre
* **Distributed [distributed]**: large deployments, Big Data, and High Performance Computing

## Prerequisites for All-in-One

#### Software

- Ansible 2.9.x
- Git

#### Hardware (including VM)

##### Minimal

- **CPU**: 2x 1.8GHz x84_64
- **RAM**: 6GB
- **Storage OS**: 20GB HDD
- **Storage Data**: 50GB HDD

##### Minimal Baremetal

- **CPU**: 2x 1.8GHz x84_64
- **RAM**: 8GB
- **Storage OS**: 100GB HDD
- **Network**: 1gbit nic dedicated for baremetal

##### Recommended

- **CPU**: 16x 3.0GHz x84_64
- **RAM**: 128GB
- **Storage OS**: 128GB SSD
- **Storage Data**: 3x 500GB SSD

## Installation

### Prerequisites

[Ansible installation reference]: https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html

#### RedHat/CentOS 7

Using distro packages:

```shell
yum -y install epel-repo
yum -y install ansible git
```

Using Python pip:

```shell
yum -y install python-pip
pip install 'ansible<2.10'
```

#### RedHat/CentOS 8

Using distro packages:

```bash
dnf -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
dnf -y install --enablerepo epel-playground ansible git
```

Using Python pip:

```shell
dnf -y install python3-pip git
python3 -m pip install 'ansible<2.10'
```

#### Debian/Ubuntu

Using distro packages:

```shell
apt install -y ansible git
```

Using Python pip:

```shell
apt install -y python3-pip git
python3 -m pip install 'ansible<2.10'
```

#### Install

```shell
git clone https://git.cloud.e4.lan/e4/underground
python3 -m pip install underground
```

Or directly from Git:

```shell
python3 -m pip install git+https://git.cloud.e4.lan/e4/underground
```

If you want to install Underground only for development purpose:

```
git clone https://git.cloud.e4.lan/e4/underground
cd underground
```

The Underground command is available using the local path syntax `tools/underground` inside the code directory or using the absolute path (e.g. `/path/to/underground/code/tools/underground`).

## Deployment

The deployment sequence follow these steps:

1. **Initialization**: `underground init [-f] <DEPLOYMENT>`
2. **Bootstrapping**: `underground bootstrap <RELEASE> [-m <MODULE(S)>] [-n <NIC>]`
3. **Configuration**: `underground configure`
4. **Deployment**: `underground deploy`
5. **Post Deployment**: `underground post-deploy`

### Initialization

> ```shell
> underground init [-f] <DEPLOYMENT>
> ```
>
> e.g.
>
> ```shell
> # underground init aio
> ```

Underground initialization is needed to create common configuration directory and the initial inventory hosts structure:

* Directories:
  * /etc/underground
  * /etc/flictus/host_vars
* Files:
  * /etc/underground/hosts

Also, the initialization step, execute all low level operation needed befor bootstrap (e.g. packages installation).

The `-f` (or `--force`) command line option will overwrite `/etc/underground/hosts` if exists.

The inventory file `/etc/underground/hosts` needs to be adapted with specified nodes an all scenario except All-on-One when the deployment machine is the target machine too.

### Bootstrapping

> ```shell
> underground bootstrap <RELEASE> [-m <MODULE(S)>] [-n <NIC>]
> ```
>
> e.g.
>
> ```shell
> # underground bootstrap victoria -m base,ceph -n enp0s8
> ```

After edited the inventory file `/etc/underground/hosts`, it is possible to procede with bootstrapping the nodes.

Atcions executed in this step are:

* Check if node OS is suitable for selected role
* Install required distribution packages (rpm and deb)
* Install correct Python version related to the selected OpenStack release
* Install required Python packages (PyPI)
* Install Kolla, Kolla Ansible, and Ceph Ansible

As a results of execution, some files under the Underground config directory is created:

* Write boostrap paramenters into /etc/underground/globals.yml

  ```yaml
  ---
  underground_deployment: aio
  underground_enable_modules:
  - base
  - ceph
  underground_internal_address: 127.0.0.2
  underground_internal_interface: lo
  underground_openstack_release: victoria
  underground_public_interface: enp0s8
  underground_replica_interface: enp0s8
  underground_storage_interface: enp0s8
  ```

This file can be safely modified by users. Subsequent invocation of booststrap will not overwrite values inside this file.

### Configuring

> ```shell
> underground configure
> ```
>
> e.g.
>
> ```shell
> # underground configure
> ```

Configuration step will populate multiple files inside /etc/underground directory:

* /etc/underground/globals.d/
  * ceph.yml
  * kolla.yml
  * passwords.yml
* /etc/underground/host_vars:
  * <hostname>

## Deploying Underground Baremetal

### Pre-Req

* 1 dedicated nic + subnet for baremetal
* no ip addresss on baremetal nic
* 2 ip address for baremetal nic

### Example

> ```shell
> # underground init aio
> ```
> ```shell
> # underground bootstrap victoria -m baremetal -n ens3 -e underground_baremetal_interface=ens5 -e underground_baremetal_network='100.127.102.200/24' -e underground_internal_address='100.127.102.201/24' -e underground_external_interface=ens4 -e underground_public_address='100.127.103.100'
> ```
> ```shell
> # underground build -t dib -e underground_baremetal_image="ipa"
> ```
> ```shell
> # underground configure
> ```
> ```shell
> # underground deploy
> ```
> ```shell
> # underground post-deploy
> ```

### Parameters

* underground_baremetal_interface: "interface where the bridge and neutron is created"
* underground_baremetal_network: "ip/prefix of ironic inspector and neutron baremetal network"
* underground_internal_address: "internal VIP address on keepalived"
* underground_external_interface: "neutron vxlan interface"
* underground_public_address: "external VIP address on keepalived
* underground_baremetal_image: "image to build witch DIB, default to IPA"

### Bootstrap Example Vars File

> ```shell
> # underground bootstrap victoria -m baremetal -n ens3 -e "@/usr/local/src/underground/contrib/vars/underground_baremetal_vars.yml"
> ```

### Set Autodiscovery , default=enabled

> ```shell
> # underground-autodiscovery disable
> ```

### Image Deployed

* Minimum set for image to be deployed

> ```shell
> # underground build -t dib -e underground_baremetal_image="underground" -e baremetal_image_upload="true"
> ```

* underground elements: "ubuntu focal gpt efi lvm"
* underground disk layout: "green/blue rootfs , docker"
