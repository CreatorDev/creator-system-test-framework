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

from enum import IntEnum

#Resource Types
class AwaResourceType(IntEnum):
    Invalid = 0
    NoneType = 1
    String = 2
    Integer = 3
    Float = 4
    Boolean = 5
    Opaque = 6
    Time = 7
    ObjectLink = 8
    StringArray = 9
    IntegerArray = 10
    FloatArray = 11
    BooleanArray = 12
    OpaqueArray = 13
    TimeArray = 14
    ObjectLinkArray = 15
    LAST = 16

#Error types
class AwaError(IntEnum):
    Success = 0
    Unspecified = 1
    Unsupported = 2
    Internal = 3
    OutOfMemory = 4

    SessionInvalid = 5
    SessionNotConnected = 6
    NotDefined = 7
    AlreadyDefined = 8
    OperationInvalid = 9

    PathInvalid = 10
    PathNotFound = 11
    TypeMismatch = 12
    Timeout = 13
    Overrun = 14

    IDInvalid = 15
    AddInvalid = 16
    CannotCreate = 17
    CannotDelete = 18
    DefinitionInvalid = 19

    AlreadySubscribed = 20
    SubscriptionInvalid = 21
    ObservationInvalid = 22
    IPCError = 23
    ResponseInvalid = 24

    ClientIDInvalid = 25
    ClientNotFound = 26
    LWM2MError = 27
    IteratorInvalid = 28
    Response = 29

    RangeInvalid = 30
    
class AwaLWM2MError(IntEnum):
    Success = 0
    Unspecified = 1
    BadRequest = 2
    Unauthorized = 3
    NotFound = 4
    MethodNotAllowed = 5
    NotAcceptable = 6
    
#Resource supported operations
class AwaResourceOperations(IntEnum):
    Invalid = -1
    TypeNone = 0
    ReadOnly = 1
    WriteOnly = 2
    ReadWrite = 3
    Execute = 4

#Supported notification changeset change types
class AwaChangeType(IntEnum):
    Invalid = 0
    ResourceCreated = 1
    ResourceModified = 2
    ResourceDeleted = 3
    ObjectInstanceCreated = 4
    ObjectInstanceModified = 5
    ObjectInstanceDeleted = 6
    Current = 7

#Subscribe operation types
class AwaSubscribeType(IntEnum):
    TypeNone = 0
    Change = 1
    Execute = 2
    
class AwaWriteMode(IntEnum):
    Replace = 0
    Update = 1
    
class SessionType(IntEnum):
    Client = 0
    Server = 1

def isArrayResourceType(resType):
    return resType > AwaResourceType.ObjectLink
