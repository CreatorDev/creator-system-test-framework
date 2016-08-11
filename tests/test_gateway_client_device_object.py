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

from framework.test_cases.gateway_client_test_case import GWClientTestCase, GWClientNUCTestCase

from framework.operation_assertions import get_operation_assertions
from framework.operation_assertions import set_operation_assertions
from framework.operation_assertions import subscribe_operation_assertions
from framework.operation_assertions import client_delete_assertions
from framework.operation_assertions import client_define_assertions
from framework.operation_assertions import client_get_definition_assertions
from framework.operation_assertions import device_server_get_definition_assertions
from framework.operation_assertions import device_server_get_operation_assertions
from framework.operation_assertions import cloud_get_operation_assertions
from framework.operation_assertions import cloud_set_operation_assertions

from framework import test_assertions
from framework.test_assertions import Assertion
from framework.test_assertions import GetAssertion
from framework.test_assertions import SetAssertion
from framework.test_assertions import SubscribeAssertion
from framework.test_assertions import DeleteAssertion
from framework.test_assertions import DefineOperationAssertion
from framework.test_assertions import GetDefinitionAssertion
from framework.test_assertions import CloudGetAssertion
from framework.test_assertions import CloudSetAssertion
from framework.definitions import ObjectDefinitionSettings, ResourceDefinitionSettings

from framework.awa_enums import AwaResourceType
from framework.awa_enums import AwaResourceOperations
from framework import awa_constants

from framework.nose_parameterised import noseParameterisedTestNameGenerator

@attr("gateway_client", "device_object")
class DeviceObjectDefinition(GWClientTestCase):

    deviceObjectSettings = ObjectDefinitionSettings(3, "Device", 1, 1)
    deviceResources = (ResourceDefinitionSettings(0, "Manufacturer", AwaResourceType.String, AwaResourceOperations.ReadOnly, 0, 1),
                       ResourceDefinitionSettings(4, "Reboot", AwaResourceType.NoneType, AwaResourceOperations.Execute, 1, 1),
                       ResourceDefinitionSettings(6, "AvailablePowerSources", AwaResourceType.IntegerArray, AwaResourceOperations.ReadOnly, 0, awa_constants.MAX_ID),
                       ResourceDefinitionSettings(10, "MemoryFree", AwaResourceType.Integer, AwaResourceOperations.ReadOnly, 0, 1),
                       ResourceDefinitionSettings(11, "ErrorCode", AwaResourceType.IntegerArray, AwaResourceOperations.ReadOnly, 1, awa_constants.MAX_ID), )

    @parameterized.expand([
        # Get definition test cases
        ["GetDeviceObjectDefinition",                (GetDefinitionAssertion(client_get_definition_assertions.CheckForSuccess, deviceObjectSettings, None), )],
        ["GetDeviceResourceDefinitions",             (GetDefinitionAssertion(client_get_definition_assertions.CheckForSuccess, deviceObjectSettings, deviceResources), )],

        # Define test cases (From a "Black Box" testing perspective)
        ["RedefineDeviceObjectDefinition", (DefineOperationAssertion(client_define_assertions.CheckForAlreadyDefined, deviceObjectSettings, ()), )],
        ["RedefineDeviceObjectDefinitionWithManufacturerResource", (DefineOperationAssertion(client_define_assertions.CheckForAlreadyDefined, deviceObjectSettings,
                                                                                             (ResourceDefinitionSettings(0, "Manufacturer", AwaResourceType.String, 
                                                                                                                         AwaResourceOperations.ReadOnly, 0, 1), )), )],
        ["RedefineDeviceObjectDefinitionWithAvailablePowerSourcesResource", (DefineOperationAssertion(client_define_assertions.CheckForAlreadyDefined,
                                                                                                      ObjectDefinitionSettings(3, "Device", 1, 1),
                                                                                                      (ResourceDefinitionSettings(6, "AvailablePowerSources", AwaResourceType.IntegerArray,
                                                                                                                                  AwaResourceOperations.ReadOnly, 0, awa_constants.MAX_ID), )), )],
    ], testcase_func_name=noseParameterisedTestNameGenerator)

    def test(self, name, assertions):
        test_assertions.callAssertions(self, assertions)

