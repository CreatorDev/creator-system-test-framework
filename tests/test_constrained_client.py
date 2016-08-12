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

import unittest
import time
import sys

import framework.provisioning as provisioning
from nose.plugins.attrib import attr
from framework.test_cases.gateway_server_and_constrained_client_test_case import GWServerAndConstrainedClientTestCase
from framework.test_cases.gateway_server_and_constrained_client_test_case import GWServerAndProvisionedConstrainedClientTestCase
from framework.awa_enums import AwaResourceType
from framework import test_objects
from framework.test_cases.constrained_client_test_case import ProvisionedConstrainedClientTestCase, ConstrainedClientTestCase, ConstrainedClientWithCustomObjectsTestCase
from framework.topology_manager import TopologyManager

@attr("constrained_client")
class SerialTests(ConstrainedClientTestCase):
    def test_Echo(self):
        inputString = "\"asdfgh32804325jnkfdsanSA====!!!!!!'#$##'@^4^%2\""
        output = self.topology.constrainedClients[0].echo(inputString)
        self.assertEqual(inputString, output)

    def test_EchoMaximum(self):
        inputString = "a"*118
        output = self.topology.constrainedClients[0].echo(inputString)
        self.assertEqual(inputString, output)

    @unittest.skip("Unresponsive")
    def test_EchoOverMaximum(self):
        inputString = "a"*120
        output = self.topology.constrainedClients[0].echo(inputString)
        self.assertEqual(inputString, output)

    def test_ReadVersion(self):
        self.topology.constrainedClients[0].start()
        version = self.topology.constrainedClients[0].version()
        print ("version {0}".format(version))
        self.assertRegexpMatches(version, "[0-9]+\.[0-9]+\.[0-9]+")

    def test_Reset(self):
        self.topology.constrainedClients[0].softwareReset()
        self.topology.constrainedClients[0].waitForResetToComplete()

@attr("constrained_client")
class ConstrainedDeviceSetGet(ConstrainedClientWithCustomObjectsTestCase):

    def test_SetGetDeviceObjectResources(self):
        self.assertEqual("0", self.topology.constrainedClients[0].setResourceValue("/3/0/0", "hello"))
        self.assertEqual("hello", self.topology.constrainedClients[0].getResourceValue("/3/0/0"))

        self.assertEqual("0", self.topology.constrainedClients[0].setResourceValue("/3/0/13", 1024))
        self.assertEqual(1024, self.topology.constrainedClients[0].getResourceValue("/3/0/13", int))

    # TODO all resource types
    def test_SetGetCustomStringResource(self):
        self.assertEqual("0", self.topology.constrainedClients[0].setResourceValue("/1000/0/202", "test"))
        self.assertEqual("test", self.topology.constrainedClients[0].getResourceValue("/1000/0/202"))

    def test_SetGetCustomIntegerResource(self):
        self.assertEqual("0", self.topology.constrainedClients[0].setResourceValue("/1000/0/203", 12345))
        self.assertEqual(12345, self.topology.constrainedClients[0].getResourceValue("/1000/0/203", int))

    def test_SetGetCustomOpaqueResource(self):
        self.assertEqual("0", self.topology.constrainedClients[0].setResourceValue("/1000/0/206", str(bytearray([65, 0, 66, ]))))
        self.assertEqual(str(bytearray([65, 0, 66, ])), self.topology.constrainedClients[0].getResourceValue("/1000/0/206"))

