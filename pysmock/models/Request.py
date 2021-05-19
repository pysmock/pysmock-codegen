from yaml import YAMLObject
from typing import Dict
from . import RequestParams
class Request(YAMLObject):
    yaml_tag = u'request'
    def __init__(self, url: str, 
          headers: Dict[str,str]=None, 
          body: Dict[str, object]=None,
          params: RequestParams = None,
          generic_fields: Dict[str, str]=None):
        self.url = url
        if headers is not None:
            self.headers = headers
        else:
            self.headers = []
        self.body=body
        self.params = params
        self.generic_fields = generic_fields
    
    def __repr__(self):
        return str({'url':self.url, 'headers':self.headers,'body':self.body,'generic_fields':self.generic_fields})
