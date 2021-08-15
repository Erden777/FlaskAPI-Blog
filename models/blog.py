from operator import pos
from models.relations.TagInBlog import TagInBlog
from sqlalchemy.orm import backref
from app.db import db, get_db
from app import bcrypt
import jwt
from datetime import datetime
from flask import current_app
from models.tag import Tag


class Blog(db.Model):
    __tablename__ = 'blog'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    message = db.Column(db.String(255), unique=True, nullable=False)

    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship("User", cascade="all, delete", foreign_keys=[user_id], backref="posts")

    creation_date = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    modification_date = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    @classmethod
    def get(cls, post_id=None):
        try:
            if post_id:
                post = Blog.query.filter_by(
                    id=post_id
                ).first()
                tags = [tag.tag for tag in post.tags]

                print(tags)
                responseObject = {'status':'Success',
                                    'code':200,
                                    'data':post,
                                    'tags':tags
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
    def search_by_tag(cls, text=''):
        try:
            search = f"%{text}%"
            print('sdfds', search)
            if text:
                tags = Tag.query.filter(Tag.text.ilike(search)).all()
                tag_ids = [tag.id for tag in tags]
                posts = db.session.query(Blog).join(TagInBlog, TagInBlog.blog_id == Blog.id).\
                                            filter(TagInBlog.tag_id.in_(tag_ids)).all()

                responseObject = {'status':'Success',
                                    'code':200,
                                    'data':posts
                                }
                return responseObject
        except Exception as e:
            print(e)
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
            print(e)
            responseObject = {
                    'status': 'fail',
                    'message': 'Something was wrong',
                    'code':400
                }
            return responseObject


    @classmethod
    def update(cls, post_id, *user, **post_data):
        try:
            post_query = Blog.query.filter_by(
                    id=post_id
                )
            post = post_query.first()
            
            if post.user_id != user[0]['user_id'] or user[0]['admin']:
                print('yes admin')
                message = post_data.get('message')
                title = post_data.get('title')
                user_id = post_data.get('user_id', post.user_id)
                
                old_tags = [tag.tag_id for tag in post.tags]
                new_tags = [int(tag['id']) for tag in post_data.get('tags')]
                deleted_tags =list(set(old_tags)-set(new_tags))
                new_tags = list(set(new_tags)-set(old_tags))
                if deleted_tags:
                    TagInBlog.query.filter_by(blog_id=post_id).\
                                            filter(TagInBlog.tag_id.in_(deleted_tags)).\
                                                delete(synchronize_session=False)

                if new_tags:
                    updated_tags = [TagInBlog(blog_id=post_id, tag_id=tag) for tag in new_tags]
                    if updated_tags:
                        db.session.bulk_save_objects(updated_tags)

                post_data = {
                    'message':message,
                    'title':title,
                    'user_id':user_id,
                    'modification_date':datetime.utcnow()
                }
                post_query.update(post_data)
                db.session.commit()
                responseObject = {
                    'status': 'success',
                    'data':{
                        'post_id':post.id,
                        'title':post.title,
                        'message':post.message,
                        'user_id':post.user_id,
                        'created':post.creation_date,
                    },
                'code':200
                }
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'Something was wrong',
                    'code':400
                }
            return responseObject
                
        except Exception as e:
            print(e)
            responseObject = {
                    'status': 'fail',
                    'message': 'Something was wrong',
                    'code':400
                }
            return responseObject

    @classmethod
    def delete(cls, post_id):
        try:
            post = Blog.query.filter_by(id=post_id).delete()
    
            db.session.commit()
            responseObject = {
                    'status': 'success',
                    'code':200,
                    'post_id':post_id
                }
            return responseObject
        except Exception as e:
            print(e)
            responseObject = {
                    'status': 'fail',
                    'message': 'Post does not exist.',
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