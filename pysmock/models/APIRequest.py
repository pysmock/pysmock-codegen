from yaml import YAMLObject
from . import Request, Response
from enum import Enum
from typing import Dict
class RequestMethod(Enum):
  GET = 'get'
  PUT = 'put'
  POST = 'post'
  DELETE = 'delete'
  OPTIONS = 'options'
  HEAD = 'head'
class APIRequest(YAMLObject):
    yaml_tag = u'apiRequest'
    def __init__(self,method: RequestMethod, request: Request, response: Response, authorization: Dict[str, object]):
        self.method = method
        self.request = request
        self.response = response
        self.authorization = authorization

    def __repr__(self):
        return str({'method':self.method, 'request':self.request,'response':self.response})
