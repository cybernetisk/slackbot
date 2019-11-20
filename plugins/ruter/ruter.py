from slackbot.bot import respond_to, listen_to
import json
import requests
import datetime
from strict_rfc3339 import rfc3339_to_timestamp
from pytz import timezone
from plugins.util import get_from_api

oslo = timezone('Europe/Oslo')
base_url = 'https://api.entur.io/'

entur_headers = {
    'ET-Client-Name': 'cybernetisk_selskab - internsystem',
    'Access-Control-Allow-Methods': 'GET, POST'
}

def entur_timestamp_to_strict_rfc3339(timestamp):
    timestamp_list = list(timestamp)
    timestamp_list.insert(-2, ':')
    return ''.join(timestamp_list)

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
@listen_to(r'^!tbane (.*)')
@listen_to(r'^!tbane$')
def tbane(message, name=None):
    ruter(message, name=name, transporttype='metro')

@respond_to(r'^trikk (.*)')
@respond_to(r'^trikk')
@listen_to(r'^!trikk (.*)')
@listen_to(r'^!trikk')
def trikk(message, name=None):
    ruter(message, name=name, transporttype='tram')


@respond_to(r'^buss (.*)')
@respond_to(r'^buss')
@listen_to(r'^!buss (.*)')
@listen_to(r'^!buss')
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
        if stop['properties']['county'] == 'Oslo':
            stopPlace = get_departures(stop['properties']['id'].split(':')[-1])['data']['stopPlace']
            if stopPlace:
                departures = [
                    departure for departure in stopPlace['estimatedCalls'] 
                    if departure['serviceJourney']['journeyPattern']['line']['transportMode'] == transporttype
                ]

                if len(departures) is not 0:
                    ret = ret + stop['properties']['name'] + ':\n'
                    for departure in departures:
                        destination = departure['destinationDisplay']['frontText']
                        line = departure['serviceJourney']['journeyPattern']['line']['id'].split(':')[-1]
                        timestamp = entur_timestamp_to_strict_rfc3339(departure['expectedDepartureTime'])
                        time = datetime.datetime.fromtimestamp(rfc3339_to_timestamp(timestamp), tz=oslo)
                        ret += ('%s %s:  %s\n' % (line, destination, pretty_time(time)))
                    ret += '\n'

    message.reply(ret)


def get_stations(name):
    stations_url = base_url + 'geocoder/v1/autocomplete?text={}&lang=no'
    return requests.get(stations_url.format(name)).json()['features']


def get_departures(stop_id, datetime=None, linenames=None):
    journey_url = base_url + 'journey-planner/v2/graphql'

    query = """
        {
            stopPlace(id: "NSR:StopPlace:%s") {
                id
                name
                estimatedCalls(timeRange: 72100, numberOfDepartures: 10) {     
                    expectedDepartureTime
                    destinationDisplay {
                        frontText
                    }
                    serviceJourney {
                        journeyPattern {
                            line {
                                id
                                transportMode
                            }
                        }
                    }
                }
            }
        }
    """ % stop_id
    
    return requests.post(journey_url, json={'query': query}, headers=entur_headers).json()
