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

from framework.test_cases.gateway_client_test_case import GWClientTestCase

from framework.operation_assertions import get_operation_assertions 
from framework.operation_assertions import set_operation_assertions
from framework.operation_assertions import subscribe_operation_assertions
from framework.operation_assertions import client_delete_assertions
from framework.operation_assertions import client_define_assertions
from framework.operation_assertions import client_get_definition_assertions

from framework import test_assertions
from framework.test_assertions import Assertion
from framework.test_assertions import GetAssertion
from framework.test_assertions import SetAssertion
from framework.test_assertions import SubscribeAssertion
from framework.test_assertions import DeleteAssertion
from framework.test_assertions import DefineOperationAssertion
from framework.test_assertions import GetDefinitionAssertion
from framework.definitions import ObjectDefinitionSettings, ResourceDefinitionSettings

from framework.test_objects import objectDefinition1000
from framework.test_objects import objectDefinition1001
from framework.test_objects import objectDefinition1002
from framework.test_objects import objectDefinition1003
from framework.test_objects import resourceDefinitions

from framework.awa_enums import AwaResourceType
from framework.awa_enums import AwaResourceOperations
from framework import awa_constants


from framework.nose_parameterised import noseParameterisedTestNameGenerator

@attr("gateway_client")
class CustomObjectDefineTestCases(GWClientTestCase):
    @parameterized.expand([
        ["DefineAndGetObject1000Definition", (DefineOperationAssertion(client_define_assertions.CheckForSuccess, objectDefinition1000, resourceDefinitions),
                                              GetDefinitionAssertion(client_get_definition_assertions.CheckForSuccess, objectDefinition1000, resourceDefinitions), )],

        ["DefineAndGetObject1001Definition", (DefineOperationAssertion(client_define_assertions.CheckForSuccess, objectDefinition1001, resourceDefinitions), 
                                              GetDefinitionAssertion(client_get_definition_assertions.CheckForSuccess, objectDefinition1001, resourceDefinitions), )],

        ["DefineAndGetObject1002Definition", (DefineOperationAssertion(client_define_assertions.CheckForSuccess, objectDefinition1002, resourceDefinitions),
                                              GetDefinitionAssertion(client_get_definition_assertions.CheckForSuccess, objectDefinition1002, resourceDefinitions), )],

        ["DefineAndGetObject1003Definition", (DefineOperationAssertion(client_define_assertions.CheckForSuccess, objectDefinition1003, resourceDefinitions), 
                                              GetDefinitionAssertion(client_get_definition_assertions.CheckForSuccess, objectDefinition1003, resourceDefinitions), )],

        #Negative define test cases
        ["RedefineObject1000",               (DefineOperationAssertion(client_define_assertions.CheckForSuccess, objectDefinition1000, resourceDefinitions), 
                                              DefineOperationAssertion(client_define_assertions.CheckForAlreadyDefined, objectDefinition1000, resourceDefinitions),)],
        ["GetNotDefinedObjectDefinition",    (GetDefinitionAssertion(client_get_definition_assertions.CheckForObjectNotDefined, ObjectDefinitionSettings(5000, "Object5000", 1, 1), ()), )],
        ["GetObjectDefinitionIDOutOfRange",  (GetDefinitionAssertion(client_get_definition_assertions.CheckForObjectNotDefined, ObjectDefinitionSettings(-500, "Object500", 1, 1), ()), )],

        ["GetNotDefinedResourceDefinition",  (DefineOperationAssertion(client_define_assertions.CheckForSuccess, objectDefinition1000, resourceDefinitions),
                                              GetDefinitionAssertion(client_get_definition_assertions.CheckForResourceNotDefined, 
                                                                    objectDefinition1000, 
                                                                    (ResourceDefinitionSettings(555, "Resource555", AwaResourceType.String, AwaResourceOperations.ReadWrite, 0, 1), )), )],

        ["DefineObjectIDOutOfRange",         (DefineOperationAssertion(client_define_assertions.CheckForNullPointerException, ObjectDefinitionSettings(999999, "Object999999", 0, 1), ()), )],

        ["DefineResourceIDOutOfRange",       (DefineOperationAssertion(client_define_assertions.CheckForSuccess, objectDefinition1000, resourceDefinitions),
                                              DefineOperationAssertion(client_define_assertions.CheckForIDInvalid, 
                                                                      objectDefinition1000, 
                                                                      (ResourceDefinitionSettings(999999, "Resource999999", AwaResourceType.String, AwaResourceOperations.ReadWrite, 0, 1), )), )],

        ["DefineObjectNegativeID",           (DefineOperationAssertion(client_define_assertions.CheckForNullPointerException, 
                                                                      ObjectDefinitionSettings(-123, "Object123", 0, 1), 
                                                                      ()), )],
        ["DefineResourceNegativeID",         (DefineOperationAssertion(client_define_assertions.CheckForSuccess, objectDefinition1000, resourceDefinitions),
                                              DefineOperationAssertion(client_define_assertions.CheckForIDInvalid, 
                                                                      objectDefinition1000, 
                                                                      (ResourceDefinitionSettings(-123, "Resource123", AwaResourceType.String, AwaResourceOperations.ReadWrite, 0, 1), )), )],
    ], testcase_func_name=noseParameterisedTestNameGenerator)

    def test(self, name, assertions):
        test_assertions.callAssertions(self, assertions)

