from marshmallow import Schema, fields, post_load

class Attendee(object):
    def __init__(self, attendee_id, first_name, last_name, gender, 
                 email_address, birth_date, phone):
        self.attendee_id = attendee_id
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.birth_date = birth_date
        self.phone = phone
        self.gender = gender
        
    def __repr__(self):
        return '<attendee(name={self.input_index!r})>'.format(self=self)
    
class AttendeeSchema(Schema):
    attendee_id = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    email_address = fields.Str()
    birth_date = fields.Str()
    phone = fields.Str()
    gender = fields.Enum()
    
    @post_load
    def get_attendee(self, data, **kwargs):
        return Attendee(**data)