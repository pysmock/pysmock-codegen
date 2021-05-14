from yaml import YAMLObject
class License(YAMLObject):
  yaml_tag = u'license'
  def __init__(self, name: str="", url: str =""):
    self.name = name
    self.url = url