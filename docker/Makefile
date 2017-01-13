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

.PHONY: contiki-tinydtls
contiki-tinydtls:
	cd $(DOCKER_DIR)/../.. ; docker build -t contiki-tinydtls --build-arg TINYDTLS=1 -f $(DOCKER_DIR)/Dockerfile.contiki .

# This target can be useful when you debugging things and need a faster build time.
.PHONY: contiki-tinydtls-volume
contiki-tinydtls-volume:
	@echo run the following:
	@echo
	@echo     make -C lwm2m-contiki/lwm2m-client-contiki-test/ TARGET=minimal-net TINYDTLS=1
	@echo
	cd $(DOCKER_DIR)/../.. ; docker run --rm -ti --entrypoint bash -v $$(pwd)/creator-system-test-framework:/home/user/creator-system-test-framework --user user test-env
