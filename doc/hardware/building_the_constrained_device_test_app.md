![Imagination Technologies Limited logo](../images/img.png)

# Creator System Test Framework

## Building the constrained device test app

Firstly you will need to change the default WPAN channel for contiki to use the
same channel as your gateway device. Edit the file
'creator-system-test-framework/lwm2m-contiki/contiki/platform/mikro-e/contiki-conf.h'
in your text editor of choice.

Modify the line below to use the channel ID of your gateway device:

    #define RF_CHANNEL                            26

Install AVRDude:

    $ sudo apt-get install avrdude

Follow the instructions [here](https://github.com/CreatorDev/lwm2m-contiki#programming-a-mikro-e-clicker-board-using-avrdude)
to program the avrdude bootloader onto the constrained device.

Build the lwm2m-contiki Test Application:

    $ cd creator-system-test-framework/lwm2m-contiki/lwm2m-client-contiki-test
    $ make TARGET=mikro-e clean

Run the following command if you are flashing the constrained device from the gateway device.

    $ make TARGET=mikro-e BOOT=0

Run the following command if you are flashing the constrained device from the host PC.

    $ make TARGET=mikro-e
