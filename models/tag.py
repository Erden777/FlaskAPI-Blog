from app.db import db, get_db
from flask import current_app

class Tag(db.Model):
    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(255), unique=True, nullable=False)

    @classmethod
    def get(cls, tag_id):
        try:
            if tag_id:
                tag = Tag.query.filter_by(
                    id=tag_id
                ).first()
                
                responseObject = {'status':'Success',
                                    'code':200,
                                    'data':tag,
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
    def get_all(cls):
        try:
            tags = Tag.query.all()
            responseObject = {
                    'status': 'success',
                    'code':200,
                    'data':tags
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
    def create(cls, **post_data):
        try:
            text = post_data.get('text')
            tag = Tag(text=text)
            db.session.add(tag)
            db.session.commit()

            responseObject = {
                'status':'success',
                'data':{
                        'tag_id':tag.id,
                        'text':tag.text
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
    def update(cls, tag_id, *user, **post_data):
        try:
            tag_query = Tag.query.filter_by(
                    id=tag_id
                )
            tag = tag_query.first()
            
            if user[0]['admin']:
                print('yes admin')
                text = post_data.get('text')
                post_data = {
                    'text':text,
                }
                tag_query.update(post_data)
                db.session.commit()
                responseObject = {
                    'status': 'success',
                    'data':{
                        'tag_id':tag.id,
                        'text':tag.text
                        
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
    def delete(cls, tag_id):
        try:
            tag = Tag.query.filter_by(id=tag_id).delete()
    
            db.session.commit()
            responseObject = {
                    'status': 'success',
                    'code':200,
                    'tag_id':tag_id
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