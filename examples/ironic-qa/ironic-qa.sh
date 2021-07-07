openstack server create --image ubuntu-bionic-cloud --flavor baremetal --key-name admin --nic net-id=baremetal --config-drive True --file /etc/cloud/cloud.cfg.d/90-networking.cfg=./qa01-cloud-init.yaml qa01


openstack server create --image ubuntu-bionic-cloud --flavor baremetal --key-name admin --nic net-id=baremetal --config-drive True --file /etc/cloud/cloud.cfg.d/90-networking.cfg=./qa02-cloud-init.yaml qa02


openstack server create --image ubuntu-bionic-cloud --flavor baremetal --key-name admin --nic net-id=baremetal --config-drive True --file /etc/cloud/cloud.cfg.d/90-networking.cfg=./qa03-cloud-init.yaml qa03