# Same as above, except runs against local DeviceServer running on NUC and checks for new object definition resources on DeviceServer
@attr("gateway_client", "device_object")
class DeviceObjectDefinitionDeviceServerCheck(GWClientNUCTestCase):

    deviceObjectSettings = ObjectDefinitionSettings(3, "Device", 1, 1)
    deviceResources = (ResourceDefinitionSettings(0, "Manufacturer", AwaResourceType.String, AwaResourceOperations.ReadOnly, 0, 1),
                       ResourceDefinitionSettings(4, "Reboot", AwaResourceType.NoneType, AwaResourceOperations.Execute, 1, 1),
                       ResourceDefinitionSettings(6, "AvailablePowerSources", AwaResourceType.IntegerArray, AwaResourceOperations.ReadOnly, 0, awa_constants.MAX_ID),
                       ResourceDefinitionSettings(10, "MemoryFree", AwaResourceType.Integer, AwaResourceOperations.ReadOnly, 0, 1),
                       ResourceDefinitionSettings(11, "ErrorCode", AwaResourceType.IntegerArray, AwaResourceOperations.ReadOnly, 1, awa_constants.MAX_ID), )

    @parameterized.expand([
        # Get definition test cases
        ["GetDeviceObjectDefinition",                (GetDefinitionAssertion(client_get_definition_assertions.CheckForSuccess, deviceObjectSettings, None), )],
        ["GetDeviceServerDeviceObjectDefinition",    (GetDefinitionAssertion(device_server_get_definition_assertions.CheckForSuccess, deviceObjectSettings, None), )],

        ["GetDeviceResourceDefinitions", (GetDefinitionAssertion(client_get_definition_assertions.CheckForSuccess, deviceObjectSettings, deviceResources), )],
        ["GetDeviceServerResourceDefinitions", (GetDefinitionAssertion(device_server_get_definition_assertions.CheckForSuccess, deviceObjectSettings, deviceResources), )],

    ], testcase_func_name=noseParameterisedTestNameGenerator)

    def test(self, name, assertions):
        test_assertions.callAssertions(self, assertions)

@attr("gateway_client", "device_object")
class DeviceObjectGetSetResource(GWClientTestCase):

    @parameterized.expand([

        # Daemon GET/SET operations. Both should succeed even if the resource is read only because the client daemon has control over all its resources.
        # Read the initial value, then see that it has changed after the set operation.
        ["SetGetManufacturerResource",       (GetAssertion(get_operation_assertions.CheckForSuccess, "/3/0/0", AwaResourceType.String, "Imagination Technologies"),
                                              SetAssertion(set_operation_assertions.CheckForSuccess, "/3/0/0", AwaResourceType.String, "Imagination Technologies 123"),
                                              GetAssertion(get_operation_assertions.CheckForSuccess, "/3/0/0", AwaResourceType.String, "Imagination Technologies 123"), )],

        ["SetGetModelNumberResource",        (GetAssertion(get_operation_assertions.CheckForSuccess, "/3/0/1", AwaResourceType.String, "Awa Client"),
                                              SetAssertion(set_operation_assertions.CheckForSuccess, "/3/0/1", AwaResourceType.String, "Awa Client 213"),
                                              GetAssertion(get_operation_assertions.CheckForSuccess, "/3/0/1", AwaResourceType.String, "Awa Client 213"), )],

        ["SetGetSerialNumberResource",       (GetAssertion(get_operation_assertions.CheckForSuccess, "/3/0/2", AwaResourceType.String, "SN12345678"),
                                              SetAssertion(set_operation_assertions.CheckForSuccess, "/3/0/2", AwaResourceType.String, "SN135792468"),
                                              GetAssertion(get_operation_assertions.CheckForSuccess, "/3/0/2", AwaResourceType.String, "SN135792468"), )],

        ["SetGetPowerSourceCurrentResource", (GetAssertion(get_operation_assertions.CheckForSuccess, "/3/0/8", AwaResourceType.IntegerArray, {0: 125, 1: 900}),
                                              SetAssertion(set_operation_assertions.CheckForSuccess, "/3/0/8", AwaResourceType.IntegerArray, {0: 123, 1: 456}),
                                              GetAssertion(get_operation_assertions.CheckForSuccess, "/3/0/8", AwaResourceType.IntegerArray, {0: 123, 1: 456}), )],
        # TODO rest of device resources ^^


        # Negative Get test cases
        ["GetManufacturerResourceWithWrongType", (GetAssertion(get_operation_assertions.CheckForTypeMismatch, "/3/0/0", AwaResourceType.Integer, None), )],
        ["GetUndefinedResource", (GetAssertion(get_operation_assertions.CheckForPathNotFound, "/3/0/100", AwaResourceType.String, None), )],


        # Negative Set test cases
        ["SetMultipleValuesOnSingleInstanceResource", (SetAssertion(set_operation_assertions.CheckForTypeMismatchWhenAddingValue, "/3/0/0", AwaResourceType.StringArray, {0: "Imagination Technologies", 1: "Imagination Technologies 2"}), )],

     ], testcase_func_name=noseParameterisedTestNameGenerator)

    def test(self, name, assertions):
        test_assertions.callAssertions(self, assertions)

