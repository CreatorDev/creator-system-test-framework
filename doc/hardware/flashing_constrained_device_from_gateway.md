![Imagination Technologies Limited logo](../images/img.png)

----

## Creator System Test Framework

----

### Flashing lwm2m-client-contiki-test onto the constrained device

Firstly, follow these [instructions](doc/hardware/building_the_constrained_device_test_app.md) 
to build the lwm2m-client-contiki-test app.

The directory in which the hex file is built will be accessible to the Ci40 through NFS 
(DeviceManagementTests/lwm2m-contiki/lwm2m-client-contiki-test/lwm2m-client-contiki-test.hex).

Plug in the constrained device to the gateway device via a programming (ribbon) cable (ICSP port on clicker to RPI connector on Ci40). 
A schematic can be seen (here)[doc/hardware/ci40_to_clicker_serial_and_programming_connection.md].

* Connect the 40-pin plug to the raspberry PI interface on the Ci40 (CN5).
* Connect the 6-way plug to the PICKIT connector on the bottom of the clicker.
* Connect the 8-way plug to the rightmost mikro-bus socket on the clicker.

This cable will provide power to the constrained device and allow the gateway to both communicate with the constrained device
and program it directly with the pickle interface. 

The constrained device should be viewable from the gateway device using the following commands:

    $ p32 info
    $ p32 config
    $ p32 id

If you receive the following message, the constrained device is incorrectly connected to the gateway.

`pic32_read_config_memory: information: device not compatible.`

Then, run the following command to flash the constrained device from the Ci40:

    $ p32 PROGRAM /mnt/qa/DeviceManagementTests/lwm2m-contiki/lwm2m-client-contiki-test/lwm2m-client-contiki-test.hex

The device should automatically reboot.

In your ssh connection to the gateway device, type:

    $ dmesg 

Which should show that the constrained device has been attached to **ttySC0**

