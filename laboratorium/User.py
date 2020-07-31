from pprint import pprint

from laboratorium import influx_functions as inf
from laboratorium import mongo_functions as mf
from laboratorium import hooks
from flask import current_app

import ldap

import time


class User:
    def __init__(self, user_dict=None):

        if user_dict is None:
            user_dict = {}

        self.user_uuid = ""
        self.tag_uuid = []
        self.key_uuid = []
        # self.device_uuid = ""
        self.lab_uuid = ""

        self.ldap_username = ""
        self.ldap_password = ""

        self.mm_username = ""
        self.first_name = ""
        self.last_name = ""
        self.project = ""
        self.administrator = False
        self.alumni = False

        # Initialize by dictionary parsed from json request.
        self.init_from_dict(user_dict)

        # if self.user_uuid == "":
        self.init_from_mongo()

    def init_from_dict(self, user_dict):
        if user_dict is not None:
            _vars = vars(self) 
            if user_dict.get('tag_uuid'):
                if not isinstance(user_dict.get('tag_uuid'), type(list)):
                    user_dict['tag_uuid'] = [user_dict['tag_uuid']]
                    
            for var in _vars:
                parsed = user_dict.get(var)
                if parsed is not None and isinstance(_vars[var], type(parsed)):
                    _vars[var] = parsed

            if user_dict.get("_id") is not None:
                self.user_uuid = user_dict.get("_id")

        # TODO: if user_uuid == None return None or something

    def init_from_mongo(self):
        user_dict = None
        if self.user_uuid != "":
            user_dict = mf.get_user("_id", self.user_uuid)
        if self.tag_uuid != []:
            user_dict = mf.get_user('tag_uuids', self.tag_uuid[0])
        elif self.mm_username != "":
            user_dict = mf.get_user('mm_username', self.mm_username)    
        if user_dict is not None:
            user_dict['user_uuid'] = user_dict['_id']
            self.init_from_dict(user_dict)

    def get_last_checkin(self):
        return 1000
        

    def checkin(self, lab_uuid):
        timestamp = time.time_ns()
        mf.checkin(self, lab_uuid)
        inf.checkin(self, timestamp)
        self.lab_uuid = lab_uuid
        hooks.lab_checker(self, lab_uuid)


    def checkout(self):
        timestamp = time.time_ns()
        mf.checkout(self)
        inf.checkout(self, timestamp)
        hooks.lab_checker(self, self.lab_uuid)
        self.lab_uuid = '0'

    def authenticate(self):

        if self.ldap_password == "" or self.ldap_username == "":
            return -1

        try:
            l = ldap.initialize("ldap://ldap.helit.org")

            l.protocol_version = ldap.VERSION3

            # Pass in a valid username and password to get
            # privileged directory access.
            # If you leave them as empty strings or pass an invalid value
            # you will still bind to the server but with limited privileges.
            service_bind_dn = current_app.config["LDAP_SERVICE_BIND_DN"]
            service_secret = current_app.config["LDAP_SERVICE_SECRET"]

            base = current_app.config["LDAP_BASE"]

            # Any errors will throw an ldap.LDAPError exception
            # or related exception so you can ignore the result codes
            print(l.simple_bind_s(service_bind_dn, service_secret))

            # Search for existing email first
            result = l.search_s(base, ldap.SCOPE_SUBTREE, "email={}".format(self.ldap_username), attrsonly=0)
            pprint(result)
            if result:
                dn = result[0][0]
                print(dn)
                print(l.simple_bind_s(dn, self.ldap_password))
                return "success"

            # If there is not an existing email, search for a username
            result = l.search_s(base, ldap.SCOPE_SUBTREE, "uid={}".format(self.ldap_username), attrsonly=0)
            pprint(result)
            if result:
                dn = result[0][0]
                print(dn)
                print(l.simple_bind_s(dn, self.ldap_password))
                return "success"

        except ldap.LDAPError as e:
            print(e)
            return str(e)
