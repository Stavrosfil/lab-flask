from laboratorium import r
import time


"""
Helper functions to interface with influxDB and Redis in a clean manner
"""


def redis_loader():

    pass


def user_handler(user, influx):
    """
    Haldler for user RFID scan.
    Checks Influx and Redis to define if the user is checking in or out.

    Arguments:
        user    {dict} -- A dictionary containing all user information, loaded from SQLite database.
    """

    # in_lab: "12345678:in_lab" -> A way to store user status in redis.
    r_in_lab = "{}:in_lab".format(user['user_id'])
    r_checkin_time = r_in_lab + ':checkin_time'

    # If the current user status is 0, user needs checkin.
    if r.get(r_in_lab) == b'0':
        user_checkin(user, r_in_lab, r_checkin_time, influx)
    else:
        user_checkout(user, r_in_lab, r_checkin_time)

    resp = {}
    resp["user_name"] = "{} {}.".format(
        user['last_name'], user['first_name'][0])
    resp["direction"] = int(r.get(r_in_lab))

    return resp


def user_checkin(user, r_in_lab, r_checkin_time, influx):

    timestamp = time.time()

    infl = {
        "measurement": "checkin",
        "tags": {
            "user_id": user['user_id'],
            "project": user['project'],
            "check_in": True,
        },
        "time": timestamp,
        "fields": {
            "delta_t": 0,
        }
    }

    influx.write(infl)
    r.set(r_in_lab, 1)
    r.set(r_checkin_time, timestamp)


def user_checkout(user, r_in_lab, r_checkin_time, influx):

    previous_checkin = int(r.get(r_in_lab + ':checkin_time'))

    infl = {
        "measurement": "checkin",
        "tags": {
            "user_id": user['user_id'],
            "project": user['project'],
            "check_in": False,
        },
        "time": time.time(),
        "fields": {
            "delta_t": time.time() - previous_checkin,
        }
    }

    influx.write(infl)
    r.set(r_in_lab, 0)
    r.set(r_checkin_time, 0)
