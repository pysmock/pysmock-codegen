from yaml import YAMLObject
from typing import Dict
from . import Callback
class Response(YAMLObject):
    yaml_tag = u'response'
    def __init__(self, status_code: int, headers: Dict[str,str]=None, json: Dict[str,object]=None, text: str =None,
          generic_fields: Dict[str, str]=None, callback: Callback = None):
        self.status_code = status_code
        self.json = json
        self.headers = headers
        self.text = text
        self.generic_fields = generic_fields
        self.callback = callback

    def __repr__(self):
        return str({'status_code':self.status_code, 'json':self.json,'headers':self.headers,'text':self.text, 'generic_fields':self.generic_fields})
