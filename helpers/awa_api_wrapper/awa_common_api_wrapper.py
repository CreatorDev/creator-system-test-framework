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

from ctypes import Structure, POINTER, c_void_p, c_size_t, c_char_p, c_char, c_int, cast, byref, CFUNCTYPE, cdll, c_ulong, c_longlong, c_double, c_bool
import cPickle as pickle
import binascii

from framework import awa_enums
from framework.awa_enums import AwaChangeType
from framework.awa_enums import AwaResourceType
from framework.awa_enums import SessionType
from framework.path import pathToIDs

def AwaOpaqueToBase64(opaqueValue):
    data = bytearray(opaqueValue.Size)
    for i in range(opaqueValue.Size):
        data[i] = cast(opaqueValue.Data, POINTER(c_char))[i]
    
    #print "opaqueValue.Data", data
    #print "opaqueValue.Size", opaqueValue.Size
    return binascii.b2a_base64(data)

class AwaOpaque(Structure):
    _fields_ = [("Data", c_void_p),
                ("Size", c_size_t)]

class AwaCommonAPIWrapper(object):
    def __init__(self, sessionType):
        #self.running = True
        self.sessionType = sessionType
        
        # create our ctypes "change" callback for change subscriptions and observations.
        C_CHANGE_FUNC = CFUNCTYPE(c_void_p, c_void_p)
        callback = C_CHANGE_FUNC(self.ChangeCallback)
        self.changeCallbackMemory = cast(callback, c_void_p)
        
        self.ClearNotifyData()
        
    def loadAwaLibrary(self, path):
        # link libawa
        self._lib = cdll.LoadLibrary(path)

    def AwaStringArray_New(self):
        self._lib.AwaStringArray_New.restype = c_void_p
        return self._lib.AwaStringArray_New()

    def AwaIntegerArray_New(self):
        self._lib.AwaIntegerArray_New.restype = c_void_p
        return self._lib.AwaIntegerArray_New()

    def AwaFloatArray_New(self):
        self._lib.AwaFloatArray_New.restype = c_void_p
        return self._lib.AwaFloatArray_New()

    def AwaBooleanArray_New(self):
        self._lib.AwaBooleanArray_New.restype = c_void_p
        return self._lib.AwaBooleanArray_New()

    def AwaOpaqueArray_New(self):
        self._lib.AwaOpaqueArray_New.restype = c_void_p
        return self._lib.AwaOpaqueArray_New()

    def AwaTimeArray_New(self):
        self._lib.AwaTimeArray_New.restype = c_void_p
        return self._lib.AwaTimeArray_New()

    def AwaObjectLinkArray_New(self):
        self._lib.AwaObjectLinkArray_New.restype = c_void_p
        return self._lib.AwaObjectLinkArray_New()

# * @}
    def AwaStringArray_Free(self, array):
        self._lib.AwaStringArray_Free.restype = None
        mem = cast(array, POINTER(c_void_p))
        return self._lib.AwaStringArray_Free(byref(mem))

    def AwaIntegerArray_Free(self, array):
        self._lib.AwaIntegerArray_Free.restype = None
        mem = cast(array, POINTER(c_void_p))
        return self._lib.AwaIntegerArray_Free(byref(mem))

    def AwaFloatArray_Free(self, array):
        self._lib.AwaFloatArray_Free.restype = None
        mem = cast(array, POINTER(c_void_p))
        return self._lib.AwaFloatArray_Free(byref(mem))

    def AwaBooleanArray_Free(self, array):
        self._lib.AwaBooleanArray_Free.restype = None
        mem = cast(array, POINTER(c_void_p))
        return self._lib.AwaBooleanArray_Free(byref(mem))

    def AwaOpaqueArray_Free(self, array):
        self._lib.AwaOpaqueArray_Free.restype = None
        mem = cast(array, POINTER(c_void_p))
        return self._lib.AwaOpaqueArray_Free(byref(mem))

    def AwaTimeArray_Free(self, array):
        self._lib.AwaTimeArray_Free.restype = None
        mem = cast(array, POINTER(c_void_p))
        return self._lib.AwaTimeArray_Free(byref(mem))

    def AwaObjectLinkArray_Free(self, array):
        self._lib.AwaObjectLinkArray_Free.restype = None
        mem = cast(array, POINTER(c_void_p))
        return self._lib.AwaObjectLinkArray_Free(byref(mem))

# * @}
    def AwaStringArray_SetValueAsCString(self, array, index, value):
        self._lib.AwaStringArray_SetValueAsCString.restype = c_void_p
        self._lib.AwaStringArray_SetValueAsCString.argtypes = [c_void_p, c_ulong, c_char_p]
        return self._lib.AwaStringArray_SetValueAsCString(array, index, value)

    def AwaIntegerArray_SetValue(self, array, index, value):
        self._lib.AwaIntegerArray_SetValue.restype = c_void_p
        self._lib.AwaIntegerArray_SetValue.argtypes = [c_void_p, c_ulong, c_longlong]
        return self._lib.AwaIntegerArray_SetValue(array, index, value)

    def AwaFloatArray_SetValue(self, array, index, value):
        self._lib.AwaFloatArray_SetValue.restype = c_void_p
        self._lib.AwaFloatArray_SetValue.argtypes = [c_void_p, c_ulong, c_double]
        return self._lib.AwaFloatArray_SetValue(array, index, value)

    def AwaBooleanArray_SetValue(self, array, index, value):
        self._lib.AwaBooleanArray_SetValue.restype = c_void_p
        self._lib.AwaBooleanArray_SetValue.argtypes = [c_void_p, c_ulong, c_bool]
        return self._lib.AwaBooleanArray_SetValue(array, index, value)

    def AwaOpaqueArray_SetValue(self, array, index, value):
        self._lib.AwaOpaqueArray_SetValue.restype = c_void_p
        self._lib.AwaOpaqueArray_SetValue.argtypes = [c_void_p, c_ulong, c_void_p]
        return self._lib.AwaOpaqueArray_SetValue(array, index, value)

    def AwaTimeArray_SetValue(self, array, index, value):
        self._lib.AwaTimeArray_SetValue.restype = c_void_p
        self._lib.AwaTimeArray_SetValue.argtypes = [c_void_p, c_ulong, c_longlong]
        return self._lib.AwaTimeArray_SetValue(array, index, value)

    def AwaObjectLinkArray_SetValue(self, array, index, value):
        self._lib.AwaObjectLinkArray_SetValue.restype = c_void_p
        self._lib.AwaObjectLinkArray_SetValue.argtypes = [c_void_p, c_ulong, c_void_p]
        return self._lib.AwaObjectLinkArray_SetValue(array, index, value)

