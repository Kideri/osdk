from pymongo import MongoClient
import config.core as core_config

client = MongoClient(core_config.DBHOST, core_config.BDPORT)
db = client.bot3
collection = db.users


def show_db():
    for post in collection.find():
        print(post)


def check_user(user_id: int) -> bool:
    if not collection.count_documents({"user_id": str(user_id)}):
        return False
    return True


def get_money(user_id: int) -> int:
    user = collection.find_one({"user_id": str(user_id)})
    return int(user['money'])


def check_product(user_id: int, name: str, price: int) -> bool:
    if not collection.count_documents({'user_id': str(user_id), 'list.name': name, 'list.price': str(price)}):
        return False
    return True


def get_product_count(user_id: str, name: str, price: int) -> int:
    products = collection.find_one({'user_id': str(user_id), 'list.name': name, 'list.price': str(price)})['list']
    for pr in products:
        if pr['name'] == name and pr['price'] == str(price):
            return int(pr['count'])


def edit_product(user_id: int, name: str, price: int, new_name=None, new_price=None, count=None) -> None:
    product_list = collection.find_one({"user_id": str(user_id), 'list.name': name, 'list.price': str(price)})['list']
    product = {}
    for pr in product_list:
        if pr['name'] == name and pr['price'] == str(price):
            product = pr
            break
    if new_name:
        product['name'] = new_name
    if new_price:
        product['price'] = new_price
    if count:
        product['count'] = count
    collection.update(
        {
            'user_id': str(user_id),
            'list.name': name,
            'list.price': str(price)
        },
        {
            '$set': {
                'list.$': product
            }
        }
    )


def set_money(user_id: int, money: str) -> None:
    if not check_user(user_id):
        collection.insert_one(
            {
                "user_id": str(user_id),
                "money": str(money)
            }
        )
    else:
        collection.update_one(
            {
                "user_id": str(user_id)
            },
            {
                "$set": {
                    "money": str(money)
                }
            }
        )


def add_money(user_id: int, extra_money: str) -> bool:
    if not check_user(user_id):
        return False
    money = get_money(user_id)
    collection.update_one(
        {
            "user_id": str(user_id)
        },
        {
            "$set": {
                "money": str(money + extra_money)
            }
        }
    )
    return True


def remove_money(user_id: int, extra_money: str) -> bool:
    if not check_user(user_id):
        return False
    money = get_money(user_id)
    collection.update_one(
        {
            "user_id": str(user_id)
        },
        {
            "$set": {
                "money": str(money - extra_money)
            }
        }
    )
    return True


def add_product(user_id: int, name: str, price: int, count: int) -> None:
    collection.update_one(
        {
            'user_id': str(user_id)
        },
        {
            '$push': {'list': {
                'name': name,
                'price': str(price),
                'count': str(count)
            }}
        }
    )


def buy(user_id: int, name: str, price: int, count: int) -> bool:
    if not check_user(user_id):
        return False
    money_diff = price * count
    remove_money(user_id, money_diff)
    if not check_product(user_id, name, price):
        add_product(user_id, name, price, count)
    else:
        edit_product(user_id, name, price, count=get_product_count(user_id, name, price) + count)
    show_db()
    return True