from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity#, create_refresh_token
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from src.database import User, db
from flasgger import swag_from
from src.logging.logs import logger

authenticate = Blueprint("authenticate", __name__, url_prefix="/Authenticate")

@authenticate.get("/Register")
def invalid_l():
    return jsonify({
        "error": "Not allowed",
        "message": "Only post method allowed for this url"
    }), HTTP_403_FORBIDDEN

@authenticate.post('/Register')
def register():
    if request.json.get('username') and request.json.get('password'):
        username = request.json.get('username')
        password = request.json.get('password')
        pwd_hash = generate_password_hash(password)
        
        if len(password)<6:
            return jsonify({'error': "Password is too short"}), HTTP_400_BAD_REQUEST

        if len(username)<3:
            return jsonify({'error': "Username is too short"}), HTTP_400_BAD_REQUEST

        if not username.isalnum() or " " in username:
            return jsonify({'error': "Username should be alphanumeric, also no spaces"}), HTTP_400_BAD_REQUEST

        pwd_hash = generate_password_hash(password)

        try:
            user = User.query.filter_by(username=username).first()
            if user:
                return jsonify({
                    'error': "Username is taken"
                }), HTTP_409_CONFLICT
            
            user = User(username=username, password=pwd_hash)
            db.session.add(user)
            db.session.commit()

            return jsonify({
                "message": "User created",
                "user": {
                    "username": username
                }
            }), HTTP_201_CREATED

        except Exception as e:
            return jsonify({
                "error": e
            }), HTTP_400_BAD_REQUEST
    
    else:
        return jsonify({
            "error" : "username or password is not passed"
        }), HTTP_400_BAD_REQUEST

@authenticate.get("/Login")
def invalid_r():
    request_data = request
    if request.is_json:
        request_data = request.json
    response_data = {
        "error": "Not allowed",
        "message": "Only post method allowed for this url"
    }
    response_code = HTTP_403_FORBIDDEN
    logger.error('Request = ( '  + str(request_data) + ' )|Response = ( ' + str(response_data) + ',' + str(response_code) + ' )')
    return jsonify(response_data), response_code

@authenticate.post("/Login")
@swag_from('./docs/auth/login.yaml')
def login():

    request_data = request
    if request.json.get('username') and request.json.get('password'):
        username = request.json.get('username')
        password = request.json.get('password')
        request_data = request.json

        try:
            user = User.query.filter_by(username=username).first()
            
            if user:
                is_pass_correct = check_password_hash(user.password, password)

                if is_pass_correct:
                    access_token = create_access_token(identity=user.username)
                    response_data = {
                        'user': {
                            'access_token': access_token,
                            'username': username
                        }
                    }
                    response_code = HTTP_200_OK
                    logger.info('Request = ( '  + str(request_data) + ' )|Response = ( ' + str(response_data) + ',' + str(response_code) + ' )')
                    return jsonify(response_data), response_code
            
                response_data = {
                    'error': 'Wrong credentials',
                    'data_passed': {
                        'username': username
                    }
                }
                response_code = HTTP_401_UNAUTHORIZED
                logger.error('Request = ( '  + str(request_data) + ' )|Response = ( ' + str(response_data) + ',' + str(response_code) + ' )')
                return jsonify(response_data), response_code

            response_data = {
                'error': 'No user is registered with given details',
                'data_passed': {
                    'username': username
                }
            }
            response_code = HTTP_404_NOT_FOUND
            logger.error('Request = ( '  + str(request_data) + ' )|Response = ( ' + str(response_data) + ',' + str(response_code) + ' )')
            return jsonify(response_data), response_code

        except Exception as e:
            response_data = {"error": e}
            response_code = HTTP_404_NOT_FOUND
            logger.error('Request = ( '  + str(request_data) + ' )|Response = ( ' + str(response_data) + ',' + str(response_code) + ' )')
            return jsonify(response_data), response_code

    else:
        response_data = {"error" : "username or password is not passed"}
        response_code = HTTP_400_BAD_REQUEST
        logger.error('Request = ( '  + str(request_data) + ' )|Response = ( ' + str(response_data) + ',' + str(response_code) + ' )')
        return jsonify(response_data), response_code

@authenticate.get("/me")
@jwt_required()
def me():
    username = get_jwt_identity()
    return {
        "user": {
            "username": username
        }
    }, HTTP_200_OK