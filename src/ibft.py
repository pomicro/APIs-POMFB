from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.constants.code_constants import ACCOUNT_BANK_IMD_CODE_LENGTH, ACCOUNT_CURRENCY_CODE_LENGTH, ACCOUNT_NUMBER_LENGTH, ACCOUNT_TYPE_CODE_LENGTH
from src.constants.http_status_codes import API_210_RESPONSE_CODE, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from src.database import User
from flasgger import swag_from
from src.logging.logs import logger

ibft = Blueprint("ibft", __name__, url_prefix="/IBFT")

@ibft.get('/')
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
    logger.error('Response: ' + str(response_data) + ',' + str(response_code))
    return jsonify(response_data), response_code

@ibft.post('/')
@jwt_required()
@swag_from('./docs/ibft.yaml')
def process_ibft():

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
                if request.json.get('From_Account_Bank_IMD_Code') and request.json.get('From_Account_Number') and request.json.get('From_Account_Type_Code') and request.json.get('From_Account_Currency_Code') and request.json.get('To_Account_Bank_IMD_Code') and request.json.get('To_Account_Number') and request.json.get('To_Account_Type_Code') and request.json.get('To_Account_Currency_Code') and request.json.get('Transaction_Amount') and request.json.get('Transaction_Currency_Code') and request.json.get('Transaction_Fee') and request.json.get('Length_Of_Narration') and request.json.get('Transaction_Narration'):
                    #print("available")
                    from_account_bank_imd_code = request.json.get('From_Account_Bank_IMD_Code')
                    from_account_number = request.json.get('From_Account_Number')
                    from_account_type_code = request.json.get('From_Account_Type_Code')
                    from_account_currency_code = request.json.get('From_Account_Currency_Code')
                    to_account_bank_imd_code = request.json.get('To_Account_Bank_IMD_Code')
                    to_account_number = request.json.get('To_Account_Number')
                    to_account_type_code = request.json.get('To_Account_Type_Code')
                    to_account_currency_code = request.json.get('To_Account_Currency_Code')
                    transaction_amount = request.json.get('Transaction_Amount')
                    transaction_currency_code = request.json.get('Transaction_Currency_Code')
                    transaction_fee = request.json.get('Transaction_Fee')
                    length_of_narration = request.json.get('Length_Of_Narration')
                    transaction_narration = request.json.get('Transaction_Narration')
                    response_code = HTTP_400_BAD_REQUEST
                    
                    if (len(str(from_account_bank_imd_code))!=ACCOUNT_BANK_IMD_CODE_LENGTH) or (type(from_account_bank_imd_code) is not str):
                        response_data = {'error': "From_Account_Bank_IMD_Code is too short or too long or is not str, it must be of length " + str(ACCOUNT_BANK_IMD_CODE_LENGTH) + " of type string"}
                        logger.error('Request = ( '  + str(request_data) + ' )|Response = ( ' + str(response_data) + ',' + str(response_code) + ' )')
                        return jsonify(response_data), response_code

                    if (len(str(from_account_number))!=ACCOUNT_NUMBER_LENGTH) or (type(from_account_number) is not str):
                        response_data = {'error': "Account_Number is too short or too long or is not str, it must be of length " + str(ACCOUNT_NUMBER_LENGTH) + " of type string"}
                        logger.error('Request = ( '  + str(request_data) + ' )|Response = ( ' + str(response_data) + ',' + str(response_code) + ' )')
                        return jsonify(response_data), response_code

                    if (len(str(from_account_type_code))!=ACCOUNT_TYPE_CODE_LENGTH) or (type(from_account_type_code) is not int):
                        response_data = {'error': "Account_Type_Code is too short or too long or is not int, it must be of length " + str(ACCOUNT_TYPE_CODE_LENGTH) + " of type integer"}
                        logger.error('Request = ( '  + str(request_data) + ' )|Response = ( ' + str(response_data) + ',' + str(response_code) + ' )')
                        return jsonify(response_data), response_code

                    if (len(str(from_account_currency_code))!=ACCOUNT_CURRENCY_CODE_LENGTH) or (type(from_account_currency_code) is not int):
                        response_data = {'error': "Account_Currency_Code is too short or too long or is not int, it must be of length " + str(ACCOUNT_CURRENCY_CODE_LENGTH) + " of type integer"}
                        logger.error('Request = ( '  + str(request_data) + ' )|Response = ( ' + str(response_data) + ',' + str(response_code) + ' )')
                        return jsonify(response_data), response_code

                    if (len(str(to_account_bank_imd_code))!=ACCOUNT_BANK_IMD_CODE_LENGTH) or (type(to_account_bank_imd_code) is not str):
                        response_data = {'error': "Account_Bank_IMD_Code is too short or too long or is not str, it must be of length " + str(ACCOUNT_BANK_IMD_CODE_LENGTH) + " of type string"}
                        logger.error('Request = ( '  + str(request_data) + ' )|Response = ( ' + str(response_data) + ',' + str(response_code) + ' )')
                        return jsonify(response_data), response_code

                    if (len(str(to_account_number))!=ACCOUNT_NUMBER_LENGTH) or (type(to_account_number) is not str):
                        response_data = {'error': "Account_Number is too short or too long or is not str, it must be of length " + str(ACCOUNT_NUMBER_LENGTH) + " of type string"}
                        logger.error('Request = ( '  + str(request_data) + ' )|Response = ( ' + str(response_data) + ',' + str(response_code) + ' )')
                        return jsonify(response_data), response_code

                    if (len(str(to_account_type_code))!=ACCOUNT_TYPE_CODE_LENGTH) or (type(to_account_type_code) is not int):
                        response_data = {'error': "Account_Type_Code is too short or too long or is not int, it must be of length " + str(ACCOUNT_TYPE_CODE_LENGTH) + " of type integer"}
                        logger.error('Request = ( '  + str(request_data) + ' )|Response = ( ' + str(response_data) + ',' + str(response_code) + ' )')
                        return jsonify(response_data), response_code

                    if (len(str(to_account_currency_code))!=ACCOUNT_CURRENCY_CODE_LENGTH) or (type(to_account_currency_code) is not int):
                        response_data = {'error': "Account_Currency_Code is too short or too long or is not int, it must be of length " + str(ACCOUNT_CURRENCY_CODE_LENGTH) + " of type integer"}
                        logger.error('Request = ( '  + str(request_data) + ' )|Response = ( ' + str(response_data) + ',' + str(response_code) + ' )')
                        return jsonify(response_data), response_code

                    if (type(transaction_amount) is not int):
                        response_data = {'error': "Transaction_Amount is not int, it must be of type integer"}
                        logger.error('Request = ( '  + str(request_data) + ' )|Response = ( ' + str(response_data) + ',' + str(response_code) + ' )')
                        return jsonify(response_data), response_code

                    if (len(str(transaction_currency_code))!=ACCOUNT_CURRENCY_CODE_LENGTH) or (type(transaction_currency_code) is not int):
                        response_data = {'error': "Account_Currency_Code is too short or too long or is not int, it must be of length " + str(ACCOUNT_CURRENCY_CODE_LENGTH) + " of type integer"}
                        logger.error('Request = ( '  + str(request_data) + ' )|Response = ( ' + str(response_data) + ',' + str(response_code) + ' )')
                        return jsonify(response_data), response_code
                    
                    if (type(transaction_fee) is not int):
                        response_data = {'error': "Transaction_Fee is not int, it must be of type integer"}
                        logger.error('Request = ( '  + str(request_data) + ' )|Response = ( ' + str(response_data) + ',' + str(response_code) + ' )')
                        return jsonify(response_data), response_code

                    if (type(length_of_narration) is not int):
                        response_data = {'error': "Length_Of_Narration is not int, it must be of type integer"}
                        logger.error('Request = ( '  + str(request_data) + ' )|Response = ( ' + str(response_data) + ',' + str(response_code) + ' )')
                        return jsonify(response_data), response_code

                    if (type(transaction_narration) is not str):
                        response_data = {'error': "Transaction_Narration is not str, it must be of type string"}
                        logger.error('Request = ( '  + str(request_data) + ' )|Response = ( ' + str(response_data) + ',' + str(response_code) + ' )')
                        return jsonify(response_data), response_code

                    #
                    #Code to process IBFT
                    #

                    response_data = {
                        "From_Account_Bank_IMD_Code": from_account_bank_imd_code,
                        "From_Account_Number": from_account_number,
                        "From_Account_Type_Code": from_account_type_code,
                        "From_Account_Currency_Code": from_account_currency_code,
                        "To_Account_Bank_IMD_Code": to_account_bank_imd_code,
                        "To_Account_Number": to_account_number,
                        "To_Account_Type_Code": to_account_type_code,
                        "To_Account_Currency_Code": to_account_currency_code,
                        "Transaction_Amount": transaction_amount,
                        "Transaction_Currency_Code": transaction_currency_code,
                        "Transaction_Fee": transaction_fee,
                        "Length_Of_Narration": length_of_narration,
                        "Transaction_Narration": transaction_narration
                    }
                    response_code = API_210_RESPONSE_CODE
                    logger.info('Request = ( '  + str(request_data) + ' )|Response = ( ' + str(response_data) + ',' + str(response_code) + ' )')
                    return jsonify(response_data), response_code

                else:
                    response_data = {
                        "error": "From_Account_Bank_IMD_Code or From_Account_Number or From_Account_Type_Code or From_Account_Currency_Code or To_Account_Bank_IMD_Code or To_Account_Number or To_Account_Type_Code or To_Account_Currency_Code or Transaction_Amount or Transaction_Currency_Code or Transaction_Fee or Length_Of_Narration or Transaction_Narration is not passed or is invalid",
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
