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

import subprocess
import re
import base64
import time
import socket
import struct
import sys
import abc

from framework.static_client import StaticClient, StaticClientError, ExpectTimeoutException
import serial

class EncodeException(StaticClientError):
    pass
class ConstrainedClientError(StaticClientError):
    pass

def Encode(value):
    if isinstance(value, int):
        data = struct.pack("=q", value)
    elif isinstance(value, float):
        data = struct.pack("=d", value)
    elif isinstance(value, str):
        data = value
    else:
        raise EncodeException("Unknown type %s with value %s" % (str(type(value)),str(value),))

    return base64.standard_b64encode(data)

def Decode(value, type):
    data = base64.standard_b64decode(value)

    print("Decoding value %s, type %s" % (str(value), str(type)))
    sys.stdout.flush()

    if type is int:
        result = struct.unpack("=q", data)[0]
    elif type is float:
        result = struct.unpack("=d", data)[0]
    elif type is str:
        result = str(data)
    else:
        raise EncodeException("Unknown type %s with value %s" % (str(type(value)),str(value),))

    return result

def WaitForAddress(bootstrapAddr, attempts=200, wait=0.1):
    """IPv6 interface takes some time to be ready. Wait until a bind operation succeeds before proceeding."""
    sys.stdout.write("Wait for %s" % (bootstrapAddr,))
    for x in xrange(attempts):
        try:
            sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            sock.bind((bootstrapAddr, 0, 0, 0))
            sock.close()
            # bind succeeded, end loop
            sys.stdout.write("OK\n")
            break
        except:
            # bind failed, wait and try again
            time.sleep(wait)
            sys.stdout.write(".")
            sys.stdout.flush()
    else:
        sys.stdout.write("TIMEOUT\n")
        raise ConstrainedClientError("unable to configure tap interface")

