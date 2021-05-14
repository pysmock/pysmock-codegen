from yaml import YAMLObject
class Contact(YAMLObject):
  yaml_tag = u'contact'
  def __init__(self,
              name: str = None,
              url: str = None,
              email: str = None):
    self.name = name
    self.url = url
    self.email = email