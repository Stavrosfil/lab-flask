from laboratorium import r
from laboratorium import User

"""
Dedicated file for everything redis
"""

# ---------------------------------- Setters --------------------------------- #


def get_lab_uuid(user: User):

    # Redis status string
    r_lab_uuid = "{}:lab_uuid".format(user.user_uuid)

    # Will return the id of the lab the user is in.
    lab_uuid = r.get(r_lab_uuid)
    return lab_uuid.decode("utf-8") if lab_uuid is not None else user.lab_uuid


def get_last_checkin(user: User):

    r_checkin_time = "{}:checkin_time".format(user.user_uuid)

    # Gets the last checkin timestamp for a specific lab.
    last_checkin = r.get(r_checkin_time)
    return int(last_checkin) if last_checkin is not None else 0


def get_key_uuid(user: User):

    r_key_uuid = "{}:key_uuid".format(user.user_uuid)

    # Will return the id of the keys the user has.
    key_uuid = r.get(r_key_uuid)
    return key_uuid.decode("utf-8") if key_uuid is not None else user.key_uuid


# ---------------------------------- Getters --------------------------------- #


def set_lab_uuid(user: User, lab_uuid: str):
    """Sets redis status user checkin status.
    
    Arguments:
        user {User} -- The user instance
    
    Keyword Arguments:
        lab_id {int} --  The lab ID the user is checking in or out. 0 means he is checked out.
    """

    r_lab_uuid = "{}:lab_uuid".format(user.user_uuid)
    r.set(r_lab_uuid, lab_uuid)


def set_last_checkin(user: User, timestamp):
    """Last checkin timestamp, only used for checking in.
    
    Arguments:
        user {User} -- User instance
    
    Keyword Arguments:
        timestamp {int} -- The time, in nanoseconds, of the checkin.
    """

    r_checkin_time = "{}:checkin_time".format(user.user_uuid)
    r.set(r_checkin_time, timestamp)


def set_key_uuid(user: User, key_uuid: str):

    # Set holder of the keys in the key object
    # 12345678:key_id -> 87654321
    r_key_uuid = "{}:key_id".format(key_uuid)
    r.set(r_key_uuid, user.user_uuid)


# ------------------------------ Initialization ------------------------------ #


def init_redis():
    pass
