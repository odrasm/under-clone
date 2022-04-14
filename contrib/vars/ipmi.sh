ipmitool -I lanplus -H 100.127.102.127 -U ADMIN -P ADMIN chassis power reset
ipmitool -I lanplus -H 100.127.102.127 -U ADMIN -P ADMIN chassis power on
sleep 5
ipmitool -I lanplus -H 100.127.102.127 -U ADMIN -P ADMIN chassis bootdev pxe

ipmitool -I lanplus -H 100.127.102.128 -U ADMIN -P ADMIN chassis power reset
ipmitool -I lanplus -H 100.127.102.128 -U ADMIN -P ADMIN chassis power on
sleep 5
ipmitool -I lanplus -H 100.127.102.128 -U ADMIN -P ADMIN chassis bootdev pxe

ipmitool -I lanplus -H 100.127.102.129 -U ADMIN -P ADMIN chassis power reset
ipmitool -I lanplus -H 100.127.102.129 -U ADMIN -P ADMIN chassis power on
sleep 5
ipmitool -I lanplus -H 100.127.102.129 -U ADMIN -P ADMIN chassis bootdev pxe
