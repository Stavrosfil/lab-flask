from laboratorium import redis_functions as rf
from laboratorium import influx_functions as inf

import time


class User:

    # TODO: make sure the user is valid before performing other tasks
    def __init__(self, user={}):

        self.user_id = None
        self.second_id = None
        self.mm_username = ""
        self.first_name = ""
        self.last_name = ""
        self.project = ""
        self.administrator = False
        self.lab_id = "0"
        self.key_id = "0"

        if user is not None:
            _vars = vars(self)
            for var in _vars:
                parsed = user.get(var)
                if parsed is not None:
                    _vars[var] = parsed

            # TODO: check other values for initialization.

    def get_lab_id(self):
        return rf.get_lab_id(self)

    def get_key_id(self):
        return rf.get_key_id(self)

    def get_last_checkin(self):
        return rf.get_last_checkin(self)

    def get_previous_checkin(self):
        return rf.get_last_checkin(self)

    def checkin(self):
        timestamp = time.time_ns()

        inf.checkin(self, timestamp)
        rf.set_lab_id(self, self.lab_id)
        rf.set_last_checkin(self, timestamp)

    def checkout(self):
        timestamp = time.time_ns()

        inf.checkout(self, timestamp)
        rf.set_lab_id(self, 0)
        rf.set_last_checkin(self, 0)
