from flask import Flask, flash, redirect, request, jsonify, make_response
import logging as logger
from deepdiff import DeepDiff
from threading import Thread
import json
import re
import requests
import time
logger.basicConfig(level=logger.DEBUG)
app=Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'

basePath="{{model.basePath}}"
from enum import IntEnum
class HttpStatus(IntEnum):
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    OK = 200

#utility functions

def check_headers(current_headers, headers_to_check):
    current_headers={k.lower():v for k,v in current_headers.items()}
    request_header_names=current_headers.keys()
    headers_to_check={k.lower():v for k,v in headers_to_check.items()}
    for key in headers_to_check.keys():
        if key not in request_header_names:
            errorMessage = "Headers missing [{}]".format(key)
            return jsonify(errorMessage), int(HttpStatus.BAD_REQUEST)
        elif headers_to_check[key] != current_headers[key]:
            errorMessage = "Headers do not match Expected[{}] got[{}]".format(headers_to_check[key],current_headers[key]) 
            return jsonify(errorMessage), int(HttpStatus.BAD_REQUEST)
    return None, None


def does_string_match_regex(regex_pattern="*", input_string=''):
    return bool(re.match(regex_pattern, input_string))

def get_field_value_by_placeholder(body={}, placeholder=""):
    found = False
    fields = placeholder.split('.')
    while not found and len(fields)!=0:
        field = fields.pop(0)
        if field not in body.keys():
            return None
        body=body[field]
    return body

def check_request_generic_fields(generic_fields={}, request_body={}):
    errors=[]
    for key,value in generic_fields.items():
        field_value = str(get_field_value_by_placeholder(request_body, key.replace('request.','')))
        if not does_string_match_regex(value, field_value):
            message={}
            message['fieldName']=key
            message['errorMessage']='{} does not match regex {}'.format(field_value, value)
            errors.append(message)
        else:
            # print('{} passed regex {}'.format(key,field_value))
            pass
    return errors

def compare_dicts(dict1={}, dict2={},exclude_paths=[]):
    errors = []
    comparison_summary=DeepDiff(dict1, dict2,ignore_order=True, exclude_paths=exclude_paths)
    if 'values_changed' in comparison_summary:
        for key in comparison_summary['values_changed'].keys():
            message={}
            key_str = key.replace('root','').replace('[\'','.').replace('\']','.').replace('..','.')[1:-1]
            message['fieldName']=key_str
            message['errorMessage']='EXPECTED: {} GOT: {}'.format(comparison_summary['values_changed'][key]['old_value'],comparison_summary['values_changed'][key]['new_value'])
            errors.append(message)
    return errors if len(errors) != 0 else None

def do_params_conform_regex(param_rules, actual_params):
    errors={}
    errors['param_mismatch']=[]
    for param_name in actual_params.keys():
        if not does_string_match_regex(param_rules[param_name], actual_params[param_name]):
            message={}
            message['paramName']=param_name
            message['errorMessage']="Value for {} = {} does not match regex {}".format(param_name, actual_params[param_name], param_rules[param_name])
            errors['param_mismatch'].append(message)
    return errors

def send_callback(url="localhost", headers={}, body={}, delay=0):
    time.sleep(delay)
    requests.post(url=url, headers=headers, data=body)

#APIs

@app.route(basePath+"/info", methods=['GET'])
def server_info():
    return jsonify({{model.info}}), int(HttpStatus.OK)

