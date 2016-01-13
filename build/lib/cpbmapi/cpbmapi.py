#!/usr/bin/env python

# Author: Will Stevens (CloudOps) - wstevens@cloudops.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
import hmac
import hashlib
import json
import logging as _logging
import os
import pprint
import requests
import time
import urllib

class API(object):
    """
    Instantiate this class with the requred arguments, then use the 'request' method to make calls to the CPBM BSS API.

    api = API(**args)
    accounts = api.request('/accounts')
    """
    def __init__(
            self,
            api_key,
            secret_key,
            endpoint="http://127.0.0.1:8080/portal/api",
            logging=False,
            log="",
            clear_log=False):

        self.api_key = api_key
        self.secret_key = secret_key
        self.endpoint = endpoint
        self.logging = logging
        self.log = log
        self.log_dir = os.path.dirname(self.log)
        self.clear_log = clear_log

        if self.logging:
            if self.log_dir and not os.path.exists(self.log_dir):
                os.makedirs(self.log_dir)

            if self.clear_log and os.path.exists(self.log):
                open(self.log, 'w').close()

            _logging.basicConfig(
                filename=self.log,
                level=_logging.DEBUG,
                format='%(asctime)s %(message)s',
                datefmt='%d-%m-%Y %I:%M:%S %p' 
            )

            self.logger = _logging.getLogger(__name__)

        
    def request(self, rest_path, params={}, payload={}, method='GET'):
        """
        Builds the request and returns a python dictionary of the result or None.
        If 'payload' is specified, the request will be a POST, otherwise it will be a GET.  Review the 'method' argument for other actions.

        :param rest_path: appended to the 'endpoint'.  remember to include the leading '/'
        :type rest_path: str or unicode

        :param params: the query parameters to be added to the url
        :type params: dict

        :param payload: the object to be passed to the server (may not work as expected due to non standard bss api implementation)
        :type payload: dict

        :param method: the request method [ GET | POST | PUT | DELETE ]
        :type method: str or unicode

        :returns: the result of the request as a python dictionary
        :rtype: dict or None
        """
        if self.api_key and self.secret_key:
            result = None
            params['_'] = str(int(round(time.time() * 1000)))
            params['apiKey'] = self.api_key

            # build the query string
            query_params = map(lambda (k,v):k+"="+urllib.quote_plus(str(v)), params.items())
            query_string = "&".join(query_params)

            # build signature
            query_params.sort()
            signature_string = rest_path+"&".join(query_params).lower()
            signature = urllib.quote(base64.b64encode(hmac.new(self.secret_key, signature_string, hashlib.sha1).digest()))

            url = self.endpoint+rest_path+'?'+query_string+'&signature='+signature

            if payload:
                response = requests.request(method.upper(), url, json=json.dumps(payload))
            else:
                response = requests.request(method.upper(), url)

            if response.ok:
                result = response.json()
            elif self.logging:
                self.logger.error(response.text)

            if self.logging:
                self.logger.info("%s %s" % (method.upper(), url))
                if payload:
                    self.logger.info(pprint.pformat(payload))
                if response.ok:
                    #self.logger.debug(pprint.pformat(response.headers))  # if you want to log the headers too...
                    self.logger.debug(pprint.pformat(result))
                else:
                    self.logger.info(response.text)
                self.logger.info('\n\n\n')

            return result
        else:
            print("ERROR: 'api_key' and 'secret_key' are required to use the api...")
            return None

