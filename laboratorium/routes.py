def init_routes(api):

    from . import admin

    api.add_resource(admin.GetUser, "/admin/getuser/<string:tag_uuid>")
    api.add_resource(admin.GetUsers, "/admin/getusers")

    api.add_resource(admin.AddUser, "/admin/adduser")
    api.add_resource(admin.CheckIn, "/admin/checkin")
    api.add_resource(admin.CheckOut, "/admin/checkout")

    api.add_resource(admin.MakeAdministrator, "/admin/makeadmin")
    api.add_resource(admin.MakeAlumni, "/admin/makealumni")
    api.add_resource(admin.AddTag, "/admin/addtag")
    api.add_resource(admin.RemoveTag, "/admin/removetag")
    api.add_resource(admin.ChangeMmUsername, "/admin/changemmusername")

    api.add_resource(admin.Authenticate, "/auth")
