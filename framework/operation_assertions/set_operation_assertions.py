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

from framework.awa_enums import AwaError
from framework.awa_exceptions import AwaUnexpectedErrorException
from operation_assertions_common import CheckForException

def CheckForSuccess(testCase, assertion):
    session = testCase.topology.gatewayClients[0]._session
    setOperation = testCase.topology.gatewayClients[0].CreateSetOperation(session)

    if assertion.createInstance:
        testCase.topology.gatewayClients[0].SetCreateObjectInstance(setOperation, assertion.path)
    if assertion.createResource:
        testCase.topology.gatewayClients[0].SetCreateOptionalResource(setOperation, assertion.path)

    if assertion.value != None:
        if isinstance(assertion.value, dict):
            if assertion.appendArray:
                testCase.topology.gatewayClients[0].SetMultipleInstanceResourceValues(setOperation, assertion.path, assertion.resourceType, assertion.value)
            else:
                testCase.topology.gatewayClients[0].SetMultipleInstanceResourceValuesAsArray(setOperation, assertion.path, assertion.resourceType, assertion.value)
        else:
            testCase.topology.gatewayClients[0].SetSingleInstanceResourceValue(setOperation, assertion.path, assertion.resourceType, assertion.value)

    testCase.topology.gatewayClients[0].PerformSetOperation(setOperation, assertion.path)

def CheckForPathInvalid(testCase, assertion):
    CheckForException(testCase, CheckForSuccess, assertion, AwaUnexpectedErrorException, AwaError.PathInvalid)

def CheckForTypeMismatchWhenAddingValue(testCase, assertion):
    CheckForException(testCase, CheckForSuccess, assertion, AwaUnexpectedErrorException, AwaError.TypeMismatch)

def CheckForTypeMismatch(testCase, assertion):
    CheckForException(testCase, CheckForSuccess, assertion, AwaUnexpectedErrorException, AwaError.Response, AwaError.TypeMismatch)

def CheckForNotDefinedWhenAddingValue(testCase, assertion):
    CheckForException(testCase, CheckForSuccess, assertion, AwaUnexpectedErrorException, AwaError.NotDefined)

def CheckForNotDefined(testCase, assertion):
    CheckForException(testCase, CheckForSuccess, assertion, AwaUnexpectedErrorException, AwaError.Response, AwaError.NotDefined)

def CheckForCannotCreate(testCase, assertion):
    CheckForException(testCase, CheckForSuccess, assertion, AwaUnexpectedErrorException, AwaError.Response, AwaError.CannotCreate)
