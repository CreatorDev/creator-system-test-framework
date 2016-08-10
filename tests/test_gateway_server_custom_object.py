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
from nose_parameterized import parameterized
from nose.plugins.attrib import attr

from framework.test_cases.gateway_server_and_client_test_case import GWServerAndClientTestCase

from framework.operation_assertions import client_get_definition_assertions
from framework.operation_assertions import client_define_assertions
from framework.operation_assertions import client_delete_assertions
from framework.operation_assertions import server_get_definition_assertions
from framework.operation_assertions import server_define_assertions
from framework.operation_assertions import server_delete_assertions
from framework.operation_assertions import read_operation_assertions
from framework.operation_assertions import write_operation_assertions
from framework.operation_assertions import observe_operation_assertions
from framework.operation_assertions import list_clients_assertions 
from framework.operation_assertions import read_operation_assertions 

from framework import test_assertions
from framework.test_assertions import Assertion
from framework.test_assertions import ReadAssertion
from framework.test_assertions import WriteAssertion
from framework.test_assertions import ObserveAssertion
from framework.test_assertions import DefineOperationAssertion
from framework.test_assertions import GetDefinitionAssertion
from framework.test_assertions import DeleteAssertion
from framework.test_assertions import ListClientsAssertion

from framework.awa_enums import AwaResourceType
from framework.awa_enums import AwaResourceOperations
from framework import awa_constants

from framework.test_objects import objectDefinition1000
from framework.test_objects import objectDefinition1001
from framework.test_objects import objectDefinition1002
from framework.test_objects import objectDefinition1003
from framework.test_objects import resourceDefinitions

from framework.nose_parameterised import noseParameterisedTestNameGenerator

# TODO:
# execute / client subscribe to execute
# write attributes
# Custom objects need to be defined through the REST API in order to do cloud validation

@attr("gateway_client", "gateway_server")
class CustomObjectDefineTestCases(GWServerAndClientTestCase):
    @parameterized.expand([
        
        # TODO move to device test cases
        ["ReadDeviceCurrentTimeResource", (ReadAssertion(read_operation_assertions.CheckForSuccess, "/3/0/13", AwaResourceType.Time, 2718619435), )],
                                                         #WriteAssertion(write_operation_assertions.CheckForSuccess, "/1000/0/202", AwaResourceType.String, "Imagination Technologies"),
                                                         #ReadAssertion(read_operation_assertions.CheckForSuccess, "/1000/0/202", AwaResourceType.String, "Imagination Technologies")))),

        
        # Server & Client define / get definition test cases
        ["ServerDefineAndGetObject1000Definition", (DefineOperationAssertion(server_define_assertions.CheckForSuccess, objectDefinition1000, resourceDefinitions),
                                                    GetDefinitionAssertion(server_get_definition_assertions.CheckForSuccess, objectDefinition1000, resourceDefinitions), )],
        ["ClientDefineAndGetObject1000Definition", (DefineOperationAssertion(client_define_assertions.CheckForSuccess, objectDefinition1000, resourceDefinitions),
                                                    GetDefinitionAssertion(client_get_definition_assertions.CheckForSuccess, objectDefinition1000, resourceDefinitions), )],

        ["ServerDefineAndGetObject1001Definition", (DefineOperationAssertion(server_define_assertions.CheckForSuccess, objectDefinition1001, resourceDefinitions),
                                                    GetDefinitionAssertion(server_get_definition_assertions.CheckForSuccess, objectDefinition1001, resourceDefinitions), )],
        ["ClientDefineAndGetObject1001Definition", (DefineOperationAssertion(client_define_assertions.CheckForSuccess, objectDefinition1001, resourceDefinitions),
                                                    GetDefinitionAssertion(client_get_definition_assertions.CheckForSuccess, objectDefinition1001, resourceDefinitions), )],

        ["ServerDefineAndGetObject1002Definition", (DefineOperationAssertion(server_define_assertions.CheckForSuccess, objectDefinition1002, resourceDefinitions),
                                                    GetDefinitionAssertion(server_get_definition_assertions.CheckForSuccess, objectDefinition1002, resourceDefinitions), )],
        ["ClientDefineAndGetObject1002Definition", (DefineOperationAssertion(client_define_assertions.CheckForSuccess, objectDefinition1002, resourceDefinitions),
                                                    GetDefinitionAssertion(client_get_definition_assertions.CheckForSuccess, objectDefinition1002, resourceDefinitions), )],

        ["ServerDefineAndGetObject1003Definition", (DefineOperationAssertion(server_define_assertions.CheckForSuccess, objectDefinition1003, resourceDefinitions),
                                                    GetDefinitionAssertion(server_get_definition_assertions.CheckForSuccess, objectDefinition1003, resourceDefinitions), )],
        ["ClientDefineAndGetObject1003Definition", (DefineOperationAssertion(client_define_assertions.CheckForSuccess, objectDefinition1003, resourceDefinitions),
                                                    GetDefinitionAssertion(client_get_definition_assertions.CheckForSuccess, objectDefinition1003, resourceDefinitions), )],
        
        
    ], testcase_func_name=noseParameterisedTestNameGenerator)
    
    def test(self, name, assertions):
        test_assertions.callAssertions(self, assertions)

