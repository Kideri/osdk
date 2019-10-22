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
        send_message(
            peer, 
            'Invalid arguments'
        )
        return
    change_type = tmp[0]
    money = tmp[1]
    if not (change_type == 'set' or change_type == 'add' or change_type == 'remove'):
        send_message(
            peer, 
            'Invalid command type'
        )
        return
    #TODO type realization
    send_message(
        peer,
        'Successfully changed'
    )


def send_message(peer, msg):
    bot.messaging.send_message(
        peer,
        msg
    )


def buy(peer, params):
    tmp = params.split(' ')
    if not (len(tmp) == 2 or len(tmp) == 3):
        send_message(peer, 'Invalid arguments')
        return
    name = tmp[0]
    price = int(tmp[1])
    count = 1
    if len(tmp) == 3:
        count = int(tmp[2])
    send_message(
        peer,
        'You bought ' + str(count) + ' products with total cost ' + str(price * count)
    )


command_list = {
    'change_money': change_money,
    'buy': buy,
}

def check(peer, command):
    params = get_other(command)
    command = get_first(command)
    if not command in command_list:
        send_message(
            peer, 
            'Invalid command'
        )
        return
    command_list[command](peer, params)
