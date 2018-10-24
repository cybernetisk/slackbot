from plugins.sio.sio import Dagens

def test_dagen_config():
    d = Dagens()
    assert d.cafeterias['ifi'] == 284

def test_dagens_config2():
    d = Dagens()
    assert d.get_dinner_cafeteria('ifi') != 'Cafeteria not found'
