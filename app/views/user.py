import requests 
from flask import Blueprint, request, make_response, jsonify
from flask_restful import Resource, reqparse
from models.user import User, BlacklistToken
from models.tag import Tag
from models.blog import Blog
from app.db import db
from flask.views import MethodView

class RegisterAPI(MethodView):
    """
    User Registration Resource
    """
    def post(self):
        # get the post data
        post_data = request.get_json()
        responseObj = User.register(post_data)
        # check if user already exists
        return make_response(jsonify(responseObj)), responseObj['code']


class LoginAPI(MethodView):
    """
    User Login Resource
    """
    def post(self):
        # get the post data
        post_data = request.get_json()
        responseObject = User.login(**post_data)
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
 