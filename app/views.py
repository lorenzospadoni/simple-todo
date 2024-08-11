import os, sys

from flask import request, json, current_app
from flask_login import current_user, login_user, logout_user, login_required
from marshmallow import Schema, fields, ValidationError

sys.path.append(os.path.join(os.path.dirname(__file__), 'database'))

from database.users import *
from database.todos import *
import database.items as dbitems
import database.projects as dbprojects
import database.containers as dbcontainers
from extensions import bcrypt
from validation_schemas import *

@login_required
@current_app.route('/todos/items/<item_id>', methods=['PUT'])
def RESTNewContent(item_id):
    try:
        response = {}
        data = new_content_schema.load(request.json)
        if dbitems.userOwnsItem(current_user.id, item_id) == True:
            dbitems.updateItemContent(item_id, data.get('new_content'))
            response['updated'] = True
        else:
            response['updated'] = False
        return json.dumps(response)
    except ValidationError as err:
        return json.dumps({'[ERROR]': err.messages}), 400 # 400: bad request

@login_required
@current_app.route('/todos/items/<item_id>', methods=['DELETE'])
def RESTDeleteItem(item_id):
    response = {}
    data = request.json
    if dbitems.userOwnsItem(current_user.id, item_id) == True:
        dbitems.deleteItem(item_id)
        dbitems.removeItemIdFromProjects(item_id)
        response['deleted'] = True
    else:
        response['deleted'] = False
    return json.dumps(response)

@current_app.route('/todos/items/new', methods=['POST'])
def handleNewItemsRequests():
    try:
        data = new_item_schema.load(request.json)
        #subject = data.get('operation_type')
        user_id = current_user.id
        response = {
            'item_id' : None,
            'created' : True
        }
        project_id = int(data.get('parent_project'))
        if dbprojects.userOwnsProject(user_id, project_id) == True:
            item_id = dbitems.insertItem(user_id, '')
            dbitems.appendItemToProjectChildren(item_id, project_id)
            response['item_id'] = item_id
            response['created'] = True
        else:
            response['item_id'] = None
            response['created'] = True
        return json.dumps(response)
    except ValidationError as err:
        return json.dumps({'[ERROR]': err.messages}), 400 # 400: bad request        

@login_required
@current_app.route('/todos/projects/new', methods=['POST'])
def RESTHandleNewProject():
    response = {

    }
    data = request.json
    #project_id = data.get('project_id')
    position = dbprojects.getBiggestPosition(current_user.id) + 1
    project_id = dbprojects.insertProject(current_user.id, '', [], position)
    response['project_id'] = project_id
    return response

@login_required
@current_app.route('/todos/projects/<project_id>', methods=['PUT'])
def RESTProjectNewTitle(project_id):
    try:
        response = {}
        data = new_project_title_schema.load(request.json)
        new_title = data.get('new_title')
        if dbprojects.userOwnsProject(current_user.id, project_id) == True:
            dbprojects.updateProjectTitle(project_id, new_title)
            response['updated'] = True
        else:
            response['updated'] = False
        return response
    except ValidationError as err:
        return json.dumps({'[ERROR]': err.messages}), 400 # 400: bad request    

@login_required
@current_app.route('/todos/projects/<project_id>', methods=['DELETE'])
def RESTDeleteProjectRequest(project_id):
    response = {}
    data = request.json
    project_id = project_id

    if dbprojects.userOwnsProject(current_user.id, project_id) == True:
        dbprojects.deleteProjectItems(project_id)
        dbprojects.deleteProject(project_id)
        response['deleted'] = True
    else:
        response['deleted'] = False
    return response

@login_required
@current_app.route('/todos/projects/project_order', methods=['PUT'])
def RESTnewProjectOrder():
    try:
        response = {}
        data = new_project_order_schema.load(request.json)
        project_order = data.get('project_order')
        counter = 0
        if userOwnsProjects(current_user.id, project_order) == True:
            for project_id in project_order:
                counter = counter + 1
                dbprojects.updateProjectPosition(project_id, counter)
                response['updated'] = True
        elif userOwnsProjects(current_user.id, project_order) == True:
            response['updated'] = False
        return json.dumps(response)
    except ValidationError as err:
        return json.dumps({'[ERROR]': err.messages}), 400 # 400: bad request    

