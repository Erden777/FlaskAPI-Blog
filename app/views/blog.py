import requests 
from flask import request, make_response, jsonify
from flask_restful import Resource, reqparse
from models.user import User
from models.blog import Blog
from flask.views import MethodView
from . import token_required

class PostAPI(MethodView):
    """
    Post api
    """
    # @token_required
    def get(self, post_id):

        if post_id is None:
            responseObj = Blog.get_all()
        else:
            responseObj = Blog.get(post_id)

        return make_response(jsonify(responseObj)), responseObj['code']

    # @token_required
    def post(self):
        auth_header = request.headers.get('Authorization')
        responseObject = User.cheek_auth_status(auth_header)

        if responseObject['code'] != 200:
            print('Errror')
            return make_response(jsonify(responseObject)), responseObject['code']
        else:
            post_data = request.get_json()
            responseObj = Blog.create(responseObject['data'], **post_data)

            return make_response(jsonify(responseObj)), responseObj['code']
    
    @token_required
    def delete(self, post_id):
        # delete a single user
        pass
    
    @token_required
    def put(self, post_id):
        auth_header = request.headers.get('Authorization')
        responseObject = User.cheek_auth_status(auth_header)

        if responseObject['code'] != 200:
            print('Errror')
            return make_response(jsonify(responseObject)), responseObject['code']
        else:
            post_data = request.get_json()
            responseObj = Blog.update(responseObject['data'], post_id, **post_data)

            return make_response(jsonify(responseObj)), responseObj['code']

