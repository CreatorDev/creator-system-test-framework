#!/usr/bin/env python

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

import cPickle as pickle

import helper
from framework.constrained_client import ConstrainedClientSimulated, ConstrainedClientSerial
from framework.static_client import StaticClient
import subprocess

class ConstrainedClientTestHelper(StaticClient, helper.Helper):
    _constrainedDevice = None

    def __init__(self):
        super(ConstrainedClientTestHelper, self).__init__()

    def setClientID(self, clientID):
        self._clientID = clientID
    
    def getClientID(self):
        return self._clientID

    def setPort(self, port):
        self._port = port

    def setBootstrapURI(self, bootstrapURI):
        self._bootstrapURI = bootstrapURI

    def initialiseConstrainedDeviceSimulated(self, daemonPath, taygaConfig):
        self._simulated = True
        self._constrainedDevice = ConstrainedClientSimulated(self._clientID, self._bootstrapURI, self._port, daemonPath, taygaConfig, debug=False, verbose=True)

    def initialiseConstrainedDeviceSerial(self, serialPort):
        self._simulated = False
        self._constrainedDevice = ConstrainedClientSerial(self._clientID, self._bootstrapURI, self._port, serialPort, debug=False, verbose=False)

    def resetConstrainedDevice(self):
        try:
            if self._constrainedDevice is not None:
                if self._simulated == True:
                    self._constrainedDevice.close()
                else:
                    self.pickleExecuteHardReset()
        except:
            print("ERROR: CONSTRAINED DEVICE IS UNRESPONSIVE")
            import traceback, sys;
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                              limit=2, file=sys.stdout)
            raise

    def executeScript(self, args):
        args = pickle.loads(args)
        args.insert(0, "bash" if self._simulated else "ash")
        return subprocess.Popen(args, stdout=subprocess.PIPE).communicate()[0]
    
    def pickleExecuteHardReset(self):
        print("Executing hard reset...")
        return subprocess.Popen(("pctrl", "RESTORE", ), stdout=subprocess.PIPE).communicate()[0]
    
    def pickleStopClicker(self): 
        return subprocess.Popen(("pctrl", "STOP", ), stdout=subprocess.PIPE).communicate()[0]
    
    def pickleRunClicker(self): 
        return subprocess.Popen(("pctrl", "RUN", ), stdout=subprocess.PIPE).communicate()[0]

######################################################################################

    def factoryBootstrap(self, serverURI, lifeTime):
        self._constrainedDevice.factoryBootstrap(serverURI, lifeTime)

    def defineObject(self, objectID, minResources, maxResources):
        return self._constrainedDevice.defineObject(objectID, minResources, maxResources)

    def defineResource(self, objectID, resourceID, resourceName, resourceType, minResources, maxResources, operations, resourceSizeInBytes):
        return self._constrainedDevice.defineResource(objectID, resourceID, resourceName, resourceType, minResources, maxResources, operations, resourceSizeInBytes)

    def start(self):
        self._constrainedDevice.start()

    def createObjectInstance(self, objectID, instanceID):
        return self._constrainedDevice.createObjectInstance(objectID, instanceID)

    def createResource(self, objectID, instanceID, resourceID):
        return self._constrainedDevice.createResource(objectID, instanceID, resourceID)

    def version(self):
        return self._constrainedDevice.version()

    def setResourceValue(self, path, value):
        return self._constrainedDevice.setResourceValue(path, pickle.loads(value))

    def getResourceValue(self, path, resourceType, checkExistsOnly=False):
        return pickle.dumps(self._constrainedDevice.getResourceValue(path, pickle.loads(resourceType), checkExistsOnly))

    def delete(self):
        return self._constrainedDevice.delete()

    def echo(self, text):
        return self._constrainedDevice.echo(pickle.loads(text))

    def softwareReset(self):
        self._constrainedDevice.softwareReset()

    def waitForResetToComplete(self):
        self._constrainedDevice.waitForResetToComplete()

    def expect(self, output, timeout=5):
        return self._constrainedDevice.expect(pickle.loads(output), timeout)

def main():
    helper.StartHelper(ConstrainedClientTestHelper())

if __name__ == "__main__":
    main()
