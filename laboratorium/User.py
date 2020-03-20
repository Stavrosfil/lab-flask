from laboratorium import redis_functions as rf
from laboratorium import influx
import time


class User:
    user_id = None
    second_id = None
    mm_username = ""
    first_name = ""
    last_name = ""
    project = ""
    administrator = False
    in_lab = 0
    has_keys = 0

    # TODO: make sure the user is valid before performing other tasks
    def __init__(self, user={}):
        if user is not None:
            self.user_id = user.get("user_id")
            self.second_id = user.get("second_id")
            self.mm_username = user.get("mm_username")
            self.first_name = user.get("first_name")
            self.last_name = user.get("last_name")
            self.project = user.get("project")
            self.in_lab = user.get("in_lab")
            self.has_keys = user.get("has_keys")

            # TODO: check other values for initialization.

    def is_in_lab(self):
        return rf.in_lab(self)

    def has_keys(self):
        return rf.has_keys(self)

    def last_checkin(self):
        pass

    def checkin(self):

        timestamp = time.time_ns()

        infl = [
            {
                "measurement": "checkin",
                "tags": {
                    "user_id": self.user_id,
                    "project": self.project,
                    "checkin": True,
                },
                "time": timestamp,
                "fields": {"delta_t": 0,},
            }
        ]

        influx.write_points(infl)
        rf.set_in_lab(self, self.in_lab)
        rf.set_last_checkin(self, timestamp)

    def checkout(self):

        previous_checkin = rf.get_last_checkin(self)
        timestamp = time.time_ns()

        infl = [
            {
                "measurement": "checkin",
                "tags": {
                    "user_id": self.user_id,
                    "project": self.project,
                    "checkin": False,
                },
                "time": timestamp,
                "fields": {"delta_t": timestamp - previous_checkin,},
            }
        ]

        influx.write_points(infl)
        rf.set_in_lab(self, 0)
        rf.set_last_checkin(self, 0)
