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

"""Device Server HTTP Client implementation"""

from framework.device_server_client import DeviceServerClient

from framework import test_defaults
from framework import test_config
from framework.awa_exceptions import CheckNone
from framework.awa_enums import AwaResourceType, AwaResourceOperations
from framework.device_server_client import ObjectDefinition, ResourceDefinition

from helpers.httphelper import HttpHelper

class DeviceServerClientHttp(DeviceServerClient):

    """Class responsible for establishing and maintaining an HTTP connection with a device server"""

    def __init__(self, clientConfig):
        super(DeviceServerClient, self).__init__()
        self._clientConfig = clientConfig
        self._session = self.CreateSession(self._clientConfig["uri"], self._clientConfig['port'])

    def __del__(self):
        try:
            self._session.logout()
        except AttributeError:
            pass

    def CreateSession(self, address, port):
        """Create a connection to the specified device server at address:port and login"""
        print 'Connecting to DeviceServer at ' + self._clientConfig["uri"] + ':' + str(self._clientConfig['port']) + '...'
        self._session = HttpHelper(self._clientConfig["uri"] + ':' + str(self._clientConfig['port']))


        accessKey = None
        accessSecret = None
        try:
            # Read PSK credentials
            with open('accessKey', 'r') as accessKeyFile:
                accessKey = accessKeyFile.read().replace('\n', '')
            with open('accessSecret', 'r') as accessSecretFile:
                accessSecret = accessSecretFile.read().replace('\n', '')
            print 'Using test credentials files'
        except:
            # Generate new test credentials if the files don't exist
            creds = self._session.create_test_credentials()
            print 'Generated new test credentials, [Key: ' + creds.Key + ', Access Secret: ' + creds.Secret + ']'
            accessKey = creds.Key 
            accessSecret = creds.Secret

        self._session.set_credentials(accessKey, accessSecret)
        self._session.login()
        return self._session

    def FreeSession(self, session):
        """Logout device server connection"""
        session.logout()

    def DefineWithSession(self, session, objectDefinitionSettings, resourceDefinitionSettingsCollection):
        return

    def Define(self, objectDefinitionSettings, resourceDefinitionSettingsCollection):
        self.DefineWithSession(self._session, objectDefinitionSettings, resourceDefinitionSettingsCollection)

    def getDeviceLoginDetails(self):
        return None

    def IsObjectDefined(self, session, objectID):
        """Check whether an object definition exists on the device server with the specified objectID"""
        result = False
        try:
            entrypoint = session.get_entry_point()
            objdeflink = session.find_link(entrypoint, 'objectdefinitions')
            objdefs = session.get_all(objdeflink['href'])
            for index in range(0, objdefs['PageInfo']['ItemsCount']):
                if objdefs['Items'][index]['ObjectID'] == str(objectID):
                    result = True
                    break

        except Exception as exception:
            print "Error encountered when retrieving object definitions to check whether object is defined."
            print exception
        return result

    def GetObjectDefinition(self, session, objectID):
        """Return the definition of an object defined on the device server with the specified objectID"""
        result = None
        try:
            entrypoint = session.get_entry_point()
            objdeflink = session.find_link(entrypoint, 'objectdefinitions')
            objdefs = session.get_all(objdeflink['href'])
            for index in range(0, objdefs['PageInfo']['ItemsCount']):
                if objdefs['Items'][index]['ObjectID'] == str(objectID):
                    result = self._GetObjectDefinition(objdefs['Items'][index])
                    break

        except Exception as exception:
            print "Error encountered when retrieving object definitions to retrieve an object definition."
            print exception
        CheckNone(result, "No Object definition exists for ID %d" % (objectID, ))
        return result

    def _GetObjectDefinition(self, responseobject):
        result = ObjectDefinition()
        result._ObjectID = int(responseobject['ObjectID'])
        result._Name = responseobject['Name'].replace(' ', '')
        result._MaximumInstances = (65535, 1)[responseobject['Singleton']]
        result._MinimumInstances = (0, 1)[responseobject['Singleton']]
        return result

    def GetObjectID(self, objectdefinition):
        """Return the ObjectID field of an object definition"""
        return objectdefinition._ObjectID

    def GetObjectName(self, objectdefinition):
        """Return the Name field of an object definition"""
        return objectdefinition._Name

    def GetObjectMinimumInstances(self, objectdefinition):
        """Return the MinimumInstances field of an object definition"""
        return objectdefinition._MinimumInstances

    def GetObjectMaximumInstances(self, objectdefinition):
        """Return the MaximumInstances field of an object definition"""
        return objectdefinition._MaximumInstances

    def IsResourceDefined(self, objectdefinition, resourceID):
        """Check whether a resource definition (with the specified resourceID) exists on the device server for an object with the specified objectID"""
        result = False
        try:
            entrypoint = self._session.get_entry_point()
            objdeflink = self._session.find_link(entrypoint, 'objectdefinitions')
            objdefs = self._session.get_all(objdeflink['href'])
            for index in range(0, int(objdefs['PageInfo']['ItemsCount'])):
                if objdefs['Items'][index]['ObjectID'] == str(self.GetObjectID(objectdefinition)):
                    for resource_index in range(0, len(objdefs['Items'][index]['Properties'])):
                        if objdefs['Items'][index]['Properties'][resource_index]['PropertyID'] == str(resourceID):
                            result = True
                            break
                    break

        except Exception as exception:
            print "Error encountered when retrieving object definitions to determine whether resource was defined."
            print exception
        return result

    def GetResourceDefinition(self, objectdefinition, resourceID):
        """Return the definition of a object resource defined on the device server with the specified objectID and resourceID"""
        result = None
        try:
            entrypoint = self._session.get_entry_point()
            objdeflink = self._session.find_link(entrypoint, 'objectdefinitions')
            objdefs = self._session.get_all(objdeflink['href'])

            for index in range(0, int(objdefs['PageInfo']['ItemsCount'])):
                if objdefs['Items'][index]['ObjectID'] == str(self.GetObjectID(objectdefinition)):
                    for resourceindex in range(0, len(objdefs['Items'][index]['Properties'])):
                        if objdefs['Items'][index]['Properties'][resourceindex]['PropertyID'] == str(resourceID):
                            result = self._GetResourceDefinition(objdefs['Items'][index]['Properties'][resourceindex])
                            break
                    break

        except Exception as exception:
            print "Error encountered when retrieving resource definitions."
            print exception
        CheckNone(result, "No Resource definition exists for " +  self.GetObjectName(objectdefinition) + " object, resourceID %d" % (resourceID, ))
        return result

    def _GetResourceDefinition(self, resource):
        result = ResourceDefinition()
        result._ResourceID = int(resource['PropertyID'])
        result._Name = resource['Name'].replace(' ', '')
        result._IsCollection = resource['IsCollection']
        result._IsMandatory = resource['IsMandatory']

        # Parse DataType property
        if resource['DataType'] == 'NotSet':
            result._Type = self._GetAwaResourceType('NoneType')

        elif resource['DataType'] == 'Boolean':
            if result._IsCollection:
                result._Type = self._GetAwaResourceType('BooleanArray')
            else:
                result._Type = self._GetAwaResourceType('Boolean')

        elif resource['DataType'] == 'String':
            if result._IsCollection:
                result._Type = self._GetAwaResourceType('StringArray')
            else:
                result._Type = self._GetAwaResourceType('String')

        elif resource['DataType'] == 'Integer':
            if result._IsCollection:
                result._Type = self._GetAwaResourceType('IntegerArray')
            else:
                result._Type = self._GetAwaResourceType('Integer')

        elif resource['DataType'] == 'Float':
            if result._IsCollection:
                result._Type = self._GetAwaResourceType('FloatArray')
            else:
                result._Type = self._GetAwaResourceType('Float')

        elif resource['DataType'] == 'DateTime':
            if result._IsCollection:
                result._Type = self._GetAwaResourceType('TimeArray')
            else:
                result._Type = self._GetAwaResourceType('Time')

        elif resource['DataType'] == 'Opaque':
            if result._IsCollection:
                result._Type = self._GetAwaResourceType('OpaqueArray')
            else:
                result._Type = self._GetAwaResourceType('Opaque')

        result._SupportedOperations = self._GetAwaResourceSupportedOperations(resource['Access'])
        result._MaximumInstances = (1, 65535)[resource['IsCollection']]
        result._MinimumInstances = (0, 1)[resource['IsMandatory']]
        return result

    def GetResourceID(self, resourceDefinition):
        """Return the ResourceID field of a resource definition"""
        return resourceDefinition._ResourceID

    def GetResourceName(self, resourceDefinition):
        """Return the Name field of a resource definition"""
        return resourceDefinition._Name

    def IsResourceMandatory(self, resourceDefinition):
        """Return the IsMandatory field of a resource definition"""
        return resourceDefinition._IsMandatory

    def GetResourceType(self, resourceDefinition):
        """Return the Type field of a resource definition"""
        return resourceDefinition._Type

    def _GetAwaResourceType(self, enumValueName):
        result = None
        if enumValueName in AwaResourceType.__members__:
            result = AwaResourceType.__members__[enumValueName].value
        return result

    def GetResourceSupportedOperations(self, resourceDefinition):
        """Return the operations supported by a resource"""
        return resourceDefinition._SupportedOperations

    def _GetAwaResourceSupportedOperations(self, accessValue):
        """Convert string to AwaResourceOperations enum value"""
        result = AwaResourceOperations.Invalid
        if accessValue == 'Read':
            result = AwaResourceOperations.ReadOnly
        elif accessValue == 'Write':
            result = AwaResourceOperations.WriteOnly
        elif accessValue == 'ReadWrite':
            result = AwaResourceOperations.ReadWrite
        elif accessValue == 'Execute':
            result = AwaResourceOperations.Execute
        elif accessValue == 'NoAccess':
            result = AwaResourceOperations.Execute
        elif accessValue == None:
            result = AwaResourceOperations.TypeNone
        return result

    def GetResourceMaximumInstances(self, resourceDefinition):
        """Return the MaximumInstrances field of a resource definition"""
        return resourceDefinition._MaximumInstances

    def GetResourceMinimumInstances(self, resourceDefinition):
        """Return the MinimumInstrances field of a resource definition"""
        return resourceDefinition._MinimumInstances
