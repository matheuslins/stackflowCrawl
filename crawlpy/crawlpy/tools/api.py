# -*- coding: utf-8 -*-
import json
import requests

from decouple import config


host = config('API_URL', cast=str)


def send_to_api(data, endpoint, method):
    if method.upper() == 'POST':
        response = requests.post(host + endpoint,
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )