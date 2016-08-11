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

from framework import test_config
from framework.static_client import StaticClient
from xml_rpc_client import XmlRpcClient

class ConstrainedClientXmlRpc(StaticClient, XmlRpcClient):

    # Establish and maintain XMLRPC connection with BootstrapServerHelper.
    def __init__(self, constrainedClientConfig):
        super(ConstrainedClientXmlRpc, self).__init__(test_config.config["proxies"][constrainedClientConfig["proxy"]])

        self._constrainedClientConfig = constrainedClientConfig

        simulated = constrainedClientConfig.get("simulated", False) # FIXME - change to "ConstrainedDeviceType" and retrieve from TestConfig

        self._xmlrpcSession.setClientID(constrainedClientConfig["client-id"])
        self._xmlrpcSession.setBootstrapURI(self._constrainedClientConfig['bootstrap-uri'])
        self._xmlrpcSession.setPort(self._constrainedClientConfig['port'])
        if simulated:
            daemonPath = test_config.config['paths']['constrained-client']
            taygaConfig = self._constrainedClientConfig.get("tayga", None)
            taygaConfig['tayga-scripts'] = test_config.config['paths']['tayga-scripts']

            self._xmlrpcSession.initialiseConstrainedDeviceSimulated(daemonPath, taygaConfig)
        else:
            serialPort = self._constrainedClientConfig['serial-port']
            self._xmlrpcSession.initialiseConstrainedDeviceSerial(serialPort)

    def __del__(self):
        self._xmlrpcSession.resetConstrainedDevice()
        del self._xmlrpcSession

    def getClientID(self):
        return self._xmlrpcSession.getClientID()

    def executeScript(self, args):
        return self._xmlrpcSession.executeScript(pickle.dumps(args))

    def pickleExecuteHardReset(self):
        return self._xmlrpcSession.pickleExecuteHardReset()

    def pickleStopClicker(self):
        return self._xmlrpcSession.pickleStopClicker()

    def pickleRunClicker(self):
        return self._xmlrpcSession.pickleRunClicker()

################################################################################

    def factoryBootstrap(self, serverURI, lifeTime=60):
        self._xmlrpcSession.factoryBootstrap(serverURI, lifeTime)

    def defineObject(self, objectID, minInstances, maxInstances):
        return self._xmlrpcSession.defineObject(objectID, minInstances, maxInstances)

    def defineResource(self, objectID, resourceID, resourceName, resourceType, minResources, maxResources, operations, resourceSizeInBytes):
        return self._xmlrpcSession.defineResource(objectID, resourceID, resourceName, resourceType, minResources, maxResources, operations, resourceSizeInBytes)

    def start(self):
        self._xmlrpcSession.start()

    def createObjectInstance(self, objectID, instanceID):
        return self._xmlrpcSession.createObjectInstance(objectID, instanceID)

    def createResource(self, objectID, instanceID, resourceID):
        return self._xmlrpcSession.createResource(objectID, instanceID, resourceID)

    def version(self):
        return self._xmlrpcSession.version()

    def setResourceValue(self, path, value):
        return self._xmlrpcSession.setResourceValue(path, pickle.dumps(value))

    def getResourceValue(self, path, resourceType=str, checkExistsOnly=False):
        return pickle.loads(self._xmlrpcSession.getResourceValue(path, pickle.dumps(resourceType), checkExistsOnly))

    def delete(self):
        return self._xmlrpcSession.delete()

    def echo(self, text):
        return self._xmlrpcSession.echo(pickle.dumps(text))

    def softwareReset(self):
        self._xmlrpcSession.softwareReset()

    def waitForResetToComplete(self):
        self._xmlrpcSession.waitForResetToComplete()

    def expect(self, output, timeout=5):
        return self._xmlrpcSession.expect(pickle.dumps(output), timeout)
