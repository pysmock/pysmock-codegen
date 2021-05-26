__version__ = "0.1.2"
__author__ = 'Harsha Sridhar'
__author_email__='contact.pysmock@gmail.com'
__description__='A tool to generate a mock server from yaml file using python'
REQUEST_TYPE=['get','post','put','delete','head','options']
import pysmock.logger
import pysmock.utils
import pysmock.models
import pkg_resources
import yaml
pkg_resources.declare_namespace(__name__)
