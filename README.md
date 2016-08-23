![Imagination Technologies Limited logo](doc/images/img.png)

----

## Creator System Test Framework

----

### License

 Copyright (c) 2016, Imagination Technologies Limited and/or its affiliated group companies.
 All rights reserved.

 Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
 following conditions are met:
     1. Redistributions of source code must retain the above copyright notice, this list of conditions and the
        following disclaimer.
     2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
        following disclaimer in the documentation and/or other materials provided with the distribution.
     3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

 THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

----

### Credits

We would like to thank all of our current [contributors](CONTRIBUTORS).

We would also like to acknowledge and thank the authors of the following projects.

* Docker : http://www.docker.com
* TestLink : https://sourceforge.net/projects/testlink
* Nose : http://nose.readthedocs.io
* AwaLWM2M : https://github.com/FlowM2M/AwaLWM2M


### Prerequisites

#### Docker - Recommended

 Follow the [Docker Instructions](https://github.com/CreatorDev/creator-system-test-framework/tree/master/docker) to install docker and run the tests within a docker container.

#### Without Docker - DEPRECATED

 Follow the [Running the Test Framework Without Docker](doc/without_docker.md) instructions to manually start helper processes and launch nosetests. Note that this requires extra software installation and is only recommended for debugging purposes.

### Getting started

 At this point you should be able to run the test framework on your local machine. 
 
 For an introduction to the layout and structure of the Test Framework, please read the [Test Framework Introduction](doc/introduction.md).
 
 To add additional test cases to the test framework, the [Getting Started Guide](doc/getting_started.md) gives an overview of linking python test cases with the test plan residing within TestLink.

### Additional information:
 
 [Running the test framework with real hardware](doc/hardware/README.md)
 
 [Test Filters](doc/test_filters.md)

 [Debugging](doc/debugging.md)