@attr("gateway_client", "gateway_server")
class CustomObjectCreateTestCases(GWServerAndClientTestCase):

    def setUp(self):
        super(CustomObjectCreateTestCases, self).setUp()
        self.topology.gatewayClients[0].DefineTestObjects()
        self.topology.gatewayServers[0].DefineTestObjects()
    
    @parameterized.expand([
        ["CreateSingleObjectInstance",             (WriteAssertion(write_operation_assertions.CheckForSuccess, "/1000/0", None, None, True), )],
    ], testcase_func_name=noseParameterisedTestNameGenerator)
    
    def test(self, name, assertions):
        test_assertions.callAssertions(self, assertions)

@attr("gateway_client", "gateway_server")
class CustomObjectTestCases(GWServerAndClientTestCase):

    def setUp(self):
        super(CustomObjectTestCases, self).setUp()
        self.topology.gatewayClients[0].DefineTestObjects()
        self.topology.gatewayServers[0].DefineTestObjects()
        self.topology.gatewayClients[0].CreateInstancesOfTestObjects();
    
    @parameterized.expand([
        # List clients test cases
        
#         FIXME: Need a better way to get client ID
#         ["ListClientsHasClientAndCustomObject",         (DeleteAssertion(client_delete_assertions.CheckForSuccess, "/1001/0"),  # delete the instance so only the object shows
#                                                          ListClientsAssertion(list_clients_assertions.CheckObjectExists, test_config.config[test_config.config['TestPlan']["local_client"]]['client_id'], "/1001"), )],
#         ["ListClientsHasObjectInstancesOnly",           (ListClientsAssertion(list_clients_assertions.CheckObjectDoesNotExist, test_config.config[test_config.config['TestPlan']["local_client"]]['client_id'], "/1000"), )],
#         ["ListClientsHasClientAndCustomObjectInstance", (ListClientsAssertion(list_clients_assertions.CheckObjectExists, test_config.config[test_config.config['TestPlan']["local_client"]]['client_id'], "/1000/0"), )],
#         ["ListClientsDoesNotHaveUnknownObject",         (ListClientsAssertion(list_clients_assertions.CheckObjectDoesNotExist, test_config.config[test_config.config['TestPlan']["local_client"]]['client_id'], "/99999"), )],
#         ["ListClientsDoesNotHaveUnknownObjectInstance", (ListClientsAssertion(list_clients_assertions.CheckObjectDoesNotExist, test_config.config[test_config.config['TestPlan']["local_client"]]['client_id'], "/1000/99999"), )],
#         ["ListClientsDoesNotHaveUnknownClient",         (ListClientsAssertion(list_clients_assertions.CheckClientDoesNotExist, "client999", None), )],
         
        # Daemon Read / Write test cases
        ["DaemonReadStringArrayResourceDefaultValue",   (ReadAssertion(read_operation_assertions.CheckForSuccess, "/1000/0/209", AwaResourceType.StringArray, {1: "Sample1", 2: "Sample2", 3: "Sample3"}), )],
         
        ["DaemonWriteReadMandatoryStringResource",      (ReadAssertion(read_operation_assertions.CheckForSuccess, "/1000/0/202", AwaResourceType.String, "test"),
                                                         WriteAssertion(write_operation_assertions.CheckForSuccess, "/1000/0/202", AwaResourceType.String, "Imagination Technologies"),
                                                         ReadAssertion(read_operation_assertions.CheckForSuccess, "/1000/0/202", AwaResourceType.String, "Imagination Technologies"))],
        
        
        # Daemon observe test cases
        ["DaemonObserveStringResource",      (ReadAssertion(read_operation_assertions.CheckForSuccess, "/1000/0/202", AwaResourceType.String, "test"),
                                                   ObserveAssertion(observe_operation_assertions.CheckForSuccess, "/1000/0/202", AwaResourceType.String, "test2", True), )], 
        
        
        # Delete object instance cases
        ["DaemonDeleteOptionalObjectInstance",               (DeleteAssertion(server_delete_assertions.CheckForSuccess, "/1000/0"), 
                                                              DeleteAssertion(server_delete_assertions.CheckForMethodNotAllowed, "/1000/0"), )],
        ["DaemonDeleteNonExistentObjectInstance",            (DeleteAssertion(server_delete_assertions.CheckForMethodNotAllowed, "/1000/1"), )],
        
        # Daemon subscribe to execute test cases
        ############################################################################
        # Subscribe to Execute - executed through Awa Server
        # TODO https://issues.ba.imgtec.org/browse/FLOWDM-672
        # DaemonSubscribeToExecuteResource /3/0/4
        #("DaemonSubscribeToExecutableResource",      Call((SubscribeToExecuteAssertion(SubscribeToChangeAssertions.CheckForSuccess, "/1000/0/102", AwaResourceType.String, "test"),
        #                                                   ObserveAssertion(observe_operation_assertions.CheckForSuccess, "/1000/0/102", AwaResourceType.String, "test2", True), ))),
        #############################################################################
    ], testcase_func_name=noseParameterisedTestNameGenerator)
    
    def test(self, name, assertions):
        test_assertions.callAssertions(self, assertions)
