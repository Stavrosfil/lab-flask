from laboratorium import redis_functions as rf
from laboratorium import influx_functions as inf
from laboratorium import mongo_functions as mf

import time


class User:
    def __init__(self, user_dict=None):

        if user_dict is None:
            user_dict = {}
        self.user_uuid = ""
        self.tag_uuid = []
        self.key_uuid = []
        self.lab_uuid = ""

        self.mm_username = ""
        self.first_name = ""
        self.last_name = ""
        self.project = ""
        self.administrator = False
        self.alumni = False

        # Initialize by dictionary parsed from json request.
        self.init_from_dict(user_dict)

    def init_from_dict(self, user_dict):
        if user_dict is not None:
            _vars = vars(self)
            for var in _vars:
                parsed = user_dict.get(var)
                if parsed is not None and isinstance(_vars[var], type(parsed)):
                    _vars[var] = parsed

        # TODO: if user_uuid == None return None or something

    def init_from_mongo(self):
        user_dict = mf.get_user_by_tag_uuid(self.tag_uuid[0])
        if user_dict is not None:
            user_dict["user_uuid"] = user_dict["_id"]
        self.init_from_dict(user_dict)

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
        rf.set_lab_id(self, self.lab_uuid)
        rf.set_last_checkin(self, timestamp)

    def checkout(self):
        timestamp = time.time_ns()

        inf.checkout(self, timestamp)
        rf.set_lab_id(self, 0)
        rf.set_last_checkin(self, 0)
