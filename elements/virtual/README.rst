=======
virtual
=======

Sets up a partitioned disk GPT (rather than building just one filesystem with
no partition table) with XFS.

The following packages are ensured to be installed:
- acpid: to manage shutdown gracefully
- haveged: unpredictable random number generator for low-entropy conditions
- open-vm-tools: handle system operations in virtual environments
- qemu-guest-agent: enable crash consistant operations

To take advantages of it set the property hw_qemu_guest_agent=yes inside the
Glance image:
``# openstack image create --property hw_qemu_guest_agent=yes ...``
