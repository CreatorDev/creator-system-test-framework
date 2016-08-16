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
import binascii
import os
import os.path

from framework import awa_enums
from framework.awa_enums import AwaResourceType
from framework.awa_enums import AwaError
from framework.awa_enums import SessionType
from framework.awa_exceptions import AwaUnexpectedErrorException
from framework.awa_exceptions import AwaInvalidArgumentException
from framework.awa_exceptions import CheckNone
from framework.awa_exceptions import CheckSuccess

from gateway_xml_rpc import GatewayXmlRpc
from framework.gateway_client import GatewayClient

from framework import test_defaults
from framework import test_config


class GWClientXmlRpc(GatewayClient, GatewayXmlRpc):

    # Establish and maintain XMLRPC connection with GWClientHelper.
    def __init__(self, clientConfig):
        super(GWClientXmlRpc, self).__init__(test_config.config["proxies"][clientConfig["proxy"]])

        print ("Executing GWClientXmlRpc class constructor from: " + os.getcwd())

        pskIdentityFile = './pskIdentity'
        pskKeyFile = './pskKey'
        
        # Read PSK credentials
        pskIdentity = None
        pskKey = None
        
        if os.path.isfile(pskIdentityFile) and os.path.isfile(pskKeyFile):
            with open(pskIdentityFile, 'r') as identityFile:
                pskIdentity=identityFile.read().replace('\n', '')
            with open(pskKeyFile, 'r') as keyFile:
                pskKey=keyFile.read().replace('\n', '')

        self._clientConfig = clientConfig
        self._xmlrpcSession.setDaemonPath(test_config.config['paths']['awa-clientd'])
        self._xmlrpcSession.setDaemonIpcPort(self._clientConfig.get('ipc-port', None))
        self._xmlrpcSession.setDaemonCoapPort(self._clientConfig.get('port', None))
        self._xmlrpcSession.setDaemonAddressFamily(self._clientConfig.get('address-family', None))
        self._xmlrpcSession.setEndpointName(self._clientConfig.get('client-id', None))
        self._xmlrpcSession.setBootstrapURI(self._clientConfig.get('bootstrap-uri', None))
        self._xmlrpcSession.setFactoryBootstrapConfigFile(self._clientConfig.get('factory-bootstrap-config', None))
        self._xmlrpcSession.setDaemonLogFilename(self._clientConfig.get('log', None))
        self._xmlrpcSession.loadAwaLibrary(test_config.config['paths']['libawa'])
        self._xmlrpcSession.setPskIdentity(pskIdentity)
        self._xmlrpcSession.setPskKey(pskKey)
        self._xmlrpcSession.setCertificate(None)
        self._xmlrpcSession.setObjDefsFile(self._clientConfig.get('object-definitions-file', None))

        self._xmlrpcSession.initialiseDaemon()
        self._xmlrpcSession.startDaemon()
        self._session = self.CreateSession(self._clientConfig['ipc-address'], self._clientConfig['ipc-port'])

    def __del__(self):
        try:
            self.FreeSession(self._session)
        except AttributeError:
            pass
        self._xmlrpcSession.stopDaemon()
        del self._xmlrpcSession

    def AwaError_ToString(self, errorCode):
        return self._xmlrpcSession.AwaError_ToString(errorCode)

    def GetPathResultError(self, pathResult):
        return self._xmlrpcSession.AwaPathResult_GetError(pathResult)

    def GetPathResultLWM2MError(self, pathResult):
        return self._xmlrpcSession.AwaPathResult_GetLWM2MError(pathResult)

    def CreateSession(self, address, port):
        session = self._xmlrpcSession.AwaClientSession_New()
        CheckNone(session, "Session is NULL")
        try:
            CheckSuccess(self._xmlrpcSession.AwaClientSession_SetIPCAsUDP(session, address, int(port)), "Failed to set _session IPC connection as UDP")
            CheckSuccess(self._xmlrpcSession.AwaClientSession_Connect(session), "Failed to connect _session")
        except AwaUnexpectedErrorException as exception:
            self._xmlrpcSession.AwaClientSession_Free(session)
            raise exception
        return session

    def FreeSession(self, session):
        CheckSuccess(self._xmlrpcSession.AwaClientSession_Free(session), "Failed to free Client Session")

    def CreateGetOperation(self, session, path):
        CheckNone(session, "Session is NULL")

        getOperation = self._xmlrpcSession.AwaClientGetOperation_New(session)
        CheckNone(getOperation, "Get Operation is NULL")
        CheckSuccess(self._xmlrpcSession.AwaClientGetOperation_AddPath(getOperation, path), "Failed to add path to Get Operation: %s" % (path,))

        result = self._xmlrpcSession.AwaClientGetOperation_Perform(getOperation, test_defaults.TIMEOUT)
        response = self._xmlrpcSession.AwaClientGetOperation_GetResponse(getOperation)
        pathResult = None
        pathResultError = AwaError.Unspecified

        if response != None:
            pathResult = self._xmlrpcSession.AwaClientGetResponse_GetPathResult(response, path)
            pathResultError = self.GetPathResultError(pathResult)

        CheckSuccess(result, "Failed to perform Get Operation", pathResultError)

        return getOperation

    def FreeGetOperation(self, operation):
        CheckSuccess(self._xmlrpcSession.AwaClientGetOperation_Free(operation), "Failed to free Get Operation")

    def __GetResourceValueFromGetResponse(self, response, path, resourceType):
        value = None
        if resourceType == AwaResourceType.Integer:
            value, error = self._xmlrpcSession.AwaClientGetResponse_GetValueAsIntegerPointer(response, path, None)
            if value != None:
                value = pickle.loads(value)  # deserialise long integer
        elif resourceType == AwaResourceType.String:
            value, error = self._xmlrpcSession.AwaClientGetResponse_GetValueAsCStringPointer(response, path, None)
        elif resourceType == AwaResourceType.Float:
            value, error = self._xmlrpcSession.AwaClientGetResponse_GetValueAsFloatPointer(response, path, None)
        elif resourceType == AwaResourceType.Boolean:
            value, error = self._xmlrpcSession.AwaClientGetResponse_GetValueAsBooleanPointer(response, path, None)
        elif resourceType == AwaResourceType.Opaque:
            value, error = self._xmlrpcSession.AwaClientGetResponse_GetValueAsOpaque(response, path, None)
            if value != None:
                value = binascii.a2b_base64(value)  # deserialise opaque base64
        elif resourceType == AwaResourceType.ObjectLink:
            value, error = self._xmlrpcSession.AwaClientGetResponse_GetValueAsObjectLink(response, path, None)
        elif resourceType == AwaResourceType.Time:
            value, error = self._xmlrpcSession.AwaClientGetResponse_GetValueAsTimePointer(response, path, None)
            if value != None:
                value = pickle.loads(value)  # deserialise long integer
        else:
            raise AwaInvalidArgumentException("Invalid resource type", resourceType)

        CheckSuccess(error, "Failed to retrieve value on path %s" % (path, ))

        return value

    def __GetResourceValuesFromGetResponse(self, response, path, resourceType):
        values = None
        if resourceType == AwaResourceType.StringArray:
            values = pickle.loads(self._xmlrpcSession.AwaClientGetResponse_GetValuesAsStringArrayPointer(response, path, None))
        elif resourceType == AwaResourceType.IntegerArray:
            values = pickle.loads(self._xmlrpcSession.AwaClientGetResponse_GetValuesAsIntegerArrayPointer(response, path, None))
        elif resourceType == AwaResourceType.FloatArray:
            values = pickle.loads(self._xmlrpcSession.AwaClientGetResponse_GetValuesAsFloatArrayPointer(response, path, None))
        elif resourceType == AwaResourceType.BooleanArray:
            values = pickle.loads(self._xmlrpcSession.AwaClientGetResponse_GetValuesAsBooleanArrayPointer(response, path, None))
        elif resourceType == AwaResourceType.OpaqueArray:
            values = pickle.loads(self._xmlrpcSession.AwaClientGetResponse_GetValuesAsOpaqueArrayPointer(response, path, None))
        elif resourceType == AwaResourceType.TimeArray:
            values = pickle.loads(self._xmlrpcSession.AwaClientGetResponse_GetValuesAsTimeArrayPointer(response, path, None))
        elif resourceType == AwaResourceType.ObjectLinkArray:
            values = pickle.loads(self._xmlrpcSession.AwaClientGetResponse_GetValuesAsObjectLinkArrayPointer(response, path, None))
        else:
            raise AwaInvalidArgumentException("Invalid resource type", resourceType)

        #CheckSuccess(error, "Failed to retrieve values on path %s" % (path, ))

        return values

    def GetResourceValueFromGetOperation(self, operation, path, resourceType):
        if awa_enums.isArrayResourceType(resourceType):
            raise AwaInvalidArgumentException("resourceType is not single instance", resourceType)

        response = self._xmlrpcSession.AwaClientGetOperation_GetResponse(operation)
        CheckNone(response, "Response is NULL")
        value = self.__GetResourceValueFromGetResponse(response, path, resourceType)
        return value

    def GetResourceValuesFromGetOperation(self, operation, path, resourceType):
        if not awa_enums.isArrayResourceType(resourceType):
            raise AwaInvalidArgumentException("resourceType is not an array", resourceType)

        response = self._xmlrpcSession.AwaClientGetOperation_GetResponse(operation)
        CheckNone(response, "Response is NULL")
        values = self.__GetResourceValuesFromGetResponse(response, path, resourceType)
        return values

    def GetPathResultFromGetOperation(self, operation, path):
        response = self._xmlrpcSession.AwaClientGetOperation_GetResponse(operation)
        CheckNone(response, "Response is NULL")
        return self._xmlrpcSession.AwaClientGetResponse_GetPathResult(response, path)

    def GetSingleResource(self, path, resourceType):
        getOperation = self.CreateGetOperation(self._session, path)
        result = self.GetResourceValueFromGetOperation(getOperation, path, resourceType)
        self.FreeGetOperation(getOperation)
        return result

    def PerformSetOperation(self, setOperation, path=None):
        result = self._xmlrpcSession.AwaClientSetOperation_Perform(setOperation, test_defaults.TIMEOUT)
        response = self._xmlrpcSession.AwaClientSetOperation_GetResponse(setOperation)
        pathResult = None
        pathResultError = AwaError.Unspecified

        if path != None and response != None:
            pathResult = self._xmlrpcSession.AwaClientSetResponse_GetPathResult(response, path)
            pathResultError = self.GetPathResultError(pathResult)

        CheckSuccess(result, "Failed to perform Set Operation", pathResultError)
        CheckSuccess(self._xmlrpcSession.AwaClientSetOperation_Free(setOperation), "Failed to free Set Operation")

    def CreateSetOperation(self,session):
        setOperation = self._xmlrpcSession.AwaClientSetOperation_New(session)
        CheckNone(setOperation, "Set Operation is NULL")
        return setOperation

    def SetSingleInstanceResourceValue(self, setOperation, path, resourceType, value):
        result = AwaError.Unspecified

        if resourceType == AwaResourceType.Integer:
            result = self._xmlrpcSession.AwaClientSetOperation_AddValueAsInteger(setOperation, path, int(value))
        elif resourceType == AwaResourceType.String:
            result = self._xmlrpcSession.AwaClientSetOperation_AddValueAsCString(setOperation, path, str(value))
        elif resourceType == AwaResourceType.Float:
            result = self._xmlrpcSession.AwaClientSetOperation_AddValueAsFloat(setOperation, path, float(value))
        elif resourceType == AwaResourceType.Boolean:
            result = self._xmlrpcSession.AwaClientSetOperation_AddValueAsBoolean(setOperation, path, bool(value))
        elif resourceType == AwaResourceType.Opaque:
            result = self._xmlrpcSession.AwaClientSetOperation_AddValueAsOpaque(setOperation, path, value)
        elif resourceType == AwaResourceType.ObjectLink:
            result = self._xmlrpcSession.AwaClientSetOperation_AddValueAsObjectLink(setOperation, path, value)
        elif resourceType == AwaResourceType.Time:
            result = self._xmlrpcSession.AwaClientSetOperation_AddValueAsTime(setOperation, path, int(value))
        else:
            raise AwaInvalidArgumentException("Invalid resource type", resourceType)

        CheckSuccess(result, "Failed to add value to Set Operation: %s" % (str(value), ))

    def SetMultipleInstanceResourceValues(self, setOperation, path, resourceType, values):
        result = AwaError.Unspecified

        for resInstanceID, value in values.iteritems():
            if resourceType == AwaResourceType.IntegerArray:
                result = self._xmlrpcSession.AwaClientSetOperation_AddArrayValueAsInteger(setOperation, path, resInstanceID, int(value))
            elif resourceType == AwaResourceType.StringArray:
                result = self._xmlrpcSession.AwaClientSetOperation_AddArrayValueAsCString(setOperation, path, resInstanceID, str(value))
            elif resourceType == AwaResourceType.FloatArray:
                result = self._xmlrpcSession.AwaClientSetOperation_AddArrayValueAsFloat(setOperation, path, resInstanceID, float(value))
            elif resourceType == AwaResourceType.BooleanArray:
                result = self._xmlrpcSession.AwaClientSetOperation_AddArrayValueAsBoolean(setOperation, path, resInstanceID, bool(value))
            elif resourceType == AwaResourceType.OpaqueArray:
                result = self._xmlrpcSession.AwaClientSetOperation_AddArrayValueAsOpaque(setOperation, path, resInstanceID, value)
            elif resourceType == AwaResourceType.ObjectLinkArray:
                result = self._xmlrpcSession.AwaClientSetOperation_AddArrayValueAsObjectLink(setOperation, path, resInstanceID, value)
            elif resourceType == AwaResourceType.TimeArray:
                result = self._xmlrpcSession.AwaClientSetOperation_AddArrayValueAsTime(setOperation, path, resInstanceID, int(value))
            else:
                raise AwaInvalidArgumentException("Invalid resource type for key %s:" % (str(resInstanceID), ), resourceType)

        CheckSuccess(result, "Failed to add value to Set Operation: %s:%s" % (str(resInstanceID), str(value)))

    def SetMultipleInstanceResourceValuesAsArray(self, setOperation, path, resourceType, values):
        result = AwaError.Unspecified
        array = self.CreateArray(resourceType, values)

        if resourceType == AwaResourceType.IntegerArray:
            result = self._xmlrpcSession.AwaClientSetOperation_AddValueAsIntegerArray(setOperation, path, array)
        elif resourceType == AwaResourceType.StringArray:
            result = self._xmlrpcSession.AwaClientSetOperation_AddValueAsStringArray(setOperation, path, array)
        elif resourceType == AwaResourceType.FloatArray:
            result = self._xmlrpcSession.AwaClientSetOperation_AddValueAsFloatArray(setOperation, path, array)
        elif resourceType == AwaResourceType.BooleanArray:
            result = self._xmlrpcSession.AwaClientSetOperation_AddValueAsBooleanArray(setOperation, path, array)
        elif resourceType == AwaResourceType.OpaqueArray:
            result = self._xmlrpcSession.AwaClientSetOperation_AddValueAsOpaqueArray(setOperation, path, array)
        elif resourceType == AwaResourceType.ObjectLinkArray:
            result = self._xmlrpcSession.AwaClientSetOperation_AddValueAsObjectLinkArray(setOperation, path, array)
        elif resourceType == AwaResourceType.TimeArray:
            result = self._xmlrpcSession.AwaClientSetOperation_AddValueAsTimeArray(setOperation, path, array)
        else:
            raise AwaInvalidArgumentException("%s is not a valid multiple instance resource type" % (resourceType, ))

        CheckSuccess(result, "Failed to add values as array to Set Operation: %s" % (str(values), ))

    def SetCreateObjectInstance(self, setOperation, path):
        CheckNone(setOperation, "Set Operation is NULL")
        result = self._xmlrpcSession.AwaClientSetOperation_CreateObjectInstance(setOperation, path)
        CheckSuccess(result, "Failed to create object instance on path: %s" % (path, ))

    def SetCreateOptionalResource(self, setOperation, path):
        CheckNone(setOperation, "Set Operation is NULL")
        result = self._xmlrpcSession.AwaClientSetOperation_CreateOptionalResource(setOperation, path)
        CheckSuccess(result, "Failed to create object instance on path: %s" % (path, ))

    def _PerformDeleteOperation(self, deleteOperation, path):
        result = self._xmlrpcSession.AwaClientDeleteOperation_Perform(deleteOperation, test_defaults.TIMEOUT)
        response = self._xmlrpcSession.AwaClientDeleteOperation_GetResponse(deleteOperation)
        pathResult = None
        pathResultError = AwaError.Unspecified

        if response != None:
            pathResult = self._xmlrpcSession.AwaClientDeleteResponse_GetPathResult(response, path)
            pathResultError = self.GetPathResultError(pathResult)

        CheckSuccess(result, "Failed to perform Delete Operation", pathResultError)
        CheckSuccess(self._xmlrpcSession.AwaClientDeleteOperation_Free(deleteOperation), "Failed to free Delete Operation")

    def DeleteResourceInstancesWithArrayRange(self, session, path, startIndex, count):
        deleteOperation = self._xmlrpcSession.AwaClientDeleteOperation_New(session)
        CheckNone(deleteOperation, "Delete Operation is NULL")

        result = self._xmlrpcSession.AwaClientDeleteOperation_AddPathWithArrayRange(deleteOperation, path, startIndex, count)
        CheckSuccess(result, "Failed to add array range to Delete operation on path %s: %d, %d" % (path, startIndex, count))

        self._PerformDeleteOperation(deleteOperation, path)

    def DeleteEntity(self, session, path):
        CheckNone(session, "Session is NULL")

        deleteOperation = self._xmlrpcSession.AwaClientDeleteOperation_New(session)
        CheckNone(deleteOperation, "Delete Operation is NULL")

        result = self._xmlrpcSession.AwaClientDeleteOperation_AddPath(deleteOperation, path)
        CheckSuccess(result, "Failed to add path to Delete operation: %s" % (path, ))

        self._PerformDeleteOperation(deleteOperation, path)

    def CreateChangeSubscription(self, path):
        self._xmlrpcSession.AwaLog_SetLevel(3)
        changeSubscription = self._xmlrpcSession.AwaClientChangeSubscription_New(path, None, None)
        CheckNone(changeSubscription, "Could not create Change Subscription on path %s" % (path, ))
        return changeSubscription

    def CreateExecuteSubscription(self, path):
        executeSubscription = self._xmlrpcSession.AwaClientExecuteSubscription_New(path, None, None)
        CheckNone(executeSubscription, "Could not create Execute Subscription on path %s" % (path, ))
        return executeSubscription

    def FreeChangeSubscription(self, changeSubscription):
        result = self._xmlrpcSession.AwaClientChangeSubscription_Free(changeSubscription)
        CheckSuccess(result, "Failed to free Change Subscription")

    def FreeExecuteSubscription(self, executeSubscription):
        result = self._xmlrpcSession.AwaClientExecuteSubscription_Free(executeSubscription)
        CheckSuccess(result, "Failed to free Execute Subscription")

    def _PerformSubscribeOperation(self, subscribeOperation, path):
        result = self._xmlrpcSession.AwaClientSubscribeOperation_Perform(subscribeOperation, test_defaults.TIMEOUT)
        response = self._xmlrpcSession.AwaClientSubscribeOperation_GetResponse(subscribeOperation)

        pathResult = None
        pathResultError = AwaError.Unspecified

        if response != None:
            pathResult = self._xmlrpcSession.AwaClientSubscribeResponse_GetPathResult(response, path)
            pathResultError = self.GetPathResultError(pathResult)

        CheckSuccess(result, "Failed to perform Subscribe Operation", pathResultError)
        CheckSuccess(self._xmlrpcSession.AwaClientSubscribeOperation_Free(subscribeOperation), "Failed to free Subscribe Operation")

    def SubscribeToChange(self, session, changeSubscription):
        subscribeOperation = self._xmlrpcSession.AwaClientSubscribeOperation_New(session)
        CheckNone(subscribeOperation, "Subscribe Operation is NULL")

        path = self._xmlrpcSession.AwaClientChangeSubscription_GetPath(changeSubscription)
        CheckNone(path, "Failed to retrieve path from Change Subscription")

        result = self._xmlrpcSession.AwaClientSubscribeOperation_AddChangeSubscription(subscribeOperation, changeSubscription)
        CheckSuccess(result, "Failed to add change subscription to Subscribe Operation for path %s" % (path, ))

        self._PerformSubscribeOperation(subscribeOperation, path)

    def SubscribeToExecute(self, session, executeSubscription):
        subscribeOperation = self._xmlrpcSession.AwaClientSubscribeOperation_New(session)
        CheckNone(subscribeOperation, "Subscribe Operation is NULL")

        path = self._xmlrpcSession.AwaClientExecuteSubscription_GetPath(executeSubscription)
        CheckNone(path, "Failed to retrieve path from Execute Subscription")

        result = self._xmlrpcSession.AwaClientSubscribeOperation_AddExecuteSubscription(subscribeOperation, executeSubscription)
        CheckSuccess(result, "Failed to add change subscription to Subscribe Operation for path %s" % (path, ))

        self._PerformSubscribeOperation(subscribeOperation, path)

    def CancelSubscribeToChange(self, session, changeSubscription):
        subscribeOperation = self._xmlrpcSession.AwaClientSubscribeOperation_New(session)
        CheckNone(subscribeOperation, "Subscribe Operation is NULL")

        path = self._xmlrpcSession.AwaClientChangeSubscription_GetPath(changeSubscription)
        CheckNone(path, "Failed to retrieve path from Change Subscription")

        result = self._xmlrpcSession.AwaClientSubscribeOperation_AddCancelChangeSubscription(subscribeOperation, changeSubscription)
        CheckSuccess(result, "Failed to add Cancel Change Subscription to Subscribe Operation for path %s" % (path, ))

        self._PerformSubscribeOperation(subscribeOperation, path)

    def CancelSubscribeToExecute(self, session, executeSubscription):
        subscribeOperation = self._xmlrpcSession.AwaClientSubscribeOperation_New(session)
        CheckNone(subscribeOperation, "Subscribe Operation is NULL")

        path = self._xmlrpcSession.AwaClientExecuteSubscription_GetPath(executeSubscription)
        CheckNone(path, "Failed to retrieve path from Execute Subscription")

        result = self._xmlrpcSession.AwaClientSubscribeOperation_AddCancelExecuteSubscription(subscribeOperation, executeSubscription)
        CheckSuccess(result, "Failed to add Cancel Execute Subscription to Subscribe Operation for path %s" % (path, ))

        self._PerformSubscribeOperation(subscribeOperation, path)

    def ProcessAndGetNotifyResponse(self, session, timeout):
        result = self._xmlrpcSession.AwaClientSession_Process(session, timeout)
        CheckSuccess(result, "Failed to process client _session")
        result = self._xmlrpcSession.AwaClientSession_DispatchCallbacks(session)
        CheckSuccess(result, "Failed to dispatch callbacks for client _session")
        response = self.GetNotifyResponse()
        self._xmlrpcSession.ClearNotifyData()
        return response

    def WaitForNotification(self, session, path, resourceInstanceID=None):
        super(GWClientXmlRpc, self).WaitForNotificationWithSession(session, SessionType.Client, path, resourceInstanceID)

    def IsObjectDefined(self, session, objectID):
        return self._xmlrpcSession.AwaClientSession_IsObjectDefined(session, int(objectID))

    def GetObjectDefinition(self, session, objectID):
        objectDefinition = self._xmlrpcSession.AwaClientSession_GetObjectDefinition(session, objectID)
        CheckNone(objectDefinition, "No Object definition exists for ID %d" % (objectID, ))
        return objectDefinition

    def GetObjectID(self, objectDefinition):
        return self._xmlrpcSession.AwaObjectDefinition_GetID(objectDefinition)

    def GetObjectName(self, objectDefinition):
        return self._xmlrpcSession.AwaObjectDefinition_GetName(objectDefinition)

    def GetObjectMinimumInstances(self, objectDefinition):
        return self._xmlrpcSession.AwaObjectDefinition_GetMinimumInstances(objectDefinition)

    def GetObjectMaximumInstances(self, objectDefinition):
        return self._xmlrpcSession.AwaObjectDefinition_GetMaximumInstances(objectDefinition)

    def IsResourceDefined(self, objectDefinition, resourceID):
        return self._xmlrpcSession.AwaObjectDefinition_IsResourceDefined(objectDefinition,resourceID)

    def GetResourceDefinition(self, objectDefinition, resourceID):
        resourceDefinition = self._xmlrpcSession.AwaObjectDefinition_GetResourceDefinition(objectDefinition,resourceID)
        CheckNone(resourceDefinition, "No Resource definition exists for ID %d" % (resourceID, ))
        return resourceDefinition

    def GetResourceID(self, resourceDefinition):
        return self._xmlrpcSession.AwaResourceDefinition_GetID(resourceDefinition)

    def GetResourceName(self, resourceDefinition):
        return self._xmlrpcSession.AwaResourceDefinition_GetName(resourceDefinition)

    def IsResourceMandatory(self, resourceDefinition):
        return self._xmlrpcSession.AwaResourceDefinition_IsMandatory(resourceDefinition)

    def GetResourceType(self, resourceDefinition):
        return self._xmlrpcSession.AwaResourceDefinition_GetType(resourceDefinition)

    def GetResourceSupportedOperations(self, resourceDefinition):
        return self._xmlrpcSession.AwaResourceDefinition_GetSupportedOperations(resourceDefinition)

    def GetResourceMaximumInstances(self, resourceDefinition):
        return self._xmlrpcSession.AwaResourceDefinition_GetMaximumInstances(resourceDefinition)

    def GetResourceMinimumInstances(self, resourceDefinition):
        return self._xmlrpcSession.AwaResourceDefinition_GetMinimumInstances(resourceDefinition)

    def DefineWithSession(self, session, objectDefinitionSettings, resourceDefinitionSettingsCollection):
        defineOperation = self._xmlrpcSession.AwaClientDefineOperation_New(session)
        CheckNone(defineOperation, "Define Operation is NULL")

        objectDefinition = self._xmlrpcSession.AwaObjectDefinition_New(objectDefinitionSettings.objectID, objectDefinitionSettings.objectName,
                                                                      objectDefinitionSettings.minimumInstances, objectDefinitionSettings.maximumInstances)
        CheckNone(objectDefinition, "Could not create object definition for objectID %d" % (objectDefinitionSettings.objectID, ))

        for resourceDefinitionSettings in resourceDefinitionSettingsCollection:
            if awa_enums.isArrayResourceType(resourceDefinitionSettings.resourceType):
                self.DefineMultipleInstanceResource(objectDefinition, resourceDefinitionSettings.resourceID, resourceDefinitionSettings.resourceName,
                                                resourceDefinitionSettings.resourceType, resourceDefinitionSettings.minimumInstances,
                                                resourceDefinitionSettings.maximumInstances, int(resourceDefinitionSettings.supportedOperations),
                                                resourceDefinitionSettings.defaultValue)
            else:
                self.DefineSingleInstanceResource(objectDefinition, resourceDefinitionSettings.resourceID, resourceDefinitionSettings.resourceName,
                                              resourceDefinitionSettings.resourceType, resourceDefinitionSettings.minimumInstances > 0,
                                              int(resourceDefinitionSettings.supportedOperations), resourceDefinitionSettings.defaultValue)

        result = self._xmlrpcSession.AwaClientDefineOperation_Add(defineOperation, objectDefinition)
        CheckSuccess(result, "Could not add object definition to Define Operation")

        result = self._xmlrpcSession.AwaClientDefineOperation_Perform(defineOperation, test_defaults.TIMEOUT)
        CheckSuccess(result, "Failed to perform Define Operation")

        result = self._xmlrpcSession.AwaClientDefineOperation_Free(defineOperation)
        CheckSuccess(result, "Failed to free Define Operation")

    def CreateObjectDefinitionIterator(self, session):
        return self._xmlrpcSession.AwaClientSession_NewObjectDefinitionIterator(self._session)

    def GetNextObjectDefinitionFromIterator(self, iterator):
        if self._xmlrpcSession.AwaObjectDefinitionIterator_Next(iterator):
            return self._xmlrpcSession.AwaObjectDefinitionIterator_Get(iterator)
        else:
            return None
