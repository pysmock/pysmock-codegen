from yaml import YAMLObject
from typing import List
class Param(YAMLObject):
    yaml_tag = u'param'
    def __init__(self,
    key: str,
    value: str):
        self.key = key
        self.value = value