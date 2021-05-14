from yaml import YAMLObject
from . import APIRequest, Info
from typing import List
class MockSetup:
  def __init__(self, info: Info = None, host: str = "http://localhost:5757", basePath: str ="/", apiRequests: List[object] = []):
    self.info = info
    self.host = host
    self.basePath = basePath
    self.apiRequests = apiRequests
  
  def __repr__(self):
    return str({'info':self.info, 'host':self.host,'basePath':self.basePath, 'apiRequests':self.apiRequests})