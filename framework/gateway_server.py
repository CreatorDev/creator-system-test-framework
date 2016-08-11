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
import sys
import time
from framework import test_objects

class ClientTimeoutException(Exception):
    pass

# Abstraction for Real and Simulated Gateway Servers.
class GatewayServer(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def CreateSession(self, address, port):
        return

    @abc.abstractmethod
    def FreeSession(self, session):
        return

    @abc.abstractmethod
    def GetPathResultError(self, pathResult):
        return

    @abc.abstractmethod
    def CreateReadOperation(self, session, clientID, path):
        return

    @abc.abstractmethod
    def FreeReadOperation(self, operation):
        return

    @abc.abstractmethod
    def GetResourceValueFromReadOperation(self, operation, clientID, path, resourceType):
        return

    @abc.abstractmethod
    def GetResourceValuesFromReadOperation(self, operation, clientID, path, resourceType):
        return

    @abc.abstractmethod
    def GetPathResultFromReadOperation(self, operation, clientID, path):
        return

    @abc.abstractmethod
    def PerformWriteOperation(self, writeOperation, clientID, path):
        return

    @abc.abstractmethod
    def CreateWriteOperation(self, session, writeMode):
        return

    @abc.abstractmethod
    def WriteSingleInstanceResourceValue(self, writeOperation, path, resourceType, value):
        return

    @abc.abstractmethod
    def WriteMultipleInstanceResourceValues(self, writeOperation, path, resourceType, values):
        return

    @abc.abstractmethod
    def WriteCreateObjectInstance(self, writeOperation, path):
        return

    @abc.abstractmethod
    def WriteCreateOptionalResource(self, writeOperation, path):
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
    def CreateObservation(self, clientID, path):
        return

    @abc.abstractmethod
    def FreeObservation(self, observation):
        return

    @abc.abstractmethod
    def Observe(self, session, observation, clientID):
        return

    @abc.abstractmethod
    def CancelObservation(self, session, observation, clientID):
        return

    @abc.abstractmethod
    def WaitForNotification(self, session, path, resourceInstanceID=None):
        return

    @abc.abstractmethod
    def DeleteEntity(self, session, clientID, path):
        return

    @abc.abstractmethod
    def ListClients(self, session):
        return

    def Define(self, objectDefinitionSettings, resourceDefinitionSettingsCollection):
        self.DefineWithSession(self._session, objectDefinitionSettings, resourceDefinitionSettingsCollection)

    def DefineTestObjects(self):
        self.Define(test_objects.objectDefinition1000, test_objects.resourceDefinitions)
        self.Define(test_objects.objectDefinition1001, test_objects.resourceDefinitions)
        self.Define(test_objects.objectDefinition1002, test_objects.resourceDefinitions)
        self.Define(test_objects.objectDefinition1003, test_objects.resourceDefinitions)

    def WaitForClient(self, clientID, attempts=200, wait=0.1):
        sys.stdout.write("Wait for client \'%s\' to connect to gateway server..." % (clientID,))
        for _ in xrange(attempts):
            clients = self.ListClients(self._session)
            if clientID in clients:
                sys.stdout.write("OK\n")
                break
            time.sleep(wait)
            sys.stdout.write(".")
            sys.stdout.flush()
        else:
            sys.stdout.write("TIMEOUT\n")
            raise ClientTimeoutException("Timeout waiting for client \'%s\' to connect to gateway server" % (clientID,))

    def WaitForClientObject(self, clientID, object, attempts=200, wait=0.5):
        sys.stdout.write("Wait for client \'%s\' to register \'%s\'" % (clientID,object,))
        for _ in xrange(attempts):
            clients = self.ListClients(self._session)
            if clientID in clients:
                if object in clients[clientID]:
                    sys.stdout.write("OK\n")
                    break
            time.sleep(wait)
            sys.stdout.write(".")
            sys.stdout.flush()
        else:
            sys.stdout.write("TIMEOUT\n")
            raise ClientTimeoutException("Timeout waiting for client \'%s\' to bootstrap" % (clientID,))

    def WaitForClientObjectToDisappear(self, clientID, object, attempts=200, wait=0.1):
        sys.stdout.write("Wait for client \'%s\' to register \'%s\'" % (clientID,object,))
        for _ in xrange(attempts):
            clients = self.ListClients(self._session)
            if clientID in clients:
                if object not in clients[clientID]: 
                    sys.stdout.write("OK\n")
                    break
            time.sleep(wait)
            sys.stdout.write(".")
            sys.stdout.flush()
        else:
            sys.stdout.write("TIMEOUT\n")
            raise ClientTimeoutException("Timeout waiting for client \'%s\' to bootstrap" % (clientID,))
