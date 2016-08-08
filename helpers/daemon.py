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

import sys
import os.path
import signal
import socket
import struct
import errno

# default binary paths can be set from the environment:
try:
    BOOTSTRAP_SERVER_BINARY = os.environ['LWM2M_BOOTSTRAPD_BIN']
except KeyError:
    # use PATH to locate
    BOOTSTRAP_SERVER_BINARY = "awa_bootstrapd"

try:
    SERVER_BINARY = os.environ['LWM2M_SERVERD_BIN']
except KeyError:
    # use PATH to locate
    SERVER_BINARY = "awa_serverd"

try:
    CLIENT_BINARY = os.environ['LWM2M_CLIENTD_BIN']
except KeyError:
    # use PATH to locate
    CLIENT_BINARY = "awa_clientd"

IPC_TIMEOUT = 10  # seconds

CONTENT_TYPE_MAP = { "text/plain" : 0,
                     "application/octet-stream" : 42,
                     "application/json" : 50,
                     "application/vnd.oma.lwm2m+text" : 1541,
                     "application/vnd.oma.lwm2m+tlv" : 1542,
                     "application/vnd.oma.lwm2m+json" : 1543,
                     }

class OverlordException(Exception):
    pass

def getContentTypeID(contentType):
    try:
        ID = CONTENT_TYPE_MAP[contentType]
    except AttributeError:
        raise OverlordException("Unknown content type '%s'" % (contentType,))
    return ID

def waitForIPC(ipcPort, timeout, request):
    """Timeout is in seconds."""
    #time.sleep(2)

    # assume 127.0.0.1 for now
    address = "127.0.0.1"
    port = int(ipcPort)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # overall timeout in microseconds
    timeout_us = timeout * 1000000

    # set socket timeout (10 ms per attempt)
    sec = 0
    usec = 10000
    timeval = struct.pack('ll', sec, usec)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeval)

    count = 0
    maxCount = timeout_us / (sec * 1000000 + usec)
    response = False
    while not response and count < maxCount:
        sock.sendto(request, (address, port))
        try:
            data, addr = sock.recvfrom(65536)
        except socket.error as serr:
            if serr.errno != errno.EAGAIN:  # EAGAIN == Resource Temporarily Unavailable
                raise serr
        else:
            response = len(data) > 0
        count += 1

    sock.close()
    return response

class Daemon(object):

    def __init__(self):
        self._pid = 0
        self._file = None
        self._args = []

    def spawn(self, wait=False, silent=False):
        """Fork and exec the target process."""
        if not os.path.isfile(self._file):
            raise OverlordException("%s not found" % (self._file, ))

        pid = os.fork()

        if pid == 0:
            # child

            if silent:
                fd = os.open("/dev/null", os.O_APPEND)
                os.dup2(fd, sys.stdout.fileno())
            else:
                print("Spawning " + " ".join(self._args))
            sys.stdout.flush()

            os.execvp(self._file, self._args)
            exit(1)

        elif pid > 0:
            # parent
            if wait:
                pid, status = os.wait()

        self._pid = pid

    def kill(self, silent=False):
        if self._pid > 0:
            os.kill(self._pid, signal.SIGKILL)
            os.waitpid(self._pid, 0)
            self._pid = 0

    def terminate(self, silent=False):
        if self._pid > 0:
            os.kill(self._pid, signal.SIGTERM)
            os.waitpid(self._pid, 0)
            self._pid = 0

    def interrupt(self, silent=False):
        if self._pid > 0:
            os.kill(self._pid, signal.SIGINT)
            self._pid = 0

    def waitForIPC(self, ipcPort, timeout):
        return waitForIPC(ipcPort, timeout, self._ipcWaitRequest)

class AwaBootstrapServerDaemon(Daemon):
    def __init__(self,
                 daemonBinary=None,
                 address=None,
                 interface=None,
                 addressFamily=None,
                 coapPort=None,
                 configFiles=None,
                 logFile=None,
                 verbose=True):

        super(AwaBootstrapServerDaemon, self).__init__()

        self._file = daemonBinary or BOOTSTRAP_SERVER_BINARY
        self._args = [ daemonBinary ]

        if address is not None:
            self._args += [ "--ip", address ]
        if interface is not None:
            self._args += [ "--interface", interface ]
        if addressFamily is not None:
            self._args += [ "--addressFamily", str(addressFamily) ]
        if coapPort is not None:
            self._args += [ "--port", str(coapPort) ]
        if configFiles:
            for configFile in configFiles:
                self._args += [ "--config", configFile ]
        if logFile is not None:
            self._args += [ "--logFile", logFile ]
        if verbose:
            self._args += [ "--verbose" ]

    def spawn(self, silent=False):
        super(AwaBootstrapServerDaemon, self).spawn(silent)

        if not silent:
            print("Awa LWM2M Bootstrap Server: pid %d" % (self._pid,))

    def kill(self, silent=False):
        pid = self._pid
        super(AwaBootstrapServerDaemon, self).kill(silent)
        if not silent:
            print("Awa LWM2M Bootstrap Server: pid %d killed" % (pid,))

