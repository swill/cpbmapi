CPBM API Wrapper
================
This project is a minimalist wrapper around the CPBM BSS API.  Its purpose is to expedite the process of testing the API and building scripts to do useful tasks.

This project exposes a single `API` class which has a single `request` method.  This method takes a BSS API call and returns a python dictionary with the result.

`request(self, rest_path, params={}, payload=None, method=None)`
----------------------------------------------------------------
``` sphinx
Builds the request and returns a python dictionary of the result or None.
If 'payload' is specified, the request will be a POST, otherwise it will be a GET. 
Review the 'method' argument for other actions.

:param rest_path: appended to 'base_path' (defaults to '/portal/api')
				  eg: rest_path='/accounts' => '/portal/api/accounts'
:type rest_path: str or unicode

:param params: the query parameters to be added to the url
:type params: dict

:param payload: the object to be passed to the server
:type payload: dict or None

:param method: the request method [ GET | POST | PUT | DELETE ]
:type method: str or unicode

:returns: the result of the request as a python dictionary
:rtype: dict or None
```


INSTALL
=======
This project does not need to be installed, it can be run in-place.  However, it does depend on a few libraries to keep things simple.

docops
------

``` bash
$ pip install docops
```

requests
--------

``` bash
$ pip install requests
```


USAGE
=====
The usage for this project is documented in the 'help' section of the scripts.

``` bash
$ ./cpbm_api.py --help
```

``` bash
$ ./api_examples.py --help
```

This project can be run as a stand alone script or the API object can be imported into other scripts in this directory as a library.

`cpbm_api.py` is a stand alone script which can be run on its own, as well as a basic library which can be imported into other scripts.

`api_examples.py` is an example of using the `cpbm_api.py` script as a library.  In this example, we  simply import the `API` object and start making requests.  This is ideal if you have multiple scripts that do different tasks and you want them to all exist at the same time.  Simply duplicate this file and change the api requests as needed.

