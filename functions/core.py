from dialog_bot_sdk.bot import DialogBot
from config.core import bot

def get_first(string):
    ret = ''
    for c in string:
        if c == ' ':
            break
        ret += c
    return ret


def get_other(string):
    ret = ''
    find = False
    for c in string:
        if c == ' ':
            find = True
        if not find:
            continue
        ret += c
    return ret


def add(peer, params):
    bot.messaging.send_message(
        peer,
        'Add command detected'
    )


def send_error(peer):
    bot.messaging.send_message(
        peer,
        'Invalid command'
    )


command_list = {
    'add': add
}

def check(peer, command):
    params = get_other(command)
    command = get_first(command)
    if not command in command_list:
        send_error(peer)
        return
    command_list[command](peer, params)
