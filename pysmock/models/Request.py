from yaml import YAMLObject
from typing import Dict
class Request(YAMLObject):
    yaml_tag = u'request'
    def __init__(self, url: str, 
          headers: Dict[str,str]=None, 
          body: Dict[str, object]=None,
          generic_fields: Dict[str, str]=None):
        self.url = url
        self.headers = headers
        self.body=body
        self.generic_fields = generic_fields
    
    def __repr__(self):
        return str({'url':self.url, 'headers':self.headers,'body':self.body,'generic_fields':self.generic_fields})