{% for  apiRequest in model.apiRequests %}
{% set hasPathParam = True if apiRequest.request.params is not none and apiRequest.request.params.path is not none else False%}
{% set params = [] %}
{% if hasPathParam %}
{% for param in apiRequest.request.params.path.keys() %}
    {% set test=params.append(param) %}
{% endfor %}
{% endif %}
@app.route(basePath+"/{{apiRequest.request.url}}", methods=["{{apiRequest.method.value}}"])
def api_request_{{loop.index}}({% if hasPathParam %}{{params|join(",")}}{% endif %}):
    current_headers=request.headers
    authorization_headers_to_check={}
    {% for header_name, value  in  apiRequest.authorization.items()  %}
    authorization_headers_to_check["{{header_name}}"]="{{value}}"
    {% endfor %}
    # logger.debug(current_headers)
    if len(authorization_headers_to_check.keys()) > 0:
        error, code = check_headers(current_headers, authorization_headers_to_check)
        if error is not None:
            return error, int(HttpStatus.UNAUTHORIZED)

    headers_to_check={{apiRequest.request.headers}}
    
    if len(headers_to_check) > 0:
        error, code = check_headers(current_headers, headers_to_check)
        if error is not None:
            return error, code

    {% if hasPathParam %}
    path_param_rules={{apiRequest.request.params.path}}
    actual_params={}
    {% for  param in params %}
    actual_params['{{param}}']={{param}}   
    {% endfor %}
    errors = do_params_conform_regex(path_param_rules,actual_params)
    if len(errors['param_mismatch']) != 0:
        return jsonify(errors), int(HttpStatus.BAD_REQUEST)
     
    {% endif %}
    requestBody = {{apiRequest.request.body}}
    request_generic_fields={{apiRequest.request.generic_fields}}
    actualBody = None
    print('Request body is {}'.format(request.data))
    if request.data is not None and request.data.decode() != '':
        actualBody = json.loads(request.data)
    errors={}
    errors['data_mismatch']={}
    # print(DeepDiff(requestBody, actualBody,ignore_order=True, exclude_paths=list(map(lambda x: 'root[\''+x.replace('request.','').replace('.','\'][\'')+'\']',list(request_generic_fields.keys())))))
    if requestBody is not None:
        errors['data_mismatch']['value']=compare_dicts(dict1=requestBody,dict2= actualBody, exclude_paths=list(map(lambda x: 'root[\''+x.replace('request.','').replace('.','\'][\'')+'\']',list(request_generic_fields.keys()))))
    if 'value' in errors['data_mismatch'].keys() and errors['data_mismatch']['value'] is not None and len(errors['data_mismatch']['value']) != 0:
        return jsonify(errors),int(HttpStatus.BAD_REQUEST)
    print(errors)
    if actualBody is not None:
        errors['data_mismatch']['regex']=check_request_generic_fields(generic_fields=request_generic_fields, request_body=actualBody)
    if requestBody is not None and actualBody is None:
        error['message']='missing request body'
        return jsonify(error), int(HttpStatus.BAD_REQUEST)
    print(errors)
    if 'regex' in errors['data_mismatch'].keys() and errors['data_mismatch']['regex'] is not None and len(errors['data_mismatch']['regex']) != 0:
        return jsonify(errors),int(HttpStatus.BAD_REQUEST)
    response_generic_fields={{apiRequest.response.generic_fields}}
    response_body={{apiRequest.response.json}}
    {% for  key, value in apiRequest.response.generic_fields.items() %}
        {% set display_str_key = key.replace('response.','').replace('.','\'][\'') %}
        {% set display_str_value = value.replace('$request.body.','').replace('.','\'][\'') %}
    response_body['{{display_str_key}}'] = actualBody['{{display_str_value}}']
    {% endfor %}
    response = jsonify(response_body)
    {% if apiRequest.response.headers is not none%}
    {% for header,value in apiRequest.response.headers.items() %}
    response.headers['{{header}}'] = '{{value}}'
    {% endfor %}
    {% endif %}

    {% if apiRequest.response.callback is not none %}
    callback_request_body={}
    {% set included_fields = [] %}
    {% set c_url = apiRequest.response.callback.url %}
    {% set c_delay = apiRequest.response.callback.delay %}
    {% set c_req = apiRequest.response.callback.request %}
    {% for key, value in c_req.generic_fields.items() %}
        {% set display_str_key = key.replace('crequest.','').replace('.','\'][\'') %}
        {% set display_str_value = value.replace('$request.body.','').replace('.','\'][\'') %}
    callback_request_body['{{display_str_key}}'] = actualBody['{{display_str_value}}']
        {% set test=included_fields.append(display_str_key) %}
    {% endfor %}
    {% for key,value in c_req.body.items() %}
        {% if key not in included_fields %}
    callback_request_body['{{key}}']='{{value}}'    
        {% endif %}
    {% endfor %}
    Thread(target=send_callback,kwargs={'url':actualBody["{{c_url.replace('$request.body.','').replace('.','\'][\'')}}"], 'headers': {{c_req.headers}}, 'body': callback_request_body,'delay':{{c_delay}}}).start()
    {% endif %}
    return response, {{apiRequest.response.status_code}}

{% endfor %}

if __name__ == '__main__':
    {% set host=model.host.split(':')[0] %}
    {% set port=model.host.split(':')[1] %}
    app.run(host="{{host}}", port=int("{{port}}"))