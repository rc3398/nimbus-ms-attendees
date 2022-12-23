from marshmallow import Schema, fields, post_load
from marshmallow_enum import EnumField
from enum import Enum

class Attendee(object):
    def __init__(self, attendee_id,first_name, last_name, gender, 
                 email_address, birth_date, phone):
        email = str.lower(email_address)
        self.attendee_id = attendee_id
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email
        self.birth_date = birth_date
        self.phone = phone
        self.gender = gender
        
    def __repr__(self):
        return '<attendee(name={self.input_index!r})>'.format(self=self)
    
class AttendeeSchema(Schema):
      # class Meta:
      #     fields = ('attendee_id', 'first_name', 'last_name', 'email_address', 'birth_date', 'phone', 'gender')
      
    class Gender(Enum):
        MALE = 1
        FEMALE = 2
        OTHER = 3
    
    attendee_id = fields.Str(required=False)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email_address = fields.Email(required=True)
    birth_date = fields.Str(required=True)
    phone = fields.Str(required=True)
    gender = EnumField(Gender, by_value=False, required=True)
    
    @post_load
    def get_attendee(self, data, **kwargs):
        return Attendee(**data)