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

from nose_parameterized import parameterized
from nose.plugins.attrib import attr

from framework.test_cases.gateway_server_and_client_test_case import GWServerAndClientTestCase

from framework.operation_assertions import read_operation_assertions
from framework.operation_assertions import write_operation_assertions

from framework import test_assertions
from framework.test_assertions import ReadAssertion
from framework.test_assertions import WriteAssertion

from framework.awa_enums import AwaResourceType

from framework.nose_parameterised import noseParameterisedTestNameGenerator

@attr("gateway_client", "gateway_server", "device_object")
class CustomObjectDefineTestCases(GWServerAndClientTestCase):
    
    
    @parameterized.expand([
        ["WriteReadDeviceCurrentTimeResource", (ReadAssertion(read_operation_assertions.CheckForSuccess, "/3/0/13", AwaResourceType.Time, 2718619435),
                                                WriteAssertion(write_operation_assertions.CheckForSuccess, "/3/0/13", AwaResourceType.Time, 1718619434),
                                                ReadAssertion(read_operation_assertions.CheckForSuccess, "/3/0/13", AwaResourceType.Time, 1718619434), )],
    ], testcase_func_name=noseParameterisedTestNameGenerator)
    
    def test(self, name, assertions):
        test_assertions.callAssertions(self, assertions)
        
    
