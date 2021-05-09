import uvicorn
from fastapi import FastAPI, Request

app = FastAPI()
basePath="{{model.basePath}}"
#Methods
{% for  apiRequest in model.apiRequests %}

@app.{{apiRequest.method.value}}(basePath+"/{{apiRequest.request.url}}")
def api_request_{{loop.index}}(request: Request):
    headers_to_check={{apiRequest.request.headers}}
    requestBody = {{apiRequest.request.body}}

    return jsonify({{apiRequest.response.json}}), {{apiRequest.response.status_code}}
    pass

{% endfor %}

if __name__ == "__main__":
    uvicorn.run("fastapi_code:app")