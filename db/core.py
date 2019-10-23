from pymongo import MongoClient
import config.core as core_config
import pprint

client = MongoClient(core_config.DBHOST, core_config.BDPORT)
db = client.bot3
collection = db.users


def show_db():
    for post in collection.find():
        print(post)


def check_user(user_id):
    if collection.count_documents({"user_id": str(user_id)}) == 0:
        return False
    return True


def get_money(user_id):
    user = collection.find_one({"user_id": str(user_id)})
    return int(user['money'])


def set_money(user_id, money):
    if not check_user:
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


def add_money(user_id, extra_money):
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
    show_db()
    return True


def remove_money(user_id, extra_money):
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
    show_db()
    return True