class ConstrainedClient(StaticClient):
    __metaclass__ = abc.ABCMeta

    def __init__(self, clientID, bootstrapURI, port, debug=False, verbose=False):
        self.client_id = clientID
        self._bootstrapURI = bootstrapURI
        self._port = port

        # implemented by ancestor classes
        self._clientSession = None
        self._verbose = verbose

    def __del__(self):
        # cannot guarantee when this will be called. Use close instead.
        pass

    def close(self):
        if self._clientSession:
            #self._sendline("stop")  # ?
            self.softwareReset()
            self.waitForResetToComplete()
            try:
                self._clientSession.terminate()
            except:
                pass
            self._clientSession.close()

    def echo(self, text):
        self._sendline("echo %s" % (text, ))

        while True:
            output = self._clientSession.readline()
            if len(text.strip()) == len(output.strip()):
                return output.strip()

    def softwareReset(self):
        self._sendline("reset")

    def waitForResetToComplete(self):
        self.expect("Short MAC address")
        self.expect("Extended MAC address")
        self.expect("nullmac nullrdc")
        self.expect("Link address")
        self.expect("Tentative link-local")
        self.expect("Tentative global")
        self.expect("Contiki>")

    def init(self):
        """ pass configuration to contiki application via "init" cmd
        """
        self._sendline("init -c {0} -b {1} -p {2} {3}".format(
                                      self.client_id,
                                      self._bootstrapURI,
                                      self._port,
                                      '-v' if self._verbose else ''))
        self.expect("Contiki>")

    def factoryBootstrap(self, serverURI, lifeTime=60):
        self._sendline("factory_bootstrap -u {0} -t {1}".format(serverURI, lifeTime))
        self.expect("Contiki>")

    def defineObject(self, objectID, minInstances, maxInstances):
        self._sendline("define_object -o {0} -n {1} -m {2}".format(
                                      objectID, minInstances, maxInstances))
        self.expect('\[RESULT\] (\d+)')
        result = self._clientSession.match.groups()[0]
        self.expect("Contiki>")
        return result

    def defineResource(self, objectID, resourceID, resourceName, resourceType, minResources, maxResources, operations, resourceSizeInBytes):
        self._sendline("define_resource -o {0} -r {1} -k {2} -t {3} -n {4} -m {5} -p {6} -s {7}".format(
                                      objectID, resourceID, resourceName, resourceType, minResources, maxResources, operations, resourceSizeInBytes))
        self.expect('\[RESULT\] (\d+)')
        result = self._clientSession.match.groups()[0]
        self.expect("Contiki>")
        return result

    def start(self):
        """ start AwaLWM2M process, must be called after all objects are defined
        """
        self._sendline("start")
        # capture version number for future usage
        #print("Expecting AwaLWM2M startup")
        #self.expect("Starting AwaLWM2M Client") # TODO REMOVE

        print("Expecting version")
        self.expect('LWM2M client - version ([0-9.]*\d+)')
        self._clientVersion = self._clientSession.match.groups()[0]

        print("Received version: %s" % (self._clientVersion, ))
        self.expect("Contiki>")

    def createObjectInstance(self, objectID, instanceID):
        self._sendline("create_object -o {0} -i {1}".format(objectID, instanceID))
        self.expect('\[RESULT\] (\d+)')
        result = self._clientSession.match.groups()[0]
        self.expect("Contiki>")
        return result

    def createResource(self, objectID, instanceID, resourceID):
        self._sendline("create_resource -o {0} -i {1} -r {2}".format(objectID, instanceID, resourceID))
        self.expect('\[RESULT\] (\d+)')
        result = self._clientSession.match.groups()[0]
        self.expect("Contiki>")
        return result

    def version(self):
        """ get the AwaLWM2M version number """
        return self._clientVersion

    def setResourceValue(self, path, value):
        oir = path.strip('/').split('/')
        if len(oir) == 3:
            oir.append('0')
        if len(oir) != 4:
            raise ConstrainedClientError("set can only be used on resource instances")
        bytesWritten = self._sendline("set_resource_value -o {0} -i {1} -r {2} -n {3} -v {4}".format(
                                      oir[0], oir[1], oir[2], oir[3], Encode(value)))
        print("Written %d bytes" % (bytesWritten, ))
        sys.stdout.flush()
        code = self.expect(['\[RESULT\] (\d+)', '\[ERROR\] (\w\s]*)'])
        result = self._clientSession.match.groups()[0]
        if code == 1:
            raise ConstrainedClientError(result)
        self.expect("Contiki>")
        return result

    def getResourceValue(self, path, resourceType=str, checkExistsOnly=False): # TODO check != a value (e.g. "")
        oir = path.strip('/').split('/')
        if len(oir) == 3:
            oir.append('0')
        elif len(oir) != 4:
            raise ConstrainedClientError("get can only be used on resource instances")
        command = "get_resource_value -o {0} -i {1} -r {2} -n {3}".format(
                                      oir[0], oir[1], oir[2], oir[3])
        print("getResourceValue: %s" % (command, ))
        print("-------------------------------------------------------------------")
        self._sendline(command)
        code = 1
        result = ""
        try:
            code = self.expect(['\[RESULT\] ([A-Za-z0-9+/=]*)', '\[ERROR\] ([\w\s]*)'])
            result = self._clientSession.match.groups()[0]

            print("code: %s" % (str(code), ))
            print("result: %s" % (str(result), ))

            sys.stdout.flush()
            self.expect("Contiki>")
        except:
            if not checkExistsOnly:
                raise

        if code == 1 and not checkExistsOnly:
            raise ConstrainedClientError(result)
        elif checkExistsOnly:
            return code == 0 and result != ""
        else:
            return Decode(result, resourceType)

    def delete(self):
        pass

    def _sendline(self, command):
        print("Sending input: %s" % (command, ))
        sys.stdout.flush()
        return self._clientSession.sendline(command+"\r\n")

# Custom Serial send/expect class
# This implementation gives a higher degree of control while monitoring output 
# from the serial device than using pexpect.fdpexpect, which seems to be unreliable.
class SerialSession():
    def __init__(self, serial):
        self._serial = serial
        #self.outFile=open("constrained_client_serial.log", "w")
        self.before = ""
        self.after = ""
        self.match = None

    def sendline(self, inputString):
        numBytesSent = self._serial.write(inputString)
        return numBytesSent

    def readline(self, expected=None):
        print("Reading line...")
        startTime = time.time()
        serialOutput = ""
        while True:
            serialOutput += self._serial.read(1)
            if serialOutput.endswith("\r\n"):
                if serialOutput.strip().endswith("Contiki>") and (expected is None or "Contiki>" not in expected):
                    print("SKIPPED %s" % (serialOutput, ))
                elif serialOutput.strip().startswith("[INFO]"):# or serialOutput.strip().startswith("[ERROR]"):
                    print("SKIPPED %s" % (serialOutput, ))
                elif len(serialOutput.strip()) > 0:
                    break;
                serialOutput = ""
            if self._serial.timeout > 0 and (time.time() - startTime) > self._serial.timeout:
                if expected != None:
                    raise ExpectTimeoutException("Expected %s" % (str(expected), ))
                else:
                    raise ExpectTimeoutException("No line read")

        print("Received output from serial: %s" % (serialOutput, ))
        print("Time taken: %f" % (time.time() - startTime, ))
        return serialOutput.strip()

    def expect(self, patterns, timeout):
        print("Expecting output: %s : Timeout=%d" % (patterns, timeout))
        self._serial.timeout = timeout

        serialOutput = self.readline(patterns)

        self.before = serialOutput
        self.after = serialOutput
        if isinstance(patterns, str):
            if self._expectString(patterns, serialOutput):
                self._matchedPattern(patterns, serialOutput)
                return 0
        else:
            for index, pattern in enumerate(patterns):
                if self._expectString(pattern, serialOutput):
                    self._matchedPattern(pattern, serialOutput)
                    return index
        raise Exception(serialOutput + " does not match pattern " + str(patterns))

    def _expectString(self, pattern, output):
        self.match = re.search(pattern, output)
        return self.match is not None and self.match.group() is not None

    def _matchedPattern(self, pattern, output):
        print("MATCHED %s : %s" % (pattern, output, ))
        try:
            print("Group: %s" % (self.match.group(), ))
        except:
            pass
        try:
            print("Groups[0]: %s" % (self.match.groups()[0], ))
        except:
            pass

    def terminate(self):
        pass

    def close(self):
        self._serial.close()


