import requests 
from flask import request, make_response, jsonify
from flask_restful import Resource, reqparse
from models.user import User
from models.tag import Tag
from models.relations.TagInBlog import TagInBlog
from flask.views import MethodView
from . import token_required
import datetime as dt
from marshmallow import Schema, fields, EXCLUDE


class TagSchema(Schema):
    id = fields.Str(required=True)
    text = fields.Str(required=True)

    class Meta:
        unknown = EXCLUDE
        ordered = True

class TagAPI(MethodView):
    """
    Post api
    """
    def get(self, tag_id):  
        if tag_id is None:
            responseObj = Tag.get_all()
            responseObj['data'] = tags_schema.dump(responseObj['data'])
        else:
            responseObj = Tag.get(tag_id)
            print(responseObj)
            responseObj['data'] = tag_schema.dump(responseObj['data'])

        return make_response(jsonify(responseObj)), responseObj['code']

    def post(self):
        auth_header = request.headers.get('Authorization')
        responseObject = User.cheek_auth_status(auth_header)

        if responseObject['code'] != 200:
            return make_response(jsonify(responseObject)), responseObject['code']
        else:
            post_data = request.get_json()
            responseObj = Tag.create(**post_data)

            return make_response(jsonify(responseObj)), responseObj['code']
    
    def delete(self, tag_id):
        auth_header = request.headers.get('Authorization')
        responseObject = User.cheek_auth_status(auth_header)

        if responseObject['code'] != 200:
            return make_response(jsonify(responseObject)), responseObject['code']
        else:
            responseObj = Tag.delete(tag_id)

        return make_response(jsonify(responseObj)), responseObj['code']
    
    
    def put(self, tag_id):
        auth_header = request.headers.get('Authorization')
        responseObject = User.cheek_auth_status(auth_header)

        if responseObject['code'] != 200:
            return make_response(jsonify(responseObject)), responseObject['code']
        else:
            post_data = request.get_json()
            responseObj = Tag.update(tag_id, responseObject['data'], **post_data)

            return make_response(jsonify(responseObj)), responseObj['code']

tags_schema = TagSchema(many=True)
tag_schema = TagSchema()