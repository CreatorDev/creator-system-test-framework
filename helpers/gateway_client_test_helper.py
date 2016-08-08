#!/usr/bin/env python

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

from daemon import AwaClientDaemon
import helper
from helper import HelperWithDaemon
from helpers.awa_api_wrapper.awa_gateway_client_api_wrapper import AwaGatewayClientAPIWrapper

class GWClientTestHelper(AwaGatewayClientAPIWrapper, HelperWithDaemon):

    def __init__(self):
        super(GWClientTestHelper, self).__init__()

    def setEndpointName(self, endpointName):
        self._endpointName = endpointName

    def setFactoryBootstrapConfigFile(self, factoryBootstrapConfigFile):
        self._factoryBootstrapConfigFile = factoryBootstrapConfigFile

    def setBootstrapURI(self, bootstrapURI):
        self._bootstrapURI = bootstrapURI

    def setPskIdentity(self, pskIdentity):
        self._pskIdentity = pskIdentity
        
    def setPskKey(self, pskKey):
        self._pskKey = pskKey

    def setCertificate(self, certificate):
        self._certificate = certificate
    
    def setObjDefsFile(self, objDefsFile):
        self._objDefsFile = objDefsFile
    
    def initialiseDaemon(self):
        self._daemon = AwaClientDaemon(daemonBinary=self._daemonPath,
                                       ipcPort=self._daemonIpcPort,
                                       coapPort=self._daemonCoapPort,
                                       addressFamily=self._daemonAddressFamily,
                                       endpointName=self._endpointName, 
                                       factoryBootstrapConfigFile=self._factoryBootstrapConfigFile,
                                       bootstrapURI=self._bootstrapURI,
                                       pskIdentity=self._pskIdentity,
                                       pskKey=self._pskKey,
                                       certificate=self._certificate,
                                       objDefsFile=self._objDefsFile,
                                       logFile=self._daemonLogFilename,
                                       verbose=True)

def main():
    helper.StartHelper(GWClientTestHelper())

if __name__ == "__main__":
    main()
