from laboratorium import mongo
import uuid
from laboratorium import User
from flask import current_app


mongo_users = mongo.db[current_app.config["MONGO_USER_COLLECTION"]]


def generate_uuid(user: User):
    generated_uuid = uuid.uuid1()
    return str(generated_uuid)


def get_all_users():
    users = []
    for user in mongo_users.find():
        users.append(User.User(user))
    for u in users:
        print(u.lab_uuid)
    return users

def remove_all_from_lab():
    users = get_all_users()
    for user in users:
        user.checkin("0")
    return users

def get_user(key, value):
    return mongo_users.find_one({key: value})

def add_user(user: User):
    to_add = {}
    generated_uuid = generate_uuid(user)
    to_add["_id"] = generated_uuid
    to_add["tag_uuid"] = user.tag_uuid
    to_add["first_name"] = user.first_name
    to_add["last_name"] = user.last_name
    to_add["mm_username"] = user.mm_username
    to_add["project"] = user.project
    to_add["administrator"] = user.administrator
    to_add["alumni"] = user.alumni

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


def checkin(user: User, lab_uuid):
    if user.lab_uuid != '':
        if user.lab_uuid != '0':
            update_object(mongo_users, {'_id': user.user_uuid}, {'lab_uuid': '0'})
            user.lab_uuid = '0'
        else:
            key = {'_id': user.user_uuid}
            data = {'lab_uuid': lab_uuid}
            update_object(mongo_users, key, data)
            user.lab_uuid = lab_uuid
    else:
        update_object(mongo_users, {'_id': user.user_uuid}, {'lab_uuid': lab_uuid})
        user.lab_uuid = '0'
    return user

        
# def checkin_by_tag(lab_uuid: str, tag_uuid: str):
#     user = mongo_users.find_one({'tag_uuids': tag_uuid})

#     if user is None: return None
#     user = User.User(user)

#     return checkin(user, lab_uuid)      


def modify_user(user: User, to_modify: dict, mode="set"):
    new_result = mongo_users.update_one({'_id': user.user_uuid},
                                        {"${}".format(mode): to_modify},
                                        upsert=False)
    return str(new_result)


def make_administrator(user: User):
    return modify_user(user, {"administrator": True}, "set")


def make_alumni(user: User):
    return modify_user(user, {"alumni": True}, "set")


def add_tag(user: User):
    print(user.tag_uuid)
    return modify_user(user, {"tag_uuid": user.tag_uuid[0]}, "push")


def remove_tag(user: User):
    return modify_user(user, {"tag_uuid": user.tag_uuid[0]}, "pull")


def change_mm_username(user: User):
    return modify_user(user, {"mm_username": user.mm_username}, "set")


def _satisfies_distinct_fields(distinct_fields: dict):
    filtered_fields = []
    for field, value in distinct_fields.items():
        if isinstance(value, list):
            for v in value:
                filtered_fields.append(mongo_users.find_one({field: v}))
        else:
            filtered_fields.append(mongo_users.find_one({field: value}))

    return all(f is None for f in filtered_fields)


def update_object(db, key, data):
    db.update_one(key, {'$set': data}, upsert=True)
