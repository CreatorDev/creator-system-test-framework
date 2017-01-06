# Docker containers for End-to-End Test Framework

The test framework can be run inside a self contained environment called a docker container that allows anyone with
docker to run the test framework.

## Beginners Guide to Docker

Run through the tutorial at https://docs.docker.com/linux/, however creating a docker hub account is not required.

Docker runs as a daemon which requires root access to connect to it. If you are seeing the message below, it could be due
to the user running the docker command not having sufficient privileges to connect to the Docker daemon.

    docker: Cannot connect to the Docker daemon. Is the docker daemon running on this host?.

In order to give the user sufficient privileges (without having to do sudo) add the user to the docker group - instructions
are here https://docs.docker.com/engine/installation/linux/ubuntulinux/#create-a-docker-group

Upon completing the tutorial above you should have a magic talking whale, and understand the basics of docker.

     ________________________________________
    / Committees have become so important    \
    | nowadays that subcommittees have to be |
    \ appointed to do the work.              /
     ----------------------------------------
        \
         \
          \
                        ##        .
                  ## ## ##       ==
               ## ## ## ##      ===
           /""""""""""""""""___/ ===
      ~~~ {~~ ~~~~ ~~~ ~~~~ ~~ ~ /  ===- ~~~
           \______ o          __/
            \    \        __/
             \____\______/

## Running the Test Framework Docker Container

There are two stages to running the Test Framework:

1. Creating a Docker Image that builds a version of AwaLWM2M and the Python Test Framework.
1. Running a Docker Container that runs the Image built in the previous step.

### Building the Test Framework Docker container

Create a directory and checkout the required repositories for building the Docker image into that directory. This
directory layout must be followed precisely:

    $ mkdir qa && cd qa
    $ git clone --recursive https://github.com/CreatorDev/creator-system-test-framework.git

This retrieves the Python Test Framework, AwaLWM2M library and Contiki AwaLWM2M implementation.

Build the Docker images:

    $ cd creator-system-test-framework/docker/
    $ make system-test-base
    $ make test-env

**WARNING:** All repositories **MUST** be in a clean state before running the above script.
This can be done by executing make clean in any of the modified repositories.

This builds a `test-env` Docker image that has a version of the AwaLWM2M library (gateway client, server and bootstrap server),
Contiki simulated AwaLWM2M client and the Python Test Framework.

### Running a Docker Container for all the tests

Run all the tests in a Docker container based on the image created in the previous step:

    $ docker run --rm -it --cap-add=NET_ADMIN --device=/dev/net/tun --privileged --workdir /home/user/creator-system-test-framework --name test-env-container test-env docker/entry.sh -svv --tc-file configs/docker_simulated.yml

### Running a Docker Container with Bash

A docker container can run the bash shell instead of the Python Test Framework:

    $ docker run --rm -it --cap-add=NET_ADMIN --device=/dev/net/tun --privileged --name test-env-container test-env

### Running a Docker Container with an external version of the Python Test Framework

The Docker image contains the Python Test Framework, however to develop and see changes to the test framework requires
rebuilding this image. This is where mounting an external volume with the Python Test Framework can be used instead of
rebuilding the image.

Volume mounting a directory makes it appear in the Docker container, so this allows the container to use a directory that
is not destroyed along with the container. This is useful when changes need to persist between Docker containers, such as
when developing the test framework.

    $ docker run --rm -it --cap-add=NET_ADMIN --device=/dev/net/tun --privileged -v $(pwd)/creator-system-test-framework:/home/user/creator-system-test-framework --name test-env-container test-env

An issue with volume mounting is that any changes to the directory that was mounted will be owned by root, so a cleanup
is required. For example, this Docker command echos text to file in creator-system-test-framework, which will then be
owned by root. Therefore another command is required to sanitize the creator-system-test-framework directory from the
point of view of the host:

    $ docker run --rm -it --cap-add=NET_ADMIN --device=/dev/net/tun --privileged -v $(pwd)/creator-system-test-framework:/home/user/creator-system-test-framework --name test-env-container test-env bash -c 'echo test > test.txt'
    $ ls -alh creator-system-test-framework/test.txt
      -rw-r--r-- 1 root root 5 Apr 20 12:14 creator-system-test-framework/test.txt
    $ echo $USER | xargs -I {} sudo chown {}:{} -R .
    $ ls -alh creator-system-test-framework/test.txt
      -rw-r--r-- 1 user user 5 Apr 20 12:14 creator-system-test-framework/test.txt

### Running all the tests with an external version of the Python Test Framework

    $ docker run -it --cap-add=NET_ADMIN --device=/dev/net/tun --privileged -v $(pwd)/creator-system-test-framework:/home/user/creator-system-test-framework --name test-env-container test-env docker/entry.sh -svv --tc-file configs/docker_simulated.yml

### Running a single test using docker: tests/test_filename.py:TestClass.test_name

    $ docker run -it --cap-add=NET_ADMIN --device=/dev/net/tun --privileged -v $(pwd)/creator-system-test-framework:/home/user/creator-system-test-framework --name test-env-container test-env docker/entry.sh -svv --tc-file configs/docker_simulated.yml tests/test_GWServerCustomObjectTestCases.py:CustomObjectTestCases.test_DaemonReadStringArrayResourceDefaultValue

### Running tests with a filter using docker (using the nose attributes plugin)

    $ docker run -it --cap-add=NET_ADMIN --device=/dev/net/tun --privileged -v $(pwd)/creator-system-test-framework:/home/user/creator-system-test-framework --name test-env-container test-env docker/entry.sh -svv --tc-file configs/docker_simulated.yml -A 'cloud'

## Executing another process in a running docker container

    docker exec test-env-container echo "Hello from container!"

## Setting a breakpoint within a test

    import pdb; pdb.set_trace()

## Debug a failed docker build

Find the last successful commit of a layer, and use it here:

    $ docker run --rm -it 5bd5124e97f0 bash -il
