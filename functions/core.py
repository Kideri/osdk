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
        if c == ' ' and not find:
            find = True
            continue
        if not find:
            continue
        ret += c
    return ret


def change_money(peer, params):
    tmp = params.split(' ')
    if len(tmp) != 2:
        send_error(peer, 'Invalid arguments')
        return
    change_type = tmp[0]
    money = tmp[1]
    if not (change_type == 'set' or change_type == 'add' or change_type == 'remove'):
        send_error(peer, 'Invalid command type')
        return
    #TODO type realization
    bot.messaging.send_message(
        peer,
        'Successfully changed'
    )


def send_error(peer, error_msg='Invalid command'):
    bot.messaging.send_message(
        peer,
        error_msg
    )


command_list = {
    'change_money': change_money
}

def check(peer, command):
    params = get_other(command)
    command = get_first(command)
    if not command in command_list:
        send_error(peer)
        return
    command_list[command](peer, params)
