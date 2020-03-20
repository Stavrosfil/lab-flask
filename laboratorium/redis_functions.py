from laboratorium import r

"""
Dedicated file for everything redis
"""


def is_in_lab(user):
    # in_lab: "12345678:in_lab" -> A way to store user status in redis.
    r_in_lab = user.user_id + ":in_lab"
    if r.get(r_in_lab) == b"0":
        return False
    else:
        return True


def set_in_lab(user, state=bool):
    r_in_lab = user.user_id + ":in_lab"
    r.set(r_in_lab, state)


def has_keys(user):
    pass


def get_last_checkin(user):
    r_checkin_time = user.user_id + ":checkin_time"
    return int(r.get(r_checkin_time))


def set_last_checkin(user, timestamp):
    r_checkin_time = user.user_id + ":checkin_time"
    r.set(r_checkin_time, timestamp)


def checkin():
    pass


def checkout():
    pass