# * @}
    def AwaStringArray_DeleteValue(self, array, index):
        self._lib.AwaStringArray_DeleteValue.restype = c_void_p
        self._lib.AwaStringArray_DeleteValue.argtypes = [c_void_p, c_ulong]
        return self._lib.AwaStringArray_DeleteValue(array, index)

    def AwaIntegerArray_DeleteValue(self, array, index):
        self._lib.AwaIntegerArray_DeleteValue.restype = c_void_p
        self._lib.AwaIntegerArray_DeleteValue.argtypes = [c_void_p, c_ulong]
        return self._lib.AwaIntegerArray_DeleteValue(array, index)

    def AwaFloatArray_DeleteValue(self, array, index):
        self._lib.AwaFloatArray_DeleteValue.restype = c_void_p
        self._lib.AwaFloatArray_DeleteValue.argtypes = [c_void_p, c_ulong]
        return self._lib.AwaFloatArray_DeleteValue(array, index)

    def AwaBooleanArray_DeleteValue(self, array, index):
        self._lib.AwaBooleanArray_DeleteValue.restype = c_void_p
        self._lib.AwaBooleanArray_DeleteValue.argtypes = [c_void_p, c_ulong]
        return self._lib.AwaBooleanArray_DeleteValue(array, index)

    def AwaOpaqueArray_DeleteValue(self, array, index):
        self._lib.AwaOpaqueArray_DeleteValue.restype = c_void_p
        self._lib.AwaOpaqueArray_DeleteValue.argtypes = [c_void_p, c_ulong]
        return self._lib.AwaOpaqueArray_DeleteValue(array, index)

    def AwaTimeArray_DeleteValue(self, array, index):
        self._lib.AwaTimeArray_DeleteValue.restype = c_void_p
        self._lib.AwaTimeArray_DeleteValue.argtypes = [c_void_p, c_ulong]
        return self._lib.AwaTimeArray_DeleteValue(array, index)

    def AwaObjectLinkArray_DeleteValue(self, array, index):
        self._lib.AwaObjectLinkArray_DeleteValue.restype = c_void_p
        self._lib.AwaObjectLinkArray_DeleteValue.argtypes = [c_void_p, c_ulong]
        return self._lib.AwaObjectLinkArray_DeleteValue(array, index)

# * @}
    def AwaStringArray_GetValueAsCString(self, array, index):
        self._lib.AwaStringArray_GetValueAsCString.restype = c_char_p
        self._lib.AwaStringArray_GetValueAsCString.argtypes = [c_void_p, c_ulong]
        return self._lib.AwaStringArray_GetValueAsCString(array, index)

    def AwaIntegerArray_GetValue(self, array, index):
        self._lib.AwaIntegerArray_GetValue.restype = c_longlong
        self._lib.AwaIntegerArray_GetValue.argtypes = [c_void_p, c_ulong]
        return self._lib.AwaIntegerArray_GetValue(array, index)

    def AwaFloatArray_GetValue(self, array, index):
        self._lib.AwaFloatArray_GetValue.restype = c_double
        self._lib.AwaFloatArray_GetValue.argtypes = [c_void_p, c_ulong]
        return self._lib.AwaFloatArray_GetValue(array, index)

    def AwaBooleanArray_GetValue(self, array, index):
        self._lib.AwaBooleanArray_GetValue.restype = c_bool
        self._lib.AwaBooleanArray_GetValue.argtypes = [c_void_p, c_ulong]
        return self._lib.AwaBooleanArray_GetValue(array, index)

    def AwaOpaqueArray_GetValue(self, array, index):
        self._lib.AwaOpaqueArray_GetValue.restype = c_void_p
        self._lib.AwaOpaqueArray_GetValue.argtypes = [c_void_p, c_ulong]
        return self._lib.AwaOpaqueArray_GetValue(array, index)

    def AwaTimeArray_GetValue(self, array, index):
        self._lib.AwaTimeArray_GetValue.restype = c_longlong
        self._lib.AwaTimeArray_GetValue.argtypes = [c_void_p, c_ulong]
        return self._lib.AwaTimeArray_GetValue(array, index)

    def AwaObjectLinkArray_GetValue(self, array, index):
        self._lib.AwaObjectLinkArray_GetValue.restype = c_void_p
        self._lib.AwaObjectLinkArray_GetValue.argtypes = [c_void_p, c_ulong]
        return self._lib.AwaObjectLinkArray_GetValue(array, index)

# * @}
    def AwaStringArray_GetValueCount(self, array):
        self._lib.AwaStringArray_GetValueCount.restype = c_ulong
        self._lib.AwaStringArray_GetValueCount.argtypes = [c_void_p]
        return self._lib.AwaStringArray_GetValueCount(array)

    def AwaIntegerArray_GetValueCount(self, array):
        self._lib.AwaIntegerArray_GetValueCount.restype = c_ulong
        self._lib.AwaIntegerArray_GetValueCount.argtypes = [c_void_p]
        return self._lib.AwaIntegerArray_GetValueCount(array)

    def AwaFloatArray_GetValueCount(self, array):
        self._lib.AwaFloatArray_GetValueCount.restype = c_ulong
        self._lib.AwaFloatArray_GetValueCount.argtypes = [c_void_p]
        return self._lib.AwaFloatArray_GetValueCount(array)

    def AwaBooleanArray_GetValueCount(self, array):
        self._lib.AwaBooleanArray_GetValueCount.restype = c_ulong
        self._lib.AwaBooleanArray_GetValueCount.argtypes = [c_void_p]
        return self._lib.AwaBooleanArray_GetValueCount(array)

    def AwaOpaqueArray_GetValueCount(self, array):
        self._lib.AwaOpaqueArray_GetValueCount.restype = c_ulong
        self._lib.AwaOpaqueArray_GetValueCount.argtypes = [c_void_p]
        return self._lib.AwaOpaqueArray_GetValueCount(array)

    def AwaTimeArray_GetValueCount(self, array):
        self._lib.AwaTimeArray_GetValueCount.restype = c_ulong
        self._lib.AwaTimeArray_GetValueCount.argtypes = [c_void_p]
        return self._lib.AwaTimeArray_GetValueCount(array)

    def AwaObjectLinkArray_GetValueCount(self, array):
        self._lib.AwaObjectLinkArray_GetValueCount.restype = c_ulong
        self._lib.AwaObjectLinkArray_GetValueCount.argtypes = [c_void_p]
        return self._lib.AwaObjectLinkArray_GetValueCount(array)

# * @}
    def AwaStringArray_NewCStringArrayIterator(self, array):
        self._lib.AwaStringArray_NewCStringArrayIterator.restype = c_void_p
        self._lib.AwaStringArray_NewCStringArrayIterator.argtypes = [c_void_p]
        return self._lib.AwaStringArray_NewCStringArrayIterator(array)

    def AwaIntegerArray_NewIntegerArrayIterator(self, array):
        self._lib.AwaIntegerArray_NewIntegerArrayIterator.restype = c_void_p
        self._lib.AwaIntegerArray_NewIntegerArrayIterator.argtypes = [c_void_p]
        return self._lib.AwaIntegerArray_NewIntegerArrayIterator(array)

    def AwaFloatArray_NewFloatArrayIterator(self, array):
        self._lib.AwaFloatArray_NewFloatArrayIterator.restype = c_void_p
        self._lib.AwaFloatArray_NewFloatArrayIterator.argtypes = [c_void_p]
        return self._lib.AwaFloatArray_NewFloatArrayIterator(array)

    def AwaBooleanArray_NewBooleanArrayIterator(self, array):
        self._lib.AwaBooleanArray_NewBooleanArrayIterator.restype = c_void_p
        self._lib.AwaBooleanArray_NewBooleanArrayIterator.argtypes = [c_void_p]
        return self._lib.AwaBooleanArray_NewBooleanArrayIterator(array)

    def AwaOpaqueArray_NewOpaqueArrayIterator(self, array):
        self._lib.AwaOpaqueArray_NewOpaqueArrayIterator.restype = c_void_p
        self._lib.AwaOpaqueArray_NewOpaqueArrayIterator.argtypes = [c_void_p]
        return self._lib.AwaOpaqueArray_NewOpaqueArrayIterator(array)

    def AwaTimeArray_NewTimeArrayIterator(self, array):
        self._lib.AwaTimeArray_NewTimeArrayIterator.restype = c_void_p
        self._lib.AwaTimeArray_NewTimeArrayIterator.argtypes = [c_void_p]
        return self._lib.AwaTimeArray_NewTimeArrayIterator(array)

    def AwaObjectLinkArray_NewObjectLinkArrayIterator(self, array):
        self._lib.AwaObjectLinkArray_NewObjectLinkArrayIterator.restype = c_void_p
        self._lib.AwaObjectLinkArray_NewObjectLinkArrayIterator.argtypes = [c_void_p]
        return self._lib.AwaObjectLinkArray_NewObjectLinkArrayIterator(array)

