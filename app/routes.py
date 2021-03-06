from re import search
from app.views.user import UserAPI, LoginAPI, RegisterAPI, LogoutAPI
from app.views.blog import PostAPI, PostSearchAPI
from app.views.tags import TagAPI
from app.views.comment import CommentAPI
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
    '/auth/profile',
    view_func=user_view,
    methods=['GET']
)

auth_blueprint.add_url_rule(
    '/auth/profile',
    view_func=user_view,
    methods=['PUT']
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


post_view = PostAPI.as_view('post_api')

auth_blueprint.add_url_rule('/posts/', defaults={'post_id': None},
                 view_func=post_view, methods=['GET',])

auth_blueprint.add_url_rule('/posts/', view_func=post_view, methods=['POST',])
auth_blueprint.add_url_rule('/posts/<int:post_id>', view_func=post_view,
                 methods=['GET', 'PUT', 'DELETE'])


tag_view = TagAPI.as_view('tag_api')

auth_blueprint.add_url_rule('/tags/', defaults={'tag_id': None},
                 view_func=tag_view, methods=['GET',])

auth_blueprint.add_url_rule('/tags/', view_func=tag_view, methods=['POST',])
auth_blueprint.add_url_rule('/tags/<int:tag_id>', view_func=tag_view,
                 methods=['GET', 'PUT', 'DELETE'])


search_view = PostSearchAPI.as_view('search_post_api')

auth_blueprint.add_url_rule('/search/',
                 view_func=search_view, methods=['POST',])


comment_view = CommentAPI.as_view('comment_api')
auth_blueprint.add_url_rule('/comment',
                            view_func=comment_view, methods=['POST',])