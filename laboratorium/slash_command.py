from flask import Flask, jsonify, request, current_app
from laboratorium import mongo, User
from laboratorium import mongo_functions as mf
from flask_restful import Resource
import json, random, requests

mongo_labs = mongo.db['labs']
mongo_users = mongo.db['users']  
    

class SlashLab(Resource):
    def post(self):
        payload = {}
        
        if request.form['text'] == '':
            for lab in mongo_labs.find():
            # mongo_labs.update({'_id': 'lab1'}, {'$inc': {'user_count': 1}})
                users = lab['users']
                if len(users) == 1:
                    message = f"There is 1 user in {lab['desc']}\n\n"
                else:
                    message = f"There are {len(users)} users in {lab['desc']}\n\n"
                for user in users:
                    user = mongo_users.find_one({'_id': user})
                    message += f"{user['first_name']} {user['last_name']}\n"
                payload = {
                    'text': message,
                    'username': 'Lab Authenticator',
                    'icon_url': 'https://eu.ui-avatars.com/api/?name={}'.format(len(users)),
                }

        elif request.form['text'] == 'stats':
            lab = mongo_labs.find_one({'_id': 'lab1'})
            payload = {
                'text': 'The lab statistics for today! {}, {}'\
                .format(lab['user_count'], lab['_id']),
                'username': 'Lab Stats',
                'icon_url': 'https://eu.ui-avatars.com/api/?name={}'.format(request.form['user_name']),
            }

        elif request.form['text'] == 'checkout':
            mm_username = request.form['user_name']
            user = User.User({'mm_username': mm_username})
            lab = mongo_labs.find_one({'_id': user.lab_uuid})
            
            if user.lab_uuid != '0':
                user.checkin('0')
                payload = {
                    'text': 'The user {} was successfully checked out!'\
                    .format(user.mm_username),
                    'username': 'Lab Authenticator',
                    'icon_url': 'https://eu.ui-avatars.com/api/?name={}'.format(user.first_name),
                }
            else:
                payload = {
                    'text': 'You are not checked in any lab!',
                    'username': 'Lab Authenticator',
                    'icon_url': 'https://eu.ui-avatars.com/api/?name={}'.format(user.first_name),
                }
                    
        elif request.form['text'] == 'open':
            pass
        elif request.form['text'] == 'count':
            pass
        elif request.form['text'].startswith('mock'):
            data = request.form['text'][5:]
            ans = []
            for c in data:
                ans.append(c.upper() if random.randint(0,1) == 1 else c.lower())
            payload = {
                'text': ''.join(ans),
                'username': 'lAB AutHeNTIcAtOr',
                'icon_url': 'https://eu.ui-avatars.com/api/?name={}'.format('M'),
            }

        return jsonify(payload)
