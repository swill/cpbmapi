CPBM BSS API Wrapper
====================

This project is a minimalist wrapper around the CPBM BSS API.  Its
purpose is to provide a CPBM BSS library that works independent of the CPBM version.
Instead of having function stubs for all of the CPBM BSS features, this lib is used
in conjunction with the CPBM BSS API documentation and the `request` function takes
the JSON values needed for each call.

There are two ways in which this lib can be consumed:

1. The `API` class can be instantiated from any code.  It has a single `request`
 method, which is used to make API calls against the CPBM BSS API.  This method 
 takes a python dictionary of request parameters and returns a python dictionary 
 with the result.

2. The `CLI` class is a subclass of `API` and is designed to be a convenience
 class for working with stand alone scripts that populate the `API` constructor
 using command line arguments parsed by `docopt`.  The command line arguments can be
 passed in directly or they can be added to a JSON file and the `--json` flag can
 be used to reference the JSON file path. A `cli_example.py` file is included in
 the package to give a working example of how to use this use case.

The core of this library is a single `request` method which is described as follows.

``` python
api.request(self, rest_path, params={}, payload={}, method='GET')
```

``` sphinx
Builds the request and returns a python dictionary of the result or None.

:param rest_path: appended to the 'endpoint'.  remember to include the leading '/'
:type rest_path: str or unicode

:param params: the query parameters to be added to the url
:type params: dict

:param payload: the object to be passed to the server (may not work as expected 
                due to non standard bss api implementation)
:type payload: dict

:param method: the request method [ GET | POST | PUT | DELETE ]
:type method: str or unicode

:returns: the result of the request as a python dictionary
:rtype: dict or None
```

**An example using the parent `API` class:**

``` python
from cpbmapi import API
api = API(api_key="your_api_key",
          secret_key="your_secred_key",
          endpoint="http://127.0.0.1:8080/portal/api")
accounts = api.request('/accounts')
```

**An example using the `CLI` sub-class:**

``` python
from cpbmapi import CLI
api = CLI(__doc__)
accounts = api.request('/accounts')
```


INSTALL
=======
The easiest way to install this library is through `pip`.

``` bash
$ pip install cpbmapi
```

Alternatively, you can pull down the source code directly and install manually.

``` bash
$ git clone https://github.com/swill/cpbmapi.git
$ cd cpbmapi
$ python setup.py install
```


USAGE
=====

The core functionality is documented above, but it is worth spending a minute
to better describe the `CLI` use case. 

``` bash
$ ./cli_example.py --help

Usage:
  cli_example.py [--json=<arg>] [--api_key=<arg> --secret_key=<arg>] [options]
  cli_example.py (-h | --help)

Options:
  -h --help             Show this screen.
  --json=<arg>          Path to a JSON config file with the same names as the 
                          options (without the -- in front).
  --api_key=<arg>       CPBM Api Key.
  --secret_key=<arg>    CPBM Secret Key.
  --endpoint=<arg>      CPBM Endpoint 
                          [default: http://127.0.0.1:8080/portal/api].
  --logging=<arg>       Boolean to turn on or off logging [default: True].
  --log=<arg>           The log file to be used [default: logs/cpbmapi.log].
  --clear_log=<arg>     Removes the log each time the API object is created 
                          [default: True].
```
