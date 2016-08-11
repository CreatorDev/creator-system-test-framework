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

import sys
from abc import ABCMeta

from framework.awa_enums import AwaError
from framework.awa_enums import AwaLWM2MError
from framework.awa_enums import AwaWriteMode
from framework.awa_exceptions import AwaUnexpectedErrorException

class Assertion(object):
    __metaclass__ = ABCMeta
    def __init__(self, function, path):
        self.function = function
        self.path = path

class GetAssertion(Assertion):
    def __init__(self, function, path, resourceType, expectedValue):
        super(GetAssertion, self).__init__(function, path)
        self.resourceType = resourceType
        self.expectedValue = expectedValue

class SetAssertion(Assertion):
    def __init__(self, function, path, resourceType, value, createInstance=False, createResource=False, appendArray=False):
        super(SetAssertion, self).__init__(function, path)
        self.resourceType = resourceType
        self.value = value
        self.createInstance = createInstance
        self.createResource = createResource
        self.appendArray = appendArray

class SubscribeAssertion(Assertion):
    def __init__(self, function, path, resourceType, expectedValue, setWithDaemon, appendArray=False):
        super(SubscribeAssertion, self).__init__(function, path)
        self.resourceType = resourceType
        self.expectedValue = expectedValue
        self.setWithDaemon = setWithDaemon
        self.appendArray = appendArray

class DefineOperationAssertion(Assertion):
    def __init__(self, function, objectDefinitionSettings, resourceDefinitionSettingsCollection):
        super(DefineOperationAssertion, self).__init__(function, None)
        self.objectDefinitionSettings = objectDefinitionSettings
        self.resourceDefinitionSettingsCollection = resourceDefinitionSettingsCollection

class GetDefinitionAssertion(Assertion):
    def __init__(self, function, objectDefinitionSettings, resourceDefinitionSettingsCollection):
        super(GetDefinitionAssertion, self).__init__(function, None)
        self.objectDefinitionSettings = objectDefinitionSettings
        self.resourceDefinitionSettingsCollection = resourceDefinitionSettingsCollection

class DeleteAssertion(Assertion):
    def __init__(self, function, path, startIndex=None, count=None):
        super(DeleteAssertion, self).__init__(function, path)
        self.startIndex = startIndex
        self.count = count

class ReadAssertion(Assertion):
    def __init__(self, function, path, resourceType, expectedValue):
        super(ReadAssertion, self).__init__(function, path)
        self.resourceType = resourceType
        self.expectedValue = expectedValue

class WriteAssertion(Assertion):
    def __init__(self, function, path, resourceType, value, createInstance=False, createResource=False, writeMode=AwaWriteMode.Update):
        super(WriteAssertion, self).__init__(function, path)
        self.resourceType = resourceType
        self.value = value
        self.createInstance = createInstance
        self.createResource = createResource
        self.writeMode = writeMode

class ObserveAssertion(Assertion):
    def __init__(self, function, path, resourceType, expectedValue, writeWithDaemon, writeMode=AwaWriteMode.Update):
        super(ObserveAssertion, self).__init__(function, path)
        self.resourceType = resourceType
        self.expectedValue = expectedValue
        self.writeWithDaemon = writeWithDaemon
        self.writeMode = writeMode

class CloudGetAssertion(Assertion):
    def __init__(self, function, path, expectedValue):
        super(CloudGetAssertion, self).__init__(function, path)
        self.function = function
        self.expectedValue = expectedValue

class CloudSetAssertion(Assertion):
    def __init__(self, function, path, value):
        super(CloudSetAssertion, self).__init__(function, path)
        self.function = function
        self.value = value

class ListClientsAssertion(Assertion):
    def __init__(self, function, clientID, path):
        super(ListClientsAssertion, self).__init__(function, path)
        self.clientID = clientID

def callAssertions(testCase, assertions):
    assertionIndex = 0
    for assertion in assertions:
        try:
            assertion.function(testCase, assertion)
            assertionIndex += 1
        except AwaUnexpectedErrorException as e:
            errorMessage = "Unexpected AwaError received: " + str(AwaError(e.args[1]))
            errorMessage += " (pathResultError = " + str(AwaError(e.args[2])) +") expected: " + str(e.args[0])
            if e.args[2] == AwaError.LWM2MError:
                errorMessage += " (LWM2MError = " + str(AwaLWM2MError(e.args[3])) +") expected: " + str(e.args[0])
            if assertion.path != None:
                errorMessage += "\npath: " + assertion.path
            errorMessage += "\nassertion index: " + str(assertionIndex)
            import traceback
            errorMessage += "\nOriginal exception: %s" % (traceback.format_exc(), )
            testCase.fail(errorMessage), sys.exc_info()[2]
        except AssertionError as e:
            additionalErrorMessage = "\nUnexpected AssertionError on assertion index %d" % (assertionIndex, )
            import sys
            raise type(e), type(e)(e.message + additionalErrorMessage), sys.exc_info()[2]


