from slackbot.bot import respond_to, listen_to
import json
import requests
import datetime
import strict_rfc3339
from pytz import timezone
from plugins.util import get_from_api

oslo = timezone('Europe/Oslo')
base_url = 'http://reisapi.ruter.no/'


def pretty_time(time):
    now = datetime.datetime.now(tz=oslo)
    diff = time - now
    if diff.seconds < 600:
        return '%d min' % (diff.seconds / 60)
    if diff.seconds < 60:
        return 'Now'

    return time.strftime('%H:%M')



@respond_to(r'^tbane (.*)')
@respond_to(r'^tbane$')
def tbane(message, name=None):
    ruter(message, name=name, transporttype='metro')

@respond_to(r'^trikk (.*)')
@respond_to(r'^trikk')
def trikk(message, name=None):
    ruter(message, name=name, transporttype='tram')


@respond_to(r'^buss (.*)')
@respond_to(r'^buss')
def buss(message, name=None):
    if name is None:
        ruter(message, name='Gaustad', transporttype='bus')
    else:
        ruter(message, name=name, transporttype='bus')

def ruter(message, name=None, transporttype=None):
    ret = ''
    if name is None:
        # 3010370 is for Forskningsparken T-Bane
        stops = get_stations('Forskningsparken')
    else:
        stops = get_stations(name)

    for stop in stops:
        if stop['PlaceType'] in 'Stop':
            departures = get_departures(stop['ID'], transporttypes=transporttype)[:5]
            if len(departures) is not 0:
                ret = ret + stop['Name'] + ':\n'
                for departure in departures:
                    mvc = departure['MonitoredVehicleJourney']
                    destination = mvc['DestinationName']
                    line = mvc['PublishedLineName']
                    timestamp = mvc['MonitoredCall']['ExpectedDepartureTime']
                    time = datetime.datetime.fromtimestamp(strict_rfc3339.rfc3339_to_timestamp(timestamp), tz=oslo)
                    ret += ('%s %s:  %s\n' % (line, destination, pretty_time(time)))

    message.reply(ret)


def get_stations(name):
    return get_from_api(base_url + 'Place/GetPlaces/' + name)


def get_departures(stop_id, datetime=None, transporttypes=None, linenames=None):
    params = dict()
    if transporttypes is not None:
        params['transporttypes'] = transporttypes
    return get_from_api(base_url + 'StopVisit/GetDepartures/' + str(stop_id), params=params)
