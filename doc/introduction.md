![Imagination Technologies Limited logo](images/img.png)

----

## Creator System Test Framework

----

### Requirements

The QA Device Management End-To-End Test Framework was developed to satisfy the following requirements, in order to confidently assure expected functionality:

* Written tests must be linked to an existing test plan, ensuring there are no discrepancies between what was intended to be tested and what actually is.
* A way to quickly see what is being tested at a high level, without any knowledge of the test system, digging into written test cases or relying upon the names of those passing/failing test cases.
* Keep track of version numbers for each component so that it is possible to quickly identify which change to which component caused a previously passing test to fail.
* Be able to quickly switch component versions and re-run the test system.
* Easy to setup and run the tests locally exactly as they would be run on a Jenkins CI server.
* Be able to write data-driven / parameterised tests, load configuration files and execute subsets of tests in a standardised way.
* Integrate the test system with third party test tools, including Jenkins.
* Make use of existing components rather than writing our own.
* Ability to run multiple test suites / test cases in parallel, independently of each other. 
* Be flexible and extensible, accommodating for the changing nature of our Device Management solution and tests with greater requirements that may need to be run in the future.

### Components

#### TestLink

TestLink is a web-based test management system that allows team members to collaborate in real-time on a the test plan, and track results as they occur. 
It is an open-source solution that fills the gap between the test plan and the test framework, allowing users to execute tests and view test reports that match the test plan they have written, all from a single application.

TestLink allows anyone to see exactly what is being tested at a high level. Without a link between test cases and a test plan, there is no way for a user to understand what is and isn't being tested without detailed knowledge of the test system .
Without a test management solution, any changes to the test cases (including failing/passing, skipping or adding/removing tests) would not be reflected in the test plan. It is important to be able to see which tests have been run, their historical esults, and which tests are specified but not yet implemented.

Jenkins uses a TestLink plugin that allows it to gather tests from TestLink, execute them, then pass the results back to TestLink so that reports can be generated and saved for future reference.

#### Docker

As the test framework becomes more complex, running tests locally without container management and deployment systems will become difficult. 
Forcing users to run and debug tests remotely through Jenkins is not a maintainable process. 

Docker provides a solution to this, with many advantages:

 * In order to run the test framework through Docker, the only dependency required is Docker itself. This vastly decreases the amount of setup required that a new / returning user must do in order to begin making changes to the test framework or tests themselves. 
 * Docker allows users to run the test framework exactly as it would be run on the main Jenkins server. Different configuration files are not required, and it removes the potential of seeing different behaviour locally compared to test executions through Jenkins.

This maximises reproducibility and minimises the potential for human error. Users do not have to worry about:

 * Making sure they have the correct version of each component running, and having to uninstall/reinstall components to switch versions.
 * Keeping repositories up to date.
 * Launching the correct programs with the correct arguments, in the correct order.
 * Ensuring no rogue processes are running or resources (such as ports) are already in use.

* Docker allows child containers to be run within a parent environment, so in the future we can implement an orchestrator that has the ability to launch multiple constrained devices, each in their own containers.

Docker also has the potential to host entire web services, meaning it supports the full simulation of an end-to-end solution.

#### Nose

The standard python unittest module is a great base for the Test Framework, but lacks standard and user-friendly solutions for:

* Loading test configuration files.
* Custom plugin support.
* Implementing parameterised tests.
* Executing subsets of test cases using test filters.
* Integrate with TestLink or another suitable Test Management System.

Nose builds upon unittest and solves the above issues, while still outputting test results to standard xUnit and TAP files that fully integrate into Jenkins and TestLink.

Nose supports custom plugins. The test framework takes advantage of this to load configuration files and record version numbers of each running component. Version numbers for each of the components are printed at the top of the test result output so that TestLink is able to mark changes to the system in its generated reports.

The test framework uses a modified Nose configuration loader plugin, allowing a YAML configuration file to be passed to the test launcher. This allows us to define our test environment - paths to libraries, executables and scripts, and topologies of components required for different test cases.
YAML was chosen as the file format as it supports configuration hierarchies that can easily be accessed from within the test framework itself. The default YAML file used by the test framework is configs/docker.yml.

Data-driven tests minimise duplicated code. This is useful when implementing tests on standard LWM2M objects, of which there are many. Nose provides a way for tests to run from data tables, where each table entry contains a test name and list of parameters for a single instance of the parameterised test.


### Contributing to the Test Framework

Ideally a detailed test plan would be developed by a QA test team, from a set of requirements identified by the designers of the system.

Before writing a python test, a test case should be created within a test suite of the Test Specification in the Test Management System (TestLink), 
detailing what is being tested by the test case (from one of the product requirements) and any steps required. Detailed instructions can be found in the [Getting Started Guide](doc/getting_started.md).

