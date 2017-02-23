import json
import requests
import requests_cache
from datetime import datetime
from pytz import timezone
import chardet


def get_from_api(url, params=None, encoding=None, cache=False, cachename='dafault',
                 cache_experation=60):
    """
    Common method to get infomration from a REST api that doesn't use authentication
    :param url: URL for the api
    :param params: the parameter for the request
    :param encoding: to override the endogind
    :param cache: Use cache(default False
    :param cachename: Name of the cache
    :param cache_experation: when do you want the cache to expire in seconds, default : 60

    :return:
    """
    response = requests.get(url, params=params)
    if cache:
        requests_cache.install_cache(cachename, expire_after=cache_experation)
    if response.encoding is None:
        if encoding is None:
            response.encoding = chardet.detect(response.raw.data)['encoding']
        else:
            response.encoding = encoding
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
