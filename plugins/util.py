import json
import requests
from datetime import datetime
from pytz import timezone

def get_from_api(url, params=None):
    response = requests.get(url, params=params)
    if response.status_code is not 200:
        raise Exception('%s:%s' % (response.status_code, response.text))
    try:
        return json.loads(response.text)
    except Exception as e:
        raise Exception('Can\'t parse the json string\n %s' % url)

def get_user_from_message(message):
    return message.channel._client.users[message.body['user']]

def semester_is_valid(semester):
    now = datetime.now(tz=timezone('Europe/Oslo'))
    if int(now.year) != int(semester['year']):
        return False
    if 'SPRING' in semester['semester']:
        if int(now.month) < 9:
            return True
        else:
            return False
    elif 'FALL' in semester['semester']:
        if int(now.month) is 1:
            return True
        elif int(now.month) > 6:
            return True
        else:
            return False
    return False