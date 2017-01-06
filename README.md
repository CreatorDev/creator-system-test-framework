![Imagination Technologies Limited logo](doc/images/img.png)

# Creator System Test Framework

## Credits

We would like to thank all of our current [contributors](CONTRIBUTORS).

We would also like to acknowledge and thank the authors of the following projects.

- [Docker](http://www.docker.com)
- [TestLink](https://sourceforge.net/projects/testlink)
- [Nose](http://nose.readthedocs.io)
- [AwaLWM2M](https://github.com/FlowM2M/AwaLWM2M)

## Prerequisites

### Docker - Recommended

Follow the [Docker Instructions](docker/README.md) to install docker and run the
tests within a docker container.

### Without Docker - DEPRECATED

Follow the [Running the Test Framework Without Docker](doc/without_docker.md) instructions
to manually start helper processes and launch nosetests. Note that this requires extra
software installation and is only recommended for debugging purposes.

## Getting started

At this point you should be able to run the test framework on your local machine.

For an introduction to the layout and structure of the Test Framework, please
read the [Test Framework Introduction](doc/introduction.md).

To add additional test cases to the test framework, the [Getting Started Guide](doc/getting_started.md)
gives an overview of linking python test cases with the test plan residing within TestLink.

## Additional information

- [Running the test framework with real hardware](doc/hardware/README.md)
- [Test Filters](doc/test_filters.md)
- [Debugging](doc/debugging.md)
