![Imagination Technologies Limited logo](images/img.png)

----

## Creator System Test Framework

----

### Prerequisites (Without Docker - DEPRECATED)

WARNING: Tayga is unstable on some operating systems and may not correctly set up a NAT64 service, causing the simulated constrained device
to not be able to access the cloud. Docker is recommended.

Note: the instructions below are assuming an Ubuntu host.


 1) Clone this repository as well as its submodules.

    $ git clone --recursive https://github.com/CreatorDev/creator-system-test-framework.git DeviceManagementTests

 2) Build the AwaLWM2M development suite in a directory of your choice by following the instructions in the readme.

    $ cd DeviceManegementTests/AwaLWM2M
    $ make
    $ cd ..
 
 3) Build the minimal-net Contiki client:
    
    $ cd lwm2m-contiki/lwm2m-client-contiki-test
    $ make TARGET=minimal-net
    $ cd ../..

 4) Ensure configs/local_simulated.yml (or copy it and create your own) contains the correct paths to your LWM2M repository, and change the following constants:
    
    CLIENT_ID
    userName

 5) Install required python libraries:
    
    $ pip install -r requirements.txt
    
 6) Install Tayga:
 
    $ sudo apt-get install tayga
    $ sudo mkdir -p /var/db


### Running the Test Framework

 Firstly, launch the helpers. Root/sudo is required in order to manipulate the network interfaces on the Contiki simulated constrained device.
 
 The proxies that the devices connect to defined in configs/local_simulated.yml must match the address and port of the running helpers, otherwise the test framework
 will not be able to connect to a helper it requires in order to complete a test.

    $ PYTHONPATH=.:$PYTHONPATH python helpers/bootstrap_server_test_helper.py --ip 127.0.0.1 --port 4442 --log xmlrpcserver_bootstrap_local.log
    $ PYTHONPATH=.:$PYTHONPATH python helpers/gateway_server_test_helper.py --ip 127.0.0.1 --port 4342 --log xmlrpcserver_gateway_server_local.log
    $ PYTHONPATH=.:$PYTHONPATH python helpers/gateway_client_test_helper.py --ip 127.0.0.1 --port 4242 --log xmlrpcserver_gateway_client_local.log
    $ sudo PYTHONPATH=.:$PYTHONPATH python helpers/constrained_client_test_helper.py --ip 127.0.0.1 --port 4142 --log xmlrpcserver_constrained_client_local.log

 Run the tests with:

    $ PYTHONPATH=.:$PYTHONPATH ./noserunner.py -svv --tc-file configs/local_simulated.yml
