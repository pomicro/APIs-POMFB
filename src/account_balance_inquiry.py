from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.constants.code_constants import ACCOUNT_CURRENCY_CODE_LENGTH, ACCOUNT_NUMBER_LENGTH, ACCOUNT_TYPE_CODE_LENGTH
from src.constants.http_status_codes import API_210_RESPONSE_CODE, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from src.database import User
from flasgger import swag_from
from src.logging.logs import logger

account_balance_inquiry = Blueprint("account_balance_inquiry", __name__, url_prefix="/AccountBalanceInquiry")

@account_balance_inquiry.get('/')
@jwt_required()
def invalid():
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

@account_balance_inquiry.post('/')
@jwt_required()
@swag_from('./docs/account_balance_inquiry.yaml')
def return_balance_inquiry():

    request_data = request
    try:
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        request_data = request

        if user:

            request_data = request
            if request.is_json:
                #print(request.is_json)

                request_data = request.json
                if request.json.get('Account_Number') and request.json.get('Account_Type_Code') and request.json.get('Account_Currency_Code'):
                    #print("available")
                    account_number = request.json.get('Account_Number')
                    account_type_code = request.json.get('Account_Type_Code')
                    account_currency_code = request.json.get('Account_Currency_Code')
                    response_code = HTTP_400_BAD_REQUEST

                    if (len(str(account_number))!=ACCOUNT_NUMBER_LENGTH) or (type(account_number) is not str):
                        response_data = {'error': "Account_Number is too short or too long or is not str, it must be of length " + str(ACCOUNT_NUMBER_LENGTH) + " of type string"}
                        logger.error('Request = ( '  + str(request_data) + ' )|Response = ( ' + str(response_data) + ',' + str(response_code) + ' )')
                        return jsonify(response_data), response_code

                    if (len(str(account_type_code))!=ACCOUNT_TYPE_CODE_LENGTH) or (type(account_type_code) is not int):
                        response_data = {'error': "Account_Type_Code is too short or too long or is not int, it must be of length " + str(ACCOUNT_TYPE_CODE_LENGTH) + " of type integer"}
                        logger.error('Request = ( '  + str(request_data) + ' )|Response = ( ' + str(response_data) + ',' + str(response_code) + ' )')
                        return jsonify(response_data), response_code

                    if (len(str(account_currency_code))!=ACCOUNT_CURRENCY_CODE_LENGTH) or (type(account_currency_code) is not int):
                        response_data = {'error': "Account_Currency_Code is too short or too long or is not int, it must be of length " + str(ACCOUNT_CURRENCY_CODE_LENGTH) + " of type integer"}
                        logger.error('Request = ( '  + str(request_data) + ' )|Response = ( ' + str(response_data) + ',' + str(response_code) + ' )')
                        return jsonify(response_data), response_code

                    #
                    #Code to retrieve account_status_code and balance_code
                    #

                    account_status_code = "101" #Change this to the value retrieved from database
                    available_balance = 99999999900 # Change this to the value retrieved from database

                    response_data = {
                        "Account_Number": account_number,
                        "Account_Type_Code": account_type_code,
                        "Account_Currency_Code": account_currency_code,
                        "Account_Status_Code": account_status_code,
                        "Available_Balance": available_balance
                    }
                    response_code = API_210_RESPONSE_CODE
                    logger.info('Request = ( '  + str(request_data) + ' )|Response = ( ' + str(response_data) + ',' + str(response_code) + ' )')
                    return jsonify(response_data), response_code

                else:
                    response_data = {
                        "error": "Account_Number or Account_Type_Code or Account_Currency_Code is not passed",
                        "data_passed": request_data
                    }
                    response_code = HTTP_400_BAD_REQUEST
                    logger.error('Request = ( '  + str(request_data) + ' )|Response = ( ' + str(response_data) + ',' + str(response_code) + ' )')
                    return jsonify(response_data), response_code

            else:
                response_data = {"error": "Data passed is not json type"}
                response_code = HTTP_403_FORBIDDEN
                logger.error('Request = ( '  + str(request_data) + ' )|Response = ( ' + str(response_data) + ',' + str(response_code) + ' )')
                return jsonify(response_data), response_code

        response_data = {'error': 'Authentication token is wrong'}
        response_code = HTTP_404_NOT_FOUND
        logger.error('Request = ( '  + str(request_data) + ' )|Response = ( ' + str(response_data) + ',' + str(response_code) + ' )')
        return jsonify(response_data), response_code

    except Exception as e:
        response_data = {"error": e}
        response_code = HTTP_400_BAD_REQUEST
        logger.error('Request = ( '  + str(request_data) + ' )|Response = ( ' + str(response_data) + ',' + str(response_code) + ' )')
        return jsonify(response_data), response_code
