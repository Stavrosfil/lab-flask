import requests
from laboratorium import mongo_functions as mf

def postHook(message):
    dictToSend = {'text': message, 'username': 'Lab Opener'}

def lab_checker(user, lab_uuid):
    print(lab_uuid)
    population = mf.get_lab_population(lab_uuid)
    if population == 0:
        message = f"The lab just closed!"
        postHook(message)
    elif population == 1:
        message = f"#working_hour\nThe lab just opened by @{user.mm_username}!\n\nReact and you are invited!"
        postHook(message)