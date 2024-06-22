from flask import request, json, current_app
from flask_login import current_user, login_user, logout_user

from database.users import *


@current_app.route('/users/login', methods=['POST'])
def loginPost():
    response = {
        'login_successful' : None,
        'error' : False
        }
    data = request.json
    username = data.get('username')
    password = data.get('password')
    attempt = checkIfUserPasswordIsCorrect(username, password)
    print(f'ATTEMPT = {attempt}')
    if attempt == True:
        response['login_successful'] = True
        response['error'] = None
        user = getUserFromUsername(username)
        login_user(user)
    elif attempt == False:
        pass
    return json.dumps(response)

@current_app.route('/users/has_token', methods=['GET'])
def hasToken():
    response = {
        'username' : None,
        'has_token' : None
    }
    if current_user.is_authenticated == True:
        response['username'] = current_user.username
        response['has_token'] = True
    else:
        response['username'] = None
        response['has_token'] = False
        print(f"RESPONSE: {response}")
    return json.dumps(response)

@current_app.route('/users/logout', methods=['POST'])
def logoutPost():
    response = { 'success' : None}
    if current_user.is_authenticated == True:
        logout_user()
        response['success'] = True
    elif current_user.is_authenticated == False:
        response['success'] == False
    else:
        raise ValueError('current_user.is_authenticated has an invalid value')
    return json.dumps(response)