from laboratorium import mongo
import uuid
from laboratorium import User


def get_user_by_tag_uuid(tag_uuid: str):
    mongo_users = mongo.db["users"]
    return mongo_users.find_one({"tag_uuids": tag_uuid})


def add_user(user: User):
    mongo_users = mongo.db["users"]

    to_add = {}
    to_add["_id"] = str(
        uuid.uuid5(
            uuid.NAMESPACE_DNS,
            user.first_name + user.last_name + str(user.tag_uuid[0]),
        ))

    to_add["tag_uuid"] = user.tag_uuid
    to_add["first_name"] = user.first_name
    to_add["last_name"] = user.last_name
    to_add["mm_username"] = user.mm_username
    to_add["project"] = user.project
    to_add["administrator"] = False

    print(to_add)
    try:
        new_result = mongo_users.insert(to_add)
        print('Multiple posts: {0}'.format(new_result))
    except Exception as e:
        print(e)