Once a test case exists in TestLink, running the test suite through Jenkins should identify that there is a new unimplemented test.

At this point, the python test should be written inside the tests/ directory of the Device Management Test Framework. 
Each test case should reside within its own class and follow both the conventions of the existing test cases and the [PEP 8](https://www.python.org/dev/peps/pep-0008) Style guide.

The name of the python test case must match the linking fields in TestLink, defined in [Getting Started Guide](doc/getting_started.md).

Follow the [Docker Instructions](http://gitlab.flowcloud.systems/FlowCloudTestTeam/DeviceManagementTests/tree/master/docker) to run your python test, 
or after making changes / bug fixes to any of the components tested by the QA Test Framework.

Logs will be saved within your DeviceManagementTests folder for each of the daemons, proxy connections with the helpers, and helpers.
The location of your DeviceManagementTests folder depends on how the test framework is executed.
Through docker, the default path is "/home/user/DeviceManagementTests". However, a popular method (for development only) is to volume mount your own DeviceManagementTests folder
so that you can make modifications directly without having to rebuild the test environment image. In that case, the logs will be saved to your volume mounted directory.

Follow the [Debugging Guide](doc/debugging.md) for more instructions on how to debug different components of the test framework.

### Test Framework Structure

#### Nose

**noserunner.py** is the entry point to the test framework. It starts nosetests, passing in the required plugins, and accepting command line
arguments to control test filters, verbosity, and test result output format.
Tests are run sequentially but in arbitrary order, completely independent of one another. No state is kept between test cases.

#### Helpers

The Test Framework contains four helpers (or proxies) that manage Awa Daemons. Each helper runs on a separate process from the Test Manager itself (nosetests):

* BootstrapServerTestHelper.py
* GWServerTestHelper.py
* GWClientTestHelper.py
* ConstrainedClientTestHelper.py

This allows the helpers to be run on separate machines or networks from the Test Manager. 

Each helper process hosts an XML-RPC server through which it is passed information from the test manager process. It can spawn or kill the associated Awa component on command, and communicate with it:

 * For the gateway client and server, this communication is through a ctypes wrapper to the Awa Gateway API.
 * For the constrained device, communication is through a real or virtual serial port.
 * The bootstrap server helper currently requires no method of communication with the bootstrap server.

The helpers are designed to communicate with both physical and virtual devices.

#### Awa Gateway API ctypes wrappers

AwaGatewayClientAPIWrapper.py and AwaGatewayServerAPIWrapper.py use the ctypes module to enable the gateway helpers to talk directly to the Awa Gateway API.
The wrapper functions are registered with the helper's XML-RPC server and allow the Test Manager to call Awa functions directly.
All Awa functionality is directly supported, except for Subscription/Observation notifications which cannot be directly passed back to the Test Manager.
The helpers will register a single callback for any subscription or observation that is set up, storing the notification changesets within a collection
which can be polled and cleared bt the Test Manager. (Note: this should be improved to support a queue of changesets to ensure notification values are not overwritten).

#### Plugins

Each .py file in the plugins/ directory is a separate nose plugin and follows the nose plugin format. A new plugin can be added to the framework simply by
adding a new .py file and creating an instance of the plugin inside the *addplugins* list of noserunner.py.

Current plugins include:

 * list_versions.py prints the version number for each of the components tested or used by the Test Framework (including the framework itself) into the top of the test output.
 * fix_test_config_encoding.py ensures all strings in loaded .yml configuration files are ASCII encoded (as opposed to unicode).
 * testconfig.py parses YAML test configuration files into the framework's test configuration class which can be easily accessed from areas of the test framework.

#### Configs
 
 Each configuration file has the following sections
 * paths
 * topologies
 * proxies
 * bootstrap-servers
 * gateway-servers
 * gateway-clients
 * constrained-clients
 * cloud-servers
 * cloud-tenants
 
 The **paths** section outlines the absolute paths to awa daemons and libraries, the virtual constrained device and tayga scripts.
 
 The **topologies** section defines individual, concrete test fixtures. Each test case will select a single topology to use, depending on its requirements.
 
 The **proxies** section defines connections to running helper processes that the topology manager can use to connect to, required for the currently running test case.
 
 The **bootstrap-servers**, **gateway-servers**, **gateway-clients**, and **constrained-clients** sections contain one to many daemon configurations for single instances of their type.
 A selected daemon configuration is read by a topology manager and allows connection to a helper through a proxy (connection details are defined in the daemon configuration) 
 and passes them required arguments to launch daemons with the selected configuration.
 
 The **cloud-servers** and **cloud-tenants** sections allow for user login and provisioning using a chosen tenant and FlowCloud server.

#### Docker

Docker replaces almost all of the manual setup and maintance required with scripts and docker image configuration files.
The test framework currently relies on three Docker images:

 * System Test Base (built from Dockerfile.system-test-base)
 * Test Environment (built from Dockerfile.test-env)
 * Contiki image    (built from Dockerfile.contiki)

The System Test Base image installs the toolchain and base packages required to build the test environment. 
It takes some time to build, however is only required to be built infrequently, when changed. This image is stored in the Docker registry for retrieval by any user.

The Test Environment sits on top of the System Test Base, and additionally contains only the components of the test environment, such as AwaLWM2M and the test framework itself.
It can be built reasonably quickly (1-5 minutes depending on the docker cache) and needs to be rebuilt whenever one of the components changes, or there is a requirement to
run one of the components of the test framework under a different version.

The Contiki image sits above the test environment and allows a contiki device to be isolated (as it would be on a physical constrained device).

The Test Environment and Contiki images are built with a single command: **jenkins.pre-iterate**.

**entry.sh** is used to run nose within a docker container, and is part of the commands defined in the [Docker Instructions](http://gitlab.flowcloud.systems/FlowCloudTestTeam/DeviceManagementTests/tree/master/docker).
Before starting nose, entry.sh executes **proxy-ctrl.sh**, which starts the helper processes that the Test Manager (nose) communicates with via XML-RPC proxies.
After the test run is completed, **proxy-ctrl.sh** will be run again to tear down the previously spawned helper processes.

**jenkins.iterate** is called by Jenkins when a test run is executed. Jenkins uses the TestLink plugin to pull a list of tests from the test suite 
defined in TestLink and saves them to a "nose.cfg" file which will be picked up by nose when it is launched. Note that this does not actually run the tests!

**jenkins.post-iterate** runs the tests specified in nose.cfg, copies the test results out of the container to the host, then removes the docker container.
This allows the Jenkins TestLink plugin to pick up the results and send them to TestLink, where a test report can be generated and saved. 

#### Framework

##### TestConfig

The TestConfig singleton stores data read from a .yml configuration file and can allows access through a nested dictionary.

`value = TestConfig.config["section"]["child_section"]["key"]`

Test configuration usage should be limited to certain areas of the test framework, and not be used by individual test cases.

##### TopologyManager

A TopologyManager is instantiated with the name of a single topology, matching one of the topologies declared in the test configuration file that nose has loaded 
for the current test run. From this single name, it is able to pick out everything it requires from the test configuration to launch required bootstrap servers,
gateway servers, gateway clients and constrained clients through proxy connections to helpers. Each of the created helper connections are accessible to the test case
that created that topology, by using self.topology.<helperType>[instanceNumber].

eg. `self.topology.constrainedClients[0].createResource(3,0,2)`

##### XML-RPC Proxy Components

The four XML-RPC proxy classes provide the Test Manager with a connection to the helpers:

* BootstrapServerXmlRpc.py
* GWClientXmlRpc.py
* GWServerXmlRpc.py
* ConstrainedClientXmlRpc.py

Each XML-RPC proxy class implements an interface containing the minimum supported functions provided by their associated component. Therefore the XML-RPC mechanism is encapsulated and could be replaced with an alternative mechanism.

GWClientXmlRpc and GWServerXmlRpc provide an additional level of abstraction, hiding the fact that ctypes is used by the helper to communicate with the Awa API.
 This removes the "C Style" requirement of having to call functions that only differ by data type, and provides exceptions on unexpected return codes from the Awa API. This allows the tests to be implemented in a pythonic style.

##### Operation Assertions

To reduce duplication, this submodule contains functions that will be called by table entries in the parameterised test cases.
These functions assert success or a certain type of failure on certain operations, and are designed to be able to be used together in order to confirm test results
(For example, use a SetOperationAssertion to assert a Set operation succeeded, then a GetOperationAssertion to verify the value was set).

##### Tests

This test framework is designed to focus on System-Level / End-To-End testing rather than focusing on testing individual component functionality 
(which should be handled by each component separately). 

Test cases are either parameterised (invoking the same operations on a table of resources from standard objects), or testing a single concept or feature
(For example, constrained device provisioning). 

Each test class inherits from unittest.TestCase, and uses models (such as a topology manager) to communicate with individual daemons through helpers, 
without requiring knowledge of launching daemons, whether the devices they are talking to are real or simulated, etc.

Each test is independent of another. In most cases, a test case will override the unittest "setUp" functions in order to:

* Create a user.
* Select a topology and launch (or connect to) the required daemons.
* Provision devices.

Each test function uses the nose *addCleanup* function to safely release and destroy any allocated resources at the end of each test. 

##### parameterised tests

The test framework supports data-driven test cases using parameterised tests to minimise duplication. 
Each table entry in each parameterised test class is converted into a seperate test case at runtime using python templates. 
Each test case will run basic "Operation Assertions" (described above, such as Define / Get / Set etc.) on a single resource path. 
The intent is to efficiently reuse the same test operations on a large set of resources.
