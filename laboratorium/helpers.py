

"""
Helper functions to interface with influxDB and Redis in a clean manner
"""


def user_handler(user, influx, r):
    """
    Haldler for user RFID scan. 
    Checks Influx and Redis to define if the user is checking in or out.

    Arguments:
        user    {dict} -- A dictionary containing all user information, loaded from SQLite database. 
        influx  {influxdb connection object} -- Handles all InfluxDB interfacing
        r       {redis connection object} -- Handles all Redis interfacing
    """

    in_lab = "{}:in_lab".format(user['user_id'])
    if r.get(in_lab) == b'0':
        r.set(in_lab, 1)
    else:
        r.set(in_lab, 0)

    resp = {}
    resp["user_name"] = "{} {}.".format(
        user['last_name'], user['first_name'][0])
    resp["direction"] = int(r.get(in_lab))

    return resp


def user_checkin():
    pass


def user_checkout():
    pass
