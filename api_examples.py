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
  api_examples.py (--api_key=<arg> --secret_key=<arg>) [options]
  api_examples.py (-h | --help)

Options:
  -h --help             Show this screen.
  --api_key=<arg>       CPBM Api Key.
  --secret_key=<arg>    CPBM Secret Key.
  --endpoint=<arg>      CPBM Endpoint [default: http://127.0.0.1:8080/portal/api].
  --logging=<arg>       Boolean to turn on or off logging [default: True].
  --log=<arg>           The log file to be used [default: logs/cpbm_api.log].
  --clear_log=<arg>     Removes the log each time the API object is created [default: True].
"""

from docopt import docopt
from cpbm_api import API
import pprint

if __name__ == '__main__':
    args = docopt(__doc__) # get the command line arguments...
    api = API(args) # call the constructor with the docopt arguments...

    pprint.pprint(api.request('/accounts'))