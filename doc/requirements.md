![Imagination Technologies Limited logo](images/img.png)

# Creator System Test Framework

## Test Framework Requirements

The Creator System Test Framework was developed to satisfy the following requirements, in order to confidently assure
expected functionality:

* Written tests must be linked to an existing test plan, ensuring there are no discrepancies between what was intended
  to be tested and what actually is.
* A way to quickly see what is being tested at a high level, without any knowledge of the test system, digging into
  written test cases or relying upon the names of those passing/failing test cases.
* Keep track of version numbers for each component so that it is possible to quickly identify which change to which
  component caused a previously passing test to fail.
* Be able to quickly switch component versions and re-run the test system.
* Easy to setup and run the tests locally exactly as they would be run on a Jenkins CI server.
* Be able to write data-driven / parameterised tests, load configuration files and execute subsets of tests in a
  standardised way.
* Integrate the test system with third party test tools, including Jenkins.
* Make use of existing components rather than writing our own.
* Ability to run multiple test suites / test cases in parallel, independently of each other.
* Be flexible and extensible, accommodating for the changing nature of our Device Management solution and tests with
  greater requirements that may need to be run in the future.