@login_required
@current_app.route('/todos/projects/<project_id>/item_order', methods=['PUT'])
def RESTProjectNewItemOrder(project_id):
    try:
        response = {
            'updated' : None
        }
        print(f'''request.json: {request.json}
              type: {type(request.json)}
                item_order: {request.json.get('item_order')}
item_order type: {type(request.json.get('item_order'))}
item_order items: {type(request.json.get('item_order')[0])}''')
        data = new_item_order_schema.load(request.json)
        item_order = data.get('item_order')
        #item_order = json.loads(item_order)
        user_owns_items = userOwnsItems(current_user.id, item_order)
        if userOwnsProject(current_user.id, project_id) == True and user_owns_items == True:
            if dbitems.setNewItemOrder(project_id, item_order) == True:
                response['updated'] = True
            else:
                response['updated'] = False
        else:
            response['updated'] = False
        return json.dumps(response)
    except ValidationError as err:
        return json.dumps({'[ERROR]': err.messages}), 400 # 400: bad request    


@login_required
@current_app.route('/todos', methods=['GET'])
def getTodos():
    # response = [
    #     {   'id' : 3,
    #         'title' : 'Saluti nel mondo',
    #         'children' : [
    #             {'id' : 3, 'content' : 'Ciao'},
    #             {'id' : 4, 'content' : 'Hello'},
    #             {'id' : 5, 'content' : 'Bojour'}
    #             ]
    #     }
    # ]
    if current_user.is_authenticated == True:
        projects = dbprojects.fetchProjectsFromUserId(current_user.id)
        projects = dbprojects.convertProjectCollectionToList(projects)
    else:
        projects = []
    response = json.dumps(projects)
    return json.dumps(response)

@current_app.route('/users/<username>', methods=['GET'])
def getUser(username):
    response = {}
    response['username'] = username
    response['available'] = usernameAvailable(username)
    response = json.dumps(response)
    return response

@current_app.route('/users/register', methods=['POST'])
def registerPost():
    try:
        data = user_schema.load(request.json)
        response = {
            'username' : data.get('username'),
            'success' : None
        }
        username_available = usernameAvailable(data.get('username'))
        if username_available == True:
            hashed_password = bcrypt.generate_password_hash(data.get('password'))
            insertUser(data.get('username'), hashed_password, True)
            response['success'] = True
        elif username_available == False:
            response['success'] = False
        return json.dumps(response)
    
    except ValidationError as err:
        return json.dumps({'[ERROR]': err.messages}), 400 # 400: bad request

@current_app.route('/users/login', methods=['POST'])
def loginPost():
    try:
        response = {
            'login_successful' : None,
            'error' : False
            }
        data = user_schema.load(request.json)
        username = data.get('username')
        password = data.get('password')
        hashed_password = getPasswordFromUsername(username)
        hashed_password = bcrypt.generate_password_hash(password)

        attempt = bcrypt.check_password_hash(hashed_password, password)

        if attempt == True:
            response['login_successful'] = True
            response['error'] = None
            user = getUserFromUsername(username)
            login_user(user)
        elif attempt == False:
            response['login_successful'] = False
            response['error'] = None
        return json.dumps(response)
    except ValidationError as err:
        return json.dumps({'error', err.messages}), 400 # 400: bad request

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

@current_app.route('/users/current_user/data', methods=['GET'])
def userDataGet():
    user_data = {
        'username' : None,
        'date_of_subscription': None,
        'logged_in': None
    }
    if current_user.is_anonymous == True:
        user_data['logged_in'] = False
    elif current_user.is_anonymous == False:
        user_data['username'] = current_user.username
        user_data['date_of_subscription'] = current_user.date_of_subscription
        user_data['logged_in'] = True
    else:
        raise ValueError('current_user.is_anonymous is nor True nor False')
    return json.dumps(user_data)

#TODO: finish this:
@current_app.route('/users/unsubscribe', methods=['GET'])
def unsubscribeUser():
    if current_user.is_authenticated == True:
        deleteUserFromId(current_user.id)
        return
    return