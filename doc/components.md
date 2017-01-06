![Imagination Technologies Limited logo](images/img.png)

# Creator System Test Framework

## Test Framework Components

### TestLink

TestLink is a web-based test management system that allows team members to collaborate
in real-time on a the test plan, and track results as they occur. It is an open-source
solution that fills the gap between the test plan and the test framework, allowing
users to execute tests and view test reports that match the test plan they have written,
all from a single application.

TestLink allows anyone to see exactly what is being tested at a high level. Without a
link between test cases and a test plan, there is no way for a user to understand what
is and isn't being tested without detailed knowledge of the test system . Without a test
management solution, any changes to the test cases (including failing/passing, skipping
or adding/removing tests) would not be reflected in the test plan. It is important to be
able to see which tests have been run, their historical esults, and which tests are
specified but not yet implemented.

Jenkins uses a TestLink plugin that allows it to gather tests from TestLink, execute them,
then pass the results back to TestLink so that reports can be generated and saved for
future reference.

### Docker

As the test framework becomes more complex, running tests locally without container
management and deployment systems will become difficult. Forcing users to run and debug
tests remotely through Jenkins is not a maintainable process.

Docker provides a solution to this, with many advantages:

* In order to run the test framework through Docker, the only dependency required is
  Docker itself. This vastly decreases the amount of setup required that a new / returning
  user must do in order to begin making changes to the test framework or tests themselves.
* Docker allows users to run the test framework exactly as it would be run on the main
  Jenkins server. Different configuration files are not required, and it removes the
  potential of seeing different behaviour locally compared to test executions through Jenkins.

This maximises reproducibility and minimises the potential for human error. Users do not
have to worry about:

* Making sure they have the correct version of each component running, and having to
  uninstall/reinstall components to switch versions.
* Keeping repositories up to date.
* Launching the correct programs with the correct arguments, in the correct order.

* Ensuring no rogue processes are running or resources (such as ports) are already in use.
  * Docker allows child containers to be run within a parent environment, so in the
    future we can implement an orchestrator that has the ability to launch multiple
    constrained devices, each in their own containers.

Docker also has the potential to host entire web services, meaning it supports the full
simulation of an end-to-end solution.

### Nose

The standard python unittest module is a great base for the Test Framework, but lacks
standard and user-friendly solutions for:

* Loading test configuration files.
* Custom plugin support.
* Implementing parameterised tests.
* Executing subsets of test cases using test filters.
* Integrate with TestLink or another suitable Test Management System.

Nose builds upon unittest and solves the above issues, while still outputting test results
to standard xUnit and TAP files that fully integrate into Jenkins and TestLink.

Nose supports custom plugins. The test framework takes advantage of this to load configuration
files and record version numbers of each running component. Version numbers for each of the
components are printed at the top of the test result output so that TestLink is able to mark
changes to the system in its generated reports.

The test framework uses a modified Nose configuration loader plugin, allowing a YAML configuration
file to be passed to the test launcher. This allows us to define our test environment - paths
to libraries, executables and scripts, and topologies of components required for different
test cases. YAML was chosen as the file format as it supports configuration hierarchies that
can easily be accessed from within the test framework itself. The default YAML file used
by the test framework is configs/docker_simulated.yml.

Data-driven tests minimise duplicated code. This is useful when implementing tests on standard
LWM2M objects, of which there are many. Nose provides a way for tests to run from data tables,
where each table entry contains a test name and list of parameters for a single instance of
the parameterised test.
