![Imagination Technologies Limited logo](../images/img.png)

# Creator System Test Framework

## Running the Test Framework on real hardware

The Test Framework supports connecting to a hardware gateway device through XMLRPC, allowing it to launch helper processes
and start Awa bootstrap servers, gateway servers and gateway clients. It can also use a constrained device helper to talk
with a constrained device over a serial cable.

### Prerequisites

* Ubuntu 16.04 installation on a host machine (PC or VM).
* Gateway Device (Ci40 or equivalent) with a power supply and vanilla OpenWRT installed onto flash.
* Constrained device(s) (eg. 6LowPAN Clicker with Avrdude-compatible bootloader)
* FTDI TTL - 232R Terminal Cable (FTDI Part #: TTL - 232R - RPI)
* USB Male - A socket to microUSB plug adapter
* 1 microUSB cable (for serial connection between host PC and Ci40)
* 1 microUSB cable (per constrained device - USB hub may be required for more than one connection to the gateway device)

### Flashing creator onto the Gateway Device

Choose instructions from one of the methods below to flash creator onto your gateway device.

* Download a prebuilt creator OpenWRT image and install dependencies through OPKG (Currently unsupported)
* Manually build creator on the host machine and flash the gateway device using Sysupgrade. [Instructions](doc/hardware/manually_building_creator.md)

Make sure to record the IP address of the gateway device by typing:

    $ ifconfig

and taking the inet address of the active interface (eth0, or wlan0 if you have setup wireless networking)
. You can now unplug the serial cable from the host to the gateway device and connect to the gateway through SSH instead.

### Setting up the Test Framework

#### Create the Test Framework root directory

If you wish to run the test framework through Jenkins, run the following commands:

    $ sudo mkdir -p /opt/jenkins/workspace/<your_job_name>
    $ sudo chmod 777 /opt/jenkins/workspace/<your_job_name>
    $ sudo ln -s /opt/jenkins/workspace/<your_job_name> /mnt/qa

Otherwise run:

    $ sudo mkdir -p /mnt/qa
    $ sudo chown <your_username> /mnt/qa

Install an NFS server on the host machine that will host the Test Framework directory. This has a number of advantages:

* Logs will be saved to the host rather than the gateway device, ensuring that the gateway device does not run out of
  disk space.
* Logs are more easily accessible from the host device.
* We do not have to copy changes made to the test framework from the host to the gateway device.

#### System-Test dependencies

Install the following dependencies that are required by the system test framework on the host machine:
    $ sudo apt-get install jq

#### NFS server setup

    $ sudo apt-get install nfs-kernel-server
    $ sudo nano /etc/exports
    $ /mnt/qa     192.168.149.27(rw,sync,no_root_squash)  # replace the IP address with the address of the gateway device
    * can be replaced with one of the hostname formats
    $ sudo exportfs -a
    $ sudo systemctl start nfs-kernel-server.service

Clone the creator-system-test-framework repository into the directory you wish to be mounted by the gateway device.
If not using the default key name, follow the guide [here](http://stackoverflow.com/questions/4565700/specify-private-ssh-key-to-use-when-executing-shell-command-with-or-without-ruby/11251797#11251797)
to enable your private key.

    $ cd /mnt/qa
    $ git clone --recursive https://github.com/CreatorDev/creator-system-test-framework.git creator-system-test-framework
    $ cd creator-system-test-framework
    $ (cd lwm2m-contiki/contiki && git checkout avrdude-mikro-e-no-local-echo)
    $ pip install -r requirements.txt

On the Ci40, run the following command to mount the Test Framework directory on the host machine:

    $ mkdir -p /mnt/qa && mount -t nfs <your_host_ip>:/mnt/qa /mnt/qa -o nolock

### Configuring OpenWRT to run the Test Framework

Enter the following commands below to enter the test framework directory and set necessary network configuration.

    $ cd /mnt/qa/creator-system-test-framework
    $ (cd hardware && ash setup-openwrt 17)  # 17 is the WPAN channel ID, can be between 0-26.

Make sure to choose a WPAN channel that is not currently in use for the gateway device, otherwise you will receive the
following error:

`no context available for interface '2001:1418:0100::1'`

### Connecting and Flashing the Constrained Device

Follow one of the instructions below to flash the test app onto the constrained device.

* Flashing the constrained device using the gateway device using
  [Pickle](doc/hardware/flashing_constrained_device_from_gateway.md) (preferred).
* Flashing the constrained device using the [host machine](doc/hardware/flashing_constrained_device_from_host.md)
  (requires manually switching the serial cable connected to the constrained device between the host machine and
  gateway device).

### Starting the Test Helpers on the Gateway Device

Run the following commands on the gateway device from within the mounted creator-system-test-framework folder to start
the required helpers to run the test framework.

Make sure to replace **gateway_ip** with the ip of the gateway device.

    $ PYTHONPATH=.:$PYTHONPATH python helpers/bootstrap_server_test_helper.py --ip $gateway_ip --port 4442 --log xmlrpcserver_bootstrap_local.log
    $ PYTHONPATH=.:$PYTHONPATH python helpers/gateway_server_test_helper.py --ip $gateway_ip --port 4342 --log xmlrpcserver_gateway_server_local.log
    $ PYTHONPATH=.:$PYTHONPATH python helpers/gateway_client_test_helper.py --ip $gateway_ip  --port 4242 --log xmlrpcserver_gateway_client_local.log
    $ PYTHONPATH=.:$PYTHONPATH python helpers/constrained_client_test_helper.py --ip $gateway_ip --port 4142 --log xmlrpcserver_constrained_client_local.log

### Running the test framework manually from the host machine

#### Creating a test configuration

Copy configs/hardware.yml in your creator-system-test-framework directory and give it a unique name. In the proxies
section, modify each ip address to match **gateway_ip** above.

#### Launching the test runner

Replace configs/hardware.yml with the name of the configuration you created above. Before you run any tests, make sure
to restart the constrained device.

Run the following two test cases to ensure the hardware setup is working as expected:

    $ PYTHONPATH=.:$PYTHONPATH ./noserunner.py -svv --tc-file configs/hardware.yml tests/test_constrained_client.py:SerialTests
    $ PYTHONPATH=.:$PYTHONPATH ./noserunner.py -svv --tc-file configs/hardware.yml tests/test_constrained_client.py:ConnectionTests

If the serial tests do not complete successfully, try:

* Make sure the constrained device is turned on.
* Make sure the constrained device is attached to ttyUSB1, or update your configuration file to use ttyUSB1 to connect
  to the constrained device.
* Check the serial connection between the gateway and constrained device.
* Ensure the serial wires are correctly connected to GND, TX and RX.

If the connection tests do not complete successfully, try:

* Make sure you ran the setup_openwrt script.
* Make sure the lwm2m-client-contiki-test app uses the same WPAN channel as the gateway device. (Run iwpan list on the
  gateway, reboot the constrained device)
* Make sure the WPAN channel is not being used by another gateway device.
* Make sure no other constrained devices are running with the same WPAN channel and PAN ID.
* View gwbootstrapd.log and see if Bootstrap Server received any COAP messages from the constrained device.
* Make sure the gateway device can ping the following addresses:

        $ ping6 2001:1418:100::1  # see if it's own interface is responding
        $ ping6 2001:1418:200:ffff::8.8.8.8  # see if the gateway device can access the internet

If these tests complete successfully, you are ready to run the entire test framework.

    $ PYTHONPATH=.:$PYTHONPATH ./noserunner.py -svv --tc-file configs/hardware.yml

### Continuous Integration

* Add a new test plan in testlink
* Create a jenkins server
* Create a new slave on Jenkins
* Install jenkins on host PC (for the slave to connect to)
* Login as jenkins user and ssh into the ci40 to add the NUC's public key to the known_hosts list
* Create a Jenkins job for the tests that uses the slave we created, testlink plugin, test framework/awa repos etc.

### Future Improvements

* Add Jenkins configurations to source control.
* Allow the helpers to start on arbitrary ports and pass those ports to the test framework -
  firewall must be modified on gateway device.
* Use a base OpenWRT image and install dependencies via OPKG.
