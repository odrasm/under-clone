### Usefule commands for ironic interaction


* list autodiscovered nodes:
> ```shell
> # openstack baremetal node list
> ```

* iteraction example:
> ```shell
> # for NODE in `openstack baremetal node list -c UUID -f value` ; do openstack baremetal node set $NODE --resource-class baremetal ; done
> ```

* sava autodiscovered intropsection data in json/yaml:
> ```shell
> # openstack baremetal introspection data save --file $NODE.json $NODE
> # cat $NODE.json | yq > $NODE.yml
> ```

* examples of setting properties and resources, in case are different from default introspection auto set rules:
> ```shell
> # openstack baremetal node set $NODE --resource-class baremetal
> # openstack baremetal node set --driver ipmi --driver-info ipmi_address=<address> --driver-info ipmi_username=<username> --driver-info ipmi_password=<password>
> # openstack baremetal node set $NODE --driver-info deploy_kernel="$DEPLOY_KERNEL" --driver-info deploy_ramdisk="$DEPLOY_RAMDISK"
> # openstack baremetal node set $NODE --property capabilities=boot_option:local,boot_mode:uefi
> # openstack baremetal node set $NODE --property capabilities=boot_option:local,boot_mode:bios
> ```

* setting node in manage clean or new inspection:
> ```shell
> # openstack baremetal node manage $NODE
> ```

* enable web console id dashboard is enabled
> ```shell
> # openstack baremetal node set $NODE --console-interface ipmitool-socat
> # openstack baremetal node set $NODE --driver-info ipmi_terminal_port=$PORT
> # openstack baremetal node console enable $NODE
> ```

* setting node in provide ready for deploy:
> ```shell
> # openstack baremetal node provide $NODE
> ```

* check if the resource for baremetal deploy are free or correctly allocable:
> ```shell
> # openstack --os-placement-api-version 1.10 allocation candidate list --resource CUSTOM_BAREMETAL='1'
> ```

* create pxe port for deploy, macaddress from previously discovered data:
> ```shell
> # cat $NODE.yml |grep -i pxe
> # openstack baremetal port create --node $NODE --pxe-enabled true $MACADDRESS
> ```

* clean node, erase metadata on disks:
> ```shell
> # openstack baremetal node clean $NODE --clean-steps '[{"interface": "deploy", "step": "erase_devices_metadata"}]' 
> ```

* set root device for deploy
> ```shell
> # openstack baremetal node set $NODE --property root_device='{"name": "/dev/$DISK"}'
> ```

* set raid configuration
> ```shell
> # openstack baremetal node set $NODE --target-raid-config /etc/underground/baremetal/templates/raid5.json 
> ```

* deploy baremetal node with config-drive:
> ```shell
> # openstack server create --config-drive True --image $IMAGE --flavor baremetal-bios --nic net-id=baremetal --key-name ironic_key $NODE
> # openstack server create --config-drive True --image $IMAGE --flavor baremetal-uefi --nic net-id=baremetal --key-name ironic_key $NODE
> ```

* deploy baremetal node with config-drive and user-data:
> ```shell
> # openstack server create --config-drive True --user-data /path/to/file --image $IMAGE --flavor baremetal-bios --nic net-id=baremetal --key-name ironic_key $NODE
> # openstack server create --config-drive True --user-data /path/to/file --image $IMAGE --flavor baremetal-uefi --nic net-id=baremetal --key-name ironic_key $NODE
> ```

* deploy baremetal node with network and config-drive:
> ```shell
> # openstack server create --config-drive True --file /etc/cloud/cloud.cfg.d/90-networking.cfg=./$NETWORK.yaml --image $IMAGE --flavor baremetal-bios --nic net-id=baremetal --key-name ironic_key $NODE
> # openstack server create --config-drive True --file /etc/cloud/cloud.cfg.d/90-networking.cfg=./$NETWORK.yam l--image $IMAGE --flavor baremetal-uefi --nic net-id=baremetal --key-name ironic_key $NODE
> ```

