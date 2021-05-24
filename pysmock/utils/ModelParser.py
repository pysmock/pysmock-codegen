from pysmock.logger import logger
from pysmock.models.MockSetup import MockSetup
from pysmock.models.Info import Info
from pysmock.models.Request import Request
from pysmock.models.Response import Response
from pysmock.models.APIRequest import APIRequest
from pysmock.models.APIRequest import RequestMethod
from pysmock.models.Param import Param
from pysmock.models.RequestParams import RequestParams
from pysmock.models.Callback import Callback
from .GenericFieldParser import GenericFieldParser
log = logger.get_logger(__name__)
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
            authorization_headers={}
            methodValue = list(apiRequest.keys())[0]
            method = RequestMethod(methodValue)
            request = apiRequest[methodValue]['request']
            response = apiRequest[methodValue]['response']

            if 'authorization' in apiRequest[methodValue].keys() and apiRequest[methodValue]['authorization'] is not None:
                authorization_headers = apiRequest[methodValue]['authorization']

            url=apiRequest[methodValue]['url']
            request_body = None
            path_params=[]
            query_params=[]
            response_body = None
            request_headers= None
            response_headers = None 
            if request is not None and 'headers' in request.keys() and request['headers'] is not None:
                request_headers = apiRequest[methodValue]['request']['headers']
            # print('Type is {} values {}'.format(type(apiRequest[methodValue]['request']),apiRequest[methodValue]['request'].keys()))
            if request is not None and 'body' in request.keys() and request['body'] is not None:
                request_generic_fields = GenericFieldParser.find_generic_fields(request['body'], prefix="request")
                request_body = request['body']
            requestParams = None
            if request is not None and 'param' in request.keys() and request['param'] is not None:
                param = request['param']
                path_parameters={}
                if 'path' in param.keys():
                    path_parameters={key:value for key,value in request['param']['path'].items()}
                    log.info('Path Params are: {}'.format(path_params))

                    # for key,value in path_params.items():
                    #     path_parameters.append(Param(key,value))
                elif 'query' in param.keys():
                    pass
                requestParams = RequestParams(path=path_parameters, query={})
            if response is not None and 'headers' in response.keys() and response['headers'] is not None:
                response_headers = apiRequest[methodValue]['response']['headers']
            if response is not None and  response['json'] is not None:
                response_generic_fields =GenericFieldParser.find_generic_fields(response['json'], prefix="response")
                response_body = response['json']
            callback=None
            if response is not None and 'callback' in response.keys() and response['callback'] is not None:
                callback_url = response['callback']['url']
                delay = response['callback']['delay']
                callback_request = response['callback']['request']
                headers = callback_request['headers']
                body = callback_request['body']
                callback_request_generic_fields = GenericFieldParser.find_generic_fields(body,'crequest')
                callback_request_obj = Request(url=callback_url, headers=headers, body=body, generic_fields=callback_request_generic_fields)
                callback=Callback(url = callback_url, delay=delay, request=callback_request_obj)
            log.debug('Generic Fields \n\tReq- {}\n\tRes- {}'.format(request_generic_fields, response_generic_fields))
            request = Request(url=url, headers=request_headers, body=request_body, generic_fields=request_generic_fields, params=requestParams)
            response = Response(status_code=response['status_code'],headers=response_headers,json=response_body, generic_fields=response_generic_fields, callback=callback)
            api_req = APIRequest(method=method,request=request, response=response, authorization=authorization_headers)
            # print(api_req)
            mockSetup.apiRequests.append(api_req)
    return mockSetup