# * @}
    def AwaStringArray_IsValid(self, array, index):
        self._lib.AwaStringArray_IsValid.restype = c_bool
        self._lib.AwaStringArray_IsValid.argtypes = [c_void_p, c_ulong]
        return self._lib.AwaStringArray_IsValid(array, index)

    def AwaIntegerArray_IsValid(self, array, index):
        self._lib.AwaIntegerArray_IsValid.restype = c_bool
        self._lib.AwaIntegerArray_IsValid.argtypes = [c_void_p, c_ulong]
        return self._lib.AwaIntegerArray_IsValid(array, index)

    def AwaFloatArray_IsValid(self, array, index):
        self._lib.AwaFloatArray_IsValid.restype = c_bool
        self._lib.AwaFloatArray_IsValid.argtypes = [c_void_p, c_ulong]
        return self._lib.AwaFloatArray_IsValid(array, index)

    def AwaBooleanArray_IsValid(self, array, index):
        self._lib.AwaBooleanArray_IsValid.restype = c_bool
        self._lib.AwaBooleanArray_IsValid.argtypes = [c_void_p, c_ulong]
        return self._lib.AwaBooleanArray_IsValid(array, index)

    def AwaOpaqueArray_IsValid(self, array, index):
        self._lib.AwaOpaqueArray_IsValid.restype = c_bool
        self._lib.AwaOpaqueArray_IsValid.argtypes = [c_void_p, c_ulong]
        return self._lib.AwaOpaqueArray_IsValid(array, index)

    def AwaTimeArray_IsValid(self, array, index):
        self._lib.AwaTimeArray_IsValid.restype = c_bool
        self._lib.AwaTimeArray_IsValid.argtypes = [c_void_p, c_ulong]
        return self._lib.AwaTimeArray_IsValid(array, index)

    def AwaObjectLinkArray_IsValid(self, array, index):
        self._lib.AwaObjectLinkArray_IsValid.restype = c_bool
        self._lib.AwaObjectLinkArray_IsValid.argtypes = [c_void_p, c_ulong]
        return self._lib.AwaObjectLinkArray_IsValid(array, index)

# * @}
    def AwaCStringArrayIterator_Next(self, iterator):
        self._lib.AwaCStringArrayIterator_Next.restype = c_bool
        self._lib.AwaCStringArrayIterator_Next.argtypes = [c_void_p]
        return self._lib.AwaCStringArrayIterator_Next(iterator)

    def AwaIntegerArrayIterator_Next(self, iterator):
        self._lib.AwaIntegerArrayIterator_Next.restype = c_bool
        self._lib.AwaIntegerArrayIterator_Next.argtypes = [c_void_p]
        return self._lib.AwaIntegerArrayIterator_Next(iterator)

    def AwaFloatArrayIterator_Next(self, iterator):
        self._lib.AwaFloatArrayIterator_Next.restype = c_bool
        self._lib.AwaFloatArrayIterator_Next.argtypes = [c_void_p]
        return self._lib.AwaFloatArrayIterator_Next(iterator)

    def AwaBooleanArrayIterator_Next(self, iterator):
        self._lib.AwaBooleanArrayIterator_Next.restype = c_bool
        self._lib.AwaBooleanArrayIterator_Next.argtypes = [c_void_p]
        return self._lib.AwaBooleanArrayIterator_Next(iterator)

    def AwaOpaqueArrayIterator_Next(self, iterator):
        self._lib.AwaOpaqueArrayIterator_Next.restype = c_bool
        self._lib.AwaOpaqueArrayIterator_Next.argtypes = [c_void_p]
        return self._lib.AwaOpaqueArrayIterator_Next(iterator)

    def AwaTimeArrayIterator_Next(self, iterator):
        self._lib.AwaTimeArrayIterator_Next.restype = c_bool
        self._lib.AwaTimeArrayIterator_Next.argtypes = [c_void_p]
        return self._lib.AwaTimeArrayIterator_Next(iterator)

    def AwaObjectLinkArrayIterator_Next(self, iterator):
        self._lib.AwaObjectLinkArrayIterator_Next.restype = c_bool
        self._lib.AwaObjectLinkArrayIterator_Next.argtypes = [c_void_p]
        return self._lib.AwaObjectLinkArrayIterator_Next(iterator)

# * @}
    def AwaCStringArrayIterator_GetIndex(self, iterator):
        self._lib.AwaCStringArrayIterator_GetIndex.restype = c_ulong
        self._lib.AwaCStringArrayIterator_GetIndex.argtypes = [c_void_p]
        return self._lib.AwaCStringArrayIterator_GetIndex(iterator)

    def AwaIntegerArrayIterator_GetIndex(self, iterator):
        self._lib.AwaIntegerArrayIterator_GetIndex.restype = c_ulong
        self._lib.AwaIntegerArrayIterator_GetIndex.argtypes = [c_void_p]
        return self._lib.AwaIntegerArrayIterator_GetIndex(iterator)

    def AwaFloatArrayIterator_GetIndex(self, iterator):
        self._lib.AwaFloatArrayIterator_GetIndex.restype = c_ulong
        self._lib.AwaFloatArrayIterator_GetIndex.argtypes = [c_void_p]
        return self._lib.AwaFloatArrayIterator_GetIndex(iterator)

    def AwaBooleanArrayIterator_GetIndex(self, iterator):
        self._lib.AwaBooleanArrayIterator_GetIndex.restype = c_ulong
        self._lib.AwaBooleanArrayIterator_GetIndex.argtypes = [c_void_p]
        return self._lib.AwaBooleanArrayIterator_GetIndex(iterator)

    def AwaOpaqueArrayIterator_GetIndex(self, iterator):
        self._lib.AwaOpaqueArrayIterator_GetIndex.restype = c_ulong
        self._lib.AwaOpaqueArrayIterator_GetIndex.argtypes = [c_void_p]
        return self._lib.AwaOpaqueArrayIterator_GetIndex(iterator)

    def AwaTimeArrayIterator_GetIndex(self, iterator):
        self._lib.AwaTimeArrayIterator_GetIndex.restype = c_ulong
        self._lib.AwaTimeArrayIterator_GetIndex.argtypes = [c_void_p]
        return self._lib.AwaTimeArrayIterator_GetIndex(iterator)

    def AwaObjectLinkArrayIterator_GetIndex(self, iterator):
        self._lib.AwaObjectLinkArrayIterator_GetIndex.restype = c_ulong
        self._lib.AwaObjectLinkArrayIterator_GetIndex.argtypes = [c_void_p]
        return self._lib.AwaObjectLinkArrayIterator_GetIndex(iterator)

