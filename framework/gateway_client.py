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

import abc
import uuid

from framework import test_objects
from framework.client import Client, DeviceLoginDetails
from framework.awa_enums import AwaResourceType

# Abstraction for Real and Simulated Gateway clients.
class GatewayClient(Client):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def CreateSession(self, address, port):
        return

    @abc.abstractmethod
    def FreeSession(self, session):
        return

    @abc.abstractmethod
    def GetSingleResource(self, path, resourceType):
        return

    @abc.abstractmethod
    def CreateGetOperation(self, session, path):
        return

    @abc.abstractmethod
    def FreeGetOperation(self, operation):
        return

    @abc.abstractmethod
    def GetResourceValueFromGetOperation(self, operation, path, resourceType):
        return

    @abc.abstractmethod
    def GetResourceValuesFromGetOperation(self, operation, path, resourceType):
        return

    @abc.abstractmethod
    def GetPathResultFromGetOperation(self, operation, path):
        return

    @abc.abstractmethod
    def CreateSetOperation(self,session):
        return

    @abc.abstractmethod
    def PerformSetOperation(self, setOperation, path=None):
        return

    @abc.abstractmethod
    def SetSingleInstanceResourceValue(self, setOperation, path, resourceType, value):
        return

    @abc.abstractmethod
    def SetMultipleInstanceResourceValues(self, setOperation, path, resourceType, values):
        return

    @abc.abstractmethod
    def SetMultipleInstanceResourceValuesAsArray(self, setOperation, path, resourceType, values):
        return

    @abc.abstractmethod
    def SetCreateObjectInstance(self, setOperation, path):
        return

    @abc.abstractmethod
    def SetCreateOptionalResource(self, setOperation, path):
        return

    @abc.abstractmethod
    def DeleteResourceInstancesWithArrayRange(self, session, path, startIndex, count):
        return

    @abc.abstractmethod
    def DeleteEntity(self, session, path):
        return

    @abc.abstractmethod
    def CreateChangeSubscription(self, path):
        return

    @abc.abstractmethod
    def CreateExecuteSubscription(self, path):
        return

    @abc.abstractmethod
    def SubscribeToChange(self, session, changeSubscription):
        return

    @abc.abstractmethod
    def SubscribeToExecute(self, session, executeSubscription):
        return

    @abc.abstractmethod
    def CancelSubscribeToChange(self, session, changeSubscription):
        return

    @abc.abstractmethod
    def CancelSubscribeToExecute(self, session, executeSubscription):
        return

    @abc.abstractmethod
    def ProcessAndGetNotifyResponse(self, session, timeout):
        return

    @abc.abstractmethod
    def WaitForNotification(self, session, path, resourceInstanceID=None):
        return

    @abc.abstractmethod
    def IsObjectDefined(self, session, objectID):
        return

    @abc.abstractmethod
    def GetObjectDefinition(self, session, objectID):
        return

    @abc.abstractmethod
    def GetObjectID(self, objectDefinition):
        return

    @abc.abstractmethod
    def GetObjectName(self, objectDefinition):
        return

    @abc.abstractmethod
    def GetObjectMinimumInstances(self, objectDefinition):
        return

    @abc.abstractmethod
    def GetObjectMaximumInstances(self, objectDefinition):
        return

    @abc.abstractmethod
    def IsResourceDefined(self, objectDefinition, resourceID):
        return

    @abc.abstractmethod
    def GetResourceDefinition(self, objectDefinition, resourceID):
        return

    @abc.abstractmethod
    def GetResourceID(self, resourceDefinition):
        return

    @abc.abstractmethod
    def GetResourceName(self, resourceDefinition):
        return

    @abc.abstractmethod
    def IsResourceMandatory(self, resourceDefinition):
        return

    @abc.abstractmethod
    def GetResourceType(self, resourceDefinition):
        return

    @abc.abstractmethod
    def GetResourceSupportedOperations(self, resourceDefinition):
        return

    @abc.abstractmethod
    def GetResourceMaximumInstances(self, resourceDefinition):
        return

    @abc.abstractmethod
    def GetResourceMinimumInstances(self, resourceDefinition):
        return

    @abc.abstractmethod
    def DefineWithSession(self, session, objectDefinitionSettings, resourceDefinitionSettingsCollection):
        return

    @abc.abstractmethod
    def CreateObjectDefinitionIterator(self, session):
        return

    @abc.abstractmethod
    def GetNextObjectDefinitionFromIterator(self, iterator):
        return

    def Define(self, objectDefinitionSettings, resourceDefinitionSettingsCollection):
        self.DefineWithSession(self._session, objectDefinitionSettings, resourceDefinitionSettingsCollection)

    def DefineTestObjects(self):
        self.Define(test_objects.objectDefinition1000, test_objects.resourceDefinitions)
        self.Define(test_objects.objectDefinition1001, test_objects.resourceDefinitions)
        self.Define(test_objects.objectDefinition1002, test_objects.resourceDefinitions)
        self.Define(test_objects.objectDefinition1003, test_objects.resourceDefinitions)

    def CreateInstancesOfTestObjects(self):
        setOperation = self.CreateSetOperation(self._session)
        self.SetCreateObjectInstance(setOperation, "/1000/0")
        self.SetCreateObjectInstance(setOperation, "/1001/0")
        self.SetCreateObjectInstance(setOperation, "/1002/0")
        self.SetCreateObjectInstance(setOperation, "/1003/0")
        self.PerformSetOperation(setOperation, None)

    def getDeviceLoginDetails(self):
        deviceType = self.GetSingleResource("/20000/0/2", AwaResourceType.String)
        deviceName = self.GetSingleResource("/20000/0/3", AwaResourceType.String)
        fcapCode = self.GetSingleResource("/20000/0/5", AwaResourceType.String)
        serialNumber = self.GetSingleResource("/3/0/2", AwaResourceType.String)
        softwareVersion = self.GetSingleResource("/3/0/19", AwaResourceType.String)
        deviceID = self.GetSingleResource("/20000/0/0", AwaResourceType.Opaque)


        try:
            deviceIDAsUUID = str(uuid.UUID(bytes_le=deviceID[:16]))
        except ValueError:
            print("Failed to convert deviceID bytes to UUID: length %d data: %s", len(deviceID), deviceID)
            #import pdb; pdb.set_trace()
            raise

        return DeviceLoginDetails(deviceType, deviceName, fcapCode, serialNumber, softwareVersion, deviceIDAsUUID)
