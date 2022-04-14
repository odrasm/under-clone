### Usefule commands for testing images

* packages requirements (Ubuntu-focal): libguestfs-tools


* check disk layout and filesystem:
> ```shell
> #LIBGUESTFS_DEBUG=1 LIBGUESTFS_TRACE=1 sudo guestfish --ro -i -a underground.raw
> ```

* test image booting:
> ```shell
> #qemu-system-x86_64 -drive file=underground.raw,format=raw -nographic -m 4G
> ```