# * @}
    def AwaCStringArrayIterator_GetValueAsCString(self, iterator):
        self._lib.AwaCStringArrayIterator_GetValueAsCString.restype = c_char_p
        self._lib.AwaCStringArrayIterator_GetValueAsCString.argtypes = [c_void_p]
        return self._lib.AwaCStringArrayIterator_GetValueAsCString(iterator)

    def AwaIntegerArrayIterator_GetValue(self, iterator):
        self._lib.AwaIntegerArrayIterator_GetValue.restype = c_longlong
        self._lib.AwaIntegerArrayIterator_GetValue.argtypes = [c_void_p]
        return self._lib.AwaIntegerArrayIterator_GetValue(iterator)

    def AwaFloatArrayIterator_GetValue(self, iterator):
        self._lib.AwaFloatArrayIterator_GetValue.restype = c_double
        self._lib.AwaFloatArrayIterator_GetValue.argtypes = [c_void_p]
        return self._lib.AwaFloatArrayIterator_GetValue(iterator)

    def AwaBooleanArrayIterator_GetValue(self, iterator):
        self._lib.AwaBooleanArrayIterator_GetValue.restype = c_bool
        self._lib.AwaBooleanArrayIterator_GetValue.argtypes = [c_void_p]
        return self._lib.AwaBooleanArrayIterator_GetValue(iterator)

    def AwaOpaqueArrayIterator_GetValue(self, iterator):
        self._lib.AwaOpaqueArrayIterator_GetValue.restype = c_void_p
        self._lib.AwaOpaqueArrayIterator_GetValue.argtypes = [c_void_p]
        return self._lib.AwaOpaqueArrayIterator_GetValue(iterator)

    def AwaTimeArrayIterator_GetValue(self, iterator):
        self._lib.AwaTimeArrayIterator_GetValue.restype = c_longlong
        self._lib.AwaTimeArrayIterator_GetValue.argtypes = [c_void_p]
        return self._lib.AwaTimeArrayIterator_GetValue(iterator)

    def AwaObjectLinkArrayIterator_GetValue(self, iterator):
        self._lib.AwaObjectLinkArrayIterator_GetValue.restype = c_void_p
        self._lib.AwaObjectLinkArrayIterator_GetValue.argtypes = [c_void_p]
        return self._lib.AwaObjectLinkArrayIterator_GetValue(iterator)

# * @}
    def AwaCStringArrayIterator_Free(self, iterator):
        self._lib.AwaCStringArrayIterator_Free.restype = c_void_p
        mem = cast(iterator, POINTER(c_void_p))
        return self._lib.AwaCStringArrayIterator_Free(byref(mem))

    def AwaIntegerArrayIterator_Free(self, iterator):
        self._lib.AwaIntegerArrayIterator_Free.restype = c_void_p
        mem = cast(iterator, POINTER(c_void_p))
        return self._lib.AwaIntegerArrayIterator_Free(byref(mem))

    def AwaFloatArrayIterator_Free(self, iterator):
        self._lib.AwaFloatArrayIterator_Free.restype = c_void_p
        mem = cast(iterator, POINTER(c_void_p))
        return self._lib.AwaFloatArrayIterator_Free(byref(mem))

    def AwaBooleanArrayIterator_Free(self, iterator):
        self._lib.AwaBooleanArrayIterator_Free.restype = c_void_p
        mem = cast(iterator, POINTER(c_void_p))
        return self._lib.AwaBooleanArrayIterator_Free(byref(mem))

    def AwaOpaqueArrayIterator_Free(self, iterator):
        self._lib.AwaOpaqueArrayIterator_Free.restype = c_void_p
        mem = cast(iterator, POINTER(c_void_p))
        return self._lib.AwaOpaqueArrayIterator_Free(byref(mem))

    def AwaTimeArrayIterator_Free(self, iterator):
        self._lib.AwaTimeArrayIterator_Free.restype = c_void_p
        mem = cast(iterator, POINTER(c_void_p))
        return self._lib.AwaTimeArrayIterator_Free(byref(mem))

    def AwaObjectLinkArrayIterator_Free(self, iterator):
        self._lib.AwaObjectLinkArrayIterator_Free.restype = c_void_p
        mem = cast(iterator, POINTER(c_void_p))
        return self._lib.AwaObjectLinkArrayIterator_Free(byref(mem))

# * @}
    def AwaObjectDefinition_New(self, objectID, objectName, minimumInstances, maximumInstances):
        self._lib.AwaObjectDefinition_New.restype = c_void_p
        self._lib.AwaObjectDefinition_New.argtypes = [c_int, c_char_p, c_int, c_int]
        return self._lib.AwaObjectDefinition_New(objectID, objectName, minimumInstances, maximumInstances)

    def AwaObjectDefinition_Free(self, objectDefinition):
        self._lib.AwaObjectDefinition_Free.restype = c_void_p
        mem = cast(objectDefinition, POINTER(c_void_p))
        return self._lib.AwaObjectDefinition_Free(byref(mem))

    def AwaObjectDefinition_AddResourceDefinitionAsNoType(self, objectDefinition, resourceID, resourceName, isMandatory, operations):
        self._lib.AwaObjectDefinition_AddResourceDefinitionAsNoType.restype = c_int
        self._lib.AwaObjectDefinition_AddResourceDefinitionAsNoType.argtypes = [c_void_p, c_int, c_char_p, c_bool, c_void_p]
        return self._lib.AwaObjectDefinition_AddResourceDefinitionAsNoType(objectDefinition, resourceID, resourceName, isMandatory, operations)

    def AwaObjectDefinition_AddResourceDefinitionAsString(self, objectDefinition, resourceID, resourceName, isMandatory, operations, defaultValue):
        self._lib.AwaObjectDefinition_AddResourceDefinitionAsString.restype = c_int
        self._lib.AwaObjectDefinition_AddResourceDefinitionAsString.argtypes = [c_void_p, c_int, c_char_p, c_bool, c_void_p, c_char_p]
        return self._lib.AwaObjectDefinition_AddResourceDefinitionAsString(objectDefinition, resourceID, resourceName, isMandatory, operations, defaultValue)

    def AwaObjectDefinition_AddResourceDefinitionAsInteger(self, objectDefinition, resourceID, resourceName, isMandatory, operations, defaultValue):
        self._lib.AwaObjectDefinition_AddResourceDefinitionAsInteger.restype = c_int
        self._lib.AwaObjectDefinition_AddResourceDefinitionAsInteger.argtypes = [c_void_p, c_int, c_char_p, c_bool, c_void_p, c_longlong]
        return self._lib.AwaObjectDefinition_AddResourceDefinitionAsInteger(objectDefinition, resourceID, resourceName, isMandatory, operations, defaultValue)

    def AwaObjectDefinition_AddResourceDefinitionAsFloat(self, objectDefinition, resourceID, resourceName, isMandatory, operations, defaultValue):
        self._lib.AwaObjectDefinition_AddResourceDefinitionAsFloat.restype = c_int
        self._lib.AwaObjectDefinition_AddResourceDefinitionAsFloat.argtypes = [c_void_p, c_int, c_char_p, c_bool, c_void_p, c_double]
        return self._lib.AwaObjectDefinition_AddResourceDefinitionAsFloat(objectDefinition, resourceID, resourceName, isMandatory, operations, defaultValue)

    def AwaObjectDefinition_AddResourceDefinitionAsBoolean(self, objectDefinition, resourceID, resourceName, isMandatory, operations, defaultValue):
        self._lib.AwaObjectDefinition_AddResourceDefinitionAsBoolean.restype = c_int
        self._lib.AwaObjectDefinition_AddResourceDefinitionAsBoolean.argtypes = [c_void_p, c_int, c_char_p, c_bool, c_void_p, c_bool]
        return self._lib.AwaObjectDefinition_AddResourceDefinitionAsBoolean(objectDefinition, resourceID, resourceName, isMandatory, operations, defaultValue)

    def AwaObjectDefinition_AddResourceDefinitionAsOpaque(self, objectDefinition, resourceID, resourceName, isMandatory, operations, defaultValue):
        self._lib.AwaObjectDefinition_AddResourceDefinitionAsOpaque.restype = c_int
        self._lib.AwaObjectDefinition_AddResourceDefinitionAsOpaque.argtypes = [c_void_p, c_int, c_char_p, c_bool, c_void_p, AwaOpaque]
        opaqueValue = None

        if defaultValue == None:
            opaqueValue = AwaOpaque(None, 0)
        elif isinstance(defaultValue, str):
            mem = cast(defaultValue, c_void_p)
            opaqueValue = AwaOpaque(mem, len(defaultValue))
        else:
            opaqueValue = AwaOpaque(cast(defaultValue['Data'], c_void_p), defaultValue['Size'])

        return self._lib.AwaObjectDefinition_AddResourceDefinitionAsOpaque(objectDefinition, resourceID, resourceName, isMandatory, operations, opaqueValue)

    def AwaObjectDefinition_AddResourceDefinitionAsTime(self, objectDefinition, resourceID, resourceName, isMandatory, operations, defaultValue):
        self._lib.AwaObjectDefinition_AddResourceDefinitionAsTime.restype = c_int
        self._lib.AwaObjectDefinition_AddResourceDefinitionAsTime.argtypes = [c_void_p, c_int, c_char_p, c_bool, c_void_p, c_longlong]
        return self._lib.AwaObjectDefinition_AddResourceDefinitionAsTime(objectDefinition, resourceID, resourceName, isMandatory, operations, defaultValue)

    def AwaObjectDefinition_AddResourceDefinitionAsObjectLink(self, objectDefinition, resourceID, resourceName, isMandatory, operations, defaultValue):
        self._lib.AwaObjectDefinition_AddResourceDefinitionAsObjectLink.restype = c_int
        self._lib.AwaObjectDefinition_AddResourceDefinitionAsObjectLink.argtypes = [c_void_p, c_int, c_char_p, c_bool, c_void_p, c_void_p]
        return self._lib.AwaObjectDefinition_AddResourceDefinitionAsObjectLink(objectDefinition, resourceID, resourceName, isMandatory, operations, defaultValue)

