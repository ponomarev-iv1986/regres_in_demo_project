import json

import allure
import requests
from allure_commons.types import AttachmentType
from curlify import to_curl


def request(method, url, **kwargs):
    with allure.step(f'{method.upper()} {url}'):
        response = requests.request(
            method=method.upper(),
            url=f'https://reqres.in{url}',
            **kwargs
        )
        allure.attach(
            body=str(response.status_code),
            name='status code',
            attachment_type=AttachmentType.TEXT,
            extension='txt'
        )
        try:
            allure.attach(
                body=json.dumps(response.json(), indent=4).encode('utf8'),
                name='response body',
                attachment_type=AttachmentType.JSON,
                extension='json'
            )
        except requests.exceptions.JSONDecodeError:
            allure.attach(
                body='no body or not JSON',
                name='response body',
                attachment_type=AttachmentType.TEXT,
                extension='txt'
            )
        curl = to_curl(response.request)
        allure.attach(
            body=curl.encode('utf8'),
            name='curl',
            attachment_type=AttachmentType.TEXT,
            extension='txt'
        )
    return response
