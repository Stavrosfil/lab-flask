from laboratorium import admin


def init_routes(api):

    api.add_resource(admin.GetUser, "/admin/getuser/<string:user_id>")
    api.add_resource(admin.GetUsers, "/admin/getusers")
    api.add_resource(admin.AddUser, "/admin/adduser")