# * @}
    def AwaObjectDefinition_AddResourceDefinitionAsStringArray(self, objectDefinition, resourceID, resourceName, minimumInstances, maximumInstances, operations, defaultArray):
        self._lib.AwaObjectDefinition_AddResourceDefinitionAsStringArray.restype = c_int
        self._lib.AwaObjectDefinition_AddResourceDefinitionAsStringArray.argtypes = [c_void_p, c_int, c_char_p, c_int, c_int, c_void_p, c_void_p]
        return self._lib.AwaObjectDefinition_AddResourceDefinitionAsStringArray(objectDefinition, resourceID, resourceName, minimumInstances, maximumInstances, operations, defaultArray)

    def AwaObjectDefinition_AddResourceDefinitionAsIntegerArray(self, objectDefinition, resourceID, resourceName, minimumInstances, maximumInstances, operations, defaultArray):
        self._lib.AwaObjectDefinition_AddResourceDefinitionAsIntegerArray.restype = c_int
        self._lib.AwaObjectDefinition_AddResourceDefinitionAsIntegerArray.argtypes = [c_void_p, c_int, c_char_p, c_int, c_int, c_void_p, c_void_p]
        return self._lib.AwaObjectDefinition_AddResourceDefinitionAsIntegerArray(objectDefinition, resourceID, resourceName, minimumInstances, maximumInstances, operations, defaultArray)

    def AwaObjectDefinition_AddResourceDefinitionAsFloatArray(self, objectDefinition, resourceID, resourceName, minimumInstances, maximumInstances, operations, defaultArray):
        self._lib.AwaObjectDefinition_AddResourceDefinitionAsFloatArray.restype = c_int
        self._lib.AwaObjectDefinition_AddResourceDefinitionAsFloatArray.argtypes = [c_void_p, c_int, c_char_p, c_int, c_int, c_void_p, c_void_p]
        return self._lib.AwaObjectDefinition_AddResourceDefinitionAsFloatArray(objectDefinition, resourceID, resourceName, minimumInstances, maximumInstances, operations, defaultArray)

    def AwaObjectDefinition_AddResourceDefinitionAsBooleanArray(self, objectDefinition, resourceID, resourceName, minimumInstances, maximumInstances, operations, defaultArray):
        self._lib.AwaObjectDefinition_AddResourceDefinitionAsBooleanArray.restype = c_int
        self._lib.AwaObjectDefinition_AddResourceDefinitionAsBooleanArray.argtypes = [c_void_p, c_int, c_char_p, c_int, c_int, c_void_p, c_void_p]
        return self._lib.AwaObjectDefinition_AddResourceDefinitionAsBooleanArray(objectDefinition, resourceID, resourceName, minimumInstances, maximumInstances, operations, defaultArray)

    def AwaObjectDefinition_AddResourceDefinitionAsTimeArray(self, objectDefinition, resourceID, resourceName, minimumInstances, maximumInstances, operations, defaultArray):
        self._lib.AwaObjectDefinition_AddResourceDefinitionAsTimeArray.restype = c_int
        self._lib.AwaObjectDefinition_AddResourceDefinitionAsTimeArray.argtypes = [c_void_p, c_int, c_char_p, c_int, c_int, c_void_p, c_void_p]
        return self._lib.AwaObjectDefinition_AddResourceDefinitionAsTimeArray(objectDefinition, resourceID, resourceName, minimumInstances, maximumInstances, operations, defaultArray)

    def AwaObjectDefinition_AddResourceDefinitionAsOpaqueArray(self, objectDefinition, resourceID, resourceName, minimumInstances, maximumInstances, operations, defaultArray):
        self._lib.AwaObjectDefinition_AddResourceDefinitionAsOpaqueArray.restype = c_int
        self._lib.AwaObjectDefinition_AddResourceDefinitionAsOpaqueArray.argtypes = [c_void_p, c_int, c_char_p, c_int, c_int, c_void_p, c_void_p]
        return self._lib.AwaObjectDefinition_AddResourceDefinitionAsOpaqueArray(objectDefinition, resourceID, resourceName, minimumInstances, maximumInstances, operations, defaultArray)

    def AwaObjectDefinition_AddResourceDefinitionAsObjectLinkArray(self, objectDefinition, resourceID, resourceName, minimumInstances, maximumInstances, operations, defaultArray):
        self._lib.AwaObjectDefinition_AddResourceDefinitionAsObjectLinkArray.restype = c_int
        self._lib.AwaObjectDefinition_AddResourceDefinitionAsObjectLinkArray.argtypes = [c_void_p, c_int, c_char_p, c_int, c_int, c_void_p, c_void_p]
        return self._lib.AwaObjectDefinition_AddResourceDefinitionAsObjectLinkArray(objectDefinition, resourceID, resourceName, minimumInstances, maximumInstances, operations, defaultArray)

