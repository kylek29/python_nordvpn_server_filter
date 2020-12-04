# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 08:30:08 2020

@author: Kyle Kimsey

Further credit to various online help repositories and other examples for
the NordVPN API endpoint.


Version 0.1:
    - This is a preliminary version made over time, needs to be cleaned up. But
    uploading to GITHUB since it works and other users may get value as a 
    reference or jumping off point.
    
    
Requirements:
    - Built with Python 3.8.5, your mileable may vary with other versions.
    
"""

from urllib.request import urlopen
import json


class NordAPI:
    ''' Retrieves the NordVPN server list and then populates various lists for quick lookup. 
    
    Usage:
        Create NordAPI() object. Access the available servers with obj.proxies or filter
        by country with obj.filter_country('US') or feature_type with 
        obj.filter_feature('proxy'). Multi-filtering available, see example and 
        filter_country / filter_feature functions below.
    
    Example:
        Multi-Filtering on retrieved list:
            x = a.filter_country( ['US', 'CA', 'UK'], proxies = a.filter_feature('socks'))
            
        Retrieve server information.
            object.get_server(*id*).ip --> Returns the IP address of server with *ID*
    
    '''
    
    
    def __init__(self):
        self.nord_api_json = "https://nordvpn.com/api/server"
        self._proxies = self._get_list()
        self.proxies = self._process_list()
        self.usr = ''
        self.pw = ''
        self.port = 1080
        
    
    def _get_list(self):
        # Retrieves the list from the API       
        response = urlopen(self.nord_api_json)
        data = response.read().decode("utf-8")
        return json.loads(data)
    
    def _process_list(self):
        # Processes the server list to a dict of individual NordServer() class objects.       
        _d = dict()
        
        for p in self._proxies:
            _d[p['id']] = NordServer()
            _d[p['id']].id = p['id']
            _d[p['id']].ip = p['ip_address']
            _d[p['id']].name = p['name']
            _d[p['id']].flag = p['flag']
            _d[p['id']].country = p['country']
            _d[p['id']].features_dict = p['features']
            _d[p['id']].keywords = p['search_keywords']
                    
            for feature, enabled in _d[p['id']].features_dict.items():
                if enabled:
                    _d[p['id']].features.append(feature)
            
        return _d
    
    
    def get_server(self, id):
        # Given an ID-int of a server in the self.proxies list, it'll return the proxy object.
        return self.proxies[id]
    
    def get_server_tuple(self, id):
        '''
        Given an ID-int of a server in the self.proxies list, it'll return a tuple
        representation of the proxy object.
        
        Returns
        -------
        tuple : Tuple ( ID[int], UsrPwd@IP:Port[str] ) 
        '''
        return (self.proxies[id].id, f'socks5h://{self.usr}:{self.pw}@{self.proxies[id].ip}:{self.port}')
    
    
    def filter_country(self, country = None, proxies = None):
        """
        Take in a single country flag code or list of flag codes, filter the 
        proxy list by flag(s) and return it as a set of proxy ID's. If symbol 
        not found, return a list of found symbols.
        
        If an optional proxies set is passed in, it will filter and return
        that set. Useful for subfiltering.
        
        Parameters
        ----------
        country : str or list
        proxies : set
    
        Returns
        -------
        set : Set of proxy objects.
        """
        if type(proxies) == set:
            try:
                _proxies = {self.proxies[p].id for p in proxies}
            except:
                print('Proxy not found')
                return None
        else:
            _proxies = self.proxies
            
        _servers = set()
                
        if country:
            if type(country) == str:
                for server in _proxies:
                    if self.proxies[server].flag.upper() == country.upper():
                        _servers.add(self.proxies[server].id)  
                        
            elif type(country) == list:
                for c in country:
                    for server in _proxies:
                        if self.proxies[server].flag.upper() == c.upper():
                            _servers.add(self.proxies[server].id) 
                            
        if len(_servers) == 0:
            _ = dict()
            for server in self.proxies:   
                _[self.proxies[server].country] = self.proxies[server].flag 
            
            _ = {s:_[s] for s in sorted(_)}
            print('No valid country given, available options:')
            for c, f in _.items():
                print(f'{c} --> {f}')
                         
        return _servers
    
    
    def filter_feature(self, feature_type = '', proxies = None):
        """
        Take in a single feature type, filter the proxy list by features 
        equaling true and return it as a set of proxy ID's. If symbol not 
        found, return a list of found symbols.
        
        If an optional proxies set is passed in, it will filter and return
        that set. Useful for subfiltering.
        
        Parameters
        ----------
        feature_type : str
        proxies : set
    
        Returns
        -------
        set
        """
        if type(proxies) == set:
            try:
                _proxies = {self.proxies[p].id for p in proxies}
            except:
                print('Proxy not found')
                return None
        else:
            _proxies = self.proxies
                 

        if feature_type.lower() == 'proxy_ssl':        
            return {self.proxies[s].id for s in _proxies if self.proxies[s].proxy_ssl}
        elif feature_type.lower() == 'proxy':      
            return {self.proxies[s].id for s in _proxies if self.proxies[s].proxy}
        elif feature_type.lower() == 'socks':
            return {self.proxies[s].id for s in _proxies if self.proxies[s].socks}
        elif feature_type.lower() == 'p2p':
            return {self.proxies[s].id for s in _proxies if self.proxies[s].p2p}
        else:
            print('Feature not found.')
            

    def filter_by_many(self, features = None, proxies = None):
        """

        WORK IN PROGRESS

        """           
        _proxies = proxies or {self.proxies[p].id for p in self.proxies}      
        _servers = [self.filter_feature(f) for f in features]            
        return _proxies.intersection(*_servers)

        
        
        

class NordServer:
    '''
    Helper Class for individual servers.
    '''
    
    def __init__(self):
        self.id = ''
        self.ip = ''
        self.name = ''
        self.flag = ''
        self.keywords = ''
        self.features_dict = dict()
        self.features = list()

    @property
    def proxy(self):
        if 'proxy' in self.features: return True
        
    @property
    def proxy_ssl(self):
        if 'proxy_ssl' in self.features: return True
        
    @property
    def socks(self):
        if 'socks' in self.features: return True
        
    @property
    def p2p(self):
        if 'P2P' in self.keywords: return True
        
        