class AwaServerDaemon(Daemon):
    def __init__(self,
                 daemonBinary=None,
                 ipcPort=None,
                 address=None,
                 interface=None,
                 addressFamily=None,
                 coapPort=None,
                 logFile=None,
                 contentType=None,
                 verbose=True):

        super(AwaServerDaemon, self).__init__()

        try:
            contentTypeID = int(contentType)
        except ValueError:
            contentTypeID = getContentTypeID(contentType)

        daemonBinary = daemonBinary or SERVER_BINARY
        self._file = daemonBinary
        self._args = [ daemonBinary ]

        if ipcPort is not None:
            self._args += [ "--ipcPort", str(ipcPort) ]
        if address is not None:
            self._args += [ "--ip", address ]
        if interface is not None:
            self._args += [ "--interface", interface ]
        if addressFamily is not None:
            self._args += [ "--addressFamily", str(addressFamily) ]
        if coapPort is not None:
            self._args += [ "--port", str(coapPort) ]
        if logFile is not None:
            self._args += [ "--logFile", logFile ]
        if contentTypeID is not None:
            self._args += [ "--contentType", str(contentTypeID) ]
        if verbose:
            self._args += [ "--verbose" ]

        self._ipcWaitRequest = "<Request><Type>ListClients</Type></Request>"
        self._ipcPort = ipcPort

    def spawn(self, silent=False):
        super(AwaServerDaemon, self).spawn(silent)

        # wait for server IPC
        if not self.waitForIPC(self._ipcPort, IPC_TIMEOUT):
            raise Exception("Awa LWM2M Server IPC timed out")

        if not silent:
            print("Awa LWM2M Server: pid %d, IPC port %d" % (self._pid, self._ipcPort))

    def kill(self, silent=False):
        pid = self._pid
        super(AwaServerDaemon, self).kill(silent)
        if not silent:
            print("Awa LWM2M Server: pid %d killed" % (pid,))


class AwaClientDaemon(Daemon):
    def __init__(self,
                 daemonBinary=None,
                 ipcPort=None,
                 coapPort=None,
                 addressFamily=None,
                 endpointName=None,
                 factoryBootstrapConfigFile=None,
                 bootstrapURI=None,
                 pskIdentity=None,
                 pskKey=None,
                 certificate=None,
                 objDefsFile=None,
                 logFile=None,
                 verbose=True):

        super(AwaClientDaemon, self).__init__()
        self._file = daemonBinary or CLIENT_BINARY
        self._args = [ daemonBinary ]

        if ipcPort is not None:
            self._args += [ "--ipcPort", str(ipcPort) ]
        if coapPort is not None:
            self._args += [ "--port", str(coapPort) ]
        if addressFamily is not None:
            self._args += [ "--addressFamily", str(addressFamily) ]
        if endpointName is not None:
            self._args += [ "--endPointName", endpointName ]
        if factoryBootstrapConfigFile is not None:
            self._args += [ "--factoryBootstrap", factoryBootstrapConfigFile ]
        if bootstrapURI is not None:
            self._args += [ "--bootstrap", bootstrapURI ]
        if pskIdentity is not None:
            self._args += [ "--pskIdentity", pskIdentity ]
        if pskKey is not None:
            self._args += [ "--pskKey", pskKey ]
        if certificate is not None:
            self._args += [ "--certificate", certificate ]
        if objDefsFile is not None:
            self._args += [ "--objDefs", objDefsFile ]
        if logFile is not None:
            self._args += [ "--logFile", logFile ]
        if verbose:
            self._args += [ "--verbose" ]

        self._ipcWaitRequest = "<Request><Type>Get</Type><Content><ObjectID>3</ObjectID><InstanceID>0</InstanceID><PropertyID>15</PropertyID></Content></Request>"
        self._ipcPort = ipcPort

    def spawn(self, silent=False):
        super(AwaClientDaemon, self).spawn(silent)

        # wait for server IPC
        if not self.waitForIPC(self._ipcPort, IPC_TIMEOUT):
            raise Exception("Awa LWM2M Client IPC timed out on port %d", self._ipcPort)

        if not silent:
            print("Awa LWM2M Client: pid %d, IPC port %d" % (self._pid, self._ipcPort))

    def kill(self, silent=False):
        pid = self._pid
        super(AwaClientDaemon, self).kill(silent)
        if not silent:
            print("Awa LWM2M Client: pid %d killed" % (pid,))

