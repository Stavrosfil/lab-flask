from laboratorium import r

"""
Dedicated file for everything redis
"""

# ---------------------------------- Setters --------------------------------- #


def get_lab_id(user):

    # Redis status string
    r_lab_id = "{}:lab_id".format(user.user_id)

    # Will return the id of the lab the user is in.
    lab_id = r.get(r_lab_id)
    return lab_id.decode("utf-8") if lab_id is not None else user.lab_id


def get_last_checkin(user):

    r_checkin_time = "{}:checkin_time".format(user.user_id)

    # Gets the last checkin timestamp for a specific lab.
    return int(r.get(r_checkin_time))


def get_key_id(user):

    r_key_id = "{}:key_id".format(user.user_id)

    # Will return the id of the keys the user has.
    key_id = r.get(r_key_id)
    return key_id.decode("utf-8") if key_id is not None else user.key_id


# ---------------------------------- Getters --------------------------------- #


def set_lab_id(user, lab_id):
    """Sets redis status user checkin status.
    
    Arguments:
        user {User} -- The user instance
    
    Keyword Arguments:
        lab_id {int} --  The lab ID the user is checking in or out. 0 means he is checked out.
    """

    r_in_lab = "{}:lab_id".format(user.user_id)
    r.set(r_in_lab, lab_id)


def set_last_checkin(user, timestamp):
    """Last checkin timestamp, only used for checking in.
    
    Arguments:
        user {User} -- User instance
    
    Keyword Arguments:
        timestamp {int} -- The time, in nanoseconds, of the checkin.
    """

    r_checkin_time = "{}:checkin_time".format(user.user_id)
    r.set(r_checkin_time, timestamp)


def set_key_id(user, key_id):

    # Set holder of the keys in the key object
    # 12345678:key_id -> 87654321
    r_key_id = "{}:key_id".format(key_id)
    r.set(r_key_id, user.user_id)


# ------------------------------ Initialization ------------------------------ #


def init_redis():
    pass