@attr("gateway_client")
class CustomObjectCreateTestCases(GWClientTestCase):

    def setUp(self):
        super(CustomObjectCreateTestCases, self).setUp()
        self.topology.gatewayClients[0].DefineTestObjects()

    @parameterized.expand([
        #  Create object instance test cases
        ["CreateSingleOptionalObjectInstance",     (SetAssertion(set_operation_assertions.CheckForSuccess, "/1000/0", None, None, True), )],
        ["CreateSingleMandatoryObjectInstance",    (SetAssertion(set_operation_assertions.CheckForSuccess, "/1001/0", None, None, True), )],
        ["CreateMultipleObjectInstance",           (SetAssertion(set_operation_assertions.CheckForSuccess, "/1002/0", None, None, True), )],

        ["CreateExistingSingleObjectInstance",     (SetAssertion(set_operation_assertions.CheckForSuccess, "/1000/0", None, None, True), 
                                                    SetAssertion(set_operation_assertions.CheckForCannotCreate, "/1000/0", None, None, True), )],
        ["CreateExistingMultipleObjectInstance",   (SetAssertion(set_operation_assertions.CheckForSuccess, "/1002/0", None, None, True), 
                                                    SetAssertion(set_operation_assertions.CheckForCannotCreate, "/1002/0", None, None, True), )],

        ["CreateMultipleOnSingleObjectInstance",   (SetAssertion(set_operation_assertions.CheckForSuccess, "/1000/0", None, None, True), 
                                                    SetAssertion(set_operation_assertions.CheckForCannotCreate, "/1000/1", None, None, True), )],

        ["CreateMultipleOnMultipleObjectInstance", (SetAssertion(set_operation_assertions.CheckForSuccess, "/1002/0", None, None, True), 
                                                    SetAssertion(set_operation_assertions.CheckForSuccess, "/1002/1", None, None, True), )],        

        # Create resource test cases
        ["CreateStringArrayResource",              (SetAssertion(set_operation_assertions.CheckForSuccess, "/1000/0", None, None, True),
                                                    SetAssertion(set_operation_assertions.CheckForSuccess, "/1000/0/109", AwaResourceType.StringArray, None, False, True), 
                                                    GetAssertion(get_operation_assertions.CheckForSuccess, "/1000/0/109", AwaResourceType.StringArray, {1: "Sample1", 2: "Sample2", 3: "Sample3"}), )],

        ["CreateExistingStringArrayResource",      (SetAssertion(set_operation_assertions.CheckForSuccess, "/1000/0", None, None, True), 
                                                    SetAssertion(set_operation_assertions.CheckForSuccess, "/1000/0/109", AwaResourceType.StringArray, None, False, True), 
                                                    SetAssertion(set_operation_assertions.CheckForCannotCreate, "/1000/0/109", AwaResourceType.StringArray, None, False, True), )],

        ["CreateStringArrayResourceWithValue",     (SetAssertion(set_operation_assertions.CheckForSuccess, "/1000/0", None, None, True),
                                                    SetAssertion(set_operation_assertions.CheckForSuccess, "/1000/0/109", AwaResourceType.StringArray, {0: "Sample0", 2: "Sample2"}, False, True), 
                                                    GetAssertion(get_operation_assertions.CheckForSuccess, "/1000/0/109", AwaResourceType.StringArray, {0: "Sample0", 2: "Sample2"}), )],
    ], testcase_func_name=noseParameterisedTestNameGenerator)

    def test(self, name, assertions):
        test_assertions.callAssertions(self, assertions)

