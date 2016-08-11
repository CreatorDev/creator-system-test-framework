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
    session = testCase.topology.gatewayServers[0]._session
    print("TestCase.client_id: " + testCase.client_id)
    readOperation = testCase.topology.gatewayServers[0].CreateReadOperation(session, testCase.client_id, assertion.path)
    pathResult = testCase.topology.gatewayServers[0].GetPathResultFromReadOperation(readOperation, testCase.client_id, assertion.path)
    testCase.assertEqual(AwaError.Success, testCase.topology.gatewayServers[0].GetPathResultError(pathResult))

    if assertion.expectedValue is not None:
        if isinstance(assertion.expectedValue, dict):
            testCase.assertGreater(len(assertion.expectedValue), 0)
            values = testCase.topology.gatewayServers[0].GetResourceValuesFromReadOperation(readOperation, testCase.client_id, assertion.path, assertion.resourceType)
            testCase.assertEqual(assertion.expectedValue, values)
        else:
            value = testCase.topology.gatewayServers[0].GetResourceValueFromReadOperation(readOperation, testCase.client_id, assertion.path, assertion.resourceType)
            testCase.assertIsNotNone(value)
            testCase.assertEqual(assertion.expectedValue, value)

    testCase.topology.gatewayServers[0].FreeReadOperation(readOperation)

def CheckForPathNotFound(testCase, assertion):
    CheckForException(testCase, CheckForSuccess, assertion, AwaUnexpectedErrorException, AwaError.Response, AwaError.PathNotFound)

def CheckForTypeMismatch(testCase, assertion):
    CheckForException(testCase, CheckForSuccess, assertion, AwaUnexpectedErrorException, AwaError.TypeMismatch)

def CheckForNotDefinedWhenAddingPath(testCase, assertion):
    CheckForException(testCase, CheckForSuccess, assertion, AwaUnexpectedErrorException, AwaError.NotDefined)

def CheckForPathInvalid(testCase, assertion):
    CheckForException(testCase, CheckForSuccess, assertion, AwaUnexpectedErrorException, AwaError.PathInvalid)
