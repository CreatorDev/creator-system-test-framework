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

from framework.awa_enums import AwaResourceType
from framework.awa_enums import AwaResourceOperations
from framework.definitions import ObjectDefinitionSettings, ResourceDefinitionSettings

objectDefinition1000 = ObjectDefinitionSettings(1000, "Object1000", 0, 1)
objectDefinition1001 = ObjectDefinitionSettings(1001, "Object1001", 1, 1)
objectDefinition1002 = ObjectDefinitionSettings(1002, "Object1002", 0, 10)
objectDefinition1003 = ObjectDefinitionSettings(1003, "Object1003", 1, 10)
resourceDefinitions = (ResourceDefinitionSettings(102, "Resource102", AwaResourceType.String, AwaResourceOperations.ReadWrite, 0, 1, "test", resourceSizeInBytes=256), 
                       ResourceDefinitionSettings(103, "Resource103", AwaResourceType.Integer, AwaResourceOperations.ReadWrite, 0, 1, 5, resourceSizeInBytes=8), 
                       ResourceDefinitionSettings(106, "Resource106", AwaResourceType.Opaque, AwaResourceOperations.ReadWrite, 0, 1, resourceSizeInBytes=256),
                       ResourceDefinitionSettings(109, "Resource109", AwaResourceType.StringArray, AwaResourceOperations.ReadWrite, 0, 10, {1: "Sample1", 2: "Sample2", 3: "Sample3"}, resourceSizeInBytes=256),
                       ResourceDefinitionSettings(110, "Resource110", AwaResourceType.IntegerArray, AwaResourceOperations.ReadWrite, 0, 10, {0: 5, 1: 10, 2: 15}, resourceSizeInBytes=256),
                       ResourceDefinitionSettings(202, "Resource202", AwaResourceType.String, AwaResourceOperations.ReadWrite, 1, 1, "test", resourceSizeInBytes=256), 
                       ResourceDefinitionSettings(206, "Resource206", AwaResourceType.Opaque, AwaResourceOperations.ReadWrite, 1, 1, resourceSizeInBytes=256),
                       ResourceDefinitionSettings(209, "Resource209", AwaResourceType.StringArray, AwaResourceOperations.ReadWrite, 1, 10, {1: "Sample1", 2: "Sample2", 3: "Sample3"}, resourceSizeInBytes=256),
                       ResourceDefinitionSettings(210, "Resource210", AwaResourceType.IntegerArray, AwaResourceOperations.ReadWrite, 1, 10, {0: 5, 1: 10, 2: 15}, resourceSizeInBytes=256),)

# WARNING: resource lengths are hard coded!
constrainedResourceDefinitions = (ResourceDefinitionSettings(202, "Resource202", AwaResourceType.String, AwaResourceOperations.ReadWrite, 1, 1, "test", resourceSizeInBytes=256), 
                                  ResourceDefinitionSettings(203, "Resource203", AwaResourceType.Integer, AwaResourceOperations.ReadWrite, 1, 1, 5, resourceSizeInBytes=8),
                                  ResourceDefinitionSettings(206, "Resource206", AwaResourceType.Opaque, AwaResourceOperations.ReadWrite, 1, 1, "abc", resourceSizeInBytes=3), ) 
