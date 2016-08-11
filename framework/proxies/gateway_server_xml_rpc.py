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

from framework import test_config
from framework import test_defaults
from framework import awa_enums
from framework.awa_enums import AwaResourceType
from framework.awa_enums import AwaError
from framework.awa_enums import AwaLWM2MError
from framework.awa_enums import SessionType
from framework.awa_exceptions import AwaUnexpectedErrorException
from framework.awa_exceptions import AwaInvalidArgumentException
from framework.awa_exceptions import CheckNone
from framework.awa_exceptions import CheckSuccess
from framework.gateway_server import GatewayServer

from gateway_xml_rpc import GatewayXmlRpc

class GwServerXmlRpcException(Exception):
    pass

class GWServerXmlRpc(GatewayServer, GatewayXmlRpc):

    # FIXME: Move duplication between client and server to parent class
    def __init__(self, serverConfig):
        super(GWServerXmlRpc, self).__init__(test_config.config["proxies"][serverConfig["proxy"]])

        self._serverConfig = serverConfig

        self._xmlrpcSession.setDaemonPath(test_config.config['paths']['awa-serverd'])
        self._xmlrpcSession.setDaemonIPAddress(self._serverConfig.get('ip-address', None))
        self._xmlrpcSession.setDaemonCoapPort(self._serverConfig.get('port', None))
        self._xmlrpcSession.setDaemonLogFilename(self._serverConfig.get('log', None))
        self._xmlrpcSession.setDaemonIpcPort(self._serverConfig.get('ipc-port', None))
        self._xmlrpcSession.setDaemonNetworkInterface(self._serverConfig.get('interface', None))
        self._xmlrpcSession.setDaemonAddressFamily(self._serverConfig.get('address-family', None))
        self._xmlrpcSession.setDefaultContentType(self._serverConfig.get('content-type', None))
        self._xmlrpcSession.loadAwaLibrary(test_config.config['paths']['libawa'])

        self._xmlrpcSession.initialiseDaemon()
        self._xmlrpcSession.startDaemon()
        self._session = self.CreateSession(self._serverConfig['ipc-address'], self._serverConfig['ipc-port'])

    def __del__(self):
        print "calling stopXMLRPCServer for GW Server..."
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
        session = self._xmlrpcSession.AwaServerSession_New()
        CheckNone(session, "Session is NULL")
        try:
            CheckSuccess(self._xmlrpcSession.AwaServerSession_SetIPCAsUDP(session, address, int(port)), "Failed to set _session IPC connection as UDP")
            CheckSuccess(self._xmlrpcSession.AwaServerSession_Connect(session), "Failed to connect _session")
        except AwaUnexpectedErrorException as exception:
            self._xmlrpcSession.AwaServerSession_Free(session)
            raise exception
        return session

    def FreeSession(self, session):
        CheckSuccess(self._xmlrpcSession.AwaServerSession_Free(session), "Failed to free Server Session")


    def CreateReadOperation(self, session, clientID, path):
        CheckNone(session, "Session is NULL")

        readOperation = self._xmlrpcSession.AwaServerReadOperation_New(session)
        CheckNone(readOperation, "Read Operation is NULL")
        CheckSuccess(self._xmlrpcSession.AwaServerReadOperation_AddPath(readOperation, clientID, path), "Failed to add path to Read Operation: %s (clientID = %s)" % (path, clientID))

        result = self._xmlrpcSession.AwaServerReadOperation_Perform(readOperation, test_defaults.TIMEOUT)
        response = self._xmlrpcSession.AwaServerReadOperation_GetResponse(readOperation, clientID)
        pathResult = None
        pathResultError = AwaError.Unspecified
        pathResultLWM2MError = AwaLWM2MError.Unspecified

        if response != None:
            pathResult = self.GetPathResultFromReadOperation(readOperation, clientID, path)
            pathResultError = self.GetPathResultError(pathResult)
            pathResultLWM2MError = self.GetPathResultLWM2MError(pathResult)

        CheckSuccess(result, "Failed to perform Read Operation", pathResultError, pathResultLWM2MError)

        return readOperation

    def FreeReadOperation(self, operation):
        CheckSuccess(self._xmlrpcSession.AwaServerReadOperation_Free(operation), "Failed to free Read Operation")

    def __GetResourceValueFromReadResponse(self, response, path, resourceType):
        value = None
        if resourceType == AwaResourceType.Integer:
            value, error = self._xmlrpcSession.AwaServerReadResponse_GetValueAsIntegerPointer(response, path, None)
            if value != None:
                value = pickle.loads(value)  # deserialise long integer
        elif resourceType == AwaResourceType.String:
            value, error = self._xmlrpcSession.AwaServerReadResponse_GetValueAsCStringPointer(response, path, None)
        elif resourceType == AwaResourceType.Float:
            value, error = self._xmlrpcSession.AwaServerReadResponse_GetValueAsFloatPointer(response, path, None)
        elif resourceType == AwaResourceType.Boolean:
            value, error = self._xmlrpcSession.AwaServerReadResponse_GetValueAsBooleanPointer(response, path, None)
        elif resourceType == AwaResourceType.Opaque:
            value, error = self._xmlrpcSession.AwaServerReadResponse_GetValueAsOpaque(response, path, None)
            if value != None:
                value = binascii.a2b_base64(value)  # deserialise opaque base64
        elif resourceType == AwaResourceType.ObjectLink:
            value, error = self._xmlrpcSession.AwaServerReadResponse_GetValueAsObjectLink(response, path, None)
        elif resourceType == AwaResourceType.Time:
            value, error = self._xmlrpcSession.AwaServerReadResponse_GetValueAsTimePointer(response, path, None)
            if value != None:
                value = pickle.loads(value)  # deserialise long integer
        else:
            raise AwaInvalidArgumentException("Invalid resource type", resourceType)

        CheckSuccess(error, "Failed to retrieve value on path %s" % (path, ))

        return value

    def __GetResourceValuesFromReadResponse(self, response, path, resourceType):
        values = None
        if resourceType == AwaResourceType.StringArray:
            values = pickle.loads(self._xmlrpcSession.AwaServerReadResponse_GetValuesAsStringArrayPointer(response, path, None))
        elif resourceType == AwaResourceType.IntegerArray:
            values = pickle.loads(self._xmlrpcSession.AwaServerReadResponse_GetValuesAsIntegerArrayPointer(response, path, None))
        elif resourceType == AwaResourceType.FloatArray:
            values = pickle.loads(self._xmlrpcSession.AwaServerReadResponse_GetValuesAsFloatArrayPointer(response, path, None))
        elif resourceType == AwaResourceType.BooleanArray:
            values = pickle.loads(self._xmlrpcSession.AwaServerReadResponse_GetValuesAsBooleanArrayPointer(response, path, None))
        elif resourceType == AwaResourceType.OpaqueArray:
            values = pickle.loads(self._xmlrpcSession.AwaServerReadResponse_GetValuesAsOpaqueArrayPointer(response, path, None))
        elif resourceType == AwaResourceType.TimeArray:
            values = pickle.loads(self._xmlrpcSession.AwaServerReadResponse_GetValuesAsTimeArrayPointer(response, path, None))
        elif resourceType == AwaResourceType.ObjectLinkArray:
            values = pickle.loads(self._xmlrpcSession.AwaServerReadResponse_GetValuesAsObjectLinkArrayPointer(response, path, None))
        else:
            raise AwaInvalidArgumentException("Invalid resource type", resourceType)

        #CheckSuccess(error, "Failed to retrieve values on path %s" % (path, ))

        return values

    def GetResourceValueFromReadOperation(self, operation, clientID, path, resourceType):
        if awa_enums.isArrayResourceType(resourceType):
            raise AwaInvalidArgumentException("resourceType is not single instance", resourceType)

        response = self._xmlrpcSession.AwaServerReadOperation_GetResponse(operation, clientID)
        CheckNone(response, "Response is NULL")
        value = self.__GetResourceValueFromReadResponse(response, path, resourceType)
        return value

    def GetResourceValuesFromReadOperation(self, operation, clientID, path, resourceType):
        if not awa_enums.isArrayResourceType(resourceType):
            raise AwaInvalidArgumentException("resourceType is not an array", resourceType)

        response = self._xmlrpcSession.AwaServerReadOperation_GetResponse(operation, clientID)
        CheckNone(response, "Response is NULL")
        values = self.__GetResourceValuesFromReadResponse(response, path, resourceType)
        return values
    
    def ReadSingleResource(self, clientID, path, resourceType):
        readOperation = self.CreateReadOperation(self._session, clientID, path)
        result = self.GetResourceValueFromReadOperation(readOperation, clientID, path, resourceType)
        self.FreeReadOperation(readOperation)
        return result

    def GetPathResultFromReadOperation(self, operation, clientID, path):
        response = self._xmlrpcSession.AwaServerReadOperation_GetResponse(operation, clientID)
        CheckNone(response, "Response is NULL")
        return self._xmlrpcSession.AwaServerReadResponse_GetPathResult(response, path)

    def PerformWriteOperation(self, writeOperation, clientID, path):
        result = self._xmlrpcSession.AwaServerWriteOperation_Perform(writeOperation, clientID, test_defaults.TIMEOUT)
        response = self._xmlrpcSession.AwaServerWriteOperation_GetResponse(writeOperation, clientID)
        pathResult = None
        pathResultError = AwaError.Unspecified
        pathResultLWM2MError = AwaLWM2MError.Unspecified

        if response != None:
            pathResult = self._xmlrpcSession.AwaServerWriteResponse_GetPathResult(response, path)
            pathResultError = self.GetPathResultError(pathResult)
            pathResultLWM2MError = self.GetPathResultLWM2MError(pathResult)

        CheckSuccess(result, "Failed to perform Write Operation", pathResultError, pathResultLWM2MError)
        CheckSuccess(self._xmlrpcSession.AwaServerWriteOperation_Free(writeOperation), "Failed to free Write Operation")

    def CreateWriteOperation(self, session, writeMode):
        writeOperation = self._xmlrpcSession.AwaServerWriteOperation_New(session, int(writeMode))
        CheckNone(writeOperation, "Write Operation is NULL")
        return writeOperation

    def WriteSingleInstanceResourceValue(self, writeOperation, path, resourceType, value):
        result = AwaError.Unspecified

        if resourceType == AwaResourceType.Integer:
            result = self._xmlrpcSession.AwaServerWriteOperation_AddValueAsInteger(writeOperation, path, int(value))
        elif resourceType == AwaResourceType.String:
            result = self._xmlrpcSession.AwaServerWriteOperation_AddValueAsCString(writeOperation, path, str(value))
        elif resourceType == AwaResourceType.Float:
            result = self._xmlrpcSession.AwaServerWriteOperation_AddValueAsFloat(writeOperation, path, float(value))
        elif resourceType == AwaResourceType.Boolean:
            result = self._xmlrpcSession.AwaServerWriteOperation_AddValueAsBoolean(writeOperation, path, bool(value))
        elif resourceType == AwaResourceType.Opaque:
            result = self._xmlrpcSession.AwaServerWriteOperation_AddValueAsOpaque(writeOperation, path, value)
        elif resourceType == AwaResourceType.ObjectLink:
            result = self._xmlrpcSession.AwaServerWriteOperation_AddValueAsObjectLink(writeOperation, path, value)
        elif resourceType == AwaResourceType.Time:
            result = self._xmlrpcSession.AwaServerWriteOperation_AddValueAsTime(writeOperation, path, int(value))
        else:
            raise AwaInvalidArgumentException("Invalid resource type", resourceType)

        CheckSuccess(result, "Failed to add value to Write Operation: %s" % (str(value), ))

    def WriteMultipleInstanceResourceValues(self, writeOperation, path, resourceType, values):
        result = AwaError.Unspecified
        array = self.CreateArray(resourceType, values)

        if resourceType == AwaResourceType.IntegerArray:
            result = self._xmlrpcSession.AwaServerWriteOperation_AddValueAsIntegerArray(writeOperation, path, array)
        elif resourceType == AwaResourceType.StringArray:
            result = self._xmlrpcSession.AwaServerWriteOperation_AddValueAsStringArray(writeOperation, path, array)
        elif resourceType == AwaResourceType.FloatArray:
            result = self._xmlrpcSession.AwaServerWriteOperation_AddValueAsFloatArray(writeOperation, path, array)
        elif resourceType == AwaResourceType.BooleanArray:
            result = self._xmlrpcSession.AwaServerWriteOperation_AddValueAsBooleanArray(writeOperation, path, array)
        elif resourceType == AwaResourceType.OpaqueArray:
            result = self._xmlrpcSession.AwaServerWriteOperation_AddValueAsOpaqueArray(writeOperation, path, array)
        elif resourceType == AwaResourceType.ObjectLinkArray:
            result = self._xmlrpcSession.AwaServerWriteOperation_AddValueAsObjectLinkArray(writeOperation, path, array)
        elif resourceType == AwaResourceType.TimeArray:
            result = self._xmlrpcSession.AwaServerWriteOperation_AddValueAsTimeArray(writeOperation, path, array)
        else:
            raise AwaInvalidArgumentException("%s is not a valid multiple instance resource type" % (resourceType, ))

        CheckSuccess(result, "Failed to add values as array to Write Operation: %s" % (str(values), ))

    def WriteCreateObjectInstance(self, writeOperation, path):
        CheckNone(writeOperation, "Write Operation is NULL")
        result = self._xmlrpcSession.AwaServerWriteOperation_CreateObjectInstance(writeOperation, path)
        CheckSuccess(result, "Failed to create object instance on path: %s" % (path, ))

    def WriteCreateOptionalResource(self, writeOperation, path):
        CheckNone(writeOperation, "Write Operation is NULL")
        result = self._xmlrpcSession.AwaServerWriteOperation_CreateOptionalResource(writeOperation, path)
        CheckSuccess(result, "Failed to create object instance on path: %s" % (path, ))


    def IsObjectDefined(self, session, objectID):
        return self._xmlrpcSession.AwaServerSession_IsObjectDefined(session, int(objectID))

    def GetObjectDefinition(self, session, objectID):
        objectDefinition = self._xmlrpcSession.AwaServerSession_GetObjectDefinition(session, objectID)
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
        defineOperation = self._xmlrpcSession.AwaServerDefineOperation_New(session)
        CheckNone(defineOperation, "Define Operation is NULL")

        objectDefinition = self._xmlrpcSession.AwaObjectDefinition_New(objectDefinitionSettings.objectID, objectDefinitionSettings.objectName, objectDefinitionSettings.minimumInstances, objectDefinitionSettings.maximumInstances)
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

        result = self._xmlrpcSession.AwaServerDefineOperation_Add(defineOperation, objectDefinition)
        CheckSuccess(result, "Could not add object definition to Define Operation")

        result = self._xmlrpcSession.AwaServerDefineOperation_Perform(defineOperation, test_defaults.TIMEOUT)
        CheckSuccess(result, "Failed to perform Define Operation")

        result = self._xmlrpcSession.AwaServerDefineOperation_Free(defineOperation)
        CheckSuccess(result, "Failed to free Define Operation")


    def CreateObservation(self, clientID, path):
        observation = self._xmlrpcSession.AwaServerObservation_New(clientID, path, None, None)
        CheckNone(observation, "Could not create Observation for clientID %s on path %s" % (clientID, path, ))
        return observation

    def FreeObservation(self, observation):
        result = self._xmlrpcSession.AwaServerObservation_Free(observation)
        CheckSuccess(result, "Failed to free Observation")

    # FIXME: Remove dependency on clientID here
    def _PerformObserveOperation(self, observeOperation, clientID, path):
        result = self._xmlrpcSession.AwaServerObserveOperation_Perform(observeOperation, test_defaults.TIMEOUT)
        response = self._xmlrpcSession.AwaServerObserveOperation_GetResponse(observeOperation, clientID)

        pathResult = None
        pathResultError = AwaError.Unspecified
        pathResultLWM2MError = AwaLWM2MError.Unspecified

        if response != None:
            pathResult = self._xmlrpcSession.AwaServerObserveResponse_GetPathResult(response, path)
            pathResultError = self.GetPathResultError(pathResult)
            pathResultLWM2MError = self.GetPathResultLWM2MError(pathResult)

        CheckSuccess(result, "Failed to perform Observe Operation", pathResultError, pathResultLWM2MError)
        CheckSuccess(self._xmlrpcSession.AwaServerObserveOperation_Free(observeOperation), "Failed to free Observe Operation")

    def Observe(self, session, observation, clientID):
        observeOperation = self._xmlrpcSession.AwaServerObserveOperation_New(session)
        CheckNone(observeOperation, "Observe Operation is NULL")

        path = self._xmlrpcSession.AwaServerObservation_GetPath(observation)
        CheckNone(path, "Failed to retrieve path from Observation")

        result = self._xmlrpcSession.AwaServerObserveOperation_AddObservation(observeOperation, observation)
        CheckSuccess(result, "Failed to add  observation to Observe Operation for path %s" % (path, ))

        self._PerformObserveOperation(observeOperation, clientID, path)

    def CancelObservation(self, session, observation, clientID):
        observeOperation = self._xmlrpcSession.AwaServerObserveOperation_New(session)
        CheckNone(observeOperation, "Observe Operation is NULL")

        path = self._xmlrpcSession.AwaServerObservation_GetPath(observation)
        CheckNone(path, "Failed to retrieve path from Observation")

        result = self._xmlrpcSession.AwaServerObserveOperation_AddCancelObservation(observeOperation, observation)
        CheckSuccess(result, "Failed to add Cancel  Observation to Observe Operation for path %s" % (path, ))

        self._PerformObserveOperation(observeOperation, clientID, path)

    def WaitForNotification(self, session, path, resourceInstanceID=None):
        super(GWServerXmlRpc, self).WaitForNotificationWithSession(session, SessionType.Server, path, resourceInstanceID)

    def DeleteEntity(self, session, clientID, path):
        CheckNone(session, "Session is NULL")

        deleteOperation = self._xmlrpcSession.AwaServerDeleteOperation_New(session)
        CheckNone(deleteOperation, "Delete Operation is NULL")

        result = self._xmlrpcSession.AwaServerDeleteOperation_AddPath(deleteOperation, clientID, path)
        CheckSuccess(result, "Failed to add path to Delete operation: %s" % (path, ))

        result = self._xmlrpcSession.AwaServerDeleteOperation_Perform(deleteOperation, test_defaults.TIMEOUT)
        response = self._xmlrpcSession.AwaServerDeleteOperation_GetResponse(deleteOperation, clientID)
        pathResult = None
        pathResultError = AwaError.Unspecified
        pathResultLWM2MError = AwaLWM2MError.Unspecified

        if response != None:
            pathResult = self._xmlrpcSession.AwaServerDeleteResponse_GetPathResult(response, path)
            pathResultError = self.GetPathResultError(pathResult)
            pathResultLWM2MError = self.GetPathResultLWM2MError(pathResult)

        CheckSuccess(result, "Failed to perform Delete Operation", pathResultError, pathResultLWM2MError)
        CheckSuccess(self._xmlrpcSession.AwaServerDeleteOperation_Free(deleteOperation), "Failed to free Delete Operation")

    def ListClients(self, session):
        CheckNone(session, "Session is NULL")
        clients = {}
        listClientsOperation = self._xmlrpcSession.AwaServerListClientsOperation_New(session)
        CheckNone(listClientsOperation, "List Clients Operation is NULL")
        result = self._xmlrpcSession.AwaServerListClientsOperation_Perform(listClientsOperation, test_defaults.TIMEOUT)
        CheckSuccess(result, "Failed to perform List clients operation")

        clientIterator = self._xmlrpcSession.AwaServerListClientsOperation_NewClientIterator(listClientsOperation)
        while self._xmlrpcSession.AwaClientIterator_Next(clientIterator):
            clientID = self._xmlrpcSession.AwaClientIterator_GetClientID(clientIterator)
            registeredEntities = []
            response = self._xmlrpcSession.AwaServerListClientsOperation_GetResponse(listClientsOperation, clientID)
            CheckNone(response, "No List Clients response for ClientID %s" % (clientID, ))

            entityIterator = self._xmlrpcSession.AwaServerListClientsResponse_NewRegisteredEntityIterator(response);
            CheckNone(entityIterator, "Failed to create Entity Iterator for List Clients response for ClientID %s" % (clientID, ))

            while self._xmlrpcSession.AwaRegisteredEntityIterator_Next(entityIterator):
                registeredEntities.append(self._xmlrpcSession.AwaRegisteredEntityIterator_GetPath(entityIterator))
            self._xmlrpcSession.AwaRegisteredEntityIterator_Free(entityIterator)

            #print "Client: %s: %s" % (clientID, str(registeredEntities))
            clients[clientID] = registeredEntities
        self._xmlrpcSession.AwaClientIterator_Free(clientIterator)
        CheckSuccess(self._xmlrpcSession.AwaServerListClientsOperation_Free(listClientsOperation), "Failed to free List Clients Operation")
        return clients


