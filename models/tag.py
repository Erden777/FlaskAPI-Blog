from app.db import db, get_db
from flask import current_app

class Tag(db.Model):
    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(255), unique=True, nullable=False)

