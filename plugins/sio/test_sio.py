from plugins.sio.sio import Dagens


def test_dagen_config():
    d = Dagens()
    assert d.cafeterias['ifi'] == 284
