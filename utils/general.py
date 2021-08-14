# from functools import wraps
# from flask import Flask, request, jsonify, make_response
# from models.user import User

# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         auth_header = None

#         if 'Authorization' in request.headers:
#             auth_header = request.headers['Authorization']

#         if not auth_header:
#             return jsonify({'message' : 'Token is missing!'}), 401
#         try: 
#             responseObject = User.cheek_auth_status(auth_header)
#             print(responseObject)
#         except:
#             return jsonify({'message' : 'Token is invalid!'}), 401

#         return make_response(jsonify(responseObject)), responseObject['code']


#     return decorated