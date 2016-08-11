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
import abc

from framework.awa_enums import AwaResourceType
from framework.awa_enums import SessionType
from framework.awa_exceptions import AwaInvalidArgumentException
from framework.awa_exceptions import NoNotificationReceivedException
from framework.awa_exceptions import CheckSuccess

from xml_rpc_client import XmlRpcClient

from framework import test_defaults

class GatewayXmlRpc(XmlRpcClient):
    __metaclass__ = abc.ABCMeta

    def __init__(self, xmlRpcServerConfig):
        super(GatewayXmlRpc, self).__init__(xmlRpcServerConfig)
        pass


    def CreateArray(self, resType, values):
        array = None
        if values != None:
            if resType == AwaResourceType.StringArray:
                array = self._xmlrpcSession.AwaStringArray_New()
                for index, value in values.iteritems():
                    self._xmlrpcSession.AwaStringArray_SetValueAsCString(array, index, value)
            elif resType == AwaResourceType.IntegerArray:
                array = self._xmlrpcSession.AwaStringArray_New()
                for index, value in values.iteritems():
                    self._xmlrpcSession.AwaIntegerArray_SetValue(array, index, value)
            #elif TODO rest of array types
            else:
                raise AwaInvalidArgumentException("Unsupported resource type: " + str(resType))
        return array

    def FreeArray(self, resType, array):
        result = None
        if resType == AwaResourceType.StringArray:
            result = self._xmlrpcSession.AwaStringArray_Free(array)
        if resType == AwaResourceType.IntegerArray:
            result = self._xmlrpcSession.AwaIntegerArray_Free(array)
        if resType == AwaResourceType.FloatArray:
            result = self._xmlrpcSession.AwaFloatArray_Free(array)
        if resType == AwaResourceType.TimeArray:
            result = self._xmlrpcSession.AwaTimeArray_Free(array)
        if resType == AwaResourceType.OpaqueArray:
            result = self._xmlrpcSession.AwaOpaqueArray_Free(array)
        if resType == AwaResourceType.ObjectLinkArray:
            result = self._xmlrpcSession.AwaObjectLinkArray_Free(array)
        #elif TODO rest of array types
        else:
            raise AwaInvalidArgumentException("Unsupported resource type: " + str(resType))
        return result

    def DefineSingleInstanceResource(self, objectDefinition, resourceID, resourceName, resourceType, isMandatory, operations, defaultValue):

        if resourceType == AwaResourceType.String:
            result = self._xmlrpcSession.AwaObjectDefinition_AddResourceDefinitionAsString(objectDefinition, resourceID, resourceName, isMandatory, operations, defaultValue)
        elif resourceType == AwaResourceType.Integer:
            result = self._xmlrpcSession.AwaObjectDefinition_AddResourceDefinitionAsInteger(objectDefinition, resourceID, resourceName, isMandatory, operations, defaultValue)
        elif resourceType == AwaResourceType.Float:
            result = self._xmlrpcSession.AwaObjectDefinition_AddResourceDefinitionAsFloat(objectDefinition, resourceID, resourceName, isMandatory, operations, defaultValue)
        elif resourceType == AwaResourceType.Boolean:
            result = self._xmlrpcSession.AwaObjectDefinition_AddResourceDefinitionAsBoolean(objectDefinition, resourceID, resourceName, isMandatory, operations, defaultValue)
        elif resourceType == AwaResourceType.Time:
            result = self._xmlrpcSession.AwaObjectDefinition_AddResourceDefinitionAsTime(objectDefinition, resourceID, resourceName, isMandatory, operations, defaultValue)
        elif resourceType == AwaResourceType.Opaque:
            result = self._xmlrpcSession.AwaObjectDefinition_AddResourceDefinitionAsOpaque(objectDefinition, resourceID, resourceName, isMandatory, operations, defaultValue)
        elif resourceType == AwaResourceType.ObjectLink:
            result = self._xmlrpcSession.AwaObjectDefinition_AddResourceDefinitionAsObjectLink(objectDefinition, resourceID, resourceName, isMandatory, operations, defaultValue)
        elif resourceType == AwaResourceType.NoneType:
            result = self._xmlrpcSession.AwaObjectDefinition_AddResourceDefinitionAsNoType(objectDefinition, resourceID, resourceName, isMandatory, operations)
        else:
            raise AwaInvalidArgumentException("Invalid resource type for single instance resource %s:" % (str(AwaResourceType(resourceType), )))

        CheckSuccess(result, "Could not add resource definition to object definition")

    def DefineMultipleInstanceResource(self, objectDefinition, resourceID, resourceName, resourceType, resMinInstance, resMaxInstance, operations, defaultValues):
        defaultArray = self.CreateArray(resourceType, defaultValues)

        if resourceType == AwaResourceType.StringArray:
            result = self._xmlrpcSession.AwaObjectDefinition_AddResourceDefinitionAsStringArray(objectDefinition, resourceID, resourceName, resMinInstance, resMaxInstance, operations, defaultArray)
        elif resourceType == AwaResourceType.IntegerArray:
            result = self._xmlrpcSession.AwaObjectDefinition_AddResourceDefinitionAsIntegerArray(objectDefinition, resourceID, resourceName, resMinInstance, resMaxInstance, operations, defaultArray)
        elif resourceType == AwaResourceType.FloatArray:
            result = self._xmlrpcSession.AwaObjectDefinition_AddResourceDefinitionAsFloatArray(objectDefinition, resourceID, resourceName, resMinInstance, resMaxInstance, operations, defaultArray)
        elif resourceType == AwaResourceType.BooleanArray:
            result = self._xmlrpcSession.AwaObjectDefinition_AddResourceDefinitionAsBooleanArray(objectDefinition, resourceID, resourceName, resMinInstance, resMaxInstance, operations, defaultArray)
        elif resourceType == AwaResourceType.TimeArray:
            result = self._xmlrpcSession.AwaObjectDefinition_AddResourceDefinitionAsTimeArray(objectDefinition, resourceID, resourceName, resMinInstance, resMaxInstance, operations, defaultArray)
        elif resourceType == AwaResourceType.OpaqueArray:
            result = self._xmlrpcSession.AwaObjectDefinition_AddResourceDefinitionAsOpaqueArray(objectDefinition, resourceID, resourceName, resMinInstance, resMaxInstance, operations, defaultArray)
        elif resourceType == AwaResourceType.ObjectLinkArray:
            result = self._xmlrpcSession.AwaObjectDefinition_AddResourceDefinitionAsObjectLinkArray(objectDefinition, resourceID, resourceName, resMinInstance, resMaxInstance, operations, defaultArray)
        else:
            raise AwaInvalidArgumentException("Invalid resource type for single instance resource %s:" % (str(AwaResourceType(resourceType), )))

        CheckSuccess(result, "Could not add resource definition to object definition")


    def WaitForNotificationWithSession(self, session, sessionType, path, resourceInstanceID=None):
        timeout = test_defaults.TIMEOUT

        while timeout > 0:
            #print "Waiting for notification..."
            if sessionType == SessionType.Client:
                result = self._xmlrpcSession.AwaClientSession_Process(session, 1000)
                CheckSuccess(result, "Failed to process client session")
                result = self._xmlrpcSession.AwaClientSession_DispatchCallbacks(session)
                CheckSuccess(result, "Failed to dispatch callbacks for client session")
            else:
                result = self._xmlrpcSession.AwaServerSession_Process(session, 1000)
                CheckSuccess(result, "Failed to process server session")
                result = self._xmlrpcSession.AwaServerSession_DispatchCallbacks(session)
                CheckSuccess(result, "Failed to dispatch callbacks for server session")

            notifyResponse = self.GetNotifyResponse()
            if notifyResponse is not None and path in notifyResponse:
                if resourceInstanceID is None:
                    #print "Got Notify on resource %s with value: %s" % (path, str(notifyResponse[path]))
                    break
                elif resourceInstanceID in notifyResponse[path]:
                    #print "Got Notify on resource %s with value: %s" % (path, str(notifyResponse[path]))
                    #print "Resource instance %d: %s" % (resourceInstanceID, str(notifyResponse[path][resourceInstanceID]))
                    break
            timeout -= 1000
        if timeout <= 0:
            errorMessage = "No notification received for path %s" % (path, )
            if resourceInstanceID != None:
                errorMessage += "(ResourceInstanceID = " + str(resourceInstanceID) + ")"
            raise NoNotificationReceivedException(errorMessage)

    #Notify response handling callback
    #NB: Opaque resources are Base64 encoded.
    def GetNotifyResponse(self, path=None):
        notifyResponse = self._xmlrpcSession.Awa_GetNotifyData()
        if notifyResponse is not None:
            # deserialise encoded object to dictionary of <path, value> pairs
            notifyResponse = pickle.loads(notifyResponse)
            #print "Notify response: " + str(notifyResponse)
            if path is not None:
                if path in notifyResponse:
                    notifyResponse = notifyResponse[path]
                else:
                    notifyResponse = None
        return notifyResponse
