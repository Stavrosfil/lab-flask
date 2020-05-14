def init_routes(api):

    from . import admin
    from . import slash_command
    prefix = '/lab/api'

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

    api.add_resource(slash_command.SlashLab, "/lab/")
