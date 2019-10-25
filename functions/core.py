from dialog_bot_sdk.bot import DialogBot
from config.core import bot
import db.core as core_db

def get_first(string: str) -> str:
    ret = ''
    for c in string:
        if c == ' ':
            break
        ret += c
    return ret


def get_other(string: str) -> str:
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


def change_money(peer, params: str) -> bool:
    tmp = params.split(' ')
    if len(tmp) != 2:
        send_message(
            peer, 
            'Invalid arguments'
        )
        return False
    change_type = tmp[0]
    money = tmp[1]
    if not (change_type == 'set' or change_type == 'add' or change_type == 'remove'):
        send_message(
            peer, 
            'Invalid command type'
        )
        return False
    #TODO type realization
    res = False
    # print(peer)
    if change_type == 'set':
        core_db.set_money(int(peer.id), int(money))
    if change_type == 'add':
        if not core_db.add_money(int(peer.id), int(money)):
            send_message(
                peer,
                'User does not exist.\nFirst you need to set your money'
            )
            return False
    if change_type == 'remove':
        if not core_db.remove_money(int(peer.id), int(money)):
            send_message(
                peer,
                'User does not exist.\nFirst you need to set your money'
            )
            return False
    send_message(
        peer,
        'Successfully changed'
    )
    return True


def send_message(peer, msg: str) -> None:
    bot.messaging.send_message(
        peer,
        msg
    )


def buy(peer, params: str) -> bool:
    tmp = params.split(' ')
    if not (len(tmp) == 2 or len(tmp) == 3):
        send_message(peer, 'Invalid arguments')
        return False
    name = tmp[0]
    price = int(tmp[1])
    count = 1
    if len(tmp) == 3:
        count = int(tmp[2])
    if not core_db.buy(int(peer.id), name, price, count):
        send_message(
            peer,
            'User does not exist.\nFirst you need to set your money'
        )
        return False
    send_message(
        peer,
        'You bought ' + str(count) + ' products with total cost ' + str(price * count)
    )
    return True


def show(peer, params: str) -> bool:
    money = core_db.show_money(int(peer.id))
    if not money:
        send_message(
            peer,
            'User does not exist.\nFirst you need to set your money'
        )
        return False
    send_message(
        peer,
        'You have -> ' + str(money) + ' money left.'
    )

command_list = {
    'change_money': change_money,
    'buy': buy,
    'show': show
}

def check(peer: str, command: str) -> bool:
    params = get_other(command)
    command = get_first(command)
    if not command in command_list:
        send_message(
            peer, 
            'Invalid command'
        )
        return False
    command_list[command](peer, params)
    return True
