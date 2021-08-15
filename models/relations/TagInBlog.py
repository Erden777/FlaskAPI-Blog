from sqlalchemy.orm import backref
from app.db import db

class TagInBlog(db.Model):
    __tablename__ = 'tag_in_blog'

    id = db.Column(db.BigInteger, primary_key=True)

    tag_id = db.Column(db.BigInteger, db.ForeignKey('tag.id'), nullable=False)
    tag = db.relationship("Tag", cascade="all,delete", foreign_keys=[tag_id], backref="blogs")

    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'), nullable=False)
    blog = db.relationship("Blog", cascade="all,delete", foreign_keys=[blog_id], backref="tags")