@attr("gateway_client", "device_object")
class DeviceObjectGetSetResourceDeviceServerCheck(GWClientNUCTestCase):

    @parameterized.expand([

        # Daemon GET/SET operations. Both should succeed even if the resource is read only because the client daemon has control over all its resources.
        # Read the initial value, then see that it has changed after the set operation.
        ["SetGetManufacturerResource",       (GetAssertion(get_operation_assertions.CheckForSuccess, "/3/0/0", AwaResourceType.String, "Imagination Technologies"),
                                              SetAssertion(set_operation_assertions.CheckForSuccess, "/3/0/0", AwaResourceType.String, "Imagination Technologies 123"),
                                              GetAssertion(get_operation_assertions.CheckForSuccess, "/3/0/0", AwaResourceType.String, "Imagination Technologies 123"),
                                              GetAssertion(device_server_get_operation_assertions.CheckForSuccess, "/3/0/0", AwaResourceType.String, "Imagination Technologies 123"), )],

        ["SetGetModelNumberResource",        (GetAssertion(get_operation_assertions.CheckForSuccess, "/3/0/1", AwaResourceType.String, "Awa Client"),
                                              SetAssertion(set_operation_assertions.CheckForSuccess, "/3/0/1", AwaResourceType.String, "Awa Client 213"),
                                              GetAssertion(get_operation_assertions.CheckForSuccess, "/3/0/1", AwaResourceType.String, "Awa Client 213"),
                                              GetAssertion(device_server_get_operation_assertions.CheckForSuccess, "/3/0/1", AwaResourceType.String, "Awa Client 213"), )],

        ["SetGetSerialNumberResource",       (GetAssertion(get_operation_assertions.CheckForSuccess, "/3/0/2", AwaResourceType.String, "SN12345678"),
                                              SetAssertion(set_operation_assertions.CheckForSuccess, "/3/0/2", AwaResourceType.String, "SN135792468"),
                                              GetAssertion(get_operation_assertions.CheckForSuccess, "/3/0/2", AwaResourceType.String, "SN135792468"),
                                              GetAssertion(device_server_get_operation_assertions.CheckForSuccess, "/3/0/2", AwaResourceType.String, "SN135792468"), )],

        ["SetGetPowerSourceCurrentResource", (GetAssertion(get_operation_assertions.CheckForSuccess, "/3/0/8", AwaResourceType.IntegerArray, {0: 125, 1: 900}),
                                              SetAssertion(set_operation_assertions.CheckForSuccess, "/3/0/8", AwaResourceType.IntegerArray, {0: 123, 1: 456}),
                                              GetAssertion(get_operation_assertions.CheckForSuccess, "/3/0/8", AwaResourceType.IntegerArray, {0: 123, 1: 456}),
                                              GetAssertion(device_server_get_operation_assertions.CheckForSuccess, "/3/0/8", AwaResourceType.IntegerArray, {0: 123, 1: 456}), )],
        # TODO rest of device resources ^^


        # Negative Get test cases
        ["GetManufacturerResourceWithWrongType", (GetAssertion(get_operation_assertions.CheckForTypeMismatch, "/3/0/0", AwaResourceType.Integer, None), )],
        ["GetUndefinedResource", (GetAssertion(get_operation_assertions.CheckForPathNotFound, "/3/0/100", AwaResourceType.String, None), )],


        # Negative Set test cases
        ["SetMultipleValuesOnSingleInstanceResource", (SetAssertion(set_operation_assertions.CheckForTypeMismatchWhenAddingValue, "/3/0/0", AwaResourceType.StringArray, {0: "Imagination Technologies", 1: "Imagination Technologies 2"}), )],

     ], testcase_func_name=noseParameterisedTestNameGenerator)

    def test(self, name, assertions):
        test_assertions.callAssertions(self, assertions)

@attr("gateway_client", "device_object")
class DeviceObjectSubscribe(GWClientTestCase):

    @parameterized.expand([

        # Daemon Subscribe to Change
        ["SubscribeToChangeManufacturerResource",            (GetAssertion(get_operation_assertions.CheckForSuccess, "/3/0/0", AwaResourceType.String, "Imagination Technologies"),
                                                              SubscribeAssertion(subscribe_operation_assertions.CheckForSuccess, "/3/0/0", AwaResourceType.String, "Imagination", True), )],

        ["SubscribeToChangeAvailablePowerSourcesResource",   (GetAssertion(get_operation_assertions.CheckForSuccess, "/3/0/6", AwaResourceType.IntegerArray, {0: 1, 1: 5}),
                                                              SubscribeAssertion(subscribe_operation_assertions.CheckForSuccess, "/3/0/6", AwaResourceType.IntegerArray, {0: 15, 1: 25}, True, True), )],

        ["SubscribeToNonExistentResource",                   (SubscribeAssertion(subscribe_operation_assertions.CheckForPathNotFound, "/3/0/200", AwaResourceType.String, "Imagination", True), )],
        # TODO rest of device resources ^^

        # TODO subscribe to object instance / object etc.
     ], testcase_func_name=noseParameterisedTestNameGenerator)

    def test(self, name, assertions):
        test_assertions.callAssertions(self, assertions)

