from laboratorium import mongo
import uuid
from laboratorium import User


def generate_uuid(user: User):
    generated_uuid = uuid.uuid1()
    return generated_uuid


def get_user_by_tag_uuid(tag_uuid: str):
    mongo_users = mongo.db["users"]
    return mongo_users.find_one({"tag_uuid": tag_uuid})


def add_user(user: User):
    mongo_users = mongo.db["users"]

    to_add = {}
    generated_uuid = generate_uuid(user)
    to_add["_id"] = generated_uuid
    to_add["tag_uuid"] = user.tag_uuid
    to_add["first_name"] = user.first_name
    to_add["last_name"] = user.last_name
    to_add["mm_username"] = user.mm_username
    to_add["project"] = user.project
    to_add["administrator"] = user.administrator

    distinct_fields = {"tag_uuid": user.tag_uuid,
                       "mm_username": user.mm_username}

    if _satisfies_distinct_fields(distinct_fields):
        try:
            new_result = mongo_users.insert(to_add)
            return str(new_result)
        except Exception as e:
            return {"Error:": str(e)}, 500
    else:
        return {"Error": "One or more of the provided fields already exists"}, 500


def modify_user(user: User, to_modify: dict, mode="set"):
    mongo_users = mongo.db["users"]

    new_result = mongo_users.update_one({'_id': generate_uuid(user)},
                                        {"${}".format(mode): to_modify},
                                        upsert=False)


def make_administrator(user: User):
    modify_user(user, {"administrator": True}, "set")


def make_alumni(user: User):
    modify_user(user, {"alumni": True}, "set")


def add_tag(user: User, tag_uuid: str):
    modify_user(user, {"tag_uuid": tag_uuid}, "push")


def remove_tag(user: User, tag_uuid: str):
    modify_user(user, {"tag_uuid": tag_uuid}, "pull")


def change_mm_username(user: User, mm_username: str):
    modify_user(user, {"mm_username": mm_username}, "set")


def _satisfies_distinct_fields(distinct_fields: dict):
    mongo_users = mongo.db["users"]

    filtered_fields = []
    for field, value in distinct_fields.items():
        if isinstance(value, list):
            for v in value:
                filtered_fields.append(mongo_users.find_one({field: v}))
        else:
            filtered_fields.append(mongo_users.find_one({field: value}))

    return all(f is None for f in filtered_fields)
