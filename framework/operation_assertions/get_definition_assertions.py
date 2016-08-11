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

OBJECT_NOT_DEFINED = "Object not defined"
RESOURCE_NOT_DEFINED = "Resource not defined"

# FIXME ipcAddress, ipcPort should come from somewhere else

def CheckForSuccess(handler, session, testCase, assertion):
    testCase.assertTrue(handler.IsObjectDefined(session, assertion.objectDefinitionSettings.objectID), OBJECT_NOT_DEFINED)
    objectDefinition = handler.GetObjectDefinition(session, assertion.objectDefinitionSettings.objectID)
    testCase.assertIsNotNone(objectDefinition)
    testCase.assertEqual(assertion.objectDefinitionSettings.objectID, handler.GetObjectID(objectDefinition))
    testCase.assertEqual(assertion.objectDefinitionSettings.objectName, handler.GetObjectName(objectDefinition))
    testCase.assertEqual(assertion.objectDefinitionSettings.minimumInstances, handler.GetObjectMinimumInstances(objectDefinition))
    testCase.assertEqual(assertion.objectDefinitionSettings.maximumInstances, handler.GetObjectMaximumInstances(objectDefinition))

    if assertion.resourceDefinitionSettingsCollection != None:
        for resourceDefinitionSettings in assertion.resourceDefinitionSettingsCollection:
            testCase.assertTrue(handler.IsResourceDefined(objectDefinition, resourceDefinitionSettings.resourceID), RESOURCE_NOT_DEFINED)
            resourceDefinition = handler.GetResourceDefinition(objectDefinition, resourceDefinitionSettings.resourceID)
            testCase.assertIsNotNone(resourceDefinition)
            testCase.assertEqual(resourceDefinitionSettings.resourceID, handler.GetResourceID(resourceDefinition))
            testCase.assertEqual(resourceDefinitionSettings.resourceName, handler.GetResourceName(resourceDefinition))
            testCase.assertEqual(resourceDefinitionSettings.resourceType, handler.GetResourceType(resourceDefinition))
            testCase.assertEqual(resourceDefinitionSettings.supportedOperations, handler.GetResourceSupportedOperations(resourceDefinition))
            testCase.assertEqual(resourceDefinitionSettings.minimumInstances, handler.GetResourceMinimumInstances(resourceDefinition))
            testCase.assertEqual(resourceDefinitionSettings.maximumInstances, handler.GetResourceMaximumInstances(resourceDefinition))
            testCase.assertEqual(resourceDefinitionSettings.minimumInstances > 0, handler.IsResourceMandatory(resourceDefinition))

def CheckForFailureWithMessage(handler, session, testCase, assertion, message):
    try:
        CheckForSuccess(handler, session, testCase, assertion)
    except AssertionError as exceptionContext:
        testCase.assertEqual(exceptionContext.args[0], message)
    else:
        testCase.fail("AssertionError was not thrown")

def CheckForObjectNotDefined(handler, session, testCase, assertion):
    CheckForFailureWithMessage(handler, session, testCase, assertion, OBJECT_NOT_DEFINED)

def CheckForResourceNotDefined(handler, session, testCase, assertion):
    CheckForFailureWithMessage(handler, session, testCase, assertion, RESOURCE_NOT_DEFINED)
