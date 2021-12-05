import requests 
from flask import request, make_response, jsonify
from flask_restful import Resource, reqparse
from models.user import User
from models.blog import Blog
from flask.views import MethodView
from . import token_required
import datetime as dt
from marshmallow import Schema, fields, EXCLUDE
from .user import UserSchema
from .tags import TagSchema, tags_schema

class PostAPI(MethodView):
    """
    Post api
    """
    def get(self, post_id):

        if post_id is None:
            responseObj = Blog.get_all()
            responseObj['data'] = blogs_schema.dump(responseObj['data'])
        else:
            responseObj = Blog.get(post_id)
            print(responseObj)
            if responseObj['code'] == 200:
                responseObj['data'] = blog_schema.dump(responseObj['data'])
                responseObj['tags'] = tags_schema.dump(responseObj['tags'])


        return make_response(jsonify(responseObj)), responseObj['code']

    def post(self):
        auth_header = request.headers.get('Authorization')
        responseObject = User.cheek_auth_status(auth_header)

        if responseObject['code'] != 200:
            return make_response(jsonify(responseObject)), responseObject['code']
        else:
            post_data = request.get_json()
            responseObj = Blog.create(responseObject['data'], **post_data)

            return make_response(jsonify(responseObj)), responseObj['code']
    
    def delete(self, post_id):
        auth_header = request.headers.get('Authorization')
        responseObject = User.cheek_auth_status(auth_header)

        if responseObject['code'] != 200:
            return make_response(jsonify(responseObject)), responseObject['code']
        else:
            responseObj = Blog.delete(post_id)

        return make_response(jsonify(responseObj)), responseObj['code']
    
    
    def put(self, post_id):
        auth_header = request.headers.get('Authorization')
        responseObject = User.cheek_auth_status(auth_header)

        if responseObject['code'] != 200:
            return make_response(jsonify(responseObject)), responseObject['code']
        else:
            post_data = request.get_json()
            print(post_data)
            responseObj = Blog.update(post_id, responseObject['data'], **post_data)

            return make_response(jsonify(responseObj)), responseObj['code']

class PostSearchAPI(MethodView):
    """
    Post api
    """
    def post(self):
        text = request.get_json()
        if text is None:
            responseObj = Blog.get_all()
            responseObj['data'] = {}
        else:
            responseObj = Blog.search_by_tag(text)
            responseObj['data'] = blogs_schema.dump(responseObj['data'])

        return make_response(jsonify(responseObj)), responseObj['code']



class BlogSchema(Schema):
    id = fields.Str(required=True)
    title = fields.Str(required=True)
    message = fields.Str(required=True)
    user_id = fields.Str(required=True)
    user = fields.Nested(UserSchema)
    # tags = fields.Dict(id=fields.Int(), text=fields.Str())
    creation_date = fields.DateTime(required=False)
    modification_date = fields.DateTime(required=False)

    class Meta:
        unknown = EXCLUDE
        ordered = True


blog_schema = BlogSchema()
blogs_schema = BlogSchema(many=True)
