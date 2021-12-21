import requests
from flask import request, make_response, jsonify
from flask_restful import Resource, reqparse

from models.comment import Comment
from models.user import User
from models.blog import Blog
from flask.views import MethodView
from . import token_required
import datetime as dt
from marshmallow import Schema, fields, EXCLUDE
from .user import UserSchema
from .tags import TagSchema, tags_schema


class CommentAPI(MethodView):
    """
    Comment Api
    """

    def post(self):
        auth_header = request.headers.get('Authorization')
        responseObject = User.cheek_auth_status(auth_header)

        if responseObject['code'] != 200:
            print(responseObject['code'], 'error')
            return make_response(jsonify(responseObject)), responseObject['code']
        else:
            post_data = request.get_json()
            post_data = {
                "text": request.form.get("text"),
                "post_id": request.form.get("post_id")
            }
            print(post_data, 12333)
            responseObj = Comment.create(responseObject['data'], post_data)

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



class CommentSchema(Schema):
    id = fields.Str(required=True)
    text = fields.Str(required=True)
    user_id = fields.Str(required=True)
    user = fields.Nested(UserSchema)
    creation_date = fields.DateTime(required=False)
    modification_date = fields.DateTime(required=False)

    class Meta:
        unknown = EXCLUDE
        ordered = True

blog_schema = CommentSchema()
blogs_schema = CommentSchema(many=True)