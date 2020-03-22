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
    lab_id = "0"
    key_id = "0"

    # TODO: make sure the user is valid before performing other tasks
    def __init__(self, user={}):
        if user is not None:
            self.user_id = user.get("user_id")
            self.second_id = user.get("second_id")
            self.mm_username = user.get("mm_username")
            self.first_name = user.get("first_name")
            self.last_name = user.get("last_name")
            self.project = user.get("project")
            self.lab_id = (
                self.lab_id if user.get("lab_id") is None else user.get("lab_id")
            )
            self.key_id = (
                self.key_id if user.get("key_id") is None else user.get("key_id")
            )

            # TODO: check other values for initialization.

    def get_lab_id(self):
        return rf.get_lab_id(self)

    def get_key_id(self):
        return rf.get_key_id(self)

    def get_last_checkin(self):
        return rf.get_last_checkin(self)

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
        rf.set_lab_id(self, self.lab_id)
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
        rf.set_lab_id(self, 0)
        rf.set_last_checkin(self, 0)
