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

from plugins import testconfig_loader
import copy

# typically, nosetests will invoke testconfig's configure() callback to load the config
_config = testconfig_loader.config

# If not running nosetests, explicitly load configuration file into testconfig.config
def InitTestData(configFile):
    print("Using configuration %s\n" % (configFile,))
    #testconfig.load_ini(configFile, 'utf-8')
    testconfig_loader.load_yaml(configFile, 'utf-8')
    _config = testconfig_loader.config
    _config = FixTestConfigEncoding(_config)

config = _config

def IsBool(value):
    return value.lower() in ['true', 'false', 'yes', 'no', 'on', 'off', '1', '0']

def ToBool(value):
    return value.lower() in ['true', 'yes', 'on', '1']

def IsNone(value):
    return value.lower() == str(None).lower()

def GetTypedValue(value):
    if isinstance(value, int):
        newValue = int(value)
    elif isinstance(value, float):
        newValue = float(value)
    elif isinstance(value, long):
        newValue = long(value)
    elif IsBool(value):
        newValue = ToBool(value)
    elif IsNone(value):
        newValue = None
    else:
        newValue = value
    return newValue

def FixTestConfigEncoding(config):
    new_config = CopyDict(config, 'ascii');
    PrintConfig(new_config)
    return new_config

def CopyValue(value, encoding):
    """Create a copy of the value, encoding strings as necessary."""
    res = None
    if isinstance(value, dict):
        res = CopyDict(value, encoding)
    elif isinstance(value, unicode):
        res = value.encode(encoding, 'strict')
    else:
        res = copy.deepcopy(value)
    return res

def CopyDict(d, encoding):
    """Create a copy of a dictionary, encoding key and value strings as necessary."""
    dest = {}
    for key, value in d.items():
        new_value = CopyValue(value, encoding)
        new_key = CopyValue(key, encoding)
        dest[new_key] = new_value
    return dest

def ValueToString(value, prefix=None):
    result = ""
    prefix = prefix is None and "" or prefix
    if isinstance(value, dict):
        # sort
        for k in sorted(value.keys()):
            result += "%s%s:\n" % (prefix, k)
            result += "%s\n" % (ValueToString(value[k], prefix + "  "),)
    else:
        result += "%s%s\n" % (prefix, value)
    return result

def PrintConfig(config):
    print("Test Config:")
    print(ValueToString(config, "  "))

# if nosetests controls testconfig, then it will be populated by this point:
if _config:
    _config = FixTestConfigEncoding(_config)
