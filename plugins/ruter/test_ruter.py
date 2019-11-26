from plugins.ruter import ruter

def test_get_station():
    name = 'Forskningsparken'
    stations = ruter.get_stations(name)

    assert name in stations[0]['properties']['name']