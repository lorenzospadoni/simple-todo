from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from validation_schemas import UserSchema, NewItemSchema, NewContentSchema, NewProjectTitleSchema

login_manager = LoginManager()
bcrypt = Bcrypt()
cors = CORS()
