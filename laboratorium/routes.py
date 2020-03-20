


def init_routes(api):

    from . import admin
    
    api.add_resource(admin.GetUser, "/admin/getuser/<string:user_id>")
    api.add_resource(admin.GetUsers, "/admin/getusers")
    api.add_resource(admin.AddUser, "/admin/adduser")
    api.add_resource(admin.CheckIn, "/admin/checkin")
    api.add_resource(admin.CheckOut, "/admin/checkout")
