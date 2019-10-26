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
    ind = 0
    for pr in product_list:
        if pr['name'] == name and pr['price'] == str(price):
            product = pr
            break
        ind += 1
    check_req = False
    if new_name:
        product['name'] = new_name
        check_req = True
    if new_price:
        product['price'] = new_price
        check_req = True
    if count:
        product['count'] = count
    
    if check_req and check_product(user_id, product['name'], product['price']):
        pr_count = get_product_count(user_id, product['name'], product['price'])
        pr_count += get_product_count(user_id, name, price)
        edit_product(user_id, product['name'], product['price'], count=pr_count)
        remove_product(user_id, name, price)
        return

    collection.update_one(
        {
            'user_id': str(user_id)
        },
        {
            '$set': {
                'list.'+str(ind): product
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


def show_money(user_id: int) -> bool or int:
    if not check_user(user_id):
        return False
    return get_money(user_id)


def get_list(user_id: int) -> bool or dict:
    if not check_user(user_id):
        return False
    products = collection.find_one({'user_id': str(user_id)})['list']
    return products


def remove_product(user_id: int, name: str, price: int, count = None) -> int:
    if not check_user(user_id):
        return 0
    if not check_product(user_id, name, price):
        return 1
    if count is None:
        collection.update(
            {
                'user_id': str(user_id),
            },
            {
                '$pull': {
                    'list': {
                        'name': name,
                        'price': str(price)
                    }
                }
            }
        )
    else:
        pr_count = get_product_count(user_id, name, price)
        if pr_count - count <= 0:
            return remove_product(user_id, name, price)
        edit_product(user_id, name, price, count=pr_count-count)
    return 2