@attr("constrained_client", "gateway_server", "bootstrap_server")
class GatewayServerSetGet(GWServerAndConstrainedClientTestCase):

    def test_SetGetDeviceObjectResources(self):
        self.assertEqual("0", self.topology.constrainedClients[0].createResource(3, 0, 0))
        self.assertEqual("0", self.topology.constrainedClients[0].setResourceValue("/3/0/0", "hello"))
        self.assertEqual("hello", self.topology.constrainedClients[0].getResourceValue("/3/0/0"))
        self.assertEqual("hello", self.topology.gatewayServers[0].ReadSingleResource(self.topology.constrainedClients[0].getClientID(), "/3/0/0", AwaResourceType.String))

    @unittest.skip("TODO")
    def test_SetGetCustomOpaqueResource(self):
        # TODO
        #define test objects on CD
        #self.topology.gatewayServers[0].Define(test_objects.objectDefinition1000, test_objects.constrainedResourceDefinitions)
        pass

        '''gatewayServer = self.topology.gatewayServers[0]
        gatewayServer.WaitForClientObject(self.topology.constrainedClients[0].getClientID(), "/1000/0")
        readOperation = gatewayServer.CreateReadOperation(gatewayServer._session, self.topology.constrainedClients[0].getClientID(), "/1000/0/206")


        value = gatewayServer.GetResourceValueFromReadOperation(readOperation, self.topology.constrainedClients[0].getClientID(), "/1000/0/206", AwaResourceType.Opaque)
        #pathResult = gatewayServer.GetPathResultFromReadOperation(readOperation, self.topology.constrainedClients[0].getClientID(), "/1000/0/206")
        #error = gatewayServer.GetPathResultError(pathResult)
        gatewayServer.FreeReadOperation(readOperation)
        print("Value on server: %s" % (str(value), ))'''
        '''while True:
            print("Sleeping...")
            import time; time.sleep(0.5)'''

@attr("constrained_client", "bootstrap_server")
class ConnectionTests(unittest.TestCase):

    def test_CanBootstrap(self):
        # instances should be added to constrained device's server object to be considered "bootstrapped"
        # /0/0: Bootstrap server (Will already exist because the client needs to know where to connect)
        # /0/1: Cloud server
        # /0/2: Gateway server
        self.topology = TopologyManager.fromConfigFile("constrained-device-without-gateway-client-uat-hobbyist")
        def delTopology(): del self.topology
        self.addCleanup(delTopology)

        self.topology.constrainedClients[0].start()
        self.topology.constrainedClients[0].WaitForResources(["/0/0/0","/0/1/0", "/0/2/0", ])

    def test_CanRegisterWithGatewayServer(self):
        self.topology = TopologyManager.fromConfigFile("constrained-device-without-gateway-client-uat-hobbyist")
        def delTopology(): del self.topology
        self.addCleanup(delTopology)

        self.topology.constrainedClients[0].start()

        self.topology.constrainedClients[0].WaitForResources(["/0/0/0","/0/1/0", "/0/2/0", ])  # wait for bootstrapping to complete
        self.topology.gatewayServers[0].WaitForClient(self.topology.constrainedClients[0].getClientID())

    def test_TaygaInterface(self):
        self.topology = TopologyManager.fromConfigFile("constrained-device-only")
        def delTopology(): del self.topology
        self.addCleanup(delTopology)

        output = self.topology.constrainedClients[0].executeScript(["hardware/check-tayga", ])
        self.assertEqual("success", output.strip())

    def test_ServerCanAccessConstrainedClient(self):
        self.topology = TopologyManager.fromConfigFile("constrained-device-without-gateway-client-uat-hobbyist")
        def delTopology(): del self.topology
        self.addCleanup(delTopology)

        self.topology.constrainedClients[0].start()

        self.assertEqual("0", self.topology.constrainedClients[0].createResource(3, 0, 0))
        self.assertEqual("0", self.topology.constrainedClients[0].setResourceValue("/3/0/0", "hello"))
        self.assertEqual("hello", self.topology.constrainedClients[0].getResourceValue("/3/0/0"))

        self.topology.constrainedClients[0].WaitForResources(["/0/0/0","/0/1/0", "/0/2/0", ])  # wait for bootstrapping to complete
        self.topology.gatewayServers[0].WaitForClient(self.topology.constrainedClients[0].getClientID())
        self.assertEqual("hello", self.topology.gatewayServers[0].ReadSingleResource(self.topology.constrainedClients[0].getClientID(), "/3/0/0", AwaResourceType.String))

