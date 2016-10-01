from slackbot.bot import respond_to, listen_to
import json
import requests
import datetime
import strict_rfc3339
from pytz import timezone

oslo = timezone('Europe/Oslo')
base_url = 'http://reisapi.ruter.no/'


def pretty_time(time):
    now = datetime.datetime.now()
    diff = time - now
    if diff.seconds < 600:
        return '%d min' % (diff.seconds / 60)
    if diff.seconds < 60:
        return 'Now'

    return time.strftime('%H:%M')


def get_from_api(url, params=None):
    response = requests.get(url, params=params)
    if response.status_code is not 200:
        raise Exception('%s:%s' % (response.status_code, response.text))
    try:
        return json.loads(response.text)
    except Exception as e:
        raise Exception('Can\'t parse the json string\n %s' % url)


@respond_to(r'tbane (.*)')
@respond_to(r'tbane$')
def tbane(message, name=None):
    ret = ''
    if name is None:
        # 3010370 is for Forskningsparken T-Bane
        stops = ({'Name': 'Forskningsparken (T-Bane)', 'ID': 3010370, 'PlaceType': 'Stop'},)
    else:
        print(name)
        stops = get_stations(name)

    for stop in stops:
        if stop['PlaceType'] in 'Stop':
            departures = get_departures(stop['ID'], transporttypes='metro')[:5]
            if len(departures) is not 0:
                ret = ret + stop['Name'] + ':\n'
                for departure in departures:
                    mvc = departure['MonitoredVehicleJourney']
                    destination = mvc['DestinationName']
                    line = mvc['PublishedLineName']
                    timestamp = mvc['MonitoredCall']['ExpectedDepartureTime']
                    time = datetime.datetime.fromtimestamp(strict_rfc3339.rfc3339_to_timestamp(timestamp))
                    ret += ('%s %s:  %s\n' % (line, destination, pretty_time(time)))

    message.reply(ret)


def get_stations(name):
    return get_from_api(base_url + 'Place/GetPlaces/' + name)


def get_departures(stop_id, datetime=None, transporttypes=None, linenames=None):
    params = dict()
    if transporttypes is not None:
        params['transporttypes'] = transporttypes
    return get_from_api(base_url + 'StopVisit/GetDepartures/' + str(stop_id), params=params)
