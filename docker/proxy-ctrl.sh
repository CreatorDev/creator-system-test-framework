#!/bin/bash

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

# Manage local proxies

BOOTSTRAP_HELPER_PID_FILE=.pid.bootstrap
GWSERVER_HELPER_PID_FILE=.pid.gwserver
GWCLIENT_HELPER_PID_FILE=.pid.gwclient
CONSTRAINED_CLIENT_HELPER_PID_FILE=.pid.constrainedclient

set -o errexit

if [ x$1 == "x" ] ; then
  COMMAND="empty"
else
  COMMAND=$1
fi

set -o nounset

function syntax {
  echo "Syntax: $0 [start|stop]"
}

function check_for_running {
  local PID=$1
  kill -0 $PID 2>/dev/null
}

function check_for_valid_pid_file {
  local PID_FILE=$1
  if [ -f $PID_FILE ] ; then
    local PID=$(cat $PID_FILE || yes)
	if check_for_running $PID ; then
	  return 0
	fi
  fi
  return 1
}

if [ x$COMMAND == "xstart" ] ; then

  if ! check_for_valid_pid_file $BOOTSTRAP_HELPER_PID_FILE ; then
    set +o nounset
    PYTHONPATH=.:$PYTHONPATH python helpers/bootstrap_server_test_helper.py --ip 127.0.0.1 --port 4442 --log xmlrpcserver_bootstrap_local.log > bootstrap_helper.log 2>&1 &
    set -o nounset
    BOOTSTRAP_HELPER_PID=$!
    echo $BOOTSTRAP_HELPER_PID > $BOOTSTRAP_HELPER_PID_FILE
    echo "Bootstrap Helper PID $BOOTSTRAP_HELPER_PID"
  else
    BOOTSTRAP_HELPER_PID=$(cat $BOOTSTRAP_HELPER_PID_FILE || true)
    echo "Bootstrap PID file exists - check helper is already running as PID $BOOTSTRAP_HELPER_PID"
  fi

  if ! check_for_valid_pid_file $GWSERVER_HELPER_PID_FILE ; then
    set +o nounset
    PYTHONPATH=.:$PYTHONPATH python helpers/gateway_server_test_helper.py --ip 127.0.0.1 --port 4342 --log xmlrpcserver_gateway_server_local.log > server_helper.log 2>&1 &
    set -o nounset
    GWSERVER_HELPER_PID=$!
    echo $GWSERVER_HELPER_PID > $GWSERVER_HELPER_PID_FILE
    echo "GWServer Helper PID $GWSERVER_HELPER_PID"
  else
    GWSERVER_HELPER_PID=$(cat $GWSERVER_HELPER_PID_FILE || true)
    echo "GWServer PID file exists - check helper is already running as PID $GWSERVER_HELPER_PID"
  fi

  if ! check_for_valid_pid_file $GWCLIENT_HELPER_PID_FILE ; then
    set +o nounset
    PYTHONPATH=.:$PYTHONPATH python helpers/gateway_client_test_helper.py --ip 127.0.0.1 --port 4242 --log xmlrpcserver_gateway_client_local.log > client_helper.log 2>&1 &
    set -o nounset
    GWCLIENT_HELPER_PID=$!
    echo $GWCLIENT_HELPER_PID > $GWCLIENT_HELPER_PID_FILE
    echo "GWClient Helper PID $GWCLIENT_HELPER_PID"
  else
    GWCLIENT_HELPER_PID=$(cat $GWCLIENT_HELPER_PID_FILE || true)
    echo "GWClient PID file exists - check helper is already running as PID $GWCLIENT_HELPER_PID"
  fi

  if ! check_for_valid_pid_file $CONSTRAINED_CLIENT_HELPER_PID_FILE ; then
    set +o nounset
    PYTHONPATH=.:$PYTHONPATH python helpers/constrained_client_test_helper.py --ip 127.0.0.1 --port 4142 --log xmlrpcserver_constrained_client_local.log > constrained_device_helper.log 2>&1 &
    set -o nounset
    CONSTRAINED_CLIENT_HELPER_PID=$!
    echo $CONSTRAINED_CLIENT_HELPER_PID > $CONSTRAINED_CLIENT_HELPER_PID_FILE
    echo "ConstrainedClient Helper PID $CONSTRAINED_CLIENT_HELPER_PID"
  else
    CONSTRAINED_CLIENT_HELPER_PID=$(cat $CONSTRAINED_CLIENT_HELPER_PID_FILE || true)
    echo "ConstrainedClient PID file exists - check helper is already running as PID $CONSTRAINED_CLIENT_HELPER_PID"
  fi

  # wait a second and check they are running
  sleep 1
  if ! check_for_running $BOOTSTRAP_HELPER_PID ; then echo "Warning: Bootstrap helper did not start properly!"; rm -f $BOOTSTRAP_HELPER_PID_FILE; fi
  if ! check_for_running $GWSERVER_HELPER_PID ; then echo "Warning: GWServer helper did not start properly!"; rm -f $GWSERVER_HELPER_PID_FILE; fi
  if ! check_for_running $GWCLIENT_HELPER_PID ; then echo "Warning: GWClient helper did not start properly!"; rm -f $GWCLIENT_HELPER_PID_FILE; fi
  if ! check_for_running $CONSTRAINED_CLIENT_HELPER_PID ; then echo "Warning: ConstrainedClient helper did not start properly!"; rm -f $CONSTRAINED_CLIENT_HELPER_PID_FILE; fi

