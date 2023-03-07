# Vagrant Development Environment

Before use this environment install [Vagrant].
In MacOS environments it is possible to install with [Homebrew]:

```
# brew install vagrant
```

## Vagrant Box

You are encouraged to use an official GNU/Linux distro, to ensure the maximum
compatibility with the real world:

* https://app.vagrantup.com/centos
* https://app.vagrantup.com/debian
* https://app.vagrantup.com/opensuse
* https://app.vagrantup.com/ubuntu

## The Vagrantfile

To make the development experience smooth, we suggest to share your Git repo
with vboxfs.

```
# vagrant plugin install vagrant-vbguest
```

[Vagrant]: https://www.vagrantup.com
[Homebrew]: https://brew.sh
[NFS]: https://www.vagrantup.com/docs/synced-folders/nfs#root-privilege-requirement
