![Imagination Technologies Limited logo](../images/img.png)

----

## Creator System Test Framework

----

### Flashing lwm2m-client-contiki-test onto the constrained device

Firstly, follow these [instructions](doc/hardware/building_the_constrained_device_test_app.md) 
to build the lwm2m-client-contiki-test app.

Plug in the serial cable from the constrained device to your host machine. Plug a microUSB from the host machine to the constrained device for power.
Turn the constrained device on while holding the T1 button down in order to halt the boot process and enable flashing of the device.
Connect to the constrained device USB driver - the device should be visible by typing:

    $ ls /dev/ttyACM*

Run the following command to use AVRDude to flash the constrained device with lwm2m-client-contiki-test:

    $ sudo make TARGET=mikro-e lwm2m-client-contiki-test.u

Once the hex file upload has finished, the constrained device will automatically reboot into the lwm2m-client-contiki-test app.

Unplug the serial cable connecting the constrained device to the host PC, and connect it from the constrained device to the gateway device.

In your ssh connection to the gateway device, type:

    $ dmesg 

Which should show that the constrained device has been attached to **ttyUSB0**




