#/************************************************************************************************************************
# Copyright (c) 2016, Imagination Technologies Limited and/or its affiliated group companies.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#     1. Redistributions of source code must retain the above copyright notice, this list of conditions and the
#        following disclaimer.
#     2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
#        following disclaimer in the documentation and/or other materials provided with the distribution.
#     3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
#        products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#************************************************************************************************************************/

import abc
import uuid
import sys

from framework.client import Client, DeviceLoginDetails
from framework import test_objects
import time

class StaticClientError(Exception):
    pass
class ExpectTimeoutException(StaticClientError):
    pass

# Abstraction for Real and Simulated Static / Constrained Device clients.
class StaticClient(Client):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def factoryBootstrap(self, serverURI, lifeTime=60):
        return

    @abc.abstractmethod
    def defineObject(self, objectID, minInstances, maxInstances):
        return

    @abc.abstractmethod
    def defineResource(self, objectID, resourceID, resourceName, resourceType, minInstances, maxInstances, operations, resourceSizeInBytes):
        return

    @abc.abstractmethod
    def createResource(self, objectID, instanceID, resourceID):
        return

    @abc.abstractmethod
    def start(self):
        return

    @abc.abstractmethod
    def softwareReset(self):
        return

    @abc.abstractmethod
    def waitForResetToComplete(self):
        return

    @abc.abstractmethod
    def expect(self, output, timeout=5):
        return

    @abc.abstractmethod
    def echo(self, text):
        return

    @abc.abstractmethod
    def createObjectInstance(self, objectID, instanceID):
        return

    @abc.abstractmethod
    def version(self):
        return

    @abc.abstractmethod
    def setResourceValue(self, path, value):
        return

    @abc.abstractmethod
    def getResourceValue(self, path, resourceType=str, checkExistsOnly=False):
        return

    @abc.abstractmethod
    def delete(self):
        return

    def getDeviceLoginDetails(self):

        deviceType = self.getResourceValue("/20000/0/2")
        deviceName = self.getResourceValue("/20000/0/3")
        fcapCode = self.getResourceValue("/20000/0/5")
        serialNumber = self.getResourceValue("/3/0/2")
        softwareVersion = self.getResourceValue("/3/0/19")
        deviceID = self.getResourceValue("/20000/0/0")  # Opaque

        try:
            deviceIDAsUUID = str(uuid.UUID(bytes_le=deviceID[:16]))
        except ValueError:
            print("Failed to convert deviceID bytes to UUID: length %d data: %s", len(deviceID), deviceID)
            raise

        return DeviceLoginDetails(deviceType, deviceName, fcapCode, serialNumber, softwareVersion, deviceIDAsUUID)

    def Define(self, objectDefinition, resourceDefinitions):
        self.defineObject(objectDefinition.objectID, objectDefinition.minimumInstances, objectDefinition.maximumInstances)
        for resourceDefinition in resourceDefinitions:
            self.defineResource(objectDefinition.objectID, resourceDefinition.resourceID, resourceDefinition.resourceName, int(resourceDefinition.resourceType), 
                                resourceDefinition.minimumInstances, resourceDefinition.maximumInstances, int(resourceDefinition.supportedOperations), resourceDefinition.resourceSizeInBytes)

    def DefineTestObjects(self):
        self.Define(test_objects.objectDefinition1000, test_objects.constrainedResourceDefinitions)
        #self.Define(test_objects.objectDefinition1001, test_objects.constrainedResourceDefinitions)
        #self.Define(test_objects.objectDefinition1002, test_objects.constrainedResourceDefinitions)
        #self.Define(test_objects.objectDefinition1003, test_objects.constrainedResourceDefinitions)

    def CreateInstancesOfTestObjects(self):
        self.createObjectInstance(test_objects.objectDefinition1000.objectID, 0)
        #self.createObjectInstance(test_objects.objectDefinition1001.objectID, 0)
        #self.createObjectInstance(test_objects.objectDefinition1002.objectID, 0)
        #self.createObjectInstance(test_objects.objectDefinition1003.objectID, 0)

    def WaitForResources(self, resources, attempts=60, wait=0.5):
        sys.stdout.write("Wait for resources to be populated: %s" % (resources,))
        exists = []
        for _ in xrange(attempts):

            #print("Hash iterations: %d" % (self.getResourceValue("/20000/0/8", int), ))
            #print("Hash iterations exists: %s" % (str(self.getResourceValue("/20000/0/8", checkExistsOnly=True)), ))

            populated = True
            for path in resources:
                #print("Path: %s" % (path, ))
                try:
                    if self.getResourceValue(path, checkExistsOnly=True) == False:
                        populated = False
                        #print("Resource does not exist yet: %s" % (path, ))
                        break
                    else:
                        if path not in exists:
                            print("Resource exists: %s" % (path, ))
                            exists.append(path)
                except ExpectTimeoutException as e:
                    print("Expect timed out: %s %s" % (path, str(e)))
                    populated = False
                    break
            if populated:
                sys.stdout.write("OK\n")
                break

            time.sleep(wait)
            sys.stdout.write(".")
            sys.stdout.flush()

        else:
            sys.stdout.write("TIMEOUT\n")
            raise StaticClientError("Timeout waiting for constrained device to receive resources")
