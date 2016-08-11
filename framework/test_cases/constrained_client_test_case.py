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
from framework import provisioning
from framework.topology_manager import TopologyManager

class ConstrainedClientTestCase(unittest.TestCase):

    def setUp(self):
        self.topology = TopologyManager.fromConfigFile("constrained-device-only")

        def delTopology(): del self.topology
        self.addCleanup(delTopology)

    def tearDown(self):
        pass

class ConstrainedClientWithCustomObjectsTestCase(ConstrainedClientTestCase):

    def setUp(self):
        super(ConstrainedClientWithCustomObjectsTestCase, self).setUp()

        print("Defining test objects")
        self.topology.constrainedClients[0].DefineTestObjects()
        print("Creating instances of test objects")
        self.topology.constrainedClients[0].CreateInstancesOfTestObjects()

    def tearDown(self):
        pass

class ProvisionedConstrainedClientTestCase(unittest.TestCase):

    def setUp(self):
        self.topology = TopologyManager.fromConfigFile("constrained-device-without-gateways-uat-hobbyist")

        def delTopology(): del self.topology
        self.addCleanup(delTopology)


        self.topology.constrainedClients[0].createResource(3,0,2)
        self.topology.constrainedClients[0].setResourceValue("/3/0/2", self.topology.constrainedClients[0]._constrainedClientConfig['serial-number'])

        self.topology.cloud.createUser()
        self.addCleanup(self.topology.cloud.deleteUser)
        self.topology.cloud.generateDeviceRegistrationToken()

        deviceType = self.topology.cloud._tenantConfig['device-type']
        licenseeID = self.topology.cloud._tenantConfig['licensee-id']
        licenseeSecret = self.topology.cloud._tenantConfig['licensee-secret']
        deviceName = self.topology.constrainedClients[0]._constrainedClientConfig['device-name']

        provisioning.ProvisionConstrainedDeviceWithoutGatewayServer(self.topology.constrainedClients[0], deviceName, deviceType, licenseeID, licenseeSecret, self.topology.cloud.FCAP)

        print("Logging into device")
        self.topology.cloud.loginToDevice(self.topology.constrainedClients[0])

    def tearDown(self):
        pass
