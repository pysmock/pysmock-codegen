from yaml import YAMLObject
from . import Contact, License
class Info(YAMLObject):
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
