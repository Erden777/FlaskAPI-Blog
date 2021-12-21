from app.db import db, get_db
from datetime import datetime

class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(255), nullable=False)

    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship("User", cascade="all, delete", foreign_keys=[user_id], backref="comments")

    creation_date = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    modification_date = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    blog_id = db.Column(db.BigInteger, db.ForeignKey('blog.id'), nullable=False)
    blog = db.relationship("Blog", cascade="all, delete", foreign_keys=[blog_id], backref="comments")


    @classmethod
    def create(cls, user, post_data):
        try:
            text = post_data.get('text')
            post_id = post_data.get('post_id')
            print(user[0]['user_id'], 'creating')
            comment = Comment(text=text, blog_id=post_id, user_id=user[0]['user_id'])\

            db.session.add(comment)
            db.session.commit()
            comment_id =comment.id
            new_comment = Comment.query.filter_by(id=comment_id).first()
            print(comment.user, 'user')
            responseObject = {
                'status': 'success',
                'data': {
                    'post_id': comment.id,
                    'user': str(comment.user.name)+' '+str(comment.user.surname),
                    'text': comment.text,
                    'created': comment.creation_date,
                },
                'code': 200
            }
            return responseObject
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Something was wrong',
                'code': 400
            }
            return responseObject

