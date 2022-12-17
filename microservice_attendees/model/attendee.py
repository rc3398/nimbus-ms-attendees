from marshmallow import Schema, fields, post_load
from marshmallow_enum import EnumField
from enum import Enum

class Attendee(object):
    def __init__(self, first_name, last_name, gender, 
                 email_address, birth_date, phone):
        self.attendee_id = email_address
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
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
    
    first_name = fields.Str()
    last_name = fields.Str()
    email_address = fields.Str()
    birth_date = fields.Str()
    phone = fields.Str()
    gender = EnumField(Gender, by_value=True)
    attendee_id = fields.Str()
    
    @post_load
    def get_attendee(self, data, **kwargs):
        return Attendee(**data)