from laboratorium import r
from laboratorium import influx_db

"""
Helper functions to interface with influxDB and Redis in a clean manner
"""


def redis_loader():

    pass


def user_handler(user):
    """
    Haldler for user RFID scan.
    Checks Influx and Redis to define if the user is checking in or out.

    Arguments:
        user    {dict} -- A dictionary containing all user information, loaded from SQLite database.
    """

    # in_lab: "12345678:in_lab" -> A way to store user status in redis.
    in_lab = "{}:in_lab".format(user['user_id'])

    # If the current user status is 0, user needs checkin.
    if r.get(in_lab) == b'0':
        user_checkin(in_lab)
    else:
        user_checkout(in_lab)

    resp = {}
    resp["user_name"] = "{} {}.".format(
        user['last_name'], user['first_name'][0])
    resp["direction"] = int(r.get(in_lab))

    return resp


def user_checkin(in_lab):
    r.set(in_lab, 1)


def user_checkout(in_lab):
    r.set(in_lab, 0)
