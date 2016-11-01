from slackbot.bot import respond_to
import json

def load_help_json():
    with open('plugins/functions.json') as f:
        functions = json.load(f)
    return functions

@respond_to(r'^help$')
@respond_to(r'^help (.*)')
def help(message, helpfunction=None):
    functions = load_help_json()
    if helpfunction is None:
        reply = "This is the commands you can use:\n"
        for function, text in functions.items():
            reply += "\t%s: %s\n" %(function, text)
        message.reply(reply)
    elif helpfunction in functions:
        message.reply("%s:%s" %(helpfunction, functions[helpfunction]))
    else:
        message.reply('I don\'t know that command')