class ConstrainedClientSerial(ConstrainedClient):

    def __init__(self, clientID, bootstrapURI, port, serialPort, debug=False, verbose=False):
        super(ConstrainedClientSerial, self).__init__(clientID, bootstrapURI, port, debug, verbose)

        print("Creating serial")
        serialConnection = serial.Serial(
                                     port=serialPort,
                                     baudrate=57600,  # 115200,
                                     parity=serial.PARITY_NONE,
                                     stopbits=serial.STOPBITS_ONE,  # STOPBITS_TWO
                                     bytesize=serial.EIGHTBITS
        )

        #self._clientSession = fdpexpect.fdspawn(self._serial, logfile=open("constrained_client_serial.log", "w"))
        self._clientSession = SerialSession(serialConnection)
        self._sendline("")  # FIXME - This should be a reboot?

        self.expect("Contiki>")
        self.init()

    def __del__(self):
        super(ConstrainedClientSerial, self).__del__()

    def expect(self, output, timeout=10):
        return self._clientSession.expect(output, timeout)

class ConstrainedClientSimulated(ConstrainedClient):

    def __init__(self, clientID, bootstrapURI, port, daemonPath, taygaConfig, debug=False, verbose=False):
        """ spawn a AwaLWM2M client in a simulated contiki environment
        """
        super(ConstrainedClientSimulated, self).__init__(clientID, bootstrapURI, port, debug, verbose)

        print("Spawning simulated client session")
        sys.stdout.flush()

        # import dynamically so that we do not need pexpect on real hardware
        import pexpect

        # start contiki application
        self._clientSession = pexpect.spawn(daemonPath)
        if debug:
            self._clientSession.logfile = sys.stdout


        try:
            self.expect('ifconfig (\w+) up')
        except pexpect.EOF, e:
            raise ConstrainedClientError("Not running as root?")
        tap = self._clientSession.match.groups()[0]

        self.expect("Contiki>")

        self.init()

        bootstrapAddr = re.search(r'\[(.*)\]', self._bootstrapURI).group(1)

        if taygaConfig is not None:
            # setup tayga to allow for access to the cloud
            subprocess.check_call(['./tayga.sh',
                                   '-c {0}'.format(tap),
                                   '-e {0}'.format(taygaConfig['ethif']),
                                   '-a {0}'.format(bootstrapAddr),
                                   '-a {0}'.format(taygaConfig['ip-address'])],
                                   cwd=taygaConfig['tayga-scripts'])
        else:
            subprocess.check_call(['ip', 'addr', 'add', bootstrapAddr+'/64', 'dev', tap])
            subprocess.check_call(['ip', 'addr', 'add', 'aaaa::1/64', 'dev', tap])

        # this delay is required to allow the ip address assignment to take effect
        # if we don't wait here, the subsequent bind() operation fails for no apparent reason.
        WaitForAddress(bootstrapAddr)

    def __del__(self):
        super(ConstrainedClientSimulated,self).__del__()

    def expect(self, output, timeout=5):
        print("Expecting output: %s : Timeout=%d" % (output, timeout))
        sys.stdout.flush()
        return self._clientSession.expect(output, timeout)

    def waitForResetToComplete(self):
        print("Skipped RESET (simulated device)")
        pass