@attr("gateway_client", "device_object")
class DeviceObjectDelete(GWClientTestCase):

    @parameterized.expand([

        # Daemon delete resource
        ["DeleteManufacturerResource",                  (GetAssertion(get_operation_assertions.CheckForSuccess, "/3/0/0", AwaResourceType.String, "Imagination Technologies"),
                                                         DeleteAssertion(client_delete_assertions.CheckForSuccess, "/3/0/0"),
                                                         GetAssertion(get_operation_assertions.CheckForPathNotFound, "/3/0/0", AwaResourceType.String, None), )],

        #FIXME https,//issues.ba.imgtec.org/browse/FLOWDM-673
        ["DeleteRebootResource",                        (DeleteAssertion(client_delete_assertions.CheckForSuccess, "/3/0/4"),
                                                         DeleteAssertion(client_delete_assertions.CheckForPathNotFound, "/3/0/4"), )],

        ["DeleteNonDefinedResource",                    (DeleteAssertion(client_delete_assertions.CheckForPathNotFound, "/3/0/888"), )],

        # Daemon delete object instance
        ["DeleteDeviceObjectInstance",                  (DeleteAssertion(client_delete_assertions.CheckForSuccess, "/3/0"),
                                                         DeleteAssertion(client_delete_assertions.CheckForPathNotFound, "/3/0"), )],

        ["DeleteNonExistentObjectInstance",             (DeleteAssertion(client_delete_assertions.CheckForPathNotFound, "/3/1"), )],

        ["DeleteAvailablePowerSourceResourceInstances", (GetAssertion(get_operation_assertions.CheckForSuccess, "/3/0/6", AwaResourceType.IntegerArray, {0: 15, 1: 25}),
                                                         DeleteAssertion(client_delete_assertions.CheckForSuccess, "/3/0/6", 0, 2),
                                                         GetAssertion(get_operation_assertions.CheckForSuccess, "/3/0/6", AwaResourceType.IntegerArray, {}), )],

        ["DeleteErrorCodeResourceResourceInstances",    (GetAssertion(get_operation_assertions.CheckForSuccess, "/3/0/11", AwaResourceType.IntegerArray, {0: 0}),
                                                         DeleteAssertion(client_delete_assertions.CheckForSuccess, "/3/0/11", 0, 1),
                                                         GetAssertion(get_operation_assertions.CheckForSuccess, "/3/0/11", AwaResourceType.IntegerArray, {}), )],

        ["DeleteAndCreateMemoryFreeResource",           (DeleteAssertion(client_delete_assertions.CheckForSuccess, "/3/0/10"),
                                                         SetAssertion(set_operation_assertions.CheckForSuccess, "/3/0/10", None, None, False, True), )],

     ], testcase_func_name=noseParameterisedTestNameGenerator)

    def test(self, name, assertions):
        test_assertions.callAssertions(self, assertions)

@attr("gateway_client", "device_object")
class DeviceObjectCreate(GWClientTestCase):

    @parameterized.expand([

        # Daemon create object instance
        ############################################################################
        ["DaemonCreateDeviceObjectInstance",             (DeleteAssertion(client_delete_assertions.CheckForSuccess, "/3/0"),
                                                          SetAssertion(set_operation_assertions.CheckForSuccess, "/3/0", None, None, True), )],

        ["DaemonCreateExistingDeviceObjectInstance",     (SetAssertion(set_operation_assertions.CheckForCannotCreate, "/3/0", None, None, True), )],

        # Daemon create resources
        ############################################################################
        ["DaemonCreateFirmwareVersionResourceWithValue", (DeleteAssertion(client_delete_assertions.CheckForSuccess, "/3/0/3"),
                                                          SetAssertion(set_operation_assertions.CheckForSuccess, "/3/0/3", AwaResourceType.String, "test", False, True),
                                                          GetAssertion(get_operation_assertions.CheckForSuccess, "/3/0/3", AwaResourceType.String, "test"), )],

        ["DaemonCreateExistingFirmwareVersionResource",  (SetAssertion(set_operation_assertions.CheckForCannotCreate, "/3/0/3", None, None, False, True), )],

    ], testcase_func_name=noseParameterisedTestNameGenerator)

    def test(self, name, assertions):
        test_assertions.callAssertions(self, assertions)
