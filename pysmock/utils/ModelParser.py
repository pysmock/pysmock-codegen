from pysmock.models.MockSetup import MockSetup
from pysmock.models.Info import Info
from pysmock.models.Request import Request
from pysmock.models.Response import Response
from pysmock.models.APIRequest import APIRequest
from pysmock.models.APIRequest import RequestMethod
from .GenericFieldParser import GenericFieldParser
class ModelParser:

  @staticmethod
  def parseToObject(yaml_dict):
    mockSetup = MockSetup()
    if "info" in yaml_dict.keys():
        info_dict=yaml_dict['info']
        info=Info()
        info_keys=info_dict.keys()
        if "name" in info_keys:
            info.name=info_dict['name']
        if "description" in info_keys:
            info.description=info_dict['description']
        if "title" in info_keys:
            info.title=info_dict['title']
        if "version" in info_keys:
            info.version=info_dict['version']
        mockSetup.info = info
    if "host" in yaml_dict.keys():
      mockSetup.host = yaml_dict['host']
    if "basePath" in yaml_dict.keys():
        mockSetup.basePath = yaml_dict['basePath']
    if "apiRequests" in yaml_dict.keys():
        mockSetup.apiRequests = []
        for apiRequest in yaml_dict['apiRequests']:
            request_generic_fields=[]
            response_generic_fields=[]
            methodValue = list(apiRequest.keys())[0]
            method = RequestMethod(methodValue)
            url=apiRequest[methodValue]['url']
            request_body = None
            response_body = None
            request_headers= None
            response_headers = None 
            if apiRequest[methodValue]['request'] is not None and 'headers' in apiRequest[methodValue]['request'].keys() and apiRequest[methodValue]['request']['headers'] is not None:
                request_headers = apiRequest[methodValue]['request']['headers']
            # print('Type is {} values {}'.format(type(apiRequest[methodValue]['request']),apiRequest[methodValue]['request'].keys()))
            if apiRequest[methodValue]['request'] is not None and 'body' in apiRequest[methodValue]['request'].keys() and apiRequest[methodValue]['request']['body'] is not None:
                request_generic_fields = GenericFieldParser.find_generic_fields(apiRequest[methodValue]['request']['body'], prefix="request")
                request_body = apiRequest[methodValue]['request']['body']
            if apiRequest[methodValue]['response'] is not None and 'headers' in apiRequest[methodValue]['response'].keys() and apiRequest[methodValue]['response']['headers'] is not None:
                response_headers = apiRequest[methodValue]['response']['headers']
            if apiRequest[methodValue]['response'] is not None and  apiRequest[methodValue]['response']['json'] is not None:
                response_generic_fields =GenericFieldParser.find_generic_fields(apiRequest[methodValue]['response']['json'], prefix="response")
                response_body = apiRequest[methodValue]['response']['json']
            # print('Generic Fields \n\tReq- {}\n\tRes- {}'.format(request_generic_fields, response_generic_fields))
            request = Request(url=url, headers=request_headers, body=request_body, generic_fields=request_generic_fields)
            response = Response(status_code=response_headers,json=response_body, generic_fields=response_generic_fields)
            api_req = APIRequest(method=method,request=request, response=response)
            # print(api_req)
            mockSetup.apiRequests.append(api_req)
    return mockSetup