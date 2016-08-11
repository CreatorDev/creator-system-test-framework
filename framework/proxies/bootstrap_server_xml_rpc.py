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

from framework import test_config
from xml_rpc_client import XmlRpcClient

class BootstrapServerXmlRpc(XmlRpcClient):

    # Establish and maintain XMLRPC connection with BootstrapServerHelper.
    def __init__(self, bootstrapConfig):
        super(BootstrapServerXmlRpc, self).__init__(test_config.config["proxies"][bootstrapConfig["proxy"]])

        self._bootstrapConfig = bootstrapConfig
        self._xmlrpcSession.setDaemonPath(test_config.config['paths']['awa-bootstrapd'])
        self._xmlrpcSession.setDaemonIPAddress(self._bootstrapConfig.get('ip-address', None))
        self._xmlrpcSession.setDaemonNetworkInterface(self._bootstrapConfig.get('interface', None))
        self._xmlrpcSession.setDaemonAddressFamily(self._bootstrapConfig.get('address-family', None))
        self._xmlrpcSession.setDaemonCoapPort(self._bootstrapConfig['port'])
        self._xmlrpcSession.setDaemonLogFilename(self._bootstrapConfig['log'])

        configFiles = [self._bootstrapConfig["config"], ]
        configNumber = 2
        while True:
            config = 'config%d' % (configNumber, )
            if not config in self._bootstrapConfig:
                break
            configFiles.append(self._bootstrapConfig[config])
            configNumber += 1
        self._xmlrpcSession.setBoostrapConfigFiles(configFiles)

        self._xmlrpcSession.initialiseDaemon()
        self._xmlrpcSession.startDaemon()

    def __del__(self):
        self._xmlrpcSession.stopDaemon()
        del self._xmlrpcSession

