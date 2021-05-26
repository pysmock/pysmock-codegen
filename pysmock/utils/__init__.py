"""utility package
"""
from .GenericFieldParser import GenericFieldParser
from .ModelParser import ModelParser
# __all__=['GenericFieldParser','ModelParser']
import pkg_resources
pkg_resources.declare_namespace(__name__)