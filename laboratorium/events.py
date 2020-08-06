from laboratorium import mongo_functions as mf
from laboratorium import User


def add_tag_after_command(user: User, tag_uuid):
    if tag_uuid is not None:
        if User.User({"tag_uuid": tag_uuid}).user_uuid != "":
            mf.add_tag(user, tag_uuid)
            return "User added successfully"
        else:
            return "User already exists!"
