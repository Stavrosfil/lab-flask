from laboratorium import influx


def checkin(user, timestamp):
    infl = [
        {
            "measurement": "checkin",
            "tags": {
                "user_id": user.user_uuid,
                "project": user.project,
                "checkin": True,
            },
            "time": timestamp,
            "fields": {"delta_t": 0, },
        }
    ]

    influx.write_points(infl)


def checkout(user, timestamp):
    last_checkin = user.get_last_checkin()
    infl = [
        {
            "measurement": "checkin",
            "tags": {
                "user_uuid": user.user_uuid,
                "project": user.project,
                "checkin": False,
            },
            "time": timestamp,
            "fields": {
                # TODO: check before adding to influx, or don't write to it at all if last check doesn't exist
                "delta_t": (timestamp - last_checkin if last_checkin != 0 else 0) // 10 ** 9},
        }
    ]

    influx.write_points(infl)
