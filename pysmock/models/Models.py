import yaml
from typing import Optional, Dict, List
from enum import Enum
class RequestMethod(Enum):
  GET = 'get'
  PUT = 'put'
  POST = 'post'
  DELETE = 'delete'
  OPTIONS = 'options'
  HEAD = 'head'

class Contact(yaml.YAMLObject):
  yaml_tag = u'contact'
  def __init__(self,
              name: str = None,
              url: str = None,
              email: str = None):
    self.name = name
    self.url = url
    self.email = email

class License(yaml.YAMLObject):
  yaml_tag = u'license'
  def __init__(self, name: str="", url: str =""):
    self.name = name
    self.url = url

class Info(yaml.YAMLObject):
  yaml_tag = u'info'
  def __init__(self,name: str ="",title: str = "", description: str = "",termsOfService: str = "",
    contact: Contact = None, license: License = None, version: str = "1.0.0"):
    self.name = name
    self.title = title
    self.description = description
    self.termsOfService = termsOfService
    self.contact = contact
    self.license = license
    self.version = version

  def __repr__(self):
    return str({'name': self.name, 'title':self.title, 'description': self.description, 'termsOfService': self.termsOfService, 'contact':self.contact ,'license':self.license ,'version':self.version})

class Request(yaml.YAMLObject):
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



class Response(yaml.YAMLObject):
    yaml_tag = u'response'
    def __init__(self, status_code: int, headers: Dict[str,str]=None, json: Dict[str,object]=None, text: str =None,
          generic_fields: Dict[str, str]=None):
        self.status_code = status_code
        self.json = json
        self.headers = headers
        self.text = text
        self.generic_fields = generic_fields

    def __repr__(self):
        return str({'status_code':self.status_code, 'json':self.json,'headers':self.headers,'text':self.text, 'generic_fields':self.generic_fields})

class APIRequest(yaml.YAMLObject):
    yaml_tag = u'apiRequest'
    def __init__(self,method: RequestMethod, request: Request, response: Response):
        self.method = method
        self.request = request
        self.response = response

    def __repr__(self):
        return str({'method':self.method, 'request':self.request,'response':self.response})

class MockSetup:
  def __init__(self, info: Info = None, host: str = "http://localhost:5757", basePath: str ="/", apiRequests: List[APIRequest] = []):
    self.info = info
    self.host = host
    self.basePath = basePath
    self.apiRequests = apiRequests
  
  def __repr__(self):
    return str({'info':self.info, 'host':self.host,'basePath':self.basePath, 'apiRequests':self.apiRequests})