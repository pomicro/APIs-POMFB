from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.constants.code_constants import ACCOUNT_BANK_IMD_CODE_LENGTH, ACCOUNT_CURRENCY_CODE_LENGTH, ACCOUNT_NUMBER_LENGTH, ACCOUNT_TYPE_CODE_LENGTH
from src.constants.http_status_codes import API_210_RESPONSE_CODE, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from src.database import User
from flasgger import swag_from
from src.logging.logs import logger

title_fetch = Blueprint("title_fetch", __name__, url_prefix="/TitleFetch")

@title_fetch.get('/')
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

@title_fetch.post('/')
@jwt_required()
@swag_from('./docs/title_fetch.yaml')
def return_title():

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
                if request.json.get('Account_Bank_IMD_Code') and request.json.get('Account_Number') and request.json.get('Account_Type_Code') and request.json.get('Account_Currency_Code') and request.json.get('Transaction_Amount'):
                    #print("available")
                    account_bank_imd_code = request.json.get('Account_Bank_IMD_Code')
                    account_number = request.json.get('Account_Number')
                    account_type_code = request.json.get('Account_Type_Code')
                    account_currency_code = request.json.get('Account_Currency_Code')
                    transaction_amount = request.json.get('Transaction_Amount')
                    response_code = HTTP_400_BAD_REQUEST

                    if (len(str(account_bank_imd_code))!=ACCOUNT_BANK_IMD_CODE_LENGTH) or (type(account_bank_imd_code) is not str):
                        response_data = {'error': "Account_Bank_IMD_Code is too short or too long or is not str, it must be of length " + str(ACCOUNT_BANK_IMD_CODE_LENGTH) + " of type string"}
                        logger.error('Request = ( '  + str(request_data) + ' )|Response = ( ' + str(response_data) + ',' + str(response_code) + ' )')
                        return jsonify(response_data), response_code

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

                    if (type(transaction_amount) is not int):
                        response_data = {'error': "Transaction_Amount is not int, it must be of type integer"}
                        logger.error('Request = ( '  + str(request_data) + ' )|Response = ( ' + str(response_data) + ',' + str(response_code) + ' )')
                        return jsonify(response_data), response_code

                    #
                    #Code to retrieve account_title, bank_name and branch_name
                    #

                    account_title = "Mr. Demo Example" #Change this to the value retrieved from database
                    bank_name = "Pak Oman Microfinance Bank Limited" #Change this to the value retrieved from database
                    branch_name = "Head Office, Karachi" #Change this to the value retrieved from database

                    response_data = {
                        "Account_Bank_IMD_Code": account_bank_imd_code,
                        "Account_Number": account_number,
                        "Account_Type_Code": account_type_code,
                        "Account_Currency_Code": account_currency_code,
                        "Transaction_Amount": transaction_amount,
                        "Account_Title": account_title,
                        "Bank_Name": bank_name,
                        "Branch_Name": branch_name
                    }
                    response_code = API_210_RESPONSE_CODE
                    logger.info('Request = ( '  + str(request_data) + ' )|Response = ( ' + str(response_data) + ',' + str(response_code) + ' )')
                    return jsonify(response_data), response_code

                else:
                    response_data = {
                        "error": "Account_Bank_IMD_Code or Account_Number or Account_Type_Code or Account_Currency_Code or Transaction_Amount is not passed or is invalid",
                        "data_passed": request.json
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
