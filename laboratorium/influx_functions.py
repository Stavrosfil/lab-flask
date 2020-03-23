from laboratorium import influx


def checkin(user, timestamp):

    infl = [
        {
            "measurement": "checkin",
            "tags": {
                "user_id": user.user_id,
                "project": user.project,
                "checkin": True,
            },
            "time": timestamp,
            "fields": {"delta_t": 0,},
        }
    ]

    influx.write_points(infl)


def checkout(user, timestamp):

    infl = [
        {
            "measurement": "checkin",
            "tags": {
                "user_id": user.user_id,
                "project": user.project,
                "checkin": False,
            },
            "time": timestamp,
            "fields": {"delta_t": (timestamp - user.get_last_checkin()) // 10 ** 9,},
        }
    ]

    influx.write_points(infl)
