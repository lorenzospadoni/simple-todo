from flask import current_app
from flask_login import login_user, logout_user, current_user, login_required
from extensions import login_manager, bcrypt
import database.users as dbusers

login_manager.init_app(current_app)

@login_manager.user_loader
def loadUser(user_id: str):
    user = dbusers.getUserFromId(int(user_id))
    return user