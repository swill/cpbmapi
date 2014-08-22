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

"""
Usage:
  cpbm_api.py (--api_key=<arg> --secret_key=<arg>) [options]
  cpbm_api.py (-h | --help)

Options:
  -h --help             Show this screen.
  --api_key=<arg>       CPBM Api Key.
  --secret_key=<arg>    CPBM Secret Key.
  --host=<arg>          CPBM IP or hostname (including port) [default: 127.0.0.1:8080].
  --protocol=<arg>      Protocol used to connect to CPBM (http | https) [default: http].
  --base_path=<arg>     Base CPBM Api path [default: /portal/api].
  --logging=<arg>       Boolean to turn on or off logging [default: True].
  --log=<arg>           The log file to be used [default: logs/cpbm_api.log].
  --clear_log=<arg>     Removes the log each time the API object is created [default: True].
"""

from docopt import docopt
import base64
import hmac
import hashlib
import json
import os
import pprint
import requests
import time
import urllib

args = docopt(__doc__)

class API(object):
    """
    Instantiate this class with the docops arguments, then use the 'request' method to make calls to the CPBM API.

    api = API(args)
    accounts = api.request('/accounts')
    """
    def __init__(self, args):
        self.api_key = args['--api_key']
        self.secret_key = args['--secret_key']
        self.host = args['--host']
        self.protocol = args['--protocol']
        self.base_path = args['--base_path']
        self.logging = True if args['--logging'].lower() == 'true' else False
        self.log = args['--log']
        self.log_dir = os.path.dirname(self.log)
        self.clear_log = True if args['--clear_log'].lower() == 'true' else False
        if self.log_dir and not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        if self.clear_log and os.path.exists(self.log):
            open(self.log, 'w').close()
        
    def request(self, rest_path, params={}, payload=None, method=None):
        """
        Builds the request and returns a python dictionary of the result or None.
        If 'payload' is specified, the request will be a POST, otherwise it will be a GET.  Review the 'method' argument for other actions.

        :param rest_path: appended to 'base_path' (defaults to '/portal/api'), eg: rest_path='/accounts' => '/portal/api/accounts'
        :type rest_path: str or unicode

        :param params: the query parameters to be added to the url
        :type params: dict

        :param payload: the object to be passed to the server
        :type payload: dict or None

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
            query_params = map(lambda (k,v):k+"="+urllib.quote(str(v)).replace('/', '%2F'), params.items())
            query_string = "&".join(query_params)

            # build signature
            query_params.sort()
            signature_string = rest_path+"&".join(query_params).lower()
            signature = urllib.quote(base64.b64encode(hmac.new(self.secret_key, signature_string, hashlib.sha1).digest()))

            url = self.protocol+'://'+self.host+self.base_path+rest_path+'?'+query_string+'&signature='+signature

            if payload:
                if method and method.upper() == 'PUT':
                    response = requests.put(url, data=json.dumps(payload)) # PUT
                else:
                    response = requests.post(url, data=json.dumps(payload)) # POST
            else:
                if method and method.upper() == 'DELETE':
                    response = requests.delete(url) # DELETE
                else:
                    response = requests.get(url) # GET

            if response.ok:
                result = response.json()
            else:
                print response.text
               
            if self.logging:
                with open(self.log, 'a') as f:
                    if payload:
                        f.write((method.upper() if method else "POST")+" "+url)
                        f.write('\n')
                        pprint.pprint(payload, f, 2)
                    else:
                        f.write((method.upper() if method else "GET")+" "+url)
                        f.write('\n')
                    f.write('\n')
                    if response.ok:
                        #pprint.pprint(response.headers, f, 2)  # if you want to log the headers too...
                        pprint.pprint(result, f, 2)
                    else:
                        f.write(response.text)
                        f.write('\n')
                    f.write('\n\n\n')
            return result
        else:
            print("ERROR: --api_key and --secret_key are required to use the api...")
            return None

            
if __name__ == '__main__':
    api = API(args) # call the constructor with the docopts arguments...

    pprint.pprint(api.request('/accounts'))

