import json
import requests

def get_from_api(url, params=None):
    response = requests.get(url, params=params)
    if response.status_code is not 200:
        raise Exception('%s:%s' % (response.status_code, response.text))
    try:
        return json.loads(response.text)
    except Exception as e:
        raise Exception('Can\'t parse the json string\n %s' % url)