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
            methodValue = list(apiRequest.keys())[0]
            method = RequestMethod(methodValue)
            url=apiRequest[methodValue]['url']
            request_generic_fields = GenericFieldParser.find_generic_fields(apiRequest[methodValue]['request']['body'], prefix="request")
            response_generic_fields =GenericFieldParser.find_generic_fields(apiRequest[methodValue]['response']['json'], prefix="response")
            print('Generic Fields \n\tReq- {}\n\tRes- {}'.format(request_generic_fields, response_generic_fields))
            request = Request(url=url, headers=apiRequest[methodValue]['request']['headers'], body=apiRequest[methodValue]['request']['body'], generic_fields=request_generic_fields)
            response = Response(status_code=apiRequest[methodValue]['response']['status_code'],json=apiRequest[methodValue]['response']['json'], generic_fields=response_generic_fields)
            api_req = APIRequest(method=method,request=request, response=response)
            # print(api_req)
            mockSetup.apiRequests.append(api_req)
    return mockSetup