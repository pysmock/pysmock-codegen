[![Build Status](https://travis-ci.org/pysmock/pysmock-codegen.svg?branch=master)](https://travis-ci.org/pysmock/pysmock-codegen)
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
