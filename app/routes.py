from app.views.user import UserAPI, LoginAPI, RegisterAPI, LogoutAPI
from app.views.blog import PostAPI
from flask_restful import Api
from functools import wraps
from flask import Blueprint
from flask import Flask, request, jsonify, make_response

auth_blueprint = Blueprint('auth', __name__)

registration_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')
user_view = UserAPI.as_view('user_api')
logout_view = LogoutAPI.as_view('logout_api')

# add Rules for API Endpoints


auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/status',
    view_func=user_view,
    methods=['GET']
)
auth_blueprint.add_url_rule(
    '/auth/logout',
    view_func=logout_view,
    methods=['POST']
)


user_view = PostAPI.as_view('post_api')

auth_blueprint.add_url_rule('/posts/', defaults={'post_id': None},
                 view_func=user_view, methods=['GET',])

auth_blueprint.add_url_rule('/posts/', view_func=user_view, methods=['POST',])
auth_blueprint.add_url_rule('/posts/<int:post_id>', view_func=user_view,
                 methods=['GET', 'PUT', 'DELETE'])