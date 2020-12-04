# NordVPN Server API Filter (Python)
GIT Hub: https://github.com/kylek29/python_nordvpn_server_filter/

A w.i.p. filter for the NordVPN API server list. Allows you to filter based on country and select feature sets. Not modulized at the moment.

Further credit to various online help repositories and other examples for
the NordVPN API endpoint.


**Version 0.1:**
This is a preliminary version made over time, needs to be cleaned up. But uploading to GITHUB since it works and other users may get value as a reference or jumping off point.


**Requirements:**
Built with Python 3.8.5, your mileable may vary with other versions.


## Setup
1. To use, copy the entire script, including the imports.
2. If you want to use the proxy URL creator, you likely will need to add your NordVPN credentials. These are stored as strings in the object.usr and object.pw attributes.


## Usage
1) Create a NordVPN (class) object. When ran, this will go out and retrieve the server list from the NordVPN Server list API.

`proxy = NordAPI()`

2) With the NordVPN object, you can now do various filtering against it.

Access the available servers with obj.proxies:

`proxy.proxies`

Outputs a dict with the key as the server-ID and the value as a NordServer class object (for organizational purposes).



Example Output:
```
{...
959381: <__main__.NordServer at 0x226540994f0>,
959384: <__main__.NordServer at 0x22654099520>,
959387: <__main__.NordServer at 0x22654099550>,
959390: <__main__.NordServer at 0x22654099580>,
 ...}
```


### To access a single proxy server and the available characteristics:

| Method      | Output Type | Output Example | Description |
| ----------- | ----------- | ----------- | ----------- |
| proxy.get_server( *id int* )      | obj |<__main__.NordServer at 0x22654099550>     | Returns a NordServer class object. |
| proxy.get_server( *id int* ).id   | int |  959387        | Selected server ID |
| proxy.get_server( *id int* ).ip   | str | 180.149.231.147    | Selected servers IPv4 address. |
| proxy.get_server( *id int* ).name | str | New Zealand #67 | Selected servers friendly name. |
| proxy.get_server( *id int* ).flag | str | NZ | Selected servers flag code. |
| proxy.get_server( *id int* ).socks | bool | False | Feature support for Socks5 | 
| proxy.get_server( *id int* ).proxy | bool | False | Feature support for Proxy (HTTP) | 
| proxy.get_server( *id int* ).proxy_ssl | bool | True | Feature support for Proxy SSL (HTTPS) | 
| proxy.get_server( *id int* ).p2p | bool | False | Feature support for P2P | 



### Filter on country:

Get the available flag codes:

`proxy.filter_country()`

Prints a list of the countries found and the available flag codes as *Country Name*  --> *FL*.

```
Thailand --> TH
Turkey --> TR
Ukraine --> UA
United Arab Emirates --> AE
United Kingdom --> GB
United States --> US
Vietnam --> VN
```


A single country (by flag-code), pass in a single flag code string:

`proxy.filter_country( 'NZ' )`

Multiple Countries, pass in a list of flag code strings:

`proxy.filter_country( ['NZ', 'US', 'CA'] )`

Returns a set() of server IDs.

```
{...
 971015,
 962825,
 971018,
 ...}
```

### Filter by feature, available options: proxy, proxy_ssl, socks:

`proxy.filter_feature('proxy')`

Returns a set() of servers that support that feature.

### To multi-filter:

You can combine filters to return a set() of server ID's that match the given parameters. Do this by passing in an existing filtered set() of server ID's to another filter, examples:

### Filter on countries US, CA & features 'socks':

```
filtered = proxy.filter_country( ['US', 'CA'], proxies = proxy.filter_feature('socks'))
```

.. or by using the filter_by_many( [list of filter strings] ) method. Acceptable features are 'socks', 'proxy', 'proxy_ssl', 'p2p'.

`proxy.filter_by_many( ['p2p', 'socks'] )`

You can also pass in a set of country filtered proxies to further narrow your search:

```
_country = proxy.filter_country( ['US', 'CA', 'GB'] )
filtered = proxy.filter_by_many( ['p2p', 'socks'], proxies = _country)
```
