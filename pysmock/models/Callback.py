from yaml import YAMLObject
from typing import Dict
from . import Request
class Callback(YAMLObject):
    yaml_tag = u'callback'

    def __init__(self, url: str, delay: int , request: Request):
        self.url = url
        self.delay = delay
        self.request = request