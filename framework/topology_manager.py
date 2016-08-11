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

from framework import test_config

from proxies.bootstrap_server_xml_rpc import BootstrapServerXmlRpc
from proxies.gateway_server_xml_rpc import GWServerXmlRpc
from proxies.gateway_client_xml_rpc import GWClientXmlRpc
from proxies.device_server_client_http import DeviceServerClientHttp
from proxies.constrained_client_xml_rpc import ConstrainedClientXmlRpc
from flowcore.flowcore_cloud_session import FlowCoreCloudSession
from helpers.httphelper import HttpHelper

class UnsupportedProxyProtocolException(Exception):
    pass

class ProxyProtocol(IntEnum):
    XMLRPC = 0

class TopologyManager(object):
    def __init__(self):
        self.cloud = None
        self.deviceServerClients = []
        self.bootstrapServers = []
        self.gatewayServers = []
        self.gatewayClients = []
        self.constrainedClients = []

    @classmethod
    def custom(cls, cloudServer=None, cloudTenant=None, deviceServers=None, bootstrapServers=None, gatewayServers=None, gatewayClients=None, constrainedClients=None):
        return cls._loadTopology(cloudServer, cloudTenant, deviceServers, bootstrapServers, gatewayServers, gatewayClients, constrainedClients)


    @classmethod
    def fromConfigFile(cls, topologyName):
        topologyConfig = test_config.config["topologies"][topologyName]
        print 'Loading Topology: ' + topologyName
        return cls._loadTopology(topologyConfig.get("cloud-server", None), \
                                 topologyConfig.get("cloud-tenant", None), \
                                 topologyConfig.get("device-servers", None), \
                                 topologyConfig.get("bootstrap-servers", None), \
                                 topologyConfig.get("gateway-servers", None), \
                                 topologyConfig.get("gateway-clients", None), \
                                 topologyConfig.get("constrained-clients", None))

    @classmethod
    def _loadTopology(cls, cloudServer, cloudTenant, deviceServers, bootstrapServers, gatewayServers, gatewayClients, constrainedClients):
        topology = cls()
        #print("Loading topology: ", topologyConfig)

        if deviceServers is not None:
            deviceServers = deviceServers.split(",")
            for deviceServer in deviceServers:
                deviceServerConfig = test_config.config["device-servers"][deviceServer.strip()]
                if deviceServerConfig is not None:
                    topology.deviceServerClients.append(DeviceServerClientHttp(deviceServerConfig))

        if cloudServer is not None and cloudTenant is not None:
            topology.cloud = FlowCoreCloudSession(cloudServer, cloudTenant)

        if constrainedClients is not None:
            constrainedClients = constrainedClients.split(",")
            for constrainedClient in constrainedClients:
                constrainedClientConfig = test_config.config["constrained-clients"][constrainedClient.strip()]

                proxyProtocol = topology._getProxyProtocolFromConfig(constrainedClientConfig)
                if proxyProtocol == ProxyProtocol.XMLRPC:
                    topology.constrainedClients.append(ConstrainedClientXmlRpc(constrainedClientConfig))
                else:
                    raise UnsupportedProxyProtocolException(proxyProtocol)

        if bootstrapServers is not None:
            bootstrapServers = bootstrapServers.split(",")
            for bootstrapServer in bootstrapServers:
                bootstrapServerConfig = test_config.config["bootstrap-servers"][bootstrapServer.strip()]
                proxyProtocol = topology._getProxyProtocolFromConfig(bootstrapServerConfig)
                if proxyProtocol == ProxyProtocol.XMLRPC:
                    topology.bootstrapServers.append(BootstrapServerXmlRpc(bootstrapServerConfig))
                else:
                    raise UnsupportedProxyProtocolException(proxyProtocol)

        if gatewayServers is not None:
            gatewayServers = gatewayServers.split(",")
            for gatewayServer in gatewayServers:
                gatewayServerConfig = test_config.config["gateway-servers"][gatewayServer.strip()]
                proxyProtocol = topology._getProxyProtocolFromConfig(gatewayServerConfig)
                if proxyProtocol == ProxyProtocol.XMLRPC:
                    topology.gatewayServers.append(GWServerXmlRpc(gatewayServerConfig))
                else:
                    raise UnsupportedProxyProtocolException(proxyProtocol)

        if gatewayClients is not None:
            gatewayClients = gatewayClients.split(",")
            for gatewayClient in gatewayClients:
                gatewayClientConfig = test_config.config["gateway-clients"][gatewayClient.strip()]
                proxyProtocol = topology._getProxyProtocolFromConfig(gatewayClientConfig)
                if proxyProtocol == ProxyProtocol.XMLRPC:
                    topology.gatewayClients.append(GWClientXmlRpc(gatewayClientConfig))
                else:
                    raise UnsupportedProxyProtocolException(proxyProtocol)
        return topology

    def __del__(self):
        pass

    def _getProxyProtocolFromConfig(self, config):
        proxyProtocol = test_config.config["proxies"][config["proxy"]]["protocol"]
        return ProxyProtocol.__members__[proxyProtocol]
