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

from ctypes import POINTER, c_void_p, c_char_p, c_int, cast, byref, CFUNCTYPE, c_ulong, c_longlong, c_double, c_bool, c_ushort
import cPickle as pickle

from awa_common_api_wrapper import AwaCommonAPIWrapper, AwaOpaqueToBase64, AwaOpaque

from framework.awa_enums import SessionType

from framework.wrap import wrap, trace_in, trace_out

class AwaGatewayClientAPIWrapper(AwaCommonAPIWrapper):

    def __init__(self):
        super(AwaGatewayClientAPIWrapper, self).__init__(SessionType.Client)

        # create our ctypes execute callback.
        C_EXECUTE_FUNC = CFUNCTYPE(c_void_p, c_void_p)
        executeCallback = C_EXECUTE_FUNC(self.ExecuteCallback)
        self.executeCallbackMemory = cast(executeCallback, c_void_p)

        self.NotifyResponse = {}

    @wrap(trace_in, trace_out)
    def AwaClientSession_New(self):
        self._lib.AwaClientSession_New.restype = c_void_p
        return self._lib.AwaClientSession_New()

    @wrap(trace_in, trace_out)
    def AwaClientSession_SetIPCAsUDP(self, session, address, port):
        self._lib.AwaClientSession_SetIPCAsUDP.restype = c_int
        self._lib.AwaClientSession_SetIPCAsUDP.argtypes = [c_void_p, c_char_p, c_ushort]
        return self._lib.AwaClientSession_SetIPCAsUDP(session, address, port)

    @wrap(trace_in, trace_out)
    def AwaClientSession_Connect(self, session):
        self._lib.AwaClientSession_Connect.restype = c_int
        self._lib.AwaClientSession_Connect.argtypes = [c_void_p]
        return self._lib.AwaClientSession_Connect(session)

    @wrap(trace_in, trace_out)
    def AwaClientAPI_RefreshSession(self, session):
        self._lib.AwaClientSession_Refresh.restype = c_int
        self._lib.AwaClientSession_Refresh.argtypes = [c_void_p]
        return self._lib.AwaClientSession_Refresh(session)

    @wrap(trace_in, trace_out)
    def AwaClientSession_IsObjectDefined(self, session, objectID):
        self._lib.AwaClientSession_IsObjectDefined.restype = c_bool
        self._lib.AwaClientSession_IsObjectDefined.argtypes = [c_void_p, c_int]
        return self._lib.AwaClientSession_IsObjectDefined(session, objectID)

    @wrap(trace_in, trace_out)
    def AwaClientSession_GetObjectDefinition(self, session, objectID):
        self._lib.AwaClientSession_GetObjectDefinition.restype = c_void_p
        self._lib.AwaClientSession_GetObjectDefinition.argtypes = [c_void_p, c_int]
        return self._lib.AwaClientSession_GetObjectDefinition(session, objectID)

    @wrap(trace_in, trace_out)
    def AwaClientSession_NewObjectDefinitionIterator(self, session):
        self._lib.AwaClientSession_NewObjectDefinitionIterator.restype = c_void_p
        self._lib.AwaClientSession_NewObjectDefinitionIterator.argtypes = [c_void_p]
        return self._lib.AwaClientSession_NewObjectDefinitionIterator(session)

    @wrap(trace_in, trace_out)
    def AwaClientSession_Disconnect(self, session):
        self._lib.AwaClientSession_Disconnect.restype = c_int
        self._lib.AwaClientSession_Disconnect.argtypes = [c_void_p]
        return self._lib.AwaClientSession_Disconnect(session)

    @wrap(trace_in, trace_out)
    def AwaClientSession_Free(self, session):
        self._lib.AwaClientSession_Free.restype = c_int
        mem = cast(session, POINTER(c_void_p))
        return self._lib.AwaClientSession_Free(byref(mem))

    @wrap(trace_in, trace_out)
    def AwaClientSession_PathToIDs(self, session, path, objectID, objectInstanceID, resourceID):
        self._lib.AwaClientSession_PathToIDs.restype = c_int
        mem = cast(objectID, POINTER(c_int))
        mem2 = cast(objectInstanceID, POINTER(c_int))
        mem3 = cast(resourceID, POINTER(c_int))

        ret = self._lib.AwaClientSession_PathToIDs(session, path, mem, mem2, mem3)
        result = {}
        if ret != 0:
            result[ret] = None
        else:
            result[ret] = cast(mem, POINTER(c_int)).contents.value
            result[ret] = cast(mem2, POINTER(c_int)).contents.value
            result[ret] = cast(mem3, POINTER(c_int)).contents.value

        return dict((str(key), value) for key, value in result.items())

    @wrap(trace_in, trace_out)
    def AwaClientDefineOperation_New(self, session):
        self._lib.AwaClientDefineOperation_New.restype = c_void_p
        self._lib.AwaClientDefineOperation_New.argtypes = [c_void_p]
        return self._lib.AwaClientDefineOperation_New(session)

    @wrap(trace_in, trace_out)
    def AwaClientDefineOperation_Add(self, operation, objectDefinition):
        self._lib.AwaClientDefineOperation_Add.restype = c_int
        self._lib.AwaClientDefineOperation_Add.argtypes = [c_void_p, c_void_p]
        return self._lib.AwaClientDefineOperation_Add(operation, objectDefinition)

    @wrap(trace_in, trace_out)
    def AwaClientDefineOperation_Perform(self, operation, timeout):
        self._lib.AwaClientDefineOperation_Perform.restype = c_int
        self._lib.AwaClientDefineOperation_Perform.argtypes = [c_void_p, c_int]
        return self._lib.AwaClientDefineOperation_Perform(operation, timeout)

    @wrap(trace_in, trace_out)
    def AwaClientDefineOperation_Free(self, operation):
        self._lib.AwaClientDefineOperation_Free.restype = c_int
        mem = cast(operation, POINTER(c_void_p))
        return self._lib.AwaClientDefineOperation_Free(byref(mem))

    @wrap(trace_in, trace_out)
    def AwaClientGetOperation_New(self, session):
        self._lib.AwaClientGetOperation_New.restype = c_void_p
        self._lib.AwaClientGetOperation_New.argtypes = [c_void_p]
        return self._lib.AwaClientGetOperation_New(session)

    @wrap(trace_in, trace_out)
    def AwaClientGetOperation_AddPath(self, operation, path):
        self._lib.AwaClientGetOperation_AddPath.restype = c_int
        self._lib.AwaClientGetOperation_AddPath.argtypes = [c_void_p, c_char_p]
        return self._lib.AwaClientGetOperation_AddPath(operation, path)

    @wrap(trace_in, trace_out)
    def AwaClientGetOperation_AddPathWithArrayRange(self, operation, path, startIndex, indexCount):
        self._lib.AwaClientGetOperation_AddPathWithArrayRange.restype = c_int
        self._lib.AwaClientGetOperation_AddPathWithArrayRange.argtypes = [c_void_p, c_char_p, c_ulong, c_ulong]
        return self._lib.AwaClientGetOperation_AddPathWithArrayRange(operation, path, startIndex, indexCount)

    @wrap(trace_in, trace_out)
    def AwaClientGetOperation_Perform(self, operation, timeout):
        self._lib.AwaClientGetOperation_Perform.restype = c_int
        self._lib.AwaClientGetOperation_Perform.argtypes = [c_void_p, c_int]
        return self._lib.AwaClientGetOperation_Perform(operation, timeout)

    @wrap(trace_in, trace_out)
    def AwaClientGetOperation_Free(self, operation):
        self._lib.AwaClientGetOperation_Free.restype = c_int
        mem = cast(operation, POINTER(c_void_p))
        return self._lib.AwaClientGetOperation_Free(byref(mem))

    @wrap(trace_in, trace_out)
    def AwaClientGetOperation_GetResponse(self, operation):
        self._lib.AwaClientGetOperation_GetResponse.restype = c_void_p
        self._lib.AwaClientGetOperation_GetResponse.argtypes = [c_void_p]
        return self._lib.AwaClientGetOperation_GetResponse(operation)

    @wrap(trace_in, trace_out)
    def AwaClientGetResponse_GetPathResult(self, response, path):
        self._lib.AwaClientGetResponse_GetPathResult.restype = c_void_p
        self._lib.AwaClientGetResponse_GetPathResult.argtypes = [c_void_p, c_char_p]
        return self._lib.AwaClientGetResponse_GetPathResult(response, path)

    @wrap(trace_in, trace_out)
    def AwaClientGetResponse_NewPathIterator(self, response):
        self._lib.AwaClientGetResponse_NewPathIterator.restype = c_void_p
        self._lib.AwaClientGetResponse_NewPathIterator.argtypes = [c_void_p]
        return self._lib.AwaClientGetResponse_NewPathIterator(response)

    @wrap(trace_in, trace_out)
    def AwaClientGetResponse_ContainsPath(self, response, path):
        self._lib.AwaClientGetResponse_ContainsPath.restype = c_bool
        self._lib.AwaClientGetResponse_ContainsPath.argtypes = [c_void_p, c_char_p]
        return self._lib.AwaClientGetResponse_ContainsPath(response, path)

    @wrap(trace_in, trace_out)
    def AwaClientGetResponse_HasValue(self, response, path):
        self._lib.AwaClientGetResponse_HasValue.restype = c_bool
        self._lib.AwaClientGetResponse_HasValue.argtypes = [c_void_p, c_char_p]
        return self._lib.AwaClientGetResponse_HasValue(response, path)

    @wrap(trace_in, trace_out)
    def AwaClientGetResponse_GetValueAsCStringPointer(self, response, path, value):
        self._lib.AwaClientGetResponse_GetValueAsCStringPointer.restype = c_int
        mem = cast(value, POINTER(c_char_p))
        ret = self._lib.AwaClientGetResponse_GetValueAsCStringPointer(response, path, byref(mem))

        result = None
        if ret == 0:
            result = cast(mem, c_char_p).value

        return result, ret

    @wrap(trace_in, trace_out)
    def AwaClientGetResponse_GetValueAsIntegerPointer(self, response, path, value):
        self._lib.AwaClientGetResponse_GetValueAsIntegerPointer.restype = c_int
        mem = cast(value, POINTER(POINTER(c_longlong)))
        ret = self._lib.AwaClientGetResponse_GetValueAsIntegerPointer(response, path, byref(mem))
        result = None
        if ret == 0:
            result = pickle.dumps(cast(mem, POINTER(c_longlong)).contents.value)  # serialise as XML-RPC only supports 32 bit integers
        return result, ret

    @wrap(trace_in, trace_out)
    def AwaClientGetResponse_GetValueAsFloatPointer(self, response, path, value):
        self._lib.AwaClientGetResponse_GetValueAsFloatPointer.restype = c_int
        mem = cast(value, POINTER(c_double))
        ret = self._lib.AwaClientGetResponse_GetValueAsFloatPointer(response, path, byref(mem))
        result = None
        if ret == 0:
            result = cast(mem, POINTER(c_double)).contents.value

        return result, ret

    @wrap(trace_in, trace_out)
    def AwaClientGetResponse_GetValueAsBooleanPointer(self, response, path, value):
        self._lib.AwaClientGetResponse_GetValueAsBooleanPointer.restype = c_int
        mem = cast(value, POINTER(c_bool))
        ret = self._lib.AwaClientGetResponse_GetValueAsBooleanPointer(response, path, byref(mem))
        result = None
        if ret == 0:
            result = cast(mem, POINTER(c_bool)).contents.value

        return result, ret

    @wrap(trace_in, trace_out)
    def AwaClientGetResponse_GetValueAsTimePointer(self, response, path, value):
        self._lib.AwaClientGetResponse_GetValueAsTimePointer.restype = c_int
        mem = cast(value, POINTER(POINTER(c_longlong)))
        ret = self._lib.AwaClientGetResponse_GetValueAsTimePointer(response, path, byref(mem))
        result = None
        if ret == 0:
            result = pickle.dumps(cast(mem, POINTER(c_longlong)).contents.value)  # serialise as XML-RPC only supports 32 bit integers
        return result, ret

    @wrap(trace_in, trace_out)
    def AwaClientGetResponse_GetValueAsOpaque(self, response, path, value):
        self._lib.AwaClientGetResponse_GetValueAsOpaque.restype = c_int
        self._lib.AwaClientGetResponse_GetValueAsOpaque.argtypes = [c_void_p, c_char_p, POINTER(AwaOpaque)]
        value = c_void_p()
        opaqueValue = AwaOpaque(value, 0)
        ret = self._lib.AwaClientGetResponse_GetValueAsOpaque(response, path, byref(opaqueValue))
        result = None
        if ret == 0:
            result = AwaOpaqueToBase64(opaqueValue)


        return result, ret

    @wrap(trace_in, trace_out)
    def AwaClientGetResponse_GetValueAsObjectLink(self, response, path, value):
        self._lib.AwaClientGetResponse_GetValueAsObjectLink.restype = c_int
        self._lib.AwaClientGetResponse_GetValueAsObjectLink.argtypes = [c_void_p, c_char_p, c_void_p]
        return self._lib.AwaClientGetResponse_GetValueAsObjectLink(response, path, value)

    @wrap(trace_in, trace_out)
    def AwaClientGetResponse_GetValuesAsStringArrayPointer(self, response, path, valueArray):
        self._lib.AwaClientGetResponse_GetValuesAsStringArrayPointer.restype = c_int
        mem = cast(valueArray, POINTER(c_void_p))
        ret = self._lib.AwaClientGetResponse_GetValuesAsStringArrayPointer(response, path, byref(mem))
        result = {}
        iterator = self._lib.AwaStringArray_NewCStringArrayIterator(mem)
        if iterator != None:
            while self._lib.AwaCStringArrayIterator_Next(iterator):
                index = self._lib.AwaCStringArrayIterator_GetIndex(iterator)
                value = cast(self._lib.AwaCStringArrayIterator_GetValueAsCString(iterator), c_char_p).value
                result[index] = value
            self._lib.AwaIntegerArrayIterator_Free(byref(cast(iterator, POINTER(c_void_p))))

        return pickle.dumps(result)

    @wrap(trace_in, trace_out)
    def AwaClientGetResponse_GetValuesAsIntegerArrayPointer(self, response, path, valueArray):
        self._lib.AwaClientGetResponse_GetValuesAsIntegerArrayPointer.restype = c_int
        mem = cast(valueArray, POINTER(c_void_p))
        ret = self._lib.AwaClientGetResponse_GetValuesAsIntegerArrayPointer(response, path, byref(mem))
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
    def AwaClientGetResponse_GetValuesAsFloatArrayPointer(self, response, path, valueArray):
        self._lib.AwaClientGetResponse_GetValuesAsFloatArrayPointer.restype = c_int
        mem = cast(valueArray, POINTER(c_void_p))
        ret = self._lib.AwaClientGetResponse_GetValuesAsFloatArrayPointer(response, path, byref(mem))
        result = {}
        iterator = self._lib.AwaFloatArray_NewFloatArrayIterator(mem)
        if iterator != None:
            while self._lib.AwaFloatArrayIterator_Next(iterator):
                index = self._lib.AwaFloatArrayIterator_GetIndex(iterator)
                value = self._lib.AwaFloatArrayIterator_GetValue(iterator)
                result[index] = value
            self._lib.AwaIntegerArrayIterator_Free(byref(cast(iterator, POINTER(c_void_p))))

        return pickle.dumps(result)

    @wrap(trace_in, trace_out)
    def AwaClientGetResponse_GetValuesAsBooleanArrayPointer(self, response, path, valueArray):
        self._lib.AwaClientGetResponse_GetValuesAsBooleanArrayPointer.restype = c_int
        mem = cast(valueArray, POINTER(c_void_p))
        ret = self._lib.AwaClientGetResponse_GetValuesAsBooleanArrayPointer(response, path, byref(mem))
        result = {}
        iterator = self._lib.AwaBooleanArray_NewBooleanArrayIterator(mem)
        if iterator != None:
            while self._lib.AwaBooleanArrayIterator_Next(iterator):
                index = self._lib.AwaBooleanArrayIterator_GetIndex(iterator)
                value = self._lib.AwaBooleanArrayIterator_GetValue(iterator)
                result[index] = value
            self._lib.AwaIntegerArrayIterator_Free(byref(cast(iterator, POINTER(c_void_p))))

        return pickle.dumps(result)

    @wrap(trace_in, trace_out)
    def AwaClientGetResponse_GetValuesAsTimeArrayPointer(self, response, path, valueArray):
        self._lib.AwaClientGetResponse_GetValuesAsTimeArrayPointer.restype = c_int
        mem = cast(valueArray, POINTER(c_void_p))
        ret = self._lib.AwaClientGetResponse_GetValuesAsTimeArrayPointer(response, path, byref(mem))
        result = {}
        iterator = self._lib.AwaTimeArray_NewTimeArrayIterator(mem)
        if iterator != None:
            while self._lib.AwaTimeArrayIterator_Next(iterator):
                index = self._lib.AwaTimeArrayIterator_GetIndex(iterator)
                value = self._lib.AwaTimeArrayIterator_GetValue(iterator)
                result[index] = value
            self._lib.AwaIntegerArrayIterator_Free(byref(cast(iterator, POINTER(c_void_p))))

        return pickle.dumps(result)

    @wrap(trace_in, trace_out)
    def AwaClientGetResponse_GetValuesAsOpaqueArrayPointer(self, response, path, valueArray):
        self._lib.AwaClientGetResponse_GetValuesAsOpaqueArrayPointer.restype = c_int
        mem = cast(valueArray, POINTER(c_void_p))
        ret = self._lib.AwaClientGetResponse_GetValuesAsOpaqueArrayPointer(response, path, byref(mem))
        result = {}
        iterator = self._lib.AwaOpaqueArray_NewOpaqueArrayIterator(mem)
        if iterator != None:
            while self._lib.AwaOpaqueArrayIterator_Next(iterator):
                index = self._lib.AwaOpaqueArrayIterator_GetIndex(iterator)
                value = self._lib.AwaOpaqueArrayIterator_GetValue(iterator)
                result[index] = value
            self._lib.AwaIntegerArrayIterator_Free(byref(cast(iterator, POINTER(c_void_p))))

        return pickle.dumps(result)

    @wrap(trace_in, trace_out)
    def AwaClientGetResponse_GetValuesAsObjectLinkArrayPointer(self, response, path, valueArray):
        self._lib.AwaClientGetResponse_GetValuesAsObjectLinkArrayPointer.restype = c_int
        mem = cast(valueArray, POINTER(c_void_p))
        ret = self._lib.AwaClientGetResponse_GetValuesAsObjectLinkArrayPointer(response, path, byref(mem))
        result = {}
        iterator = self._lib.AwaObjectLinkArray_NewObjectLinkArrayIterator(mem)
        if iterator != None:
            while self._lib.AwaObjectLinkArrayIterator_Next(iterator):
                index = self._lib.AwaObjectLinkArrayIterator_GetIndex(iterator)
                value = self._lib.AwaObjectLinkArrayIterator_GetValue(iterator)
                result[index] = value
            self._lib.AwaIntegerArrayIterator_Free(byref(cast(iterator, POINTER(c_void_p))))

        return pickle.dumps(result)

    @wrap(trace_in, trace_out)
    def AwaClientSetOperation_New(self, session):
        self._lib.AwaClientSetOperation_New.restype = c_void_p
        self._lib.AwaClientSetOperation_New.argtypes = [c_void_p]
        return self._lib.AwaClientSetOperation_New(session)

    @wrap(trace_in, trace_out)
    def AwaClientSetOperation_CreateObjectInstance(self, operation, path):
        self._lib.AwaClientSetOperation_CreateObjectInstance.restype = c_int
        self._lib.AwaClientSetOperation_CreateObjectInstance.argtypes = [c_void_p, c_char_p]
        return self._lib.AwaClientSetOperation_CreateObjectInstance(operation, path)

    @wrap(trace_in, trace_out)
    def AwaClientSetOperation_CreateOptionalResource(self, operation, path):
        self._lib.AwaClientSetOperation_CreateOptionalResource.restype = c_int
        self._lib.AwaClientSetOperation_CreateOptionalResource.argtypes = [c_void_p, c_char_p]
        return self._lib.AwaClientSetOperation_CreateOptionalResource(operation, path)

    @wrap(trace_in, trace_out)
    def AwaClientSetOperation_GetResponse(self, operation):
        self._lib.AwaClientSetOperation_GetResponse.restype = c_void_p
        self._lib.AwaClientSetOperation_GetResponse.argtypes = [c_void_p]
        return self._lib.AwaClientSetOperation_GetResponse(operation)

    @wrap(trace_in, trace_out)
    def AwaClientSetResponse_NewPathIterator(self, response):
        self._lib.AwaClientSetResponse_NewPathIterator.restype = c_void_p
        self._lib.AwaClientSetResponse_NewPathIterator.argtypes = [c_void_p]
        return self._lib.AwaClientSetResponse_NewPathIterator(response)

    @wrap(trace_in, trace_out)
    def AwaClientSetResponse_GetPathResult(self, response, path):
        self._lib.AwaClientSetResponse_GetPathResult.restype = c_void_p
        self._lib.AwaClientSetResponse_GetPathResult.argtypes = [c_void_p, c_char_p]
        return self._lib.AwaClientSetResponse_GetPathResult(response, path)

    @wrap(trace_in, trace_out)
    def AwaClientSetOperation_AddValueAsCString(self, operation, path, value):
        self._lib.AwaClientSetOperation_AddValueAsCString.restype = c_int
        self._lib.AwaClientSetOperation_AddValueAsCString.argtypes = [c_void_p, c_char_p, c_char_p]
        return self._lib.AwaClientSetOperation_AddValueAsCString(operation, path, value)

    @wrap(trace_in, trace_out)
    def AwaClientSetOperation_AddValueAsInteger(self, operation, path, value):
        self._lib.AwaClientSetOperation_AddValueAsInteger.restype = c_int
        self._lib.AwaClientSetOperation_AddValueAsInteger.argtypes = [c_void_p, c_char_p, c_longlong]
        return self._lib.AwaClientSetOperation_AddValueAsInteger(operation, path, value)

    @wrap(trace_in, trace_out)
    def AwaClientSetOperation_AddValueAsFloat(self, operation, path, value):
        self._lib.AwaClientSetOperation_AddValueAsFloat.restype = c_int
        self._lib.AwaClientSetOperation_AddValueAsFloat.argtypes = [c_void_p, c_char_p, c_double]
        return self._lib.AwaClientSetOperation_AddValueAsFloat(operation, path, value)

    @wrap(trace_in, trace_out)
    def AwaClientSetOperation_AddValueAsBoolean(self, operation, path, value):
        self._lib.AwaClientSetOperation_AddValueAsBoolean.restype = c_int
        self._lib.AwaClientSetOperation_AddValueAsBoolean.argtypes = [c_void_p, c_char_p, c_bool]
        return self._lib.AwaClientSetOperation_AddValueAsBoolean(operation, path, value)

    @wrap(trace_in, trace_out)
    def AwaClientSetOperation_AddValueAsTime(self, operation, path, value):
        self._lib.AwaClientSetOperation_AddValueAsTime.restype = c_int
        self._lib.AwaClientSetOperation_AddValueAsTime.argtypes = [c_void_p, c_char_p, c_longlong]
        return self._lib.AwaClientSetOperation_AddValueAsTime(operation, path, value)

    @wrap(trace_in, trace_out)
    def AwaClientSetOperation_AddValueAsOpaque(self, operation, path, value):
        self._lib.AwaClientSetOperation_AddValueAsOpaque.restype = c_int
        self._lib.AwaClientSetOperation_AddValueAsOpaque.argtypes = [c_void_p, c_char_p, AwaOpaque]
        opaqueValue = None
        if isinstance(value, str):
            mem = cast(value, c_void_p)
            opaqueValue = AwaOpaque(mem, len(value))
        elif isinstance(value, dict):
            opaqueValue = AwaOpaque(cast(str(value['Data']), c_void_p), value['Size'])

        return self._lib.AwaClientSetOperation_AddValueAsOpaque(operation, path, opaqueValue)

    @wrap(trace_in, trace_out)
    def AwaClientSetOperation_AddValueAsObjectLink(self, operation, path, value):
        self._lib.AwaClientSetOperation_AddValueAsObjectLink.restype = c_int
        self._lib.AwaClientSetOperation_AddValueAsObjectLink.argtypes = [c_void_p, c_char_p, c_void_p]
        return self._lib.AwaClientSetOperation_AddValueAsObjectLink(operation, path, value)

    @wrap(trace_in, trace_out)
    def AwaClientSetOperation_AddValueAsStringArray(self, operation, path, array):
        self._lib.AwaClientSetOperation_AddValueAsStringArray.restype = c_int
        self._lib.AwaClientSetOperation_AddValueAsStringArray.argtypes = [c_void_p, c_char_p, c_void_p]
        return self._lib.AwaClientSetOperation_AddValueAsStringArray(operation, path, array)

    @wrap(trace_in, trace_out)
    def AwaClientSetOperation_AddValueAsIntegerArray(self, operation, path, array):
        self._lib.AwaClientSetOperation_AddValueAsIntegerArray.restype = c_int
        self._lib.AwaClientSetOperation_AddValueAsIntegerArray.argtypes = [c_void_p, c_char_p, c_void_p]
        return self._lib.AwaClientSetOperation_AddValueAsIntegerArray(operation, path, array)

    @wrap(trace_in, trace_out)
    def AwaClientSetOperation_AddValueAsFloatArray(self, operation, path, array):
        self._lib.AwaClientSetOperation_AddValueAsFloatArray.restype = c_int
        self._lib.AwaClientSetOperation_AddValueAsFloatArray.argtypes = [c_void_p, c_char_p, c_void_p]
        return self._lib.AwaClientSetOperation_AddValueAsFloatArray(operation, path, array)

    @wrap(trace_in, trace_out)
    def AwaClientSetOperation_AddValueAsBooleanArray(self, operation, path, array):
        self._lib.AwaClientSetOperation_AddValueAsBooleanArray.restype = c_int
        self._lib.AwaClientSetOperation_AddValueAsBooleanArray.argtypes = [c_void_p, c_char_p, c_void_p]
        return self._lib.AwaClientSetOperation_AddValueAsBooleanArray(operation, path, array)

    @wrap(trace_in, trace_out)
    def AwaClientSetOperation_AddValueAsTimeArray(self, operation, path, array):
        self._lib.AwaClientSetOperation_AddValueAsTimeArray.restype = c_int
        self._lib.AwaClientSetOperation_AddValueAsTimeArray.argtypes = [c_void_p, c_char_p, c_void_p]
        return self._lib.AwaClientSetOperation_AddValueAsTimeArray(operation, path, array)

    @wrap(trace_in, trace_out)
    def AwaClientSetOperation_AddValueAsOpaqueArray(self, operation, path, array):
        self._lib.AwaClientSetOperation_AddValueAsOpaqueArray.restype = c_int
        self._lib.AwaClientSetOperation_AddValueAsOpaqueArray.argtypes = [c_void_p, c_char_p, c_void_p]
        return self._lib.AwaClientSetOperation_AddValueAsOpaqueArray(operation, path, array)

    @wrap(trace_in, trace_out)
    def AwaClientSetOperation_AddValueAsObjectLinkArray(self, operation, path, array):
        self._lib.AwaClientSetOperation_AddValueAsObjectLinkArray.restype = c_int
        self._lib.AwaClientSetOperation_AddValueAsObjectLinkArray.argtypes = [c_void_p, c_char_p, c_void_p]
        return self._lib.AwaClientSetOperation_AddValueAsObjectLinkArray(operation, path, array)

    @wrap(trace_in, trace_out)
    def AwaClientSetOperation_AddArrayValueAsCString(self, operation, path, resourceInstanceID, value):
        self._lib.AwaClientSetOperation_AddArrayValueAsCString.restype = c_int
        self._lib.AwaClientSetOperation_AddArrayValueAsCString.argtypes = [c_void_p, c_char_p, c_int, c_char_p]
        return self._lib.AwaClientSetOperation_AddArrayValueAsCString(operation, path, resourceInstanceID, value)

    @wrap(trace_in, trace_out)
    def AwaClientSetOperation_AddArrayValueAsInteger(self, operation, path, resourceInstanceID, value):
        self._lib.AwaClientSetOperation_AddArrayValueAsInteger.restype = c_int
        self._lib.AwaClientSetOperation_AddArrayValueAsInteger.argtypes = [c_void_p, c_char_p, c_int, c_longlong]
        return self._lib.AwaClientSetOperation_AddArrayValueAsInteger(operation, path, resourceInstanceID, value)

    @wrap(trace_in, trace_out)
    def AwaClientSetOperation_AddArrayValueAsFloat(self, operation, path, resourceInstanceID, value):
        self._lib.AwaClientSetOperation_AddArrayValueAsFloat.restype = c_int
        self._lib.AwaClientSetOperation_AddArrayValueAsFloat.argtypes = [c_void_p, c_char_p, c_int, c_double]
        return self._lib.AwaClientSetOperation_AddArrayValueAsFloat(operation, path, resourceInstanceID, value)

    @wrap(trace_in, trace_out)
    def AwaClientSetOperation_AddArrayValueAsBoolean(self, operation, path, resourceInstanceID, value):
        self._lib.AwaClientSetOperation_AddArrayValueAsBoolean.restype = c_int
        self._lib.AwaClientSetOperation_AddArrayValueAsBoolean.argtypes = [c_void_p, c_char_p, c_int, c_bool]
        return self._lib.AwaClientSetOperation_AddArrayValueAsBoolean(operation, path, resourceInstanceID, value)

    @wrap(trace_in, trace_out)
    def AwaClientSetOperation_AddArrayValueAsTime(self, operation, path, resourceInstanceID, value):
        self._lib.AwaClientSetOperation_AddArrayValueAsTime.restype = c_int
        self._lib.AwaClientSetOperation_AddArrayValueAsTime.argtypes = [c_void_p, c_char_p, c_int, c_longlong]
        return self._lib.AwaClientSetOperation_AddArrayValueAsTime(operation, path, resourceInstanceID, value)

    @wrap(trace_in, trace_out)
    def AwaClientSetOperation_AddArrayValueAsOpaque(self, operation, path, resourceInstanceID, value):
        self._lib.AwaClientSetOperation_AddArrayValueAsOpaque.restype = c_int
        self._lib.AwaClientSetOperation_AddArrayValueAsOpaque.argtypes = [c_void_p, c_char_p, c_int, c_void_p]
        return self._lib.AwaClientSetOperation_AddArrayValueAsOpaque(operation, path, resourceInstanceID, value)

    @wrap(trace_in, trace_out)
    def AwaClientSetOperation_AddArrayValueAsObjectLink(self, operation, path, resourceInstanceID, value):
        self._lib.AwaClientSetOperation_AddArrayValueAsObjectLink.restype = c_int
        self._lib.AwaClientSetOperation_AddArrayValueAsObjectLink.argtypes = [c_void_p, c_char_p, c_int, c_void_p]
        return self._lib.AwaClientSetOperation_AddArrayValueAsObjectLink(operation, path, resourceInstanceID, value)

    @wrap(trace_in, trace_out)
    def AwaClientSetOperation_Perform(self, operation, timeout):
        self._lib.AwaClientSetOperation_Perform.restype = c_int
        self._lib.AwaClientSetOperation_Perform.argtypes = [c_void_p, c_int]
        return self._lib.AwaClientSetOperation_Perform(operation, timeout)

    @wrap(trace_in, trace_out)
    def AwaClientSetOperation_Free(self, operation):
        self._lib.AwaClientSetOperation_Free.restype = c_int
        mem = cast(operation, POINTER(c_void_p))
        return self._lib.AwaClientSetOperation_Free(byref(mem))

    @wrap(trace_in, trace_out)
    def AwaClientDeleteOperation_New(self, session):
        self._lib.AwaClientDeleteOperation_New.restype = c_void_p
        self._lib.AwaClientDeleteOperation_New.argtypes = [c_void_p]
        return self._lib.AwaClientDeleteOperation_New(session)

    @wrap(trace_in, trace_out)
    def AwaClientDeleteOperation_AddPath(self, operation, path):
        self._lib.AwaClientDeleteOperation_AddPath.restype = c_int
        self._lib.AwaClientDeleteOperation_AddPath.argtypes = [c_void_p, c_char_p]
        return self._lib.AwaClientDeleteOperation_AddPath(operation, path)

    @wrap(trace_in, trace_out)
    def AwaClientDeleteOperation_AddPathWithArrayRange(self, operation, path, startIndex, indexCount):
        self._lib.AwaClientDeleteOperation_AddPathWithArrayRange.restype = c_int
        self._lib.AwaClientDeleteOperation_AddPathWithArrayRange.argtypes = [c_void_p, c_char_p, c_ulong, c_ulong]
        return self._lib.AwaClientDeleteOperation_AddPathWithArrayRange(operation, path, startIndex, indexCount)

    @wrap(trace_in, trace_out)
    def AwaClientDeleteOperation_Perform(self, operation, timeout):
        self._lib.AwaClientDeleteOperation_Perform.restype = c_int
        self._lib.AwaClientDeleteOperation_Perform.argtypes = [c_void_p, c_int]
        return self._lib.AwaClientDeleteOperation_Perform(operation, timeout)

    @wrap(trace_in, trace_out)
    def AwaClientDeleteOperation_Free(self, operation):
        self._lib.AwaClientDeleteOperation_Free.restype = c_int
        mem = cast(operation, POINTER(c_void_p))
        return self._lib.AwaClientDeleteOperation_Free(byref(mem))

    @wrap(trace_in, trace_out)
    def AwaClientDeleteOperation_GetResponse(self, operation):
        self._lib.AwaClientDeleteOperation_GetResponse.restype = c_void_p
        self._lib.AwaClientDeleteOperation_GetResponse.argtypes = [c_void_p]
        return self._lib.AwaClientDeleteOperation_GetResponse(operation)

    @wrap(trace_in, trace_out)
    def AwaClientDeleteResponse_NewPathIterator(self, response):
        self._lib.AwaClientDeleteResponse_NewPathIterator.restype = c_void_p
        self._lib.AwaClientDeleteResponse_NewPathIterator.argtypes = [c_void_p]
        return self._lib.AwaClientDeleteResponse_NewPathIterator(response)

    @wrap(trace_in, trace_out)
    def AwaClientDeleteResponse_GetPathResult(self, response, path):
        self._lib.AwaClientDeleteResponse_GetPathResult.restype = c_void_p
        self._lib.AwaClientDeleteResponse_GetPathResult.argtypes = [c_void_p, c_char_p]
        return self._lib.AwaClientDeleteResponse_GetPathResult(response, path)

    @wrap(trace_in, trace_out)
    def AwaClientSubscribeOperation_New(self, session):
        self._lib.AwaClientSubscribeOperation_New.restype = c_void_p
        self._lib.AwaClientSubscribeOperation_New.argtypes = [c_void_p]
        return self._lib.AwaClientSubscribeOperation_New(session)

    @wrap(trace_in, trace_out)
    def AwaClientSubscribeOperation_Free(self, operation):
        self._lib.AwaClientSubscribeOperation_Free.restype = c_int
        mem = cast(operation, POINTER(c_void_p))
        return self._lib.AwaClientSubscribeOperation_Free(byref(mem))

    @wrap(trace_in, trace_out)
    def AwaClientSubscribeOperation_AddChangeSubscription(self, operation, subscription):
        self._lib.AwaClientSubscribeOperation_AddChangeSubscription.restype = c_int
        self._lib.AwaClientSubscribeOperation_AddChangeSubscription.argtypes = [c_void_p, c_void_p]
        return self._lib.AwaClientSubscribeOperation_AddChangeSubscription(operation, subscription)

    @wrap(trace_in, trace_out)
    def AwaClientSubscribeOperation_AddExecuteSubscription(self, operation, subscription):
        self._lib.AwaClientSubscribeOperation_AddExecuteSubscription.restype = c_int
        self._lib.AwaClientSubscribeOperation_AddExecuteSubscription.argtypes = [c_void_p, c_void_p]
        return self._lib.AwaClientSubscribeOperation_AddExecuteSubscription(operation, subscription)

    @wrap(trace_in, trace_out)
    def AwaClientSubscribeOperation_AddCancelChangeSubscription(self, operation, subscription):
        self._lib.AwaClientSubscribeOperation_AddCancelChangeSubscription.restype = c_int
        self._lib.AwaClientSubscribeOperation_AddCancelChangeSubscription.argtypes = [c_void_p, c_void_p]
        return self._lib.AwaClientSubscribeOperation_AddCancelChangeSubscription(operation, subscription)

    @wrap(trace_in, trace_out)
    def AwaClientSubscribeOperation_AddCancelExecuteSubscription(self, operation, subscription):
        self._lib.AwaClientSubscribeOperation_AddCancelExecuteSubscription.restype = c_int
        self._lib.AwaClientSubscribeOperation_AddCancelExecuteSubscription.argtypes = [c_void_p, c_void_p]
        return self._lib.AwaClientSubscribeOperation_AddCancelExecuteSubscription(operation, subscription)

    @wrap(trace_in, trace_out)
    def AwaClientSubscribeOperation_Perform(self, operation, timeout):
        self._lib.AwaClientSubscribeOperation_Perform.restype = c_int
        self._lib.AwaClientSubscribeOperation_Perform.argtypes = [c_void_p, c_int]
        return self._lib.AwaClientSubscribeOperation_Perform(operation, timeout)

    @wrap(trace_in, trace_out)
    def AwaClientSubscribeOperation_GetResponse(self, operation):
        self._lib.AwaClientSubscribeOperation_GetResponse.restype = c_void_p
        self._lib.AwaClientSubscribeOperation_GetResponse.argtypes = [c_void_p]
        return self._lib.AwaClientSubscribeOperation_GetResponse(operation)

    @wrap(trace_in, trace_out)
    def AwaClientSubscribeResponse_NewPathIterator(self, response):
        self._lib.AwaClientSubscribeResponse_NewPathIterator.restype = c_void_p
        self._lib.AwaClientSubscribeResponse_NewPathIterator.argtypes = [c_void_p]
        return self._lib.AwaClientSubscribeResponse_NewPathIterator(response)

    @wrap(trace_in, trace_out)
    def AwaClientSubscribeResponse_GetPathResult(self, response, path):
        self._lib.AwaClientSubscribeResponse_GetPathResult.restype = c_void_p
        self._lib.AwaClientSubscribeResponse_GetPathResult.argtypes = [c_void_p, c_char_p]
        return self._lib.AwaClientSubscribeResponse_GetPathResult(response, path)

    @wrap(trace_in, trace_out)
    def AwaClientChangeSubscription_New(self, path, callback, context):
        self._lib.AwaClientChangeSubscription_New.restype = c_void_p
        self._lib.AwaClientChangeSubscription_New.argtypes = [c_char_p, c_void_p, c_void_p]

        if callback is not None:
            raise Exception("ERROR: callback as argument is not supported")

        p1 = c_char_p("TestContext")  # FIXME: Replace with "context" argument
        mem = cast(p1, c_void_p)

        return self._lib.AwaClientChangeSubscription_New(path, self.changeCallbackMemory, mem)

    @wrap(trace_in, trace_out)
    def AwaClientChangeSubscription_Free(self, subscription):
        self._lib.AwaClientChangeSubscription_Free.restype = c_int
        mem = cast(subscription, POINTER(c_void_p))
        return self._lib.AwaClientChangeSubscription_Free(byref(mem))

    @wrap(trace_in, trace_out)
    def AwaClientChangeSubscription_GetPath(self, subscription):
        self._lib.AwaClientChangeSubscription_GetPath.restype = c_char_p
        self._lib.AwaClientChangeSubscription_GetPath.argtypes = [c_void_p]
        return self._lib.AwaClientChangeSubscription_GetPath(subscription)

    @wrap(trace_in, trace_out)
    def AwaChangeSet_GetClientSession(self, changeSet):
        self._lib.AwaChangeSet_GetClientSession.restype = c_void_p
        self._lib.AwaChangeSet_GetClientSession.argtypes = [c_void_p]
        return self._lib.AwaChangeSet_GetClientSession(changeSet)


    @wrap(trace_in, trace_out)# * @}
    def AwaClientExecuteSubscription_New(self, path, executeCallback, context):
        if executeCallback is not None:
            raise Exception("ERROR: callback as argument is not supported")

        print 'AwaClientExecuteSubscription_New start\n'
        #context creation
        p1 = c_char_p("TestContext")
        mem = cast(p1, c_void_p)

        self._lib.AwaClientExecuteSubscription_New.restype = c_void_p
        self._lib.AwaClientExecuteSubscription_New.argtypes = [c_char_p, c_void_p, c_void_p]
        return self._lib.AwaClientExecuteSubscription_New(path, self.executeCallbackMemory, mem)

    @wrap(trace_in, trace_out)
    def AwaClientExecuteSubscription_Free(self, subscription):
        self._lib.AwaClientExecuteSubscription_Free.restype = c_int
        mem = cast(subscription, POINTER(c_void_p))
        return self._lib.AwaClientExecuteSubscription_Free(byref(mem))

    @wrap(trace_in, trace_out)
    def AwaClientExecuteSubscription_GetPath(self, subscription):
        self._lib.AwaClientExecuteSubscription_GetPath.restype = c_char_p
        self._lib.AwaClientExecuteSubscription_GetPath.argtypes = [c_void_p]
        return self._lib.AwaClientExecuteSubscription_GetPath(subscription)

    @wrap(trace_in, trace_out)
    def AwaClientSession_Process(self, session, timeout):
        self._lib.AwaClientSession_Process.restype = c_int
        self._lib.AwaClientSession_Process.argtypes = [c_void_p, c_int]
        return self._lib.AwaClientSession_Process(session, timeout)

    @wrap(trace_in, trace_out)
    def AwaClientSession_DispatchCallbacks(self, session):
        self._lib.AwaClientSession_DispatchCallbacks.restype = c_int
        self._lib.AwaClientSession_DispatchCallbacks.argtypes = [c_void_p]
        return self._lib.AwaClientSession_DispatchCallbacks(session)

    @wrap(trace_in, trace_out)
    def ExecuteCallback(self, changeSet):
        print "ExecuteCallback\n"
        if (changeSet != None and changeSet.Data != None and changeSet.Size > 0):
            print ("DATA: length %zu, payload: [", changeSet.Size)
            for i in range(0, changeSet.Size):
                print("%x ", (changeSet.Data)[i])
            print("]\n")

        else:
            print("NO DATA\n")
