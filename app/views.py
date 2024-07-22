import os, sys

from flask import request, json, current_app
from flask_login import current_user, login_user, logout_user, login_required

sys.path.append(os.path.join(os.path.dirname(__file__), 'database'))

from database.users import *
from database.todos import *
import database.items as dbitems
import database.projects as dbprojects
import database.containers as dbcontainers
from extensions import bcrypt

@current_app.route('/todos/items', methods=['POST'])
def handleItemsRequests():
    data = request.json
    subject = data.get('operation_type')
    user_id = current_user.id
    if subject == 'update_content':
        response = {
            'updated' : None
        }
        item_id = data.get('id')
        item_id = int(item_id)
        new_content = data.get('new_content')
        #print(f'ITEM_ID : {item_id}\ntype: {type(item_id)}\nnew_content: {new_content}\ntype: {type(new_content)}\n')
        if dbitems.userOwnsItem(user_id, item_id) == True:
            dbitems.updateItemContent(item_id, new_content)
            response['updated'] = True
        else:
            response['updated'] = False
    if subject == 'new_item':
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

@login_required
@current_app.route('/todos/items', methods=['DELETE'])
def handleItemsDelete():
    data = request.json
    response = {
        'deleted' : None
    }
    if dbitems.userOwnsItem(current_user.id, data.get('id')) == True:
        response['deleted'] = True
        dbitems.removeItemIdFromProjects(data.get('id')) # this doesn't look safe at all lmao
    else:
        response['deleted'] = False
    return json.dumps(response)

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
        response = {}
        data = request.json
        new_title = data.get('new_title')
        if dbprojects.userOwnsProject(current_user.id, project_id) == True:
            dbprojects.updateProjectTitle(project_id, new_title)
            response['updated'] = True
        else:
            response['updated'] = False
        return response

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
    response = {}
    data = request.json
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

@login_required
@current_app.route('/todos/projects/<project_id>/item_order', methods=['PUT'])
def RESTProjectNewItemOrder(project_id):
    response = {
        'updated' : None
    }
    data = request.json
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
    data = request.json
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

@current_app.route('/users/login', methods=['POST'])
def loginPost():
    response = {
        'login_successful' : None,
        'error' : False
        }
    data = request.json
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