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

from nose.plugins import Plugin
import subprocess
import re

from framework import test_config

class ListVersions(Plugin):
    name = 'listversions'

    def getTestFrameworkVersion(self):
        repo = subprocess.check_output(["git", "config", "--get", "remote.origin.url"]).strip()
        repo = re.compile('^.*@').sub('', repo)       # remove user@ prefix if it exists
        repo = re.compile('^https\://').sub('', repo) # remove https:// prefix if it exists
        sha1 = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip()[0:7]  # 7 chars is enough
        return repo + "::" + sha1

    def getAwaLWM2MVersion(self):
        awaDaemon = test_config.config['paths']['awa-clientd']
        try:
            version = subprocess.check_output([awaDaemon, "--version"]).strip()
        except OSError:
            version = "unknown"
        return version

    def getFlowCloudVersion(self):
        return "unknown"

    def getContikiVersion(self):
        app_version = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip()[0:7]
        # currently, lwm2m-contiki has an Awa LWM2M submodule which may differ in version to the main Awa component
        awa_sha = subprocess.check_output(["git", "rev-parse", "HEAD:AwaLWM2M"], cwd="../lwm2m-contiki").strip()[0:7]
        return "%s [Awa LWM2M %s]" % (app_version, awa_sha)

    def configure(self, options, noseconfig):
        print('*' * 100)
        print(' Component Versions:')
        print('   Test Harness:')
        print('     Framework     : %s' % (self.getTestFrameworkVersion(),))
        print('   Test Fixture:')
        print('     Awa LWM2M     : %s' % (self.getAwaLWM2MVersion(),))
        print('     LWM2M-Contiki : %s' % (self.getContikiVersion(),))
        print('*' * 100)