# * @}
    def AwaObjectDefinition_GetID(self, objectDefinition):
        self._lib.AwaObjectDefinition_GetID.restype = c_int
        self._lib.AwaObjectDefinition_GetID.argtypes = [c_void_p]
        return self._lib.AwaObjectDefinition_GetID(objectDefinition)

    def AwaObjectDefinition_GetName(self, objectDefinition):
        self._lib.AwaObjectDefinition_GetName.restype = c_char_p
        self._lib.AwaObjectDefinition_GetName.argtypes = [c_void_p]
        return self._lib.AwaObjectDefinition_GetName(objectDefinition)

    def AwaObjectDefinition_GetMinimumInstances(self, objectDefinition):
        self._lib.AwaObjectDefinition_GetMinimumInstances.restype = c_int
        self._lib.AwaObjectDefinition_GetMinimumInstances.argtypes = [c_void_p]
        return self._lib.AwaObjectDefinition_GetMinimumInstances(objectDefinition)

    def AwaObjectDefinition_GetMaximumInstances(self, objectDefinition):
        self._lib.AwaObjectDefinition_GetMaximumInstances.restype = c_int
        self._lib.AwaObjectDefinition_GetMaximumInstances.argtypes = [c_void_p]
        return self._lib.AwaObjectDefinition_GetMaximumInstances(objectDefinition)

    def AwaObjectDefinition_IsResourceDefined(self, objectDefinition, resourceID):
        self._lib.AwaObjectDefinition_IsResourceDefined.restype = c_bool
        self._lib.AwaObjectDefinition_IsResourceDefined.argtypes = [c_void_p, c_int]
        return self._lib.AwaObjectDefinition_IsResourceDefined(objectDefinition, resourceID)

    def AwaObjectDefinition_GetResourceDefinition(self, objectDefinition, resourceID):
        self._lib.AwaObjectDefinition_GetResourceDefinition.restype = c_void_p
        self._lib.AwaObjectDefinition_GetResourceDefinition.argtypes = [c_void_p, c_int]
        return self._lib.AwaObjectDefinition_GetResourceDefinition(objectDefinition, resourceID)

    def AwaObjectDefinitionIterator_Next(self, iterator):
        self._lib.AwaObjectDefinitionIterator_Next.restype = c_bool
        self._lib.AwaObjectDefinitionIterator_Next.argtypes = [c_void_p]
        return self._lib.AwaObjectDefinitionIterator_Next(iterator)

    def AwaObjectDefinitionIterator_Get(self, iterator):
        self._lib.AwaObjectDefinitionIterator_Get.restype = c_void_p
        self._lib.AwaObjectDefinitionIterator_Get.argtypes = [c_void_p]
        return self._lib.AwaObjectDefinitionIterator_Get(iterator)

    def AwaObjectDefinitionIterator_Free(self, iterator):
        self._lib.AwaObjectDefinitionIterator_Free.restype = c_void_p
        mem = cast(iterator, POINTER(c_void_p))
        return self._lib.AwaObjectDefinitionIterator_Free(byref(mem))

    def AwaResourceDefinition_GetID(self, resourceDefinition):
        self._lib.AwaResourceDefinition_GetID.restype = c_int
        self._lib.AwaResourceDefinition_GetID.argtypes = [c_void_p]
        return self._lib.AwaResourceDefinition_GetID(resourceDefinition)

    def AwaResourceDefinition_GetType(self, resourceDefinition):
    #self._lib.AwaResourceDefinition_GetType.restype = c_void_p
        self._lib.AwaResourceDefinition_GetType.restype = c_int
        self._lib.AwaResourceDefinition_GetType.argtypes = [c_void_p]
        return self._lib.AwaResourceDefinition_GetType(resourceDefinition)

    def AwaResourceDefinition_GetName(self, resourceDefinition):
        self._lib.AwaResourceDefinition_GetName.restype = c_char_p
        self._lib.AwaResourceDefinition_GetName.argtypes = [c_void_p]
        return self._lib.AwaResourceDefinition_GetName(resourceDefinition)

    def AwaResourceDefinition_GetMinimumInstances(self, resourceDefinition):
        self._lib.AwaResourceDefinition_GetMinimumInstances.restype = c_int
        self._lib.AwaResourceDefinition_GetMinimumInstances.argtypes = [c_void_p]
        return self._lib.AwaResourceDefinition_GetMinimumInstances(resourceDefinition)

    def AwaResourceDefinition_GetMaximumInstances(self, resourceDefinition):
        self._lib.AwaResourceDefinition_GetMaximumInstances.restype = c_int
        self._lib.AwaResourceDefinition_GetMaximumInstances.argtypes = [c_void_p]
        return self._lib.AwaResourceDefinition_GetMaximumInstances(resourceDefinition)

    def AwaResourceDefinition_GetSupportedOperations(self, resourceDefinition):
        self._lib.AwaResourceDefinition_GetSupportedOperations.restype = c_void_p
        self._lib.AwaResourceDefinition_GetSupportedOperations.argtypes = [c_void_p]
        return self._lib.AwaResourceDefinition_GetSupportedOperations(resourceDefinition)

    def AwaResourceDefinition_IsMandatory(self, resourceDefinition):
        self._lib.AwaResourceDefinition_IsMandatory.restype = c_bool
        self._lib.AwaResourceDefinition_IsMandatory.argtypes = [c_void_p]
        return self._lib.AwaResourceDefinition_IsMandatory(resourceDefinition)

    def AwaObjectDefinition_NewResourceDefinitionIterator(self, objectDefinition):
        self._lib.AwaObjectDefinition_NewResourceDefinitionIterator.restype = c_void_p
        self._lib.AwaObjectDefinition_NewResourceDefinitionIterator.argtypes = [c_void_p]
        return self._lib.AwaObjectDefinition_NewResourceDefinitionIterator(objectDefinition)

    def AwaResourceDefinitionIterator_Next(self, iterator):
        self._lib.AwaResourceDefinitionIterator_Next.restype = c_bool
        self._lib.AwaResourceDefinitionIterator_Next.argtypes = [c_void_p]
        return self._lib.AwaResourceDefinitionIterator_Next(iterator)

    def AwaResourceDefinitionIterator_Get(self, iterator):
        self._lib.AwaResourceDefinitionIterator_Get.restype = c_void_p
        self._lib.AwaResourceDefinitionIterator_Get.argtypes = [c_void_p]
        return self._lib.AwaResourceDefinitionIterator_Get(iterator)

    def AwaResourceDefinitionIterator_Free(self, iterator):
        self._lib.AwaResourceDefinitionIterator_Free.restype = c_void_p
        mem = cast(iterator, POINTER(c_void_p))
        return self._lib.AwaResourceDefinitionIterator_Free(byref(mem))

    def AwaPathIterator_Next(self, iterator):
        self._lib.AwaPathIterator_Next.restype = c_bool
        self._lib.AwaPathIterator_Next.argtypes = [c_void_p]
        return self._lib.AwaPathIterator_Next(iterator)

    def AwaPathIterator_Get(self, iterator):
        self._lib.AwaPathIterator_Get.restype = c_char_p
        self._lib.AwaPathIterator_Get.argtypes = [c_void_p]
        return self._lib.AwaPathIterator_Get(iterator)

    def AwaPathIterator_Free(self, iterator):
        self._lib.AwaPathIterator_Free.restype = c_void_p
        mem = cast(iterator, POINTER(c_void_p))
        return self._lib.AwaPathIterator_Free(byref(mem))

    def AwaAPI_MakeObjectPath(self, path, pathSize, objectID):
        self._lib.AwaAPI_MakeObjectPath.restype = c_int
        self._lib.AwaAPI_MakeObjectPath.argtypes = [c_char_p, c_ulong, c_int]
        return self._lib.AwaAPI_MakeObjectPath(path, pathSize, objectID)

    def AwaAPI_MakeObjectInstancePath(self, path, pathSize, objectID, objectInstanceID):
        self._lib.AwaAPI_MakeObjectInstancePath.restype = c_int
        self._lib.AwaAPI_MakeObjectInstancePath.argtypes = [c_char_p, c_ulong, c_int, c_int]
        return self._lib.AwaAPI_MakeObjectInstancePath(path, pathSize, objectID, objectInstanceID)

    def AwaAPI_MakeResourcePath(self, path, pathSize, objectID, objectInstanceID, resourceID):
        self._lib.AwaAPI_MakeResourcePath.restype = c_int
        self._lib.AwaAPI_MakeResourcePath.argtypes = [c_char_p, c_ulong, c_int, c_int, c_int]
        return self._lib.AwaAPI_MakeResourcePath(path, pathSize, objectID, objectInstanceID, resourceID)

    def AwaAPI_MakePath(self, path, pathSize, objectID, objectInstanceID, resourceID):
        self._lib.AwaAPI_MakePath.restype = c_int
        self._lib.AwaAPI_MakePath.argtypes = [c_char_p, c_ulong, c_int, c_int, c_int]
        return self._lib.AwaAPI_MakePath(path, pathSize, objectID, objectInstanceID, resourceID)

    def AwaAPI_IsPathValid(self, path):
        self._lib.AwaAPI_IsPathValid.restype = c_bool
        self._lib.AwaAPI_IsPathValid.argtypes = [c_char_p]
        return self._lib.AwaAPI_IsPathValid(path)

    def AwaPathResult_GetError(self, result):
        self._lib.AwaPathResult_GetError.restype = c_int
        self._lib.AwaPathResult_GetError.argtypes = [c_void_p]
        return self._lib.AwaPathResult_GetError(result)

    def AwaPathResult_GetLWM2MError(self, result):
        self._lib.AwaPathResult_GetLWM2MError.restype = c_void_p
        self._lib.AwaPathResult_GetLWM2MError.argtypes = [c_void_p]
        return self._lib.AwaPathResult_GetLWM2MError(result)

    def AwaLog_SetLevel(self, level):
        self._lib.AwaLog_SetLevel.restype = c_void_p
        self._lib.AwaLog_SetLevel.argtypes = [c_void_p]
        return self._lib.AwaLog_SetLevel(level)

    def AwaError_ToString(self, error):
        self._lib.AwaError_ToString.restype = c_char_p
        self._lib.AwaError_ToString.argtypes = [c_int]
        return self._lib.AwaError_ToString(error)

    def AwaError_FromString(self, errorString):
        self._lib.AwaError_FromString.restype = c_int
        self._lib.AwaError_FromString.argtypes = [c_char_p]
        return self._lib.AwaError_FromString(errorString)

    def AwaServerError_ToString(self, error):
        self._lib.AwaServerError_ToString.restype = c_char_p
        self._lib.AwaServerError_ToString.argtypes = [c_void_p]
        return self._lib.AwaServerError_ToString(error)

    def AwaServerError_FromString(self, errorString):
        self._lib.AwaServerError_FromString.restype = c_void_p
        self._lib.AwaServerError_FromString.argtypes = [c_char_p]
        return self._lib.AwaServerError_FromString(errorString)

    def AwaChangeSet_NewPathIterator(self, changeSet):
        self._lib.AwaChangeSet_NewPathIterator.restype = c_void_p
        self._lib.AwaChangeSet_NewPathIterator.argtypes = [c_void_p]
        return self._lib.AwaChangeSet_NewPathIterator(changeSet)

    def AwaChangeSet_GetChangeType(self, changeSet, path):
        self._lib.AwaChangeSet_GetChangeType.restype = c_void_p
        self._lib.AwaChangeSet_GetChangeType.argtypes = [c_void_p, c_char_p]
        return self._lib.AwaChangeSet_GetChangeType(changeSet, path)

    def AwaChangeSet_HasValue(self, changeSet, path):
        self._lib.AwaChangeSet_HasValue.restype = c_bool
        self._lib.AwaChangeSet_HasValue.argtypes = [c_void_p, c_char_p]
        return self._lib.AwaChangeSet_HasValue(changeSet, path)

    def AwaChangeSet_ContainsPath(self, changeSet, path):
        self._lib.AwaChangeSet_ContainsPath.restype = c_bool
        self._lib.AwaChangeSet_ContainsPath.argtypes = [c_void_p, c_char_p]
        return self._lib.AwaChangeSet_ContainsPath(changeSet, path)

    def AwaChangeSet_GetResourceType(self, changeSet, path):
        self._lib.AwaChangeSet_GetResourceType.restype = c_void_p
        self._lib.AwaChangeSet_GetResourceType.argtypes = [c_void_p, c_char_p]
        return self._lib.AwaChangeSet_GetResourceType(changeSet, path)

    def AwaChangeSet_GetValueAsCStringPointer(self, changeSet, path, value):
        self._lib.AwaChangeSet_GetValueAsCStringPointer.restype = c_int
        mem = cast(value, POINTER(c_char_p))
        ret = self._lib.AwaChangeSet_GetValueAsCStringPointer(changeSet, path, byref(mem))
        result = None
        if ret == 0:
            result = cast(mem, c_char_p).value

        return result

    def AwaChangeSet_GetValueAsIntegerPointer(self, changeSet, path, value):
        self._lib.AwaChangeSet_GetValueAsIntegerPointer.restype = c_int
        mem = cast(value, POINTER(POINTER(c_longlong)))
        ret = self._lib.AwaChangeSet_GetValueAsIntegerPointer(changeSet, path, byref(mem))
        result = None
        if ret == 0:
            result = cast(mem, POINTER(c_longlong)).contents.value

        return result

    def AwaChangeSet_GetValueAsFloatPointer(self, changeSet, path, value):
        self._lib.AwaChangeSet_GetValueAsFloatPointer.restype = c_int
        mem = cast(value, POINTER(POINTER(c_double)))
        ret = self._lib.AwaChangeSet_GetValueAsFloatPointer(changeSet, path, byref(mem))
        result = None
        if ret == 0:
            result = cast(mem, POINTER(c_double)).contents.value

        return result


    def AwaChangeSet_GetValueAsBooleanPointer(self, changeSet, path, value):
        self._lib.AwaChangeSet_GetValueAsBooleanPointer.restype = c_int
        mem = cast(value, POINTER(c_bool))
        ret = self._lib.AwaChangeSet_GetValueAsBooleanPointer(changeSet, path, byref(mem))
        result = None
        if ret == 0:
            result = cast(mem, c_bool).value

        return result


    def AwaChangeSet_GetValueAsTimePointer(self, changeSet, path, value):
        self._lib.AwaChangeSet_GetValueAsTimePointer.restype = c_int
        mem = cast(value, POINTER(POINTER(c_longlong)))
        ret = self._lib.AwaChangeSet_GetValueAsTimePointer(changeSet, path, byref(mem))
        result = None
        if ret == 0:
            result = cast(mem, POINTER(c_longlong)).contents.value

        return result

