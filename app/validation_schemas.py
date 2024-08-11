from marshmallow import Schema, fields, ValidationError
        
class UserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class NewItemSchema(Schema):
    parent_project = fields.Int(required=True)

class NewContentSchema(Schema):
    new_content = fields.Str(required=True)

class NewProjectTitleSchema(Schema):
    new_title = fields.Str(required=True)

class NewProjectOrderSchema(Schema):
    project_order = fields.List(fields.Int, required=True)

class NewItemOrderSchema(Schema):
    operation_type = fields.Str(required=False)
    item_order = fields.List(fields.Int, required=True)


user_schema = UserSchema()
new_item_schema = NewItemSchema()
new_content_schema = NewContentSchema()
new_project_title_schema = NewProjectTitleSchema()
new_project_order_schema = NewProjectOrderSchema()
new_item_order_schema = NewItemOrderSchema()

#user_schema = UserSchema()