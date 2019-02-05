#!/usr/bin/env python3

from slackbot.bot import respond_to, listen_to

from plugins.sio.sio import Dagens


@respond_to(r'(?i)^dagens\s*$')
@respond_to(r'(?i)^dagens\s\s*(.*)')
@listen_to(r'(?i)^!dagens\s*$')
@listen_to(r'(?i)^!dagens\s\s*(.*)')
def dagens(message, cafeteria=None):
    sio = Dagens()
    if not cafeteria:
        message.reply(sio.get_dinner_from_sio())
    elif cafeteria.lower() == 'dana':
        message.reply("Børek. Varme 1337?")
    elif cafeteria.lower() == 'list':
        message.reply(sio.help())
        return
    else:
        message.reply(sio.get_dinner_from_sio(cafeteria.lower()))
