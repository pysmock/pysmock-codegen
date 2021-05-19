from yaml import YAMLObject
from typing import Dict
from . import Param
class RequestParams(YAMLObject):
    yaml_tag = u'param'
    def __init__(self, 
        query: Dict[str, object] = {},
        path: Dict[str, object] = {}
        ):
        self.query = query
        self.path = path
        