@attr("gateway_client")
class CustomObjectDeleteTestCases(GWClientTestCase):

    def setUp(self):
        super(CustomObjectDeleteTestCases, self).setUp()
        self.topology.gatewayClients[0].DefineTestObjects()
        self.topology.gatewayClients[0].CreateInstancesOfTestObjects()

    @parameterized.expand([
        # Delete resource test cases
        ["DeleteMandatoryResource",     (DeleteAssertion(client_delete_assertions.CheckForSuccess, "/1000/0/202"), )],
        ["DeleteOptionalResource",      (SetAssertion(set_operation_assertions.CheckForSuccess, "/1000/0/102", AwaResourceType.String, None, False, True), 
                                               DeleteAssertion(client_delete_assertions.CheckForSuccess, "/1000/0/102"), )],
        ["DeleteNonExistentResource",   (DeleteAssertion(client_delete_assertions.CheckForPathNotFound, "/1000/0/102"), )],
        ["DeleteUndefinedResource",     (DeleteAssertion(client_delete_assertions.CheckForPathNotFound, "/1000/0/999"), )],


        # Delete object instance success cases
        ["DeleteMandatoryObjectInstance", (DeleteAssertion(client_delete_assertions.CheckForSuccess, "/1001/0"), )],
        ["DeleteOptionalObjectInstance", (DeleteAssertion(client_delete_assertions.CheckForSuccess, "/1000/0"), )],
        ["DeleteNonExistentObjectInstance", (DeleteAssertion(client_delete_assertions.CheckForPathNotFound, "/1000/999"), )],
        ["DeleteUndefinedObject", (DeleteAssertion(client_delete_assertions.CheckForPathNotFound, "/9999"), )],

        # TODO delete whole object cases
    ], testcase_func_name=noseParameterisedTestNameGenerator)
    def test(self, name, assertions):
        test_assertions.callAssertions(self, assertions)

