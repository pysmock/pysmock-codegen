[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)<br>
[![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)
[![PyPI pyversions](https://img.shields.io/badge/python-3.6%7C3.7%7C3.8%7C3.9-blue)]()
[![Build Status](https://travis-ci.org/pysmock/pysmock-codegen.svg?branch=master)](https://travis-ci.org/pysmock/pysmock-codegen)
<br><b>Note:</b>This is still in development stage, and will probably have bugs in it, feel free to raise an issue for the same
# pysmock
Python module to generate mock server from yaml file<br>
Usage: `python3 -m pysmock --input input_data.yaml --output app/`<br>
## Sample YAML File

```yaml
info:
  name: "Test APIs"
  description: "description of your API"
  version: "v1"
  title: "Mock APIs"
host: "localhost:8080"
basePath: "/mock"
apiRequests:
 - get:
      request:
      response:
        json:
          resourceId: 1
          type: ResourceInfo
        status_code: 200
      url: resource/1
- post:
      request:
        body:
            name: "[A-Za-z0-9 ]*"
            data: Some data for resource
        headers:
          content-type: application/json
      response:
        json:
          resourceId: 1
          type: ResourceInfo
          name: $request.body.name
          data: $request.body.data
        status_code: 200
      url: resource
```
#### REST Endpoints
* Server Info:<br>
GET /base_url+"/info"

```javascript
{
    "contact": null,
    "description": "description of your API",
    "license": null,
    "name": "Test APIs",
    "termsOfService": "",
    "title": "Mock APIs",
    "version": "v1"
}
```
* API 1<br>
GET /base_url+"/resource/1"
```json
{
    "resourceId": 1,
    "type": "ResourceInfo"
}
```
* API 2<br>
POST /base_url+"/resource"<br>
Request:
```
{
    "name": "My new Resource1",
    "data": "Some data for resource"
}
```
Response
```json
{
    "data": "Some data for resource",
    "name": "My new Resource1",
    "resourceId": 1,
    "type": "ResourceInfo"
}
```
