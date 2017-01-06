DOCKER_DIR:=$(realpath $(shell pwd)/$(firstword $(dir $(MAKEFILE_LIST))))

.PHONY: help
help:
	@echo For help running this, please see the instructions at https://github.com/CreatorDev/creator-system-test-framework/tree/master/docker

.PHONY: all
all: system-test-base test-env contiki

.PHONY: system-test-base
system-test-base:
	cd $(DOCKER_DIR); docker build -t creatordev/system-test-base -f Dockerfile.system-test-base .

.PHONY: test-env
test-env:
	cd $(DOCKER_DIR)/../.. ; $(DOCKER_DIR)/jenkins.pre-iterate

.PHONY: contiki
contiki:
	cd $(DOCKER_DIR)/../.. ; docker build -t contiki -f $(DOCKER_DIR)/Dockerfile.contiki .
