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

import logging
import SimpleXMLRPCServer
import xmlrpclib
import sys

class LoggingSimpleXMLRPCRequestHandler(SimpleXMLRPCServer.SimpleXMLRPCRequestHandler):
    """Overides the default SimpleXMLRPCRequestHander to support logging.  Logs
    client IP and the XML request and response.
    """

    def do_POST(self):
        clientIP, port = self.client_address
        logger = self.server.instance.logger

        # Log client IP and Port
        logger.info('Client IP: %s - Port: %s' % (clientIP, port))
        try:
            # get arguments
            data = self.rfile.read(int(self.headers["content-length"]))
            # Log client request
            logger.info('Client request: \n%s\n' % data)

            response = self.server._marshaled_dispatch(data, getattr(self, '_dispatch', None))
            # Log server response
            logger.info('Server response: \n%s\n' % response)

        except: # This should only happen if the module is buggy
            # internal error, report as HTTP server error
            self.send_response(500)
            self.end_headers()
        else:
            # got a valid XML RPC response
            self.send_response(200)
            self.send_header("Content-type", "text/xml")
            self.send_header("Content-length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)

            # shut down the connection
            self.wfile.flush()
            self.connection.shutdown(1)

class VerboseFaultXMLRPCServer(SimpleXMLRPCServer.SimpleXMLRPCServer):
    def _marshaled_dispatch(self, data, dispatch_method = None, path = None):
        try:
            params, method = xmlrpclib.loads(data)

            # generate response
            if dispatch_method is not None:
                response = dispatch_method(method, params)
            else:
                response = self._dispatch(method, params)
            # wrap response in a singleton tuple
            response = (response,)
            response = xmlrpclib.dumps(response, methodresponse=1,
                                       allow_none=self.allow_none, encoding=self.encoding)
        except:
            # report low level exception back to server
            # (each dispatcher should have handled their own
            # exceptions)
            exc_type, exc_value, tb = sys.exc_info()
            while tb.tb_next is not None:
                tb = tb.tb_next  # find last frame of the traceback
            lineno = tb.tb_lineno
            code = tb.tb_frame.f_code
            filename = code.co_filename
            name = code.co_name
            response = xmlrpclib.dumps(
                xmlrpclib.Fault(1, "%s:%s FILENAME: %s LINE: %s NAME: %s" % (
                    exc_type, exc_value, filename, lineno, name)),
                encoding=self.encoding, allow_none=self.allow_none)
        return response

def createLogger(filename):
    logger = logging.getLogger(filename)
    hdlr = logging.FileHandler(filename)
    formatter = logging.Formatter("%(asctime)s  %(levelname)s  %(message)s")
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)
    return logger

def startXMLRPCServer(rpcInstance, address, port, logFilename):
    
    rpcInstance.logger = createLogger(logFilename)
    #server = SimpleXMLRPCServer.SimpleXMLRPCServer((address, port), allow_none=True, logRequests = True)
    server = VerboseFaultXMLRPCServer((address, port), LoggingSimpleXMLRPCRequestHandler, allow_none=True)
    print "SimpleXMLRPCServer Started. Listening on %s:%d..." % (address, port, )
    server.register_instance(rpcInstance, True)
    try:
        while True:
            server.handle_request()
        #server.serve_forever()
    except KeyboardInterrupt:
        pass
    except Exception:
        raise
    finally:
        print "Exiting"
        server.server_close()
