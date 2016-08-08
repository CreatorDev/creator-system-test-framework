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

import collections
import requests
import json
from dicttoxml import dicttoxml
from lxml import objectify
from time import time



# HTTP Client Abstraction class that encapsulates a number of modules for making HTTP requests to the device server
# - HTTP client
# - JSON serialiser/deserialiser
# - XML serialiser/deserialiser


# ToDos
# - GetEntrypoint could just call Get()
# - Paging
# - Handle error responses better

class HttpHelper():

    _entry_point = None
    _last_response = None
    
    # Credentials
    _key = None
    _secret = None

    # API Tokens    
    _access_token = None
    _access_token_type = None
    _access_token_expiry = None
    _refresh_token = None
    
    # Settings
    _json_content_mode = True
    _default_timeout_seconds = 2.0
    _default_page_size = 20
    _default_start_index = 0


    
    def __init__(self, entry_point, key='', secret='', json_content_mode=True, default_timeout_seconds=2.0):       
        self._entry_point = entry_point
        self._key = key
        self._secret = secret
        self._json_content_mode = json_content_mode
        self._default_timeout_seconds = default_timeout_seconds
    
    
    def create_test_credentials(self, timeout=None):
        if self._entry_point is None:
            raise NoneType

        create_credentials_Url = self._entry_point + '/accesskeys'
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJPcmdJRCI6IjAiLCJleHAiOjE0OTA5NTgwMDB9.zw-laBQRc7Xcxo5excZQeiWRy67UqUq5SNP64U__NxE'}
        body = '{"Name":"Tester"}'
        response = requests.post(create_credentials_Url, data=body, headers=headers, timeout=(timeout, self._default_timeout_seconds)[timeout is None])

        # Parse response
        if response != None:

            # Check content type of response and invoke appropriate deserialiser
            response_content_type = response.headers['Content-Type']
            response_status_code = response.status_code

            #'json' response:
            response_object = json.loads(response.text)
            key = None
            secret = None
            if 'Key' in response_object:
                key = response_object['Key']               
            if 'Secret' in response_object:
                secret = response_object['Secret']

            CredentialsType = collections.namedtuple('Credentials', ['Key', 'Secret'])
            return CredentialsType (key, secret)

        else:
            return None


    ################################################################################################### 
    # Login client
    ###################################################################################################
    def login(self, timeout=None):
        if self._entry_point is None:
            raise NoneType
        
        # Send login request        
        content_mode_string = ('xml', 'json')[self._json_content_mode]
        print "Logging-in to " + self._entry_point + " (content mode: " + content_mode_string + ")..."
        
        login_url = self._entry_point + '/oauth/token'        
        accept_type = 'application/vnd.imgtec.com.oauthtoken+' + content_mode_string
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Accept': accept_type}        
        body = 'grant_type=password&username=' + self._key + '&password=' + self._secret
        current_datetime = time()
        response = requests.post(login_url, data=body, headers=headers, timeout=(timeout, self._default_timeout_seconds)[timeout is None])        
        _last_response = response        
        
        # Parse response
        if response != None:
        
            # Check content type of response and invoke appropriate deserialiser
            response_content_type = response.headers['Content-Type']
            response_status_code = response.status_code            
            
            if 'xml' in response_content_type:
                response_object = objectify.fromstring(response.text)
                if hasattr(response_object, 'access_token'):
                    self._access_token = response_object.access_token
                if hasattr(response_object, 'token_type'):
                    self._access_token_type = response_object.token_type
                if hasattr(response_object, 'expires_in'):
                    self._access_token_expiry = current_datetime + int(response_object.expires_in)
                if hasattr(response_object, 'refresh_token'):
                    self._refresh_token = response_object.refresh_token

            else:
            #elif 'json' in response_content_type:
                response_object = json.loads(response.text)                
                if 'access_token' in response_object:
                    self._access_token = response_object['access_token']
                if 'token_type' in response_object:
                    self._access_token_type = response_object['token_type']
                if 'expires_in' in response_object:               
                    self._access_token_expiry = current_datetime + int(response_object['expires_in'])
                if 'refresh_token' in response_object:
                    self._refresh_token = response_object['refresh_token']
            
            return response_object

        else:
            print "Login failed"
            return None
    
    
    ###################################################################################################
    # Logout client
    ###################################################################################################
    def logout(self):
        self._last_response = None
        self._access_token = None
        self._access_token_type = None
        self._access_token_expiry = None
        self._refresh_token = None
    
    
    ###################################################################################################
    # Get Web Service Entry Point
    ###################################################################################################
    def get_entry_point(self, timeout=None):
        if self._entry_point is None:
            raise NoneType
        
        # Get entry point    
        url = self._entry_point
        print 'HTTP GET ' + url
        content_mode_string = ('xml', 'json')[self._json_content_mode]        
        accept_type = 'application/' + content_mode_string
        headers = {'Accept': accept_type}
        
        if self._access_token != None:
            headers['Authorization'] = 'Bearer ' + self._access_token
                
        current_datetime = time()
        response = requests.get(url, headers=headers, timeout=(timeout, self._default_timeout_seconds)[timeout is None])                
        _last_response = response
                
        # Parse response
        response_object = None
        if response != None:
        
            # Check content type of response and invoke appropriate deserialiser
            response_content_type = response.headers['Content-Type']
            response_status_code = response.status_code        

            if 'xml' in response_content_type:
                response_object = objectify.fromstring(response.text)
            else:
            #elif 'json' in response_content_type:
                response_object = json.loads(response.text)                

        return response_object
 
 
    ###################################################################################################
    # Find Link
    ###################################################################################################
    def find_link(self, response_object=None, rel=None):
        if response_object is None:
            raise NoneType        
        if rel is None:
            raise NoneType

        result = None
        for index in range(0, len(response_object['Links'])):
            if response_object['Links'][index]['rel'] == rel:
                result = response_object['Links'][index] 
      
        return result
 
    
    ###################################################################################################
    # Get request
    ###################################################################################################
    def get(self, url, start_index=None, page_size=None, timeout=None):
        
        if self._entry_point is None:
            raise NoneType
        if url is None:
            raise NoneType
        if start_index is None:
            start_index = self._default_start_index
        if page_size is None:
            page_size = self._default_page_size
        
        # Append pageSize and startIndex query parameters to URL to support paging
        if '?' in url:
            url = url + '&'
        else:
            url = url + '?'            
        url = url + 'pageSize=' + str(page_size) + '&startIndex=' + str(start_index)
        
        print 'HTTP GET ' + url
        content_mode_string = ('xml', 'json')[self._json_content_mode]        
        accept_type = 'application/' + content_mode_string
        headers = {'Accept': accept_type}
        
        if self._access_token != None:
            headers['Authorization'] = 'Bearer ' + self._access_token

        current_datetime = time()
        response = requests.get(url, headers=headers, timeout=(timeout, self._default_timeout_seconds)[timeout is None])                
        _last_response = response        
        
        # Parse response
        response_object = None
        if response != None:
        
            # Check content type of response and invoke appropriate deserialiser
            response_content_type = response.headers['Content-Type']
            response_status_code = response.status_code        

            if 'xml' in response_content_type:
                response_object = objectify.fromstring(response.text)
            else:
            #elif 'json' in response_content_type:
                response_object = json.loads(response.text)                

        return response_object 
    
    
    ###################################################################################################
    # Get request (pages and retrieves all items)
    ###################################################################################################
    def get_all(self, url, timeout=None):

        if self._entry_point is None:
            raise NoneType
        if url is None:
            raise NoneType

        itemsReceived = 0
        response = self.get(url, 0, self._default_page_size, timeout)
        last_response = response        

        if last_response is not None:
            totalCount = last_response['PageInfo']['TotalCount']
            if totalCount > 0:
                while itemsReceived < totalCount:
                    itemsCount = last_response['PageInfo']['ItemsCount']                    
                    response['PageInfo']['ItemsCount'] += itemsCount
                    response['Items'].append(last_response['Items'])
                    itemsReceived += itemsCount

                    if itemsReceived >= totalCount:
                        response['PageInfo']['ItemsCount'] = itemsReceived
                        if 'next' in response['Links']:
                            response['Links'].remove('next')
                        if 'last' in response['Links']:
                            response['Links'].remove('last')
                    else:                    
                        last_response = self.get(url, itemsReceived, self._default_page_size, timeout)

        return response


    ###################################################################################################
    # POST Request
    ###################################################################################################
    def post(self, url, body=None, content_type=None, timeout=None):
        
        if self._entry_point is None:
            raise NoneType
        if url is None:
            raise NoneType
        
        # Post request
        print 'HTTP POST ' + url
        
        content_mode_string = ('xml', 'json')[self._json_content_mode]
        
        if content_type != None:
            content_type_string = content_type
        else:  
            content_type_string = 'application/' + content_mode_string        
        
        accept_type = 'application/' + content_mode_string   
        headers = {'Content-Type': content_type_string, 'Accept': accept_type}
        
        if self._access_token != None:
            headers['Authorization'] = 'Bearer ' + self._access_token
        
        current_datetime = time()
        response = requests.post(url, headers=headers, data=body, timeout=(timeout, self._default_timeout_seconds)[timeout is None])                
        _last_response = response
                
        # Parse response
        response_object = None
        if response != None:
        
            # Check content type of response and invoke appropriate deserialiser
            response_content_type = response.headers['Content-Type']
            response_status_code = response.status_code        
                       
            if 'xml' in response_content_type:
                response_object = objectify.fromstring(response.text)
            else:
            #elif 'json' in response_content_type:
                response_object = json.loads(response.text)                

        return response_object
    
    
    
    ###################################################################################################
    # POST Request (post a Python object)
    ###################################################################################################
    def post_object(self, url, object=None, root_element_name=None, content_type=None, timeout=None):
        if object is None:
            raise NoneType

        body = None
        
        if self._json_content_mode:
            body = json.dumps(object.__dict__)
        else:
                       
            body = dicttoxml(object.__dict__, custom_root=(root_element_name, 'Object')[root_element_name is None], attr_type=False)
            body = body[39:]   # Remove xml prologue string (first 39-chars)

        return self.post(url, body, content_type, timeout)



    ###################################################################################################
    # PUT Request
    ###################################################################################################   
    def put(self, url, body=None, content_type=None, timeout=None):
        
        if self._entry_point is None:
            raise NoneType
        if url is None:
            raise NoneType
        
        # Post request
        print 'HTTP POST ' + url
        
        content_mode_string = ('xml', 'json')[self._json_content_mode]
        
        if content_type != None:
            content_type_string = content_type
        else:  
            content_type_string = 'application/' + content_mode_string        
        
        accept_type = 'application/' + content_mode_string   
        headers = {'Content-Type': content_type_string, 'Accept': accept_type}
        
        if self._access_token != None:
            headers['Authorization'] = 'Bearer ' + self._access_token
        
        current_datetime = time()
        response = requests.put(url, headers=headers, data=body, timeout=(timeout, self._default_timeout_seconds)[timeout is None])                
        _last_response = response
                
        # Parse response
        response_object = None
        if response != None:
        
            # Check content type of response and invoke appropriate deserialiser
            response_content_type = response.headers['Content-Type']
            response_status_code = response.status_code        
                       
            if 'xml' in response_content_type:
                response_object = objectify.fromstring(response.text)
            else:
            #elif 'json' in response_content_type:
                response_object = json.loads(response.text)                

        return response_object
    
    
       

    ###################################################################################################
    # PUT Request (put a Python object)
    ###################################################################################################    
    def put_object(self, url, object=None, root_element_name=None, content_type=None, timeout=None):
        if object is None:
            raise NoneType

        body = None
        
        if self._json_content_mode:
            body = json.dumps(object.__dict__)
        else:
                       
            body = dicttoxml(object.__dict__, custom_root=(root_element_name, 'Object')[root_element_name is None], attr_type=False)
            body = body[39:]   # Remove xml prologue string (first 39-chars)

        return self.put(url, body, content_type, timeout)
    
    
    ###################################################################################################
    # DELETE Request
    ###################################################################################################    
    def delete(self, url, body=None, content_type=None, timeout=None):
        
        if self._entry_point is None:
            raise NoneType
        if url is None:
            raise NoneType
        
        # Post request
        print 'HTTP POST ' + url
        
        content_mode_string = ('xml', 'json')[self._json_content_mode]
        
        if content_type != None:
            content_type_string = content_type
        else:  
            content_type_string = 'application/' + content_mode_string        
        
        accept_type = 'application/' + content_mode_string   
        headers = {'Content-Type': content_type_string, 'Accept': accept_type}
        
        if self._access_token != None:
            headers['Authorization'] = 'Bearer ' + self._access_token
        
        current_datetime = time()
        response = requests.put(url, headers=headers, data=body, timeout=(timeout, self._default_timeout_seconds)[timeout is None])                
        _last_response = response
                
        # Parse response
        response_object = None
        if response != None:
        
            # Check content type of response and invoke appropriate deserialiser
            response_content_type = response.headers['Content-Type']
            response_status_code = response.status_code        
                       
            if 'xml' in response_content_type:
                response_object = objectify.fromstring(response.text)
            else:
            #elif 'json' in response_content_type:
                response_object = json.loads(response.text)                

        return response_object
    

    ###################################################################################################
    # Client configuration
    ###################################################################################################

    def set_content_mode_JSON(self):
        self._json_content_mode = True
        
    def set_content_mode_XML(self):
        self._json_content_mode = False

    def set_credentials(self, key, secret):
        self._key = key
        self._secret = secret

    def get_entry_point_URL(self):
        return self._entry_point

    def set_default_timeout(self, timeout):
        self._default_timeout_seconds = timeout
