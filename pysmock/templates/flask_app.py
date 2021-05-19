from flask import Flask, flash, redirect, request, jsonify, make_response
import logging as logger
from deepdiff import DeepDiff
import json
import re
logger.basicConfig(level=logger.DEBUG)
app=Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'

basePath="{{model.basePath}}"

#utility functions

def check_headers(current_headers, headers_to_check):
    current_headers={k.lower():v for k,v in current_headers.items()}
    request_header_names=current_headers.keys()
    headers_to_check={k.lower():v for k,v in headers_to_check.items()}
    for key in headers_to_check.keys():
        if key not in request_header_names:
            errorMessage = "Headers missing [{}]".format(key)
            return jsonify(errorMessage), 400
        elif headers_to_check[key] != current_headers[key]:
            errorMessage = "Headers do not match Expected[{}] got[{}]".format(headers_to_check[key],current_headers[key]) 
            return jsonify(errorMessage), 400
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

#APIs

@app.route(basePath+"/info", methods=['GET'])
def server_info():
    return jsonify({{model.info}}), 200

{% for  apiRequest in model.apiRequests %}
{% set hasPathParam = True if apiRequest.request.params is not none and apiRequest.request.params.path is not none else False%}
{% set params = [] %}
{% if hasPathParam %}
{% for param in apiRequest.request.params.path.keys() %}
    {{params.append(param)}}
{% endfor %}
{% endif %}
@app.route(basePath+"/{{apiRequest.request.url}}", methods=["{{apiRequest.method.value}}"])
def api_request_{{loop.index}}({% if hasPathParam %}{{params|join(",")}}{% endif %}):
    current_headers=request.headers
    # logger.debug(current_headers)
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
        return jsonify(errors), 400
     
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
        return jsonify(errors),400
    print(errors)
    if actualBody is not None:
        errors['data_mismatch']['regex']=check_request_generic_fields(generic_fields=request_generic_fields, request_body=actualBody)
    if requestBody is not None and actualBody is None:
        error['message']='missing request body'
        return jsonify(error), 400
    print(errors)
    if 'regex' in errors['data_mismatch'].keys() and errors['data_mismatch']['regex'] is not None and len(errors['data_mismatch']['regex']) != 0:
        return jsonify(errors),400
    response_generic_fields={{apiRequest.response.generic_fields}}
    response_body={{apiRequest.response.json}}
    {% for  key, value in apiRequest.response.generic_fields.items() %}
        {% set display_str_key = key.replace('response.','').replace('.','\'][\'') %}
        {% set display_str_value = value.replace('$request.body.','').replace('.','\'][\'') %}
    response_body['{{display_str_key}}'] = actualBody['{{display_str_value}}']
    {% endfor %}
    return jsonify(response_body), {{apiRequest.response.status_code}}

{% endfor %}

if __name__ == '__main__':
    {% set host=model.host.split(':')[0] %}
    {% set port=model.host.split(':')[1] %}
    app.run(host="{{host}}", port=int("{{port}}"))