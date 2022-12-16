from marshmallow import Schema, fields, post_load

class User(object):
    def __init__(self, user_id, first_name, last_name, gender, 
                 email_address, birth_date, phone):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.birth_date = birth_date
        self.phone = phone
        
    def __repr__(self):
        return '<User(name={self.input_index!r})>'.format(self=self)
    
class UserSchema(Schema):
    user_id = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    email_address = fields.Str()
    birth_date = fields.Str()
    phone = fields.Str()
    
    @post_load
    def get_user(self, data, **kwargs):
        return User(**data)