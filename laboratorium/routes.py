def init_routes(api):

    from . import admin
    prefix = '/lab-flask'

<<<<<<< Updated upstream
    api.add_resource(admin.GetUser, "/admin/getuser/<string:user_id>")
    api.add_resource(admin.GetUsers, "/admin/getusers")
    api.add_resource(admin.AddUser, "/admin/adduser")
    api.add_resource(admin.CheckIn, "/admin/checkin")
    api.add_resource(admin.CheckOut, "/admin/checkout")
=======
    api.add_resource(admin.GetUser, "{}/admin/getuser/<string:tag_uuid>".format(prefix))
    api.add_resource(admin.GetUsers, "{}/admin/getusers".format(prefix))

    api.add_resource(admin.AddUser, "{}/admin/adduser".format(prefix))
    api.add_resource(admin.CheckIn, "{}/admin/checkin".format(prefix))
    api.add_resource(admin.CheckOut, "{}/admin/checkout".format(prefix))

    api.add_resource(admin.MakeAdministrator, "{}/admin/makeadmin".format(prefix))
    api.add_resource(admin.MakeAlumni, "{}/admin/makealumni".format(prefix))
    api.add_resource(admin.AddTag, "{}/admin/addtag".format(prefix))
    api.add_resource(admin.RemoveTag, "{}/admin/removetag".format(prefix))
    api.add_resource(admin.ChangeMmUsername, "{}/admin/changemmusername".format(prefix))

    api.add_resource(admin.Authenticate, "/auth")
>>>>>>> Stashed changes
