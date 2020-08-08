from laboratorium import influx


def checkin(user, timestamp):
    infl = [
        {
            "measurement": "checkin",
            "tags": {
                "user_id": user.user_uuid,
                "mm_username": f"{user.mm_username}",
                "project": user.project,
                "checkin": True,
            },
            "time": timestamp,
            "fields": {"delta_t": 0,},
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
                "mm_username": f"{user.mm_username}",
                "project": user.project,
                "checkin": False,
            },
            "time": timestamp,
            "fields": {
                "delta_t": (
                    (
                        timestamp - last_checkin
                        if last_checkin != 0 or last_checkin is not None
                        else 0
                    )
                    // 10 ** 9
                )
            },
        }
    ]

    influx.write_points(infl)


def lab_status(lab_uuid, user_count, timestamp):
    infl = [
        {
            "measurement": "lab",
            "tags": {
                "lab_uuid": lab_uuid,
                "open": (True if user_count > 0 else False),
            },
            "time": timestamp,
            "fields": {"user_count": user_count,},
        }
    ]
    influx.write_points(infl)

