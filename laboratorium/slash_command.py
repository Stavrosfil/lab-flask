from flask import Flask, jsonify, request
from laboratorium import mongo, User
from laboratorium import mongo_functions as mf
from flask_restful import Resource
import json
import random

mongo_labs = mongo.db['labs']
mongo_users = mongo.db['users']  
    
key = {'_id': '1'}
data = {'user_count': 0, 'users': []}
mf.update_object(mongo_labs, key, data)

key = {'_id': '2'}
data = {'user_count': 0, 'users': []}
mf.update_object(mongo_labs, key, data)


class SlashLab(Resource):
    def post(self):
        payload = {}
        
        if request.form['text'] == '':
            mongo_labs.update({'_id': '1'}, {'$inc': {'user_count': 1}})
            lab = mongo_labs.find_one({'_id': '1'})
            payload = {
                'text': 'There are {} people in lab: {}.'\
                .format(lab['user_count'], lab['_id']),
                'username': 'Lab Authenticator',
                'icon_url': 'https://eu.ui-avatars.com/api/?name={}'.format(lab['user_count']),
            }

        elif request.form['text'] == 'stats':
            lab = mongo_labs.find_one({'_id': '1'})
            payload = {
                'text': 'The lab statistics for today! {}, {}'\
                .format(lab['user_count'], lab['_id']),
                'username': 'Lab Stats',
                'icon_url': 'https://eu.ui-avatars.com/api/?name={}'.format(request.form['user_name']),
            }

        elif request.form['text'] == 'checkout':
            lab = mongo_labs.find_one({'_id': '1'})
            mm_username = request.form['user_name']
            user = User.User({'mm_username': mm_username})
            
            if user.lab_uuid != '0':
                user.checkin(lab_uuid='0')
                payload = {
                    'text': 'The user {} was successfully checked out!'\
                    .format(user.mm_username),
                    'username': 'Lab Authenticator',
                    'icon_url': 'https://eu.ui-avatars.com/api/?name={}'.format(lab['user_count']),
                }
            else:
                payload = {
                    'text': 'You are not checked in any lab!',
                    'username': 'Lab Authenticator',
                    'icon_url': 'https://eu.ui-avatars.com/api/?name={}'.format(lab['user_count']),
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
