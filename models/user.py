from app.db import db, get_db
from flask import Blueprint, request, make_response, jsonify
from app import bcrypt
import jwt
import datetime 
from flask import current_app
import enum


class Group(db.Model):
    __tablename__ = "group"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_name = db.Column(db.String(500), nullable=False)


class CourseChoices(enum.Enum):
    first = 1
    second = 2
    third = 3
    fourth = 4


class Speciality(db.Model):
    __tablename__ = "speciality"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(100), nullable=False)
    name_kk = db.Column(db.String(500), nullable=False)
    name_en = db.Column(db.String(500), nullable=True)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    full_name_kk = db.Column(db.String(255), nullable=True)
    full_name_en = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    group_id = db.Column(db.BigInteger, db.ForeignKey('group.id'), nullable=False)
    group = db.relationship("Group", cascade="all, delete", foreign_keys=[group_id], backref="users")
    speciality_id = db.Column(db.BigInteger, db.ForeignKey('speciality.id'), nullable=True)
    speciality = db.relationship("Speciality", cascade="all, delete", foreign_keys=[speciality_id], backref="users")
    course = db.Column(db.Enum(CourseChoices))

    def __init__(self, email, password, group_id,admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config['BCRYPT_LOG_ROUNDS']
        ).decode()
        self.group_id = group_id
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def encode_auth_token(self, user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30, seconds=3000),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id,
                'full_name_kk': self.full_name_kk,
                'full_name_en': self.full_name_en,
                'group': {
                    'id': self.group_id,
                    'group_name': self.group.group_name
                },
                'speciality': {
                    'name_kk': self.speciality.name_kk,
                    'name_en': self.speciality.name_en,
                    'code': self.speciality.code
                },
                'birth_date': str(self.birth_date),
                'course': self.course.value
            }

            print(payload)
            return jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e


    @classmethod
    def register(cls, post_data):
        user = User.query.filter_by(email=post_data.get('email')).first()
        if not user:
            try:
                user = User(
                    email=post_data.get('email'),
                    password=post_data.get('password'),
                    group_id=post_data.get('group_id')
                )
                # insert the user
                db.session.add(user)
                db.session.commit()
                # generate the auth token
                auth_token = user.encode_auth_token(user.id)
                responseObject = {
                    'status': 'success',
                    'tdid': user.id,
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode(),
                    'code':201
                }
                return responseObject
            except Exception as e:
                print(e)
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.',
                    'code':401
                }
                return responseObject
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
                'code':202
            }
            return make_response(jsonify(responseObject)), 202


    @classmethod
    def profile_update(cls, **post_data):
        print(post_data, 'post_data')
        try:
            # fetch the user data]
            print(post_data['user'], 1233)
            user_query = User.query.filter_by(
                email=post_data.get('user')
            )
            user = user_query.first()
            user.name = post_data.get('name')
            user.surname = post_data.get('surname')
            updated = {
                'name': post_data.get('name'),
                'surname': post_data.get('surname')
            }

            user_query.update(updated)
            db.session.commit()
            
            responseObject = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'email': user.email,
                        'name': user.name,
                        'surname': user.surname,
                        'admin': user.admin,
                        'registered_on': user.registered_on
                    },
                    'code':200
                }

            return responseObject

        except Exception as e:
            print(e, 12333333)
            responseObject = {
                'status': 'fail',
                'message': 'Try again',
                'code':400
            }


    @classmethod
    def cheek_auth_status(cls, auth_header):
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]

            except IndexError:
                responseObject = {
                    'status': 'fail',
                    'message': 'Bearer token invalid.',
                    'code':401
                }
                return responseObject
        else:
            auth_token = ''
        if auth_token:
            resp = cls.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                responseObject = {
                    'status': 'success',
                    'data': [{
                        'user_id': user.id,
                        'email': user.email,
                        'name': user.name,
                        'surname': user.surname,
                        'admin': user.admin,
                        'registered_on': user.registered_on
                    }],
                    'code':200
                }
                return responseObject
            responseObject = {
                'status': 'fail',
                'message': resp,
                'code':401
            }
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.',
                'code':400
            }
        return responseObject
        

    @classmethod
    def login(cls, **post_data):
        try:
            # fetch the user data
            user = User.query.filter_by(
                email=post_data.get('email')
            ).first()
            if user and bcrypt.check_password_hash(
                user.password, post_data.get('password')
            ):
                auth_token = user.encode_auth_token(user.id)
                print(auth_token)
                if auth_token:
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token.decode(),
                        'user_id': user.id,
                        'full_name': user.full_name_kk,
                        'code': 200
                    }
                    return responseObject
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'User does not exist.',
                    'code':400
                }
                return responseObject

        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again',
                'code':400
            }
    

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, current_app.config.get('SECRET_KEY'))
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'




class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False