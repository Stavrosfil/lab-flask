from laboratorium import redis_functions as rf
from laboratorium import influx


class User:
    user_id = None
    second_id = None
    first_name = ""
    last_name = ""
    mm_username = ""
    project = ""
    administrator = False
    # in_lab = False
    # has_keys = False

    def __init__(self, user={}):
        if user is not None:
            self.user_id = user.get("user_id")
            self.second_id = user.get("second_id")
            self.mm_username = user.get("mm_username")
            self.first_name = user.get("first_name")
            self.last_name = user.get("last_name")
            self.project = user.get("project")

    def is_in_lab(self):
        return rf.in_lab(self)

    def has_keys(self):
        return rf.has_keys(self)

    def last_checkin(self):
        pass

    def checkin(self):
        timestamp = time.time()

        infl = {
            "measurement": "checkin",
            "tags": {
                "user_id": self.user_id,
                "project": self.project,
                "check_in": True,
            },
            "time": timestamp,
            "fields": {"delta_t": 0,},
        }

        influx.write(infl)
        rf.set_in_lab(self, True)
        rf.set_last_checkin(self, timestamp)

    def checkout(self):
        previous_checkin = rf.get_last_checkin(self)

        infl = {
            "measurement": "checkin",
            "tags": {
                "user_id": self.user_id,
                "project": self.project,
                "check_in": False,
            },
            "time": time.time(),
            "fields": {"delta_t": time.time() - previous_checkin,},
        }

        influx.write(infl)
        rf.set_in_lab(self, True)
        rf.set_last_checkin(self, 0)
