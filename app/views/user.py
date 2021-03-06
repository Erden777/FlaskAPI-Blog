import requests 
from flask import Blueprint, request, make_response, jsonify
from flask_restful import Resource, reqparse
from models.user import User, BlacklistToken
from models.tag import Tag
from models.blog import Blog
from app.db import db
from flask.views import MethodView
from marshmallow import Schema, fields, EXCLUDE


class RegisterAPI(MethodView):
    """
    User Registration Resource
    """
    def post(self):
        # get the post data

        data = request.get_json()
        print(data)
        post_data = {
            "email": request.form.get("email") or data['email'],
            "password": request.form.get("password") or data['password'],
            "surname": request.form.get("surname"),
            "group_id": request.form.get('group_id') or data['group_id'],
            "name": request.form.get("name")
        }
        responseObj = User.register(post_data)
        # check if user already exists
        print(responseObj, 'this is resposne obj')
        return make_response(jsonify(responseObj)), responseObj['code']


class LoginAPI(MethodView):
    """
    User Login Resource
    """
    def post(self):
        data = request.data
        data = request.get_json()
        post_data = {
            "email": request.form.get('email') or data['email'],
            "password": request.form.get('password') or data['password']
        }
        print('login in')
        print(post_data)
        responseObject = User.login(**post_data)
        print(responseObject, 'this is resposne obj')

        return make_response(jsonify(responseObject)), responseObject['code']


class UserAPI(MethodView):
    """
    User Resource
    """
    def get(self):
        # get the auth token
        auth_header = request.headers.get('Authorization')
        print(auth_header)
        responseObject = User.cheek_auth_status(auth_header)
        print(responseObject, 12312312)
        return make_response(jsonify(responseObject)), responseObject['code']

    def put(self):
        auth_header = request.headers.get('Authorization')
        responseObject = User.cheek_auth_status(auth_header)
        if responseObject['code'] == 200:
            post_data = request.get_json()
            print(responseObject)
            post_data['user'] = responseObject['data'][0]['email']
            print(post_data)
            responseObject = User.profile_update(**post_data)
            print(post_data)

        return make_response(jsonify(responseObject)), responseObject['code']

class LogoutAPI(MethodView):
    
    def post(self):
        # get auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                # mark the token as blacklisted
                blacklist_token = BlacklistToken(token=auth_token)
                try:
                    # insert the token
                    db.session.add(blacklist_token)
                    db.session.commit()
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged out.'
                    }
                    return make_response(jsonify(responseObject)), 200
                except Exception as e:
                    responseObject = {
                        'status': 'fail',
                        'message': e
                    }
                    return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': resp
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 403
 

class UserSchema(Schema):
    id = fields.Str(required=True)
    email = fields.Str(required=True)
    name = fields.Str(required=True)
    surname = fields.Str(required=True)
    admin = fields.Bool(required=True)