# * @}
    def AwaChangeSet_GetValueAsOpaque(self, changeSet, path, value):
        self._lib.AwaChangeSet_GetValueAsOpaque.restype = c_int
        self._lib.AwaChangeSet_GetValueAsOpaque.argtypes = [c_void_p, c_char_p, POINTER(AwaOpaque)]
        value = c_void_p()
        opaqueValue = AwaOpaque(value, 0)
        ret = self._lib.AwaChangeSet_GetValueAsOpaque(changeSet, path, byref(opaqueValue))
        result = None
        if ret == 0:
            result = AwaOpaqueToBase64(opaqueValue)
        return result

    def AwaChangeSet_GetValueAsObjectLink(self, changeSet, path, value):
        self._lib.AwaChangeSet_GetValueAsObjectLink.restype = c_int
        self._lib.AwaChangeSet_GetValueAsObjectLink.argtypes = [c_void_p, c_char_p, c_void_p]
        return self._lib.AwaChangeSet_GetValueAsObjectLink(changeSet, path, value)

    def AwaChangeSet_GetValuesAsStringArrayPointer(self, changeSet, path, valueArray):
        self._lib.AwaChangeSet_GetValuesAsStringArrayPointer.restype = c_int
        mem = cast(valueArray, POINTER(c_void_p))
        ret = self._lib.AwaChangeSet_GetValuesAsStringArrayPointer(changeSet, path, byref(mem))
        result = {}
        iterator = self._lib.AwaStringArray_NewCStringArrayIterator(mem)
        if iterator is not None:
            while self._lib.AwaCStringArrayIterator_Next(iterator):
                index = self._lib.AwaCStringArrayIterator_GetIndex(iterator)
                value = cast(self._lib.AwaCStringArrayIterator_GetValueAsCString(iterator), c_char_p).value
                result[index] = value

            self._lib.AwaCStringArrayIterator_Free(byref(cast(iterator, POINTER(c_void_p))))

        return result

    def AwaChangeSet_GetValuesAsIntegerArrayPointer(self, changeSet, path, valueArray):
        self._lib.AwaChangeSet_GetValuesAsIntegerArrayPointer.restype = c_int
        mem = cast(valueArray, POINTER(c_void_p))
        ret = self._lib.AwaChangeSet_GetValuesAsIntegerArrayPointer(changeSet, path, byref(mem))
        result = {}
        iterator = self._lib.AwaIntegerArray_NewIntegerArrayIterator(mem)
        if iterator is not None:
            while self._lib.AwaIntegerArrayIterator_Next(iterator):
                index = self._lib.AwaIntegerArrayIterator_GetIndex(iterator)
                value = self._lib.AwaIntegerArrayIterator_GetValue(iterator)
                result[index] = value

            self._lib.AwaIntegerArrayIterator_Free(byref(cast(iterator, POINTER(c_void_p))))

        return result

    def AwaChangeSet_GetValuesAsFloatArrayPointer(self, changeSet, path, valueArray):
        self._lib.AwaChangeSet_GetValuesAsFloatArrayPointer.restype = c_int
        mem = cast(valueArray, POINTER(c_void_p))
        return self._lib.AwaChangeSet_GetValuesAsFloatArrayPointer(byref(mem))

    def AwaChangeSet_GetValuesAsBooleanArrayPointer(self, changeSet, path, valueArray):
        self._lib.AwaChangeSet_GetValuesAsBooleanArrayPointer.restype = c_int
        mem = cast(valueArray, POINTER(c_void_p))
        return self._lib.AwaChangeSet_GetValuesAsBooleanArrayPointer(byref(mem))

    def AwaChangeSet_GetValuesAsTimeArrayPointer(self, changeSet, path, valueArray):
        self._lib.AwaChangeSet_GetValuesAsTimeArrayPointer.restype = c_int
        mem = cast(valueArray, POINTER(c_void_p))
        return self._lib.AwaChangeSet_GetValuesAsTimeArrayPointer(byref(mem))

    def AwaChangeSet_GetValuesAsOpaqueArrayPointer(self, changeSet, path, valueArray):
        self._lib.AwaChangeSet_GetValuesAsOpaqueArrayPointer.restype = c_int
        mem = cast(valueArray, POINTER(c_void_p))
        return self._lib.AwaChangeSet_GetValuesAsOpaqueArrayPointer(byref(mem))

    def AwaChangeSet_GetValuesAsObjectLinkArrayPointer(self, changeSet, path, valueArray):
        self._lib.AwaChangeSet_GetValuesAsObjectLinkArrayPointer.restype = c_int
        mem = cast(valueArray, POINTER(c_void_p))
        return self._lib.AwaChangeSet_GetValuesAsObjectLinkArrayPointer(byref(mem))

        # NON-API helper polling functions
    def ClearNotifyData(self):
        self.NotifyResponse = {}
        #print("Notify Response Cleared")

    def Awa_GetNotifyData(self):
        print "Awa_GetNotifyData\n"
        import sys
        sys.stdout.flush()
        if self.NotifyResponse != None:
            # must serialise dictionary to send through XML RPC
            # otherwise opaque values aren't encoded correctly
            return pickle.dumps(self.NotifyResponse)
        else:
            return None

    def ChangeCallback(self, changeSet):
        print "ChangeCallback\n"
        result = None
        session = None

        if self.sessionType == SessionType.Client:
            session = self.AwaChangeSet_GetClientSession(changeSet)
        else:
            session = self.AwaChangeSet_GetServerSession(changeSet)

        iterator = self.AwaChangeSet_NewPathIterator(changeSet)

        while (self.AwaPathIterator_Next(iterator)):
            path = self.AwaPathIterator_Get(iterator)
            changeType = self.AwaChangeSet_GetChangeType(changeSet, path)
            if changeType == AwaChangeType.ResourceCreated:
                print "Changed: %s %s:\n"%(path, "Resource Created")
            elif changeType == AwaChangeType.ResourceModified:
                print "Changed: %s %s:\n"%(path, "Resource Modified")
            elif changeType == AwaChangeType.ResourceDeleted:
                print "Changed: %s %s:\n"%(path, "Resource Deleted")
            elif changeType == AwaChangeType.ObjectInstanceCreated:
                print "Changed: %s %s:\n"%(path, "Object Instance Created")
            elif changeType == AwaChangeType.ObjectInstanceModified:
                print "Changed: %s %s:\n"%(path, "Object Instance Modified")
            elif changeType == AwaChangeType.ObjectInstanceDeleted:
                print "Changed: %s %s:\n"%(path, "Object Instance Deleted")
            elif changeType == AwaChangeType.Current:
                print "Changed: %s %s:\n"%(path, "Current Value")
            else:
                print "ChangeType was Invalid\n"

            if ( changeType == AwaChangeType.ResourceCreated or changeType == AwaChangeType.ResourceModified ):
                print "Get response data from change-set.......\n"
                #val = self.AwaClientSession_PathToIDs(session, path, objectID, objectInstanceID, resourceID)

                objectID, objectInstanceID, resourceID = pathToIDs(path)

                objectDefinition = None
                if self.sessionType == SessionType.Client:
                    objectDefinition = self.AwaClientSession_GetObjectDefinition(session, objectID)
                else:
                    objectDefinition = self.AwaServerSession_GetObjectDefinition(session, objectID)

                resDefinition = self.AwaObjectDefinition_GetResourceDefinition(objectDefinition, resourceID)
                resType = self.AwaResourceDefinition_GetType(resDefinition)
                print "resource Type found in response as::%d"%resType

                if not awa_enums.isArrayResourceType(resType):
                    if resType == AwaResourceType.String:
                        result = self.AwaChangeSet_GetValueAsCStringPointer(changeSet, path, None)
                    elif resType == AwaResourceType.Integer:
                        result = self.AwaChangeSet_GetValueAsIntegerPointer(changeSet, path, None)
                    elif resType == AwaResourceType.Float:
                        result = self.AwaChangeSet_GetValueAsFloatPointer(changeSet, path, None)
                    elif resType == AwaResourceType.Boolean:
                        result = self.AwaChangeSet_GetValueAsBooleanPointer(changeSet, path, None)
                    elif resType == AwaResourceType.Opaque:
                        result = self.AwaChangeSet_GetValueAsOpaque(changeSet, path, None)
                    elif resType == AwaResourceType.Time:
                        result = self.AwaChangeSet_GetValueAsTimePointer(changeSet, path, None)
                    elif resType == AwaResourceType.ObjectLink:
                        result = self.AwaChangeSet_GetValueAsObjectLink(changeSet, path, None)
                    else:
                        print "Unhandled Type found: %d\n" % (resType, )

                    #Set <path,value> pairs in TestData to pass the response notify to the test cases
                    if result is not None:
                        print "Changeset value for path " + path +" = " + str(result);
                        self.NotifyResponse[path] = result
                else:

                    if resType == AwaResourceType.StringArray:
                        result = self.AwaChangeSet_GetValuesAsStringArrayPointer(changeSet, path, None)
                    elif resType == AwaResourceType.IntegerArray:
                        result = self.AwaChangeSet_GetValuesAsIntegerArrayPointer(changeSet, path, None)
                    else:
                        print "Unhandled Type found: %d\n" % (resType, )
                    #Set <path,dict<instance, value>> pairs in TestData to pass the response notify to the test cases
                    if result is not None:
                        print "Changeset value for path " + path +" = " + str(result);
                        if path not in self.NotifyResponse:
                            self.NotifyResponse[path] = {}
                        self.NotifyResponse[path].update(result)

            else:
                print "Change Type Not mached\n"


        self.AwaPathIterator_Free(iterator)
        print "ChangeCallback end"

    #def finish(self):
    #    self.running = False