elif [ x$COMMAND == "xstop" ] ; then

  CONSTRAINED_CLIENT_HELPER_PID=$(cat $CONSTRAINED_CLIENT_HELPER_PID_FILE 2>/dev/null || true)
  if [ x$CONSTRAINED_CLIENT_HELPER_PID != "x" ] && kill -0 $CONSTRAINED_CLIENT_HELPER_PID 2>/dev/null ; then
    echo "Killing ConstrainedClient Helper PID $CONSTRAINED_CLIENT_HELPER_PID"
    kill $CONSTRAINED_CLIENT_HELPER_PID
  fi
  rm -f $CONSTRAINED_CLIENT_HELPER_PID_FILE

  GWCLIENT_HELPER_PID=$(cat $GWCLIENT_HELPER_PID_FILE 2>/dev/null || true)
  if [ x$GWCLIENT_HELPER_PID != "x" ] && kill -0 $GWCLIENT_HELPER_PID 2>/dev/null ; then
    echo "Killing GWClient Helper PID $GWCLIENT_HELPER_PID"
    kill $GWCLIENT_HELPER_PID
  fi
  rm -f $GWCLIENT_HELPER_PID_FILE

  GWSERVER_HELPER_PID=$(cat $GWSERVER_HELPER_PID_FILE 2>/dev/null || true)
  if [ x$GWSERVER_HELPER_PID != "x" ] && kill -0 $GWSERVER_HELPER_PID 2>/dev/null ; then
    echo "Killing GWServer Helper PID $GWSERVER_HELPER_PID"
    kill $GWSERVER_HELPER_PID
  fi
  rm -f $GWSERVER_HELPER_PID_FILE

  BOOTSTRAP_HELPER_PID=$(cat $BOOTSTRAP_HELPER_PID_FILE 2>/dev/null || true)
  if [ x$BOOTSTRAP_HELPER_PID != "x" ] && kill -0 $BOOTSTRAP_HELPER_PID 2>/dev/null ; then
    echo "Killing Bootstrap Helper PID $BOOTSTRAP_HELPER_PID"
    kill $BOOTSTRAP_HELPER_PID
  fi
  rm -f $BOOTSTRAP_HELPER_PID_FILE

else
  syntax
  exit 1
fi

