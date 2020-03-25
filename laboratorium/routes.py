def init_routes(api):

    from . import admin

    api.add_resource(admin.GetUser, "/admin/getuser/<string:tag_uuid>")
    api.add_resource(admin.GetUsers, "/admin/getusers/<string:lab_uuid>")

    api.add_resource(admin.AddUser, "/admin/adduser")
    api.add_resource(admin.CheckIn, "/admin/checkin")
    api.add_resource(admin.CheckOut, "/admin/checkout")
