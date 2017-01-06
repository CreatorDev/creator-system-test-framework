![Imagination Technologies Limited logo](../images/img.png)

# Creator System Test Framework

## Installing Creator on the Gateway Device with Sysupgrade

First, follow these [instructions](https://github.com/CreatorDev/openwrt#serial-console) to connect to your
gateway device via serial through a microUSB cable.

At this point you should be able to putty in and see output when you reboot the Ci40.

### Ensure you have enough space available

Type the following command:

    $ df -h

Make sure you have at least enough space in tmpfs to be able to scp your image across. You may want to
delete any large log files or reboot before continuing.

### Sysupgrade

Run the below command on your gateway device, changing the following variables:

* username
* host_ip (Address of the host machine you used to build openWRT)
* guest_path_to_ubifs_image (eg. /repos/creator/dist/openwrt/bin/pistachio/openwrt-dev-pistachio-marduk-marduk_cc2520-ubifs.img)
* ubifs_image_filename (must be the same as the filename in the above line)

    `cd /tmp; scp username@host_ip:guest_path_to_ubifs_image ./ && sysupgrade -v ubifs_image_filename`

Wait for OpenWRT to reboot.

You can confirm your Awa version by typing:

    $ awa_clientd --version

Ensure no Awa daemons are running by typing:

    $ ps | grep awa
