from operator import pos
from app.db import db, get_db
from app import bcrypt
import jwt
from datetime import datetime
from flask import current_app

class Blog(db.Model):
    __tablename__ = 'blog'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    message = db.Column(db.String(255), unique=True, nullable=False)

    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship("User", cascade="all,delete", foreign_keys=[user_id])

    creation_date = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    modification_date = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    @classmethod
    def get(cls, post_id=None):
        try:
            if post_id:
                post = Blog.query.filter_by(
                    id=post_id
                ).first()
                responseObject = {'status':'Success',
                                    'code':200,
                                    'data':{
                                        'post_id':post.id,
                                        'title':post.title,
                                        'message':post.message,
                                        'user_id':post.user_id,
                                        'user':{
                                            'user_id': post.user.id,
                                            'email': post.user.email,
                                        },
                                        'created':post.creation_date,
                                    }
                                }
                return responseObject
        except Exception as e:
            responseObject = {
                    'status': 'fail',
                    'message': 'Post does not exist.',
                    'code':400
                }
            return responseObject

    @classmethod
    def create(cls, user, **post_data):
        try:
            title = post_data.get('title')
            message = post_data.get('message')
            post = Blog(title=title, message=message, user_id=user['user_id'])
            db.session.add(post)
            db.session.commit()

            responseObject = {
                'status':'success',
                'data':{
                        'post_id':post.id,
                        'title':post.title,
                        'message':post.message,
                        'user_id':post.user_id,
                        'created':post.creation_date,
                    },
                'code':200
            }
            return responseObject
        except Exception as e:
            responseObject = {
                    'status': 'fail',
                    'message': 'Something was wrong',
                    'code':400
                }
            return responseObject


    @classmethod
    def update(cls, user, post_id, **post_data):
        try:
            post_query = Blog.query.filter_by(
                    id=post_id
                )
            post = post_query.first()
            if post.user_id != user['user_id'] or user['admin']:
                message = post_data.get('message')
                title = post_data.get('message')
                user_id = post_data.get('user_id', post.user_id)

                post_data = {
                    'message':message,
                    'title':title,
                    'user_id':user_id,
                    'modification_date':datetime.utcnow()
                }
                post_query.update(post_data)
                db.session.commit()
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'Something was wrong',
                    'code':400
                }
            return responseObject
                
        except Exception as e:
            responseObject = {
                    'status': 'fail',
                    'message': 'Something was wrong',
                    'code':400
                }
            return responseObject

    @classmethod
    def get_all(cls):
        try:
            posts = Blog.query.all()
            responseObject = {
                    'status': 'success',
                    'code':200,
                    'data':posts
                }
            return responseObject
        except Exception as e:
            responseObject = {
                    'status': 'fail',
                    'message': 'Post does not exist.',
                    'code':400
                }
            return responseObject