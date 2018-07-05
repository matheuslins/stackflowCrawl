# -*- coding: utf-8 -*-
import json
import requests

from decouple import config


host = config('API_URL', cast=str)
email = config('USER_EMAIL', cast=str)
password = config('USER_PASSWORD', cast=str)


def send_to_api(data, endpoint, method):
    if method.upper() == 'POST':
        requests.post(host + endpoint,
            auth=(email, password),
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'})
