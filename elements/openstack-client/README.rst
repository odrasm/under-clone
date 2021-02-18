================
openstack-client
================

This element install the OpenStack client from PyPi repository.
It also install the most common OpenStack modules.

Environment Variables
---------------------

DIB_OPENSTACK_MODULES
  :Required: No
  :Default: ``barbican cinder cloudkitty congress designate glance heat
            ironic keystone magnum manila mistral monasca neutron nova
            octavia swift trove watcher``
  :Description: List of OpenStack modules to install.
