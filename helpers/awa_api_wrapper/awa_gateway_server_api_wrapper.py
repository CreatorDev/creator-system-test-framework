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

from ctypes import POINTER, c_void_p, c_char_p, c_int, cast, byref, c_longlong, c_double, c_bool, c_ushort
import cPickle as pickle

from awa_common_api_wrapper import AwaCommonAPIWrapper, AwaOpaque, AwaOpaqueToBase64

from framework.awa_enums import SessionType

from framework.wrap import wrap, trace_in, trace_out

class AwaGatewayServerAPIWrapper(AwaCommonAPIWrapper):

    @wrap(trace_in, trace_out)
    def __init__(self):
        super(AwaGatewayServerAPIWrapper, self).__init__(SessionType.Server)

    @wrap(trace_in, trace_out)
    def AwaServerSession_New(self):
        self._lib.AwaServerSession_New.restype = c_void_p
        return self._lib.AwaServerSession_New()

    @wrap(trace_in, trace_out)
    def AwaServerSession_SetIPCAsUDP(self, session, address, port):
        self._lib.AwaClientSession_SetIPCAsUDP.restype = c_int
        self._lib.AwaClientSession_SetIPCAsUDP.argtypes = [c_void_p, c_char_p, c_ushort]
        return self._lib.AwaServerSession_SetIPCAsUDP(session, address, port)

    @wrap(trace_in, trace_out)
    def AwaServerSession_Connect(self, session):
        self._lib.AwaServerSession_Connect.restype = c_int
        self._lib.AwaServerSession_Connect.argtypes = [c_void_p]
        return self._lib.AwaServerSession_Connect(session)

    @wrap(trace_in, trace_out)
    def AwaServerSession_Refresh(self, session):
        self._lib.AwaServerSession_Refresh.restype = c_int
        self._lib.AwaServerSession_Refresh.argtypes = [c_void_p]
        return self._lib.AwaServerSession_Refresh(session)

    @wrap(trace_in, trace_out)
    def AwaServerSession_IsObjectDefined(self, session, objectID):
        self._lib.AwaServerSession_IsObjectDefined.restype = c_bool
        self._lib.AwaServerSession_IsObjectDefined.argtypes = [c_void_p, c_int]
        return self._lib.AwaServerSession_IsObjectDefined(session, objectID)

    @wrap(trace_in, trace_out)
    def AwaServerSession_GetObjectDefinition(self, session, objectID):
        self._lib.AwaServerSession_GetObjectDefinition.restype = c_void_p
        self._lib.AwaServerSession_GetObjectDefinition.argtypes = [c_void_p, c_int]
        return self._lib.AwaServerSession_GetObjectDefinition(session, objectID)

    @wrap(trace_in, trace_out)
    def AwaServerSession_NewObjectDefinitionIterator(self, session):
        self._lib.AwaServerSession_NewObjectDefinitionIterator.restype = c_void_p
        self._lib.AwaServerSession_NewObjectDefinitionIterator.argtypes = [c_void_p]
        return self._lib.AwaServerSession_NewObjectDefinitionIterator(session)

    @wrap(trace_in, trace_out)
    def AwaServerSession_Disconnect(self, session):
        self._lib.AwaServerSession_Disconnect.restype = c_int
        self._lib.AwaServerSession_Disconnect.argtypes = [c_void_p]
        return self._lib.AwaServerSession_Disconnect(session)

    @wrap(trace_in, trace_out)
    def AwaServerSession_Free(self, session):
        self._lib.AwaServerSession_Free.restype = c_int
        mem = cast(session, POINTER(c_void_p))
        return self._lib.AwaServerSession_Free(byref(mem))

    @wrap(trace_in, trace_out)
    def AwaServerSession_PathToIDs(self, session, path, objectID, objectInstanceID, resourceID):
        self._lib.AwaServerSession_PathToIDs.restype = c_int
        self._lib.AwaServerSession_PathToIDs.argtypes = [c_void_p, c_char_p, POINTER(c_int), POINTER(c_int), POINTER(c_int)]
        return self._lib.AwaServerSession_PathToIDs(session, path, objectID, objectInstanceID, resourceID)

    @wrap(trace_in, trace_out)
    def AwaServerListClientsOperation_New(self, session):
        self._lib.AwaServerListClientsOperation_New.restype = c_void_p
        self._lib.AwaServerListClientsOperation_New.argtypes = [c_void_p]
        return self._lib.AwaServerListClientsOperation_New(session)

    @wrap(trace_in, trace_out)
    def AwaServerListClientsOperation_Perform(self, operation, timeout):
        self._lib.AwaServerListClientsOperation_Perform.restype = c_int
        self._lib.AwaServerListClientsOperation_Perform.argtypes = [c_void_p, c_int]
        return self._lib.AwaServerListClientsOperation_Perform(operation, timeout)

    @wrap(trace_in, trace_out)
    def AwaServerListClientsOperation_Free(self, operation):
        self._lib.AwaServerListClientsOperation_Free.restype = c_int
        mem = cast(operation, POINTER(c_void_p))
        return self._lib.AwaServerListClientsOperation_Free(byref(mem))

    @wrap(trace_in, trace_out)
    def AwaClientIterator_Next(self, iterator):
        self._lib.AwaClientIterator_Next.restype = c_bool
        self._lib.AwaClientIterator_Next.argtypes = [c_void_p]
        return self._lib.AwaClientIterator_Next(iterator)

    @wrap(trace_in, trace_out)
    def AwaClientIterator_GetClientID(self, iterator):
        self._lib.AwaClientIterator_GetClientID.restype = c_char_p
        self._lib.AwaClientIterator_GetClientID.argtypes = [c_void_p]
        return self._lib.AwaClientIterator_GetClientID(iterator)

    @wrap(trace_in, trace_out)
    def AwaClientIterator_Free(self, iterator):
        self._lib.AwaClientIterator_Free.restype = c_int
        self._lib.AwaClientIterator_Free.argtypes = [c_void_p]
        mem = cast(iterator, POINTER(c_void_p))
        return self._lib.AwaClientIterator_Free(byref(mem))

    @wrap(trace_in, trace_out)
    def AwaServerListClientsOperation_NewClientIterator(self, operation):
        self._lib.AwaServerListClientsOperation_NewClientIterator.restype = c_void_p
        self._lib.AwaServerListClientsOperation_NewClientIterator.argtypes = [c_void_p]
        return self._lib.AwaServerListClientsOperation_NewClientIterator(operation)

    @wrap(trace_in, trace_out)
    def AwaServerListClientsOperation_GetResponse(self, operation, clientID):
        self._lib.AwaServerListClientsOperation_GetResponse.restype = c_void_p
        self._lib.AwaServerListClientsOperation_GetResponse.argtypes = [c_void_p, c_char_p]
        return self._lib.AwaServerListClientsOperation_GetResponse(operation, clientID)

    @wrap(trace_in, trace_out)
    def AwaServerListClientsResponse_NewRegisteredEntityIterator(self, response):
        self._lib.AwaServerListClientsResponse_NewRegisteredEntityIterator.restype = c_void_p
        self._lib.AwaServerListClientsResponse_NewRegisteredEntityIterator.argtypes = [c_void_p]
        return self._lib.AwaServerListClientsResponse_NewRegisteredEntityIterator(response)

    @wrap(trace_in, trace_out)
    def AwaRegisteredEntityIterator_Next(self, iterator):
        self._lib.AwaRegisteredEntityIterator_Next.restype = c_bool
        self._lib.AwaRegisteredEntityIterator_Next.argtypes = [c_void_p]
        return self._lib.AwaRegisteredEntityIterator_Next(iterator)

    @wrap(trace_in, trace_out)
    def AwaRegisteredEntityIterator_GetPath(self, iterator):
        self._lib.AwaRegisteredEntityIterator_GetPath.restype = c_char_p
        self._lib.AwaRegisteredEntityIterator_GetPath.argtypes = [c_void_p]
        return self._lib.AwaRegisteredEntityIterator_GetPath(iterator)

    @wrap(trace_in, trace_out)
    def AwaRegisteredEntityIterator_Free(self, iterator):
        self._lib.AwaRegisteredEntityIterator_Free.restype = c_int
        self._lib.AwaRegisteredEntityIterator_Free.argtypes = [c_void_p]
        mem = cast(iterator, POINTER(c_void_p))
        return self._lib.AwaRegisteredEntityIterator_Free(byref(mem))

    @wrap(trace_in, trace_out)
    def AwaServerDefineOperation_New(self, session):
        self._lib.AwaServerDefineOperation_New.restype = c_void_p
        self._lib.AwaServerDefineOperation_New.argtypes = [c_void_p]
        return self._lib.AwaServerDefineOperation_New(session)

    @wrap(trace_in, trace_out)
    def AwaServerDefineOperation_Add(self, operation, objectDefinition):
        self._lib.AwaServerDefineOperation_Add.restype = c_int
        self._lib.AwaServerDefineOperation_Add.argtypes = [c_void_p, c_void_p]
        return self._lib.AwaServerDefineOperation_Add(operation, objectDefinition)

    @wrap(trace_in, trace_out)
    def AwaServerDefineOperation_Perform(self, operation, timeout):
        self._lib.AwaServerDefineOperation_Perform.restype = c_int
        self._lib.AwaServerDefineOperation_Perform.argtypes = [c_void_p, c_int]
        return self._lib.AwaServerDefineOperation_Perform(operation, timeout)

    @wrap(trace_in, trace_out)
    def AwaServerDefineOperation_Free(self, operation):
        self._lib.AwaServerDefineOperation_Free.restype = c_int
        mem = cast(operation, POINTER(c_void_p))
        return self._lib.AwaServerDefineOperation_Free(byref(mem))

    @wrap(trace_in, trace_out)
    def AwaServerDefineOperation_GetResponse(self, operation):
        self._lib.AwaServerDefineOperation_GetResponse.restype = c_void_p
        self._lib.AwaServerDefineOperation_GetResponse.argtypes = [c_void_p]
        return self._lib.AwaServerDefineOperation_GetResponse(operation)

    @wrap(trace_in, trace_out)
    def AwaServerDefineResponse_NewPathIterator(self, response):
        self._lib.AwaServerDefineResponse_NewPathIterator.restype = c_void_p
        self._lib.AwaServerDefineResponse_NewPathIterator.argtypes = [c_void_p]
        return self._lib.AwaServerDefineResponse_NewPathIterator(response)

    @wrap(trace_in, trace_out)
    def AwaServerDefineResponse_GetPathResult(self, response, path):
        self._lib.AwaServerDefineResponse_GetPathResult.restype = c_void_p
        self._lib.AwaServerDefineResponse_GetPathResult.argtypes = [c_void_p, c_char_p]
        return self._lib.AwaServerDefineResponse_GetPathResult(response, path)

    @wrap(trace_in, trace_out)
    def AwaServerReadOperation_New(self, session):
        self._lib.AwaServerReadOperation_New.restype = c_void_p
        self._lib.AwaServerReadOperation_New.argtypes = [c_void_p]
        return self._lib.AwaServerReadOperation_New(session)

    @wrap(trace_in, trace_out)
    def AwaServerReadOperation_AddPath(self, operation, clientID, path):
        self._lib.AwaServerReadOperation_AddPath.restype = c_int
        self._lib.AwaServerReadOperation_AddPath.argtypes = [c_void_p, c_char_p, c_char_p]
        return self._lib.AwaServerReadOperation_AddPath(operation, clientID, path)

    @wrap(trace_in, trace_out)
    def AwaServerReadOperation_Perform(self, operation, timeout):
        self._lib.AwaServerReadOperation_Perform.restype = c_int
        self._lib.AwaServerReadOperation_Perform.argtypes = [c_void_p, c_int]
        return self._lib.AwaServerReadOperation_Perform(operation, timeout)

    @wrap(trace_in, trace_out)
    def AwaServerReadOperation_Free(self, operation):
        self._lib.AwaServerReadOperation_Free.restype = c_int
        mem = cast(operation, POINTER(c_void_p))
        return self._lib.AwaServerReadOperation_Free(byref(mem))

    @wrap(trace_in, trace_out)
    def AwaServerReadOperation_NewClientIterator(self, operation):
        self._lib.AwaServerReadOperation_NewClientIterator.restype = c_void_p
        self._lib.AwaServerReadOperation_NewClientIterator.argtypes = [c_void_p]
        return self._lib.AwaServerReadOperation_NewClientIterator(operation)

    @wrap(trace_in, trace_out)
    def AwaServerReadOperation_GetResponse(self, operation, clientID):
        self._lib.AwaServerReadOperation_GetResponse.restype = c_void_p
        self._lib.AwaServerReadOperation_GetResponse.argtypes = [c_void_p, c_char_p]
        return self._lib.AwaServerReadOperation_GetResponse(operation, clientID)

    @wrap(trace_in, trace_out)
    def AwaServerReadResponse_NewPathIterator(self, response):
        self._lib.AwaServerReadResponse_NewPathIterator.restype = c_void_p
        self._lib.AwaServerReadResponse_NewPathIterator.argtypes = [c_void_p]
        return self._lib.AwaServerReadResponse_NewPathIterator(response)

    @wrap(trace_in, trace_out)
    def AwaServerReadResponse_GetPathResult(self, response, path):
        self._lib.AwaServerReadResponse_GetPathResult.restype = c_void_p
        self._lib.AwaServerReadResponse_GetPathResult.argtypes = [c_void_p, c_char_p]
        return self._lib.AwaServerReadResponse_GetPathResult(response, path)

    @wrap(trace_in, trace_out)
    def AwaServerReadResponse_ContainsPath(self, response, path):
        self._lib.AwaServerReadResponse_ContainsPath.restype = c_bool
        self._lib.AwaServerReadResponse_ContainsPath.argtypes = [c_void_p, c_char_p]
        return self._lib.AwaServerReadResponse_ContainsPath(response, path)

    @wrap(trace_in, trace_out)
    def AwaServerReadResponse_HasValue(self, response, path):
        self._lib.AwaServerReadResponse_HasValue.restype = c_bool
        self._lib.AwaServerReadResponse_HasValue.argtypes = [c_void_p, c_char_p]
        return self._lib.AwaServerReadResponse_HasValue(response, path)

    @wrap(trace_in, trace_out)
    def AwaServerReadResponse_GetValueAsCStringPointer(self, response, path, value):
        self._lib.AwaServerReadResponse_GetValueAsCStringPointer.restype = c_int
        mem = cast(value, POINTER(c_char_p))
        ret = self._lib.AwaServerReadResponse_GetValueAsCStringPointer(response, path, byref(mem))

        result = None
        if ret == 0:
            result = cast(mem, c_char_p).value

        return result, ret

    @wrap(trace_in, trace_out)
    def AwaServerReadResponse_GetValueAsIntegerPointer(self, response, path, value):
        self._lib.AwaServerReadResponse_GetValueAsIntegerPointer.restype = c_int
        mem = cast(value, POINTER(POINTER(c_longlong)))
        ret = self._lib.AwaServerReadResponse_GetValueAsIntegerPointer(response, path, byref(mem))  # serialise as XML-RPC only supports 32 bit integers

        result = None
        if ret == 0:
            result = pickle.dumps(cast(mem, POINTER(c_longlong)).contents.value)
        return result, ret

    @wrap(trace_in, trace_out)
    def AwaServerReadResponse_GetValueAsFloatPointer(self, response, path, value):
        self._lib.AwaServerReadResponse_GetValueAsFloatPointer.restype = c_int
        mem = cast(value, POINTER(c_double))
        ret = self._lib.AwaServerReadResponse_GetValueAsFloatPointer(response, path, byref(mem))
        result = None
        if ret == 0:
            result = cast(mem, POINTER(c_double)).contents.value

        return result, ret

    @wrap(trace_in, trace_out)
    def AwaServerReadResponse_GetValueAsBooleanPointer(self, response, path, value):
        self._lib.AwaServerReadResponse_GetValueAsBooleanPointer.restype = c_int
        mem = cast(value, POINTER(c_bool))
        ret = self._lib.AwaServerReadResponse_GetValueAsBooleanPointer(response, path, byref(mem))
        result = None
        if ret == 0:
            result = cast(mem, POINTER(c_bool)).contents.value

        return result, ret

    @wrap(trace_in, trace_out)
    def AwaServerReadResponse_GetValueAsTimePointer(self, response, path, value):
        self._lib.AwaServerReadResponse_GetValueAsTimePointer.restype = c_int
        mem = cast(value, POINTER(POINTER(c_longlong)))
        ret = self._lib.AwaServerReadResponse_GetValueAsTimePointer(response, path, byref(mem))
        result = None
        if ret == 0:
            result = pickle.dumps(cast(mem, POINTER(c_longlong)).contents.value)  # serialise as XML-RPC only supports 32 bit integers

        return result, ret

    @wrap(trace_in, trace_out)
    def AwaServerReadResponse_GetValueAsOpaque(self, response, path, value):
        self._lib.AwaServerReadResponse_GetValueAsOpaque.restype = c_int
        self._lib.AwaServerReadResponse_GetValueAsOpaque.argtypes = [c_void_p, c_char_p, POINTER(AwaOpaque)]
        value = c_void_p()
        opaqueValue = AwaOpaque(value, 0)
        ret = self._lib.AwaServerReadResponse_GetValueAsOpaque(response, path, byref(opaqueValue))
        result = None
        if ret == 0:
            result = AwaOpaqueToBase64(opaqueValue)

        return result, ret

    @wrap(trace_in, trace_out)
    def AwaServerReadResponse_GetValueAsObjectLink(self, response, path, value):
        self._lib.AwaServerReadResponse_GetValueAsObjectLink.restype = c_int
        self._lib.AwaServerReadResponse_GetValueAsObjectLink.argtypes = [c_void_p, c_char_p, c_void_p]
        return self._lib.AwaServerReadResponse_GetValueAsObjectLink(response, path, value)

    @wrap(trace_in, trace_out)
    def AwaServerReadResponse_GetValuesAsStringArrayPointer(self, response, path, valueArray):
        self._lib.AwaServerReadResponse_GetValuesAsStringArrayPointer.restype = c_int
        mem = cast(valueArray, POINTER(c_void_p))
        ret = self._lib.AwaServerReadResponse_GetValuesAsStringArrayPointer(response, path, byref(mem))
        result = {}
        iterator = self._lib.AwaStringArray_NewCStringArrayIterator(mem)
        if iterator != None:
            while self._lib.AwaCStringArrayIterator_Next(iterator):
                index = self._lib.AwaCStringArrayIterator_GetIndex(iterator)
                value = cast(self._lib.AwaCStringArrayIterator_GetValueAsCString(iterator), c_char_p).value
                result[index] = value
            self._lib.AwaCStringArrayIterator_Free(byref(cast(iterator, POINTER(c_void_p))))

        return pickle.dumps(result)

    @wrap(trace_in, trace_out)
    def AwaServerReadResponse_GetValuesAsIntegerArrayPointer(self, response, path, valueArray):
        self._lib.AwaServerReadResponse_GetValuesAsIntegerArrayPointer.restype = c_int
        mem = cast(valueArray, POINTER(c_void_p))
        ret = self._lib.AwaServerReadResponse_GetValuesAsIntegerArrayPointer(response, path, byref(mem))
        result = {}
        iterator = self._lib.AwaIntegerArray_NewIntegerArrayIterator(mem)
        if iterator != None:
            while self._lib.AwaIntegerArrayIterator_Next(iterator):
                index = self._lib.AwaIntegerArrayIterator_GetIndex(iterator)
                value = self._lib.AwaIntegerArrayIterator_GetValue(iterator)
                result[index] = value
            self._lib.AwaIntegerArrayIterator_Free(byref(cast(iterator, POINTER(c_void_p))))

        return pickle.dumps(result)

    @wrap(trace_in, trace_out)
    def AwaServerReadResponse_GetValuesAsFloatArrayPointer(self, response, path, valueArray):
        self._lib.AwaServerReadResponse_GetValuesAsFloatArrayPointer.restype = c_int
        mem = cast(valueArray, POINTER(c_void_p))
        ret = self._lib.AwaServerReadResponse_GetValuesAsFloatArrayPointer(response, path, byref(mem))
        result = {}
        iterator = self._lib.AwaFloatArray_NewFloatArrayIterator(mem)
        if iterator != None:
            while self._lib.AwaFloatArrayIterator_Next(iterator):
                index = self._lib.AwaFloatArrayIterator_GetIndex(iterator)
                value = self._lib.AwaFloatArrayIterator_GetValue(iterator)
                result[index] = value
            self._lib.AwaFloatArrayIterator_Free(byref(cast(iterator, POINTER(c_void_p))))

        return pickle.dumps(result)

    @wrap(trace_in, trace_out)
    def AwaServerReadResponse_GetValuesAsBooleanArrayPointer(self, response, path, valueArray):
        self._lib.AwaServerReadResponse_GetValuesAsBooleanArrayPointer.restype = c_int
        mem = cast(valueArray, POINTER(c_void_p))
        ret = self._lib.AwaServerReadResponse_GetValuesAsBooleanArrayPointer(response, path, byref(mem))
        result = {}
        iterator = self._lib.AwaBooleanArray_NewBooleanArrayIterator(mem)
        if iterator != None:
            while self._lib.AwaBooleanArrayIterator_Next(iterator):
                index = self._lib.AwaBooleanArrayIterator_GetIndex(iterator)
                value = self._lib.AwaBooleanArrayIterator_GetValue(iterator)
                result[index] = value
            self._lib.AwaBooleanArrayIterator_Free(byref(cast(iterator, POINTER(c_void_p))))

        return pickle.dumps(result)

    @wrap(trace_in, trace_out)
    def AwaServerReadResponse_GetValuesAsTimeArrayPointer(self, response, path, valueArray):
        self._lib.AwaServerReadResponse_GetValuesAsTimeArrayPointer.restype = c_int
        mem = cast(valueArray, POINTER(c_void_p))
        ret = self._lib.AwaServerReadResponse_GetValuesAsTimeArrayPointer(byref(mem))
        result = {}
        iterator = self._lib.AwaTimeArray_NewTimeArrayIterator(mem)
        if iterator != None:
            while self._lib.AwaTimeArrayIterator_Next(iterator):
                index = self._lib.AwaTimeArrayIterator_GetIndex(iterator)
                value = self._lib.AwaTimeArrayIterator_GetValue(iterator)
                result[index] = value
            self._lib.AwaTimeArrayIterator_Free(byref(cast(iterator, POINTER(c_void_p))))

        return pickle.dumps(result)

    @wrap(trace_in, trace_out)
    def AwaServerReadResponse_GetValuesAsOpaqueArrayPointer(self, response, path, valueArray):
        self._lib.AwaServerReadResponse_GetValuesAsOpaqueArrayPointer.restype = c_int
        mem = cast(valueArray, POINTER(c_void_p))
        ret = self._lib.AwaServerReadResponse_GetValuesAsOpaqueArrayPointer(response, path, byref(mem))
        result = {}
        iterator = self._lib.AwaOpaqueArray_NewOpaqueArrayIterator(mem)
        if iterator != None:
            while self._lib.AwaOpaqueArrayIterator_Next(iterator):
                index = self._lib.AwaOpaqueArrayIterator_GetIndex(iterator)
                value = self._lib.AwaOpaqueArrayIterator_GetValue(iterator)
                result[index] = value
            self._lib.AwaOpaqueArrayIterator_Free(byref(cast(iterator, POINTER(c_void_p))))

        return pickle.dumps(result)

    @wrap(trace_in, trace_out)
    def AwaServerReadResponse_GetValuesAsObjectLinkArrayPointer(self, response, path, valueArray):
        self._lib.AwaServerReadResponse_GetValuesAsObjectLinkArrayPointer.restype = c_int
        mem = cast(valueArray, POINTER(c_void_p))
        ret = self._lib.AwaServerReadResponse_GetValuesAsObjectLinkArrayPointer(response, path, byref(mem))
        result = {}
        iterator = self._lib.AwaObjectLinkArray_NewObjectLinkArrayIterator(mem)
        if iterator != None:
            while self._lib.AwaObjectLinkArrayIterator_Next(iterator):
                index = self._lib.AwaObjectLinkArrayIterator_GetIndex(iterator)
                value = self._lib.AwaObjectLinkArrayIterator_GetValue(iterator)
                result[index] = value
            self._lib.AwaObjectLinkArrayIterator_Free(byref(cast(iterator, POINTER(c_void_p))))

        return pickle.dumps(result)

    @wrap(trace_in, trace_out)
    def AwaServerWriteOperation_New(self, session, defaultMode):
        self._lib.AwaServerWriteOperation_New.restype = c_void_p
        self._lib.AwaServerWriteOperation_New.argtypes = [c_void_p, c_longlong]
        return self._lib.AwaServerWriteOperation_New(session, defaultMode)

    @wrap(trace_in, trace_out)
    def AwaServerWriteOperation_SetObjectInstanceWriteMode(self, operation, path, mode):
        self._lib.AwaServerWriteOperation_SetObjectInstanceWriteMode.restype = c_int
        self._lib.AwaServerWriteOperation_SetObjectInstanceWriteMode.argtypes = [c_void_p, c_char_p, c_void_p]
        return self._lib.AwaServerWriteOperation_SetObjectInstanceWriteMode(operation, path, mode)

    @wrap(trace_in, trace_out)
    def AwaServerWriteOperation_SetResourceInstancesWriteMode(self, operation, path, mode):
        self._lib.AwaServerWriteOperation_SetResourceInstancesWriteMode.restype = c_int
        self._lib.AwaServerWriteOperation_SetResourceInstancesWriteMode.argtypes = [c_void_p, c_char_p, c_void_p]
        return self._lib.AwaServerWriteOperation_SetResourceInstancesWriteMode(operation, path, mode)

    @wrap(trace_in, trace_out)
    def AwaServerWriteOperation_AddValueAsCString(self, operation, path, value):
        self._lib.AwaServerWriteOperation_AddValueAsCString.restype = c_int
        self._lib.AwaServerWriteOperation_AddValueAsCString.argtypes = [c_void_p, c_char_p, c_char_p]
        return self._lib.AwaServerWriteOperation_AddValueAsCString(operation, path, value)

    @wrap(trace_in, trace_out)
    def AwaServerWriteOperation_AddValueAsInteger(self, operation, path, value):
        self._lib.AwaServerWriteOperation_AddValueAsInteger.restype = c_int
        self._lib.AwaServerWriteOperation_AddValueAsInteger.argtypes = [c_void_p, c_char_p, c_longlong]
        return self._lib.AwaServerWriteOperation_AddValueAsInteger(operation, path, value)

    @wrap(trace_in, trace_out)
    def AwaServerWriteOperation_AddValueAsFloat(self, operation, path, value):
        self._lib.AwaServerWriteOperation_AddValueAsFloat.restype = c_int
        self._lib.AwaServerWriteOperation_AddValueAsFloat.argtypes = [c_void_p, c_char_p, c_double]
        return self._lib.AwaServerWriteOperation_AddValueAsFloat(operation, path, value)

    @wrap(trace_in, trace_out)
    def AwaServerWriteOperation_AddValueAsBoolean(self, operation, path, value):
        self._lib.AwaServerWriteOperation_AddValueAsBoolean.restype = c_int
        self._lib.AwaServerWriteOperation_AddValueAsBoolean.argtypes = [c_void_p, c_char_p, c_bool]
        return self._lib.AwaServerWriteOperation_AddValueAsBoolean(operation, path, value)

    @wrap(trace_in, trace_out)
    def AwaServerWriteOperation_AddValueAsTime(self, operation, path, value):
        self._lib.AwaServerWriteOperation_AddValueAsTime.restype = c_int
        self._lib.AwaServerWriteOperation_AddValueAsTime.argtypes = [c_void_p, c_char_p, c_longlong]
        return self._lib.AwaServerWriteOperation_AddValueAsTime(operation, path, value)

    @wrap(trace_in, trace_out)
    def AwaServerWriteOperation_AddValueAsOpaque(self, operation, path, value):
        self._lib.AwaServerWriteOperation_AddValueAsOpaque.restype = c_int
        self._lib.AwaServerWriteOperation_AddValueAsOpaque.argtypes = [c_void_p, c_char_p, AwaOpaque]
        #mem = cast(value, c_void_p)
        opaqueValue = None
        if isinstance(value, str):
            mem = cast(value, c_void_p)
            opaqueValue = AwaOpaque(mem, len(value))
        else:
            mem = cast(value.data, c_void_p)
            opaqueValue = AwaOpaque(mem, len(value.data))

        return self._lib.AwaServerWriteOperation_AddValueAsOpaque(operation, path, opaqueValue)

    @wrap(trace_in, trace_out)
    def AwaServerWriteOperation_AddValueAsObjectLink(self, operation, path, value):
        self._lib.AwaServerWriteOperation_AddValueAsObjectLink.restype = c_int
        self._lib.AwaServerWriteOperation_AddValueAsObjectLink.argtypes = [c_void_p, c_char_p, c_void_p]
        return self._lib.AwaServerWriteOperation_AddValueAsObjectLink(operation, path, value)

    @wrap(trace_in, trace_out)
    def AwaServerWriteOperation_AddValueAsStringArray(self, operation, path, array):
        self._lib.AwaServerWriteOperation_AddValueAsStringArray.restype = c_int
        self._lib.AwaServerWriteOperation_AddValueAsStringArray.argtypes = [c_void_p, c_char_p, c_void_p]
        return self._lib.AwaServerWriteOperation_AddValueAsStringArray(operation, path, array)

    @wrap(trace_in, trace_out)
    def AwaServerWriteOperation_AddValueAsIntegerArray(self, operation, path, array):
        self._lib.AwaServerWriteOperation_AddValueAsIntegerArray.restype = c_int
        self._lib.AwaServerWriteOperation_AddValueAsIntegerArray.argtypes = [c_void_p, c_char_p, c_void_p]
        return self._lib.AwaServerWriteOperation_AddValueAsIntegerArray(operation, path, array)

    @wrap(trace_in, trace_out)
    def AwaServerWriteOperation_AddValueAsFloatArray(self, operation, path, array):
        self._lib.AwaServerWriteOperation_AddValueAsFloatArray.restype = c_int
        self._lib.AwaServerWriteOperation_AddValueAsFloatArray.argtypes = [c_void_p, c_char_p, c_void_p]
        return self._lib.AwaServerWriteOperation_AddValueAsFloatArray(operation, path, array)

    @wrap(trace_in, trace_out)
    def AwaServerWriteOperation_AddValueAsBooleanArray(self, operation, path, array):
        self._lib.AwaServerWriteOperation_AddValueAsBooleanArray.restype = c_int
        self._lib.AwaServerWriteOperation_AddValueAsBooleanArray.argtypes = [c_void_p, c_char_p, c_void_p]
        return self._lib.AwaServerWriteOperation_AddValueAsBooleanArray(operation, path, array)

    @wrap(trace_in, trace_out)
    def AwaServerWriteOperation_AddValueAsTimeArray(self, operation, path, array):
        self._lib.AwaServerWriteOperation_AddValueAsTimeArray.restype = c_int
        self._lib.AwaServerWriteOperation_AddValueAsTimeArray.argtypes = [c_void_p, c_char_p, c_void_p]
        return self._lib.AwaServerWriteOperation_AddValueAsTimeArray(operation, path, array)

    @wrap(trace_in, trace_out)
    def AwaServerWriteOperation_AddValueAsOpaqueArray(self, operation, path, array):
        self._lib.AwaServerWriteOperation_AddValueAsOpaqueArray.restype = c_int
        self._lib.AwaServerWriteOperation_AddValueAsOpaqueArray.argtypes = [c_void_p, c_char_p, c_void_p]
        return self._lib.AwaServerWriteOperation_AddValueAsOpaqueArray(operation, path, array)

    @wrap(trace_in, trace_out)
    def AwaServerWriteOperation_AddValueAsObjectLinkArray(self, operation, path, array):
        self._lib.AwaServerWriteOperation_AddValueAsObjectLinkArray.restype = c_int
        self._lib.AwaServerWriteOperation_AddValueAsObjectLinkArray.argtypes = [c_void_p, c_char_p, c_void_p]
        return self._lib.AwaServerWriteOperation_AddValueAsObjectLinkArray(operation, path, array)

    @wrap(trace_in, trace_out)
    def AwaServerWriteOperation_AddArrayValueAsCString(self, operation, path, resourceInstanceID, value):
        self._lib.AwaServerWriteOperation_AddArrayValueAsCString.restype = c_int
        self._lib.AwaServerWriteOperation_AddArrayValueAsCString.argtypes = [c_void_p, c_char_p, c_int, c_char_p]
        return self._lib.AwaServerWriteOperation_AddArrayValueAsCString(operation, path, resourceInstanceID, value)

    @wrap(trace_in, trace_out)
    def AwaServerWriteOperation_AddArrayValueAsInteger(self, operation, path, resourceInstanceID, value):
        self._lib.AwaServerWriteOperation_AddArrayValueAsInteger.restype = c_int
        self._lib.AwaServerWriteOperation_AddArrayValueAsInteger.argtypes = [c_void_p, c_char_p, c_int, c_longlong]
        return self._lib.AwaServerWriteOperation_AddArrayValueAsInteger(operation, path, resourceInstanceID, value)

    @wrap(trace_in, trace_out)
    def AwaServerWriteOperation_AddArrayValueAsFloat(self, operation, path, resourceInstanceID, value):
        self._lib.AwaServerWriteOperation_AddArrayValueAsFloat.restype = c_int
        self._lib.AwaServerWriteOperation_AddArrayValueAsFloat.argtypes = [c_void_p, c_char_p, c_int, c_double]
        return self._lib.AwaServerWriteOperation_AddArrayValueAsFloat(operation, path, resourceInstanceID, value)

    @wrap(trace_in, trace_out)
    def AwaServerWriteOperation_AddArrayValueAsBoolean(self, operation, path, resourceInstanceID, value):
        self._lib.AwaServerWriteOperation_AddArrayValueAsBoolean.restype = c_int
        self._lib.AwaServerWriteOperation_AddArrayValueAsBoolean.argtypes = [c_void_p, c_char_p, c_int, c_bool]
        return self._lib.AwaServerWriteOperation_AddArrayValueAsBoolean(operation, path, resourceInstanceID, value)

    @wrap(trace_in, trace_out)
    def AwaServerWriteOperation_AddArrayValueAsTime(self, operation, path, resourceInstanceID, value):
        self._lib.AwaServerWriteOperation_AddArrayValueAsTime.restype = c_int
        self._lib.AwaServerWriteOperation_AddArrayValueAsTime.argtypes = [c_void_p, c_char_p, c_int, c_longlong]
        return self._lib.AwaServerWriteOperation_AddArrayValueAsTime(operation, path, resourceInstanceID, value)

    @wrap(trace_in, trace_out)
    def AwaServerWriteOperation_AddArrayValueAsOpaque(self, operation, path, resourceInstanceID, value):
        self._lib.AwaServerWriteOperation_AddArrayValueAsOpaque.restype = c_int
        self._lib.AwaServerWriteOperation_AddArrayValueAsOpaque.argtypes = [c_void_p, c_char_p, c_int, c_void_p]
        return self._lib.AwaServerWriteOperation_AddArrayValueAsOpaque(operation, path, resourceInstanceID, value)

    @wrap(trace_in, trace_out)
    def AwaServerWriteOperation_AddArrayValueAsObjectLink(self, operation, path, resourceInstanceID, value):
        self._lib.AwaServerWriteOperation_AddArrayValueAsObjectLink.restype = c_int
        self._lib.AwaServerWriteOperation_AddArrayValueAsObjectLink.argtypes = [c_void_p, c_char_p, c_int, c_void_p]
        return self._lib.AwaServerWriteOperation_AddArrayValueAsObjectLink(operation, path, resourceInstanceID, value)

    @wrap(trace_in, trace_out)
    def AwaServerWriteOperation_Perform(self, operation, clientID, timeout):
        self._lib.AwaServerWriteOperation_Perform.restype = c_int
        self._lib.AwaServerWriteOperation_Perform.argtypes = [c_void_p, c_char_p, c_int]
        return self._lib.AwaServerWriteOperation_Perform(operation, clientID, timeout)

    @wrap(trace_in, trace_out)
    def AwaServerWriteOperation_Free(self, operation):
        self._lib.AwaServerWriteOperation_Free.restype = c_int
        mem = cast(operation, POINTER(c_void_p))
        return self._lib.AwaServerWriteOperation_Free(byref(mem))

    @wrap(trace_in, trace_out)
    def AwaServerWriteOperation_NewClientIterator(self, operation):
        self._lib.AwaServerWriteOperation_NewClientIterator.restype = c_void_p
        self._lib.AwaServerWriteOperation_NewClientIterator.argtypes = [c_void_p]
        return self._lib.AwaServerWriteOperation_NewClientIterator(operation)

    @wrap(trace_in, trace_out)
    def AwaServerWriteOperation_GetResponse(self, operation, clientID):
        self._lib.AwaServerWriteOperation_GetResponse.restype = c_void_p
        self._lib.AwaServerWriteOperation_GetResponse.argtypes = [c_void_p, c_char_p]
        return self._lib.AwaServerWriteOperation_GetResponse(operation, clientID)

    @wrap(trace_in, trace_out)
    def AwaServerWriteOperation_CreateObjectInstance(self, operation, path):
        self._lib.AwaServerWriteOperation_CreateObjectInstance.restype = c_int
        self._lib.AwaServerWriteOperation_GetResponse.argtypes = [c_void_p, c_char_p]
        return self._lib.AwaServerWriteOperation_CreateObjectInstance(operation, path)

    @wrap(trace_in, trace_out)
    def AwaServerWriteResponse_NewPathIterator(self, response):
        self._lib.AwaServerWriteResponse_NewPathIterator.restype = c_void_p
        self._lib.AwaServerWriteResponse_NewPathIterator.argtypes = [c_void_p]
        return self._lib.AwaServerWriteResponse_NewPathIterator(response)

    @wrap(trace_in, trace_out)
    def AwaServerWriteResponse_GetPathResult(self, response, path):
        self._lib.AwaServerWriteResponse_GetPathResult.restype = c_void_p
        self._lib.AwaServerWriteResponse_GetPathResult.argtypes = [c_void_p, c_char_p]
        return self._lib.AwaServerWriteResponse_GetPathResult(response, path)

    @wrap(trace_in, trace_out)
    def AwaServerDeleteOperation_New(self, session):
        self._lib.AwaServerDeleteOperation_New.restype = c_void_p
        self._lib.AwaServerDeleteOperation_New.argtypes = [c_void_p]
        return self._lib.AwaServerDeleteOperation_New(session)

    @wrap(trace_in, trace_out)
    def AwaServerDeleteOperation_AddPath(self, operation, clientID, path):
        self._lib.AwaServerDeleteOperation_AddPath.restype = c_int
        self._lib.AwaServerDeleteOperation_AddPath.argtypes = [c_void_p, c_char_p, c_char_p]
        return self._lib.AwaServerDeleteOperation_AddPath(operation, clientID, path)

    @wrap(trace_in, trace_out)
    def AwaServerDeleteOperation_Perform(self, operation, timeout):
        self._lib.AwaServerDeleteOperation_Perform.restype = c_int
        self._lib.AwaServerDeleteOperation_Perform.argtypes = [c_void_p, c_int]
        return self._lib.AwaServerDeleteOperation_Perform(operation, timeout)

    @wrap(trace_in, trace_out)
    def AwaServerDeleteOperation_Free(self, operation):
        self._lib.AwaServerDeleteOperation_Free.restype = c_int
        mem = cast(operation, POINTER(c_void_p))
        return self._lib.AwaServerDeleteOperation_Free(byref(mem))

    @wrap(trace_in, trace_out)
    def AwaServerDeleteOperation_NewClientIterator(self, operation):
        self._lib.AwaServerDeleteOperation_NewClientIterator.restype = c_void_p
        self._lib.AwaServerDeleteOperation_NewClientIterator.argtypes = [c_void_p]
        return self._lib.AwaServerDeleteOperation_NewClientIterator(operation)

    @wrap(trace_in, trace_out)
    def AwaServerDeleteOperation_GetResponse(self, operation, clientID):
        self._lib.AwaServerDeleteOperation_GetResponse.restype = c_void_p
        self._lib.AwaServerDeleteOperation_GetResponse.argtypes = [c_void_p, c_char_p]
        return self._lib.AwaServerDeleteOperation_GetResponse(operation, clientID)

    @wrap(trace_in, trace_out)
    def AwaServerDeleteResponse_NewPathIterator(self, response):
        self._lib.AwaServerDeleteResponse_NewPathIterator.restype = c_void_p
        self._lib.AwaServerDeleteResponse_NewPathIterator.argtypes = [c_void_p]
        return self._lib.AwaServerDeleteResponse_NewPathIterator(response)

    @wrap(trace_in, trace_out)
    def AwaServerDeleteResponse_GetPathResult(self, response, path):
        self._lib.AwaServerDeleteResponse_GetPathResult.restype = c_void_p
        self._lib.AwaServerDeleteResponse_GetPathResult.argtypes = [c_void_p, c_char_p]
        return self._lib.AwaServerDeleteResponse_GetPathResult(response, path)

    @wrap(trace_in, trace_out)
    def AwaServerExecuteOperation_New(self, session):
        self._lib.AwaServerExecuteOperation_New.restype = c_void_p
        self._lib.AwaServerExecuteOperation_New.argtypes = [c_void_p]
        return self._lib.AwaServerExecuteOperation_New(session)

    @wrap(trace_in, trace_out)
    def AwaServerExecuteOperation_AddPath(self, operation, clientID, path, arguments):
        self._lib.AwaServerExecuteOperation_AddPath.restype = c_int
        self._lib.AwaServerExecuteOperation_AddPath.argtypes = [c_void_p, c_char_p, c_char_p, c_void_p]
        return self._lib.AwaServerExecuteOperation_AddPath(operation, clientID, path, arguments)

    @wrap(trace_in, trace_out)
    def AwaServerExecuteOperation_Perform(self, operation, timeout):
        self._lib.AwaServerExecuteOperation_Perform.restype = c_int
        self._lib.AwaServerExecuteOperation_Perform.argtypes = [c_void_p, c_int]
        return self._lib.AwaServerExecuteOperation_Perform(operation, timeout)

    @wrap(trace_in, trace_out)
    def AwaServerExecuteOperation_Free(self, operation):
        self._lib.AwaServerExecuteOperation_Free.restype = c_int
        mem = cast(operation, POINTER(c_void_p))
        return self._lib.AwaServerExecuteOperation_Free(byref(mem))

    @wrap(trace_in, trace_out)
    def AwaServerExecuteOperation_NewClientIterator(self, operation):
        self._lib.AwaServerExecuteOperation_NewClientIterator.restype = c_void_p
        self._lib.AwaServerExecuteOperation_NewClientIterator.argtypes = [c_void_p]
        return self._lib.AwaServerExecuteOperation_NewClientIterator(operation)

    @wrap(trace_in, trace_out)
    def AwaServerExecuteOperation_GetResponse(self, operation, clientID):
        self._lib.AwaServerExecuteOperation_GetResponse.restype = c_void_p
        self._lib.AwaServerExecuteOperation_GetResponse.argtypes = [c_void_p, c_char_p]
        return self._lib.AwaServerExecuteOperation_GetResponse(operation, clientID)

    @wrap(trace_in, trace_out)
    def AwaServerExecuteResponse_NewPathIterator(self, response):
        self._lib.AwaServerExecuteResponse_NewPathIterator.restype = c_void_p
        self._lib.AwaServerExecuteResponse_NewPathIterator.argtypes = [c_void_p]
        return self._lib.AwaServerExecuteResponse_NewPathIterator(response)

    @wrap(trace_in, trace_out)
    def AwaServerExecuteResponse_GetPathResult(self, response, path):
        self._lib.AwaServerExecuteResponse_GetPathResult.restype = c_void_p
        self._lib.AwaServerExecuteResponse_GetPathResult.argtypes = [c_void_p, c_char_p]
        return self._lib.AwaServerExecuteResponse_GetPathResult(response, path)

    @wrap(trace_in, trace_out)
    def AwaServerWriteAttributesOperation_New(self, session):
        self._lib.AwaServerWriteAttributesOperation_New.restype = c_void_p
        self._lib.AwaServerWriteAttributesOperation_New.argtypes = [c_void_p]
        return self._lib.AwaServerWriteAttributesOperation_New(session)

    @wrap(trace_in, trace_out)
    def AwaServerWriteAttributesOperation_AddAttributeAsInteger(self, operation, clientID, path, link, value):
        self._lib.AwaServerWriteAttributesOperation_AddAttributeAsInteger.restype = c_int
        self._lib.AwaServerWriteAttributesOperation_AddAttributeAsInteger.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p, c_longlong]
        return self._lib.AwaServerWriteAttributesOperation_AddAttributeAsInteger(operation, clientID, path, link, value)

    @wrap(trace_in, trace_out)
    def AwaServerWriteAttributesOperation_AddAttributeAsFloat(self, operation, clientID, path, link, value):
        self._lib.AwaServerWriteAttributesOperation_AddAttributeAsFloat.restype = c_int
        self._lib.AwaServerWriteAttributesOperation_AddAttributeAsFloat.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p, c_double]
        return self._lib.AwaServerWriteAttributesOperation_AddAttributeAsFloat(operation, clientID, path, link, value)

    @wrap(trace_in, trace_out)
    def AwaServerWriteAttributesOperation_Perform(self, operation, timeout):
        self._lib.AwaServerWriteAttributesOperation_Perform.restype = c_int
        self._lib.AwaServerWriteAttributesOperation_Perform.argtypes = [c_void_p, c_int]
        return self._lib.AwaServerWriteAttributesOperation_Perform(operation, timeout)

    @wrap(trace_in, trace_out)
    def AwaServeWriteAttributesOperation_Free(self, operation):
        self._lib.AwaServeWriteAttributesOperation_Free.restype = c_int
        mem = cast(operation, POINTER(c_void_p))
        return self._lib.AwaServeWriteAttributesOperation_Free(byref(mem))

    @wrap(trace_in, trace_out)
    def AwaServerWriteAttributesOperation_NewClientIterator(self, operation):
        self._lib.AwaServerWriteAttributesOperation_NewClientIterator.restype = c_void_p
        self._lib.AwaServerWriteAttributesOperation_NewClientIterator.argtypes = [c_void_p]
        return self._lib.AwaServerWriteAttributesOperation_NewClientIterator(operation)

    @wrap(trace_in, trace_out)
    def AwaServerWriteAttributesOperation_GetResponse(self, operation, clientID):
        self._lib.AwaServerWriteAttributesOperation_GetResponse.restype = c_void_p
        self._lib.AwaServerWriteAttributesOperation_GetResponse.argtypes = [c_void_p, c_char_p]
        return self._lib.AwaServerWriteAttributesOperation_GetResponse(operation, clientID)

    @wrap(trace_in, trace_out)
    def AwaServerWriteAttributesResponse_NewPathIterator(self, response):
        self._lib.AwaServerWriteAttributesResponse_NewPathIterator.restype = c_void_p
        self._lib.AwaServerWriteAttributesResponse_NewPathIterator.argtypes = [c_void_p]
        return self._lib.AwaServerWriteAttributesResponse_NewPathIterator(response)

    @wrap(trace_in, trace_out)
    def AwaServerWriteAttributesResponse_GetPathResult(self, response, path):
        self._lib.AwaServerWriteAttributesResponse_GetPathResult.restype = c_void_p
        self._lib.AwaServerWriteAttributesResponse_GetPathResult.argtypes = [c_void_p, c_char_p]
        return self._lib.AwaServerWriteAttributesResponse_GetPathResult(response, path)

    @wrap(trace_in, trace_out)
    def AwaServerDiscoverOperation_New(self, session):
        self._lib.AwaServerDiscoverOperation_New.restype = c_void_p
        self._lib.AwaServerDiscoverOperation_New.argtypes = [c_void_p]
        return self._lib.AwaServerDiscoverOperation_New(session)

    @wrap(trace_in, trace_out)
    def AwaServerDiscoverOperation_AddPath(self, operation, clientID, path):
        self._lib.AwaServerDiscoverOperation_AddPath.restype = c_int
        self._lib.AwaServerDiscoverOperation_AddPath.argtypes = [c_void_p, c_char_p, c_char_p]
        return self._lib.AwaServerDiscoverOperation_AddPath(operation, clientID, path)

    @wrap(trace_in, trace_out)
    def AwaServerDiscoverOperation_Perform(self, operation, timeout):
        self._lib.AwaServerDiscoverOperation_Perform.restype = c_int
        self._lib.AwaServerDiscoverOperation_Perform.argtypes = [c_void_p, c_int]
        return self._lib.AwaServerDiscoverOperation_Perform(operation, timeout)

    @wrap(trace_in, trace_out)
    def AwaServerDiscoverOperation_Free(self, operation):
        self._lib.AwaServerDiscoverOperation_Free.restype = c_int
        mem = cast(operation, POINTER(c_void_p))
        return self._lib.AwaServerDiscoverOperation_Free(byref(mem))

    @wrap(trace_in, trace_out)
    def AwaServerDiscoverOperation_NewClientIterator(self, operation):
        self._lib.AwaServerDiscoverOperation_NewClientIterator.restype = c_void_p
        self._lib.AwaServerDiscoverOperation_NewClientIterator.argtypes = [c_void_p]
        return self._lib.AwaServerDiscoverOperation_NewClientIterator(operation)

    @wrap(trace_in, trace_out)
    def AwaServerDiscoverOperation_GetResponse(self, operation, clientID):
        self._lib.AwaServerDiscoverOperation_GetResponse.restype = c_void_p
        self._lib.AwaServerDiscoverOperation_GetResponse.argtypes = [c_void_p, c_char_p]
        return self._lib.AwaServerDiscoverOperation_GetResponse(operation, clientID)

    @wrap(trace_in, trace_out)
    def AwaServerDiscoverResponse_NewPathIterator(self, response):
        self._lib.AwaServerDiscoverResponse_NewPathIterator.restype = c_void_p
        self._lib.AwaServerDiscoverResponse_NewPathIterator.argtypes = [c_void_p]
        return self._lib.AwaServerDiscoverResponse_NewPathIterator(response)

    @wrap(trace_in, trace_out)
    def AwaServerDiscoverResponse_GetPathResult(self, response, path):
        self._lib.AwaServerDiscoverResponse_GetPathResult.restype = c_void_p
        self._lib.AwaServerDiscoverResponse_GetPathResult.argtypes = [c_void_p, c_char_p]
        return self._lib.AwaServerDiscoverResponse_GetPathResult(response, path)

    @wrap(trace_in, trace_out)
    def AwaServerDiscoverResponse_ContainsPath(self, response, path):
        self._lib.AwaServerDiscoverResponse_ContainsPath.restype = c_bool
        self._lib.AwaServerDiscoverResponse_ContainsPath.argtypes = [c_void_p, c_char_p]
        return self._lib.AwaServerDiscoverResponse_ContainsPath(response, path)

    @wrap(trace_in, trace_out)
    def AwaServerDiscoverResponse_NewAttributeIterator(self, response, path):
        self._lib.AwaServerDiscoverResponse_NewAttributeIterator.restype = c_void_p
        self._lib.AwaServerDiscoverResponse_NewAttributeIterator.argtypes = [c_void_p, c_char_p]
        return self._lib.AwaServerDiscoverResponse_NewAttributeIterator(response, path)

    @wrap(trace_in, trace_out)
    def AwaAttributeIterator_Next(self, iterator):
        self._lib.AwaAttributeIterator_Next.restype = c_bool
        self._lib.AwaAttributeIterator_Next.argtypes = [c_void_p]
        return self._lib.AwaAttributeIterator_Next(iterator)

    @wrap(trace_in, trace_out)
    def AwaAttributeIterator_GetLink(self, iterator):
        self._lib.AwaAttributeIterator_GetLink.restype = c_char_p
        self._lib.AwaAttributeIterator_GetLink.argtypes = [c_void_p]
        return self._lib.AwaAttributeIterator_GetLink(iterator)

    @wrap(trace_in, trace_out)
    def AwaAttributeIterator_Free(self, iterator):
        self._lib.AwaAttributeIterator_Free.restype = c_void_p
        mem = cast(iterator, POINTER(c_void_p))
        return self._lib.AwaAttributeIterator_Free(byref(mem))

    @wrap(trace_in, trace_out)
    def AwaServerDiscoverResponse_GetAttributeValueAsIntegerPointer(self, response, path, link, value):
        self._lib.AwaServerDiscoverResponse_GetAttributeValueAsIntegerPointer.restype = c_int
        mem = cast(value, POINTER(c_longlong))
        return self._lib.AwaServerDiscoverResponse_GetAttributeValueAsIntegerPointer(byref(mem))

    @wrap(trace_in, trace_out)
    def AwaServerDiscoverResponse_GetAttributeValueAsFloatPointer(self, response, path, link, value):
        self._lib.AwaServerDiscoverResponse_GetAttributeValueAsFloatPointer.restype = c_int
        mem = cast(value, POINTER(c_double))
        return self._lib.AwaServerDiscoverResponse_GetAttributeValueAsFloatPointer(byref(mem))

    @wrap(trace_in, trace_out)
    def AwaServerCreateOperation_New(self, session):
        self._lib.AwaServerCreateOperation_New.restype = c_void_p
        self._lib.AwaServerCreateOperation_New.argtypes = [c_void_p]
        return self._lib.AwaServerCreateOperation_New(session)

    @wrap(trace_in, trace_out)
    def AwaServerCreateOperation_AddPath(self, operation, clientID, path):
        self._lib.AwaServerCreateOperation_AddPath.restype = c_int
        self._lib.AwaServerCreateOperation_AddPath.argtypes = [c_void_p, c_char_p, c_char_p]
        return self._lib.AwaServerCreateOperation_AddPath(operation, clientID, path)

    @wrap(trace_in, trace_out)
    def AwaServerCreateOperation_Perform(self, operation, timeout):
        self._lib.AwaServerCreateOperation_Perform.restype = c_int
        self._lib.AwaServerCreateOperation_Perform.argtypes = [c_void_p, c_int]
        return self._lib.AwaServerCreateOperation_Perform(operation, timeout)

    @wrap(trace_in, trace_out)
    def AwaServerCreateOperation_Free(self, operation):
        self._lib.AwaServerCreateOperation_Free.restype = c_int
        mem = cast(operation, POINTER(c_void_p))
        return self._lib.AwaServerCreateOperation_Free(byref(mem))

    @wrap(trace_in, trace_out)
    def AwaServerCreateResponse_NewAttributeIterator(self, response, path):
        self._lib.AwaServerCreateResponse_NewAttributeIterator.restype = c_void_p
        self._lib.AwaServerCreateResponse_NewAttributeIterator.argtypes = [c_void_p, c_char_p]
        return self._lib.AwaServerCreateResponse_NewAttributeIterator(response, path)

    @wrap(trace_in, trace_out)
    def AwaServerCreateOperation_GetResponse(self, operation, clientID):
        self._lib.AwaServerCreateOperation_GetResponse.restype = c_void_p
        self._lib.AwaServerCreateOperation_GetResponse.argtypes = [c_void_p, c_char_p]
        return self._lib.AwaServerCreateOperation_GetResponse(operation, clientID)

    @wrap(trace_in, trace_out)
    def AwaServerCreateResponse_NewPathIterator(self, response):
        self._lib.AwaServerCreateResponse_NewPathIterator.restype = c_void_p
        self._lib.AwaServerCreateResponse_NewPathIterator.argtypes = [c_void_p]
        return self._lib.AwaServerCreateResponse_NewPathIterator(response)

    @wrap(trace_in, trace_out)
    def AwaServerCreateResponse_GetPathResult(self, response, path):
        self._lib.AwaServerCreateResponse_GetPathResult.restype = c_void_p
        self._lib.AwaServerCreateResponse_GetPathResult.argtypes = [c_void_p, c_char_p]
        return self._lib.AwaServerCreateResponse_GetPathResult(response, path)

    @wrap(trace_in, trace_out)
    def AwaServerCreateResponse_ContainsPath(self, response, path):
        self._lib.AwaServerCreateResponse_ContainsPath.restype = c_bool
        self._lib.AwaServerCreateResponse_ContainsPath.argtypes = [c_void_p, c_char_p]
        return self._lib.AwaServerCreateResponse_ContainsPath(response, path)

    @wrap(trace_in, trace_out)
    def AwaChangeSet_GetServerSession(self, changeSet):
        self._lib.AwaChangeSet_GetServerSession.restype = c_void_p
        self._lib.AwaChangeSet_GetServerSession.argtypes = [c_void_p]
        return self._lib.AwaChangeSet_GetServerSession(changeSet)

    @wrap(trace_in, trace_out)
    def AwaChangeSet_GetClientID(self, changeSet):
        self._lib.AwaChangeSet_GetClientID.restype = c_char_p
        self._lib.AwaChangeSet_GetClientID.argtypes = [c_void_p]
        return self._lib.AwaChangeSet_GetClientID(changeSet)

    @wrap(trace_in, trace_out)
    def AwaServerObserveOperation_New(self, session):
        self._lib.AwaServerObserveOperation_New.restype = c_void_p
        self._lib.AwaServerObserveOperation_New.argtypes = [c_void_p]
        return self._lib.AwaServerObserveOperation_New(session)

    @wrap(trace_in, trace_out)
    def AwaServerObservation_New(self, clientID, path, callback, context):
        self._lib.AwaServerObservation_New.restype = c_void_p
        self._lib.AwaServerObservation_New.argtypes = [c_char_p, c_char_p, c_void_p, c_void_p]

        if callback is not None:
            raise Exception("ERROR: callback as argument is not supported")

        p1 = c_char_p("Test_Context")  # FIXME: Replace with "context" argument
        mem = cast(p1, c_void_p)

        return self._lib.AwaServerObservation_New(clientID, path, self.changeCallbackMemory, mem)

    @wrap(trace_in, trace_out)
    def AwaServerObservation_GetPath(self, observation):
        self._lib.AwaServerObservation_GetPath.restype = c_char_p
        self._lib.AwaServerObservation_GetPath.argtypes = [c_void_p]
        return self._lib.AwaServerObservation_GetPath(observation)

    @wrap(trace_in, trace_out)
    def AwaServerObservation_Free(self, observation):
        self._lib.AwaServerObservation_Free.restype = c_int
        mem = cast(observation, POINTER(c_void_p))
        return self._lib.AwaServerObservation_Free(byref(mem))

    @wrap(trace_in, trace_out)
    def AwaServerObserveOperation_AddObservation(self, operation, observation):
        self._lib.AwaServerObserveOperation_AddObservation.restype = c_int
        self._lib.AwaServerObserveOperation_AddObservation.argtypes = [c_void_p, c_void_p]
        return self._lib.AwaServerObserveOperation_AddObservation(operation, observation)

    @wrap(trace_in, trace_out)
    def AwaServerObserveOperation_AddCancelObservation(self, operation, observation):
        self._lib.AwaServerObserveOperation_AddCancelObservation.restype = c_int
        self._lib.AwaServerObserveOperation_AddCancelObservation.argtypes = [c_void_p, c_void_p]
        return self._lib.AwaServerObserveOperation_AddCancelObservation(operation, observation)

    @wrap(trace_in, trace_out)
    def AwaServerObserveOperation_Perform(self, operation, timeout):
        self._lib.AwaServerObserveOperation_Perform.restype = c_int
        self._lib.AwaServerObserveOperation_Perform.argtypes = [c_void_p, c_int]
        return self._lib.AwaServerObserveOperation_Perform(operation, timeout)

    @wrap(trace_in, trace_out)
    def AwaServerObserveOperation_Free(self, operation):
        self._lib.AwaServerObserveOperation_Free.restype = c_int
        mem = cast(operation, POINTER(c_void_p))
        return self._lib.AwaServerObserveOperation_Free(byref(mem))

    @wrap(trace_in, trace_out)
    def AwaServerObserveOperation_NewClientIterator(self, operation):
        self._lib.AwaServerObserveOperation_NewClientIterator.restype = c_void_p
        self._lib.AwaServerObserveOperation_NewClientIterator.argtypes = [c_void_p]
        return self._lib.AwaServerObserveOperation_NewClientIterator(operation)

    @wrap(trace_in, trace_out)
    def AwaServerObserveOperation_GetResponse(self, operation, clientID):
        self._lib.AwaServerObserveOperation_GetResponse.restype = c_void_p
        self._lib.AwaServerObserveOperation_GetResponse.argtypes = [c_void_p, c_char_p]
        return self._lib.AwaServerObserveOperation_GetResponse(operation, clientID)

    @wrap(trace_in, trace_out)
    def AwaServerObserveResponse_NewPathIterator(self, response):
        self._lib.AwaServerObserveResponse_NewPathIterator.restype = c_void_p
        self._lib.AwaServerObserveResponse_NewPathIterator.argtypes = [c_void_p]
        return self._lib.AwaServerObserveResponse_NewPathIterator(response)

    @wrap(trace_in, trace_out)
    def AwaServerObserveResponse_GetPathResult(self, response, path):
        self._lib.AwaServerObserveResponse_GetPathResult.restype = c_void_p
        self._lib.AwaServerObserveResponse_GetPathResult.argtypes = [c_void_p, c_char_p]
        return self._lib.AwaServerObserveResponse_GetPathResult(response, path)

    @wrap(trace_in, trace_out)
    def AwaServerSession_Process(self, session, timeout):
        self._lib.AwaServerSession_Process.restype = c_int
        self._lib.AwaServerSession_Process.argtypes = [c_void_p, c_int]
        return self._lib.AwaServerSession_Process(session, timeout)

    @wrap(trace_in, trace_out)
    def AwaServerSession_DispatchCallbacks(self, session):
        self._lib.AwaServerSession_DispatchCallbacks.restype = c_int
        self._lib.AwaServerSession_DispatchCallbacks.argtypes = [c_void_p]
        return self._lib.AwaServerSession_DispatchCallbacks(session)