@attr("gateway_client")
class CustomObjectTestCases(GWClientTestCase):

    def setUp(self):
        super(CustomObjectTestCases, self).setUp()
        self.topology.gatewayClients[0].DefineTestObjects()
        self.topology.gatewayClients[0].CreateInstancesOfTestObjects()

    @parameterized.expand([
        #  Create object instance test cases
        ["SetGetMandatoryStringResource",      (GetAssertion(get_operation_assertions.CheckForSuccess, "/1000/0/202", AwaResourceType.String, "test"),
                                                SetAssertion(set_operation_assertions.CheckForSuccess, "/1000/0/202", AwaResourceType.String, "Imagination Technologies"),
                                                GetAssertion(get_operation_assertions.CheckForSuccess, "/1000/0/202", AwaResourceType.String, "Imagination Technologies"), )],

        ["SetGetMandatoryStringArrayResource", (GetAssertion(get_operation_assertions.CheckForSuccess, "/1000/0/209", AwaResourceType.StringArray, {1: "Sample1", 2: "Sample2", 3: "Sample3"}),
                                                SetAssertion(set_operation_assertions.CheckForSuccess, "/1000/0/209", AwaResourceType.StringArray, {0: "Sample0", 20: "Sample20"}),
                                                GetAssertion(get_operation_assertions.CheckForSuccess, "/1000/0/209", AwaResourceType.StringArray, {0: "Sample0", 20: "Sample20"}), )],

        ["SetGetMandatoryIntegerArrayResource", (GetAssertion(get_operation_assertions.CheckForSuccess, "/1000/0/210", AwaResourceType.IntegerArray, {0: 5, 1: 10, 2: 15}),
                                                 SetAssertion(set_operation_assertions.CheckForSuccess, "/1000/0/210", AwaResourceType.IntegerArray, {3: 5, 4: 10, 5: 15}),
                                                 GetAssertion(get_operation_assertions.CheckForSuccess, "/1000/0/210", AwaResourceType.IntegerArray, {3: 5, 4: 10, 5: 15}), )],

        ["UpdateMandatoryIntegerArrayResource", (GetAssertion(get_operation_assertions.CheckForSuccess, "/1000/0/210", AwaResourceType.IntegerArray, {3: 5, 4: 10, 5: 15}),
                                                 SetAssertion(set_operation_assertions.CheckForSuccess, "/1000/0/210", AwaResourceType.IntegerArray, {6: 20}, False, False, True),
                                                 GetAssertion(get_operation_assertions.CheckForSuccess, "/1000/0/210", AwaResourceType.IntegerArray, {3: 5, 4: 10, 5: 15, 6: 20}), )],

        ["SetGetOptionalStringResource",        (SetAssertion(set_operation_assertions.CheckForSuccess, "/1000/0/102", None, None, False, True), #  create resource
                                                 GetAssertion(get_operation_assertions.CheckForSuccess, "/1000/0/102", AwaResourceType.String, "test"),
                                                 SetAssertion(set_operation_assertions.CheckForSuccess, "/1000/0/102", AwaResourceType.String, "Imagination Technologies"),
                                                 GetAssertion(get_operation_assertions.CheckForSuccess, "/1000/0/102", AwaResourceType.String, "Imagination Technologies"), )],


        #  Set negative test cases
        ["SetIntegerValueOnUndefinedObject",         (SetAssertion(set_operation_assertions.CheckForNotDefinedWhenAddingValue, "/9999/0/0", AwaResourceType.Integer, 1234), )],
        ["SetIntegerValueOnUndefinedObjectInstance", (SetAssertion(set_operation_assertions.CheckForNotDefinedWhenAddingValue, "/1000/9999/0", AwaResourceType.Integer, 1234), )],
        ["SetIntegerValueOnUndefinedResource",       (SetAssertion(set_operation_assertions.CheckForNotDefinedWhenAddingValue, "/1000/0/9999", AwaResourceType.Integer, 1234), )],
        ["SetIntegerValueOnInvalidPath",             (SetAssertion(set_operation_assertions.CheckForPathInvalid, "/@%@!#$/0/9999", AwaResourceType.Integer, 1234), )],

        #  Get negative test cases
        ["GetIntegerValueOnUndefinedObject",         (GetAssertion(get_operation_assertions.CheckForPathNotFound, "/9999/0/0", AwaResourceType.Integer, 1234), )],
        ["GetIntegerValueOnUndefinedObjectInstance", (GetAssertion(get_operation_assertions.CheckForPathNotFound, "/1000/9999/0", AwaResourceType.Integer, 1234), )],
        ["GetIntegerValueOnUndefinedResource",       (GetAssertion(get_operation_assertions.CheckForPathNotFound, "/1000/0/9999", AwaResourceType.Integer, 1234), )],
        ["GetIntegerValueOnInvalidPath",             (GetAssertion(get_operation_assertions.CheckForPathInvalid, "/@%@!#$/0/9999", AwaResourceType.Integer, 1234), )],


        #  subscribe test cases
        ["SubscribeToChangeStringResource",          (GetAssertion(get_operation_assertions.CheckForSuccess, "/1000/0/202", AwaResourceType.String, "test"),
                                                      SubscribeAssertion(subscribe_operation_assertions.CheckForSuccess, "/1000/0/202", AwaResourceType.String, "test2", True), )],

        ["SubscribeToChangeStringArrayResource",     (GetAssertion(get_operation_assertions.CheckForSuccess, "/1000/0/209", AwaResourceType.StringArray, {1: "Sample1", 2: "Sample2", 3: "Sample3"}),
                                                      SubscribeAssertion(subscribe_operation_assertions.CheckForSuccess, "/1000/0/209", AwaResourceType.StringArray, {0: "Sample0", 5: "Sample5"}, True, True), )],
    ], testcase_func_name=noseParameterisedTestNameGenerator)
    def test(self, name, assertions):
        test_assertions.callAssertions(self, assertions)
