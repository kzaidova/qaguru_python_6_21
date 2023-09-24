import json
import os

import allure
from allure_commons.types import AttachmentType
from requests import sessions
from curlify import to_curl


resources_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'resources'))

def requests_api(service, method, url, **kwargs):
    base_url = {"reqres": "https://reqres.in", "catfact": "https://catfact.ninja"}
    new_url = base_url[service] + url
    method = method.upper()
    with allure.step(f"{method} {url}"):
        with sessions.Session() as session:
            response = session.request(method=method, url=new_url, **kwargs)
            message = to_curl(response.request)
            allure.attach(body=message.encode("utf8"), name="Curl", attachment_type=AttachmentType.TEXT,
                          extension='txt')
            if not response.content:
                allure.attach(body='empty response', name='Empty Response', attachment_type=AttachmentType.TEXT,
                              extension='txt')
            else:
                allure.attach(body=json.dumps(response.json(), indent=4).encode("utf8"), name="Response Json",
                              attachment_type=AttachmentType.JSON, extension='json')
    return response
