![Imagination Technologies Limited logo](images/img.png)

# Creator System Test Framework

## Test Filters

Using the [nose attrib plugin](http://nose.readthedocs.org/en/latest/plugins/attrib.html), tags have been added to each
test class. The tests can then be run with custom filters by adding the -A flag to the command you use to run nosetests
(dependent on whether docker is used or not).

    <nose_runner_command> -A 'gateway_server or gateway_client'
    <nose_runner_command> -A 'not gateway_server and device_object'

To view your filter before running the test cases, add the following flag:

    --collect-only

Current tags:

Tag | Description
--- | -------------
user | user creation / deletion test cases
gateway_server | test cases that involve a gateway server
gateway_client | test cases that involve a client
constrained_device | test cases that involve a constrained device
device_object | test cases that operate on an LWM2M device object
