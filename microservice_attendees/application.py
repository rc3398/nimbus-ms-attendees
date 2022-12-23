import json, sentry_sdk, copy
from flask import Flask, Response, request,  abort, jsonify, session
from flask_restx import Resource, Api, fields, inputs
from datetime import datetime
from email_validator import validate_email, EmailNotValidError
from marshmallow import (ValidationError, Schema, post_load )
from nimbus_attendees import Nimbus_Attendees
from model.attendee import Attendee, AttendeeSchema
from flask_cors import CORS
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk import capture_exception
from werkzeug.middleware.proxy_fix import ProxyFix
from marshmallow_enum import EnumField
from flask_marshmallow import Marshmallow
from enum import Enum
from flask_jwt_extended import ( jwt_required, current_user, get_jwt_identity, JWTManager )
from auth_utils import NimbusJWT_Authentication

# Create the Flask application object.
application = app = Flask(__name__,
                          static_url_path='/',
                          static_folder='static/class-ui/',
                          template_folder='web/templates')
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', 
          title='Nimbus Attendees API',
          description='Nimbus APIs for Attendee CRUD operations',
          default='ms-attendees',
          default_label='ms-attendees',
)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)
# print(vars(jwt))
CORS(app)
ma = Marshmallow(app)

# TODO: Add caching
# TODO: store these constants in a shared file
CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_PLAIN_TEXT = "text/plain"


sentry_sdk.init(
    dsn="https://e5b945e2a05647c3bcb9fe454e7b6249@o4504313332170752.ingest.sentry.io/4504369353326592",
    traces_sample_rate=1.0,
    integrations=[
        FlaskIntegration(),
    ]
)


# TODO: add middleware to check if requestor is authorized to make this call
"""
TODO: Add Middleware
- @before_request : social login OIDC IAM GOOGL,
- @after_request 

@app.before_request
def before_request_func():
    print("BEFORE_REQUEST executing!")
    print("Request = ", json.dumps(request, indent=2, default=str))

@app.after_request
def after_request_func():
    print("AFTER_REQUEST executing!")
    print("Request = ", json.dumps(response, indent=2, default=str))
    sns_middleware.check_publish(request, response)
    return response

"""

attendee_model = api.model('Attendee', {
    'uid': fields.String(required=False, description="Attendee ID. Omitted for Create, Update."),
    'first_name': fields.String(description=""),
    'last_name': fields.String(description=""),
    'email_address': fields.String(description=""),
    'birth_date': fields.String(description="YYYY-MM-DD"),
    'phone': fields.String(description="XXX-XXX-XXXX"),
    'gender': fields.String(description="[MALE, FEMALE, OTHER]"),
})

@api.route("/<string:uid>", endpoint='attendees_resource')
class Attendees(Resource):

    @api.doc(id='Get attendee by uid', params={'uid': 'Attendee ID'})
    @api.doc(responses={
        200: 'Success',
        404: 'Not Found',
        500: 'Internal Server Error'
    })
    @NimbusJWT_Authentication.id_token_required()
    def get(self, uid: str) -> Response:
        auth_header = request.headers['Authorization']
        print(auth_header)
        # user_id = get_jwt_identity()
        # print(vars(user_id))
        print(f'Input is: {uid}')
        
        db_result = Nimbus_Attendees.get_attendee_by_uid(uid)
        
        attendee_schema_response = AttendeeSchemaResponse(many=False) 
        #print(f'This is our resp: {attendee_schema_response.dumps(db_result,default=str)}')
        if db_result:
            response = Response(attendee_schema_response.dumps(db_result,default=str), status=200,
                                content_type=CONTENT_TYPE_JSON)
        else:
            response = Response("NOT FOUND", status=404,
                                content_type=CONTENT_TYPE_PLAIN_TEXT)
        return response


    @api.doc(id='Update attendee by uid', params={'uid': 'Attendee ID'}, body=attendee_model)
    # @api.expect(resource_fields)
    @api.doc(responses={
        200: 'Success',
        404: 'Not Found',
        500: 'Internal Server Error'
    })
    @jwt_required()
    def put(self, uid):
        json_input = request.get_json()
        print(f'Input is: {json_input}')
        if not json_input:
            return {"message": "No input data provided"}, 400
        # Validate and deserialize input
        try:
            attendee_schema = AttendeeSchema(many=False)
            up_attendee = attendee_schema.load(json_input)
            print(str(up_attendee.gender))
            if 'Female'.lower() in str(up_attendee.gender).lower():
                up_attendee.gender = 'Female'
            elif 'Male'.lower() in str(up_attendee.gender).lower():
                up_attendee.gender = 'Male'
            else:
                up_attendee.gender = 'Other'
            
            print(up_attendee.gender)
            is_email = validate_the_email(up_attendee.email_address)

        except ValidationError as err:
            capture_exception(err)
            return {"errors": err.messages}, 422
    
        db_result = Nimbus_Attendees.update_attendee_by_uid(uid,up_attendee)
        
        if db_result != 0:
            response = Response(attendee_schema.dumps(db_result), status=200,
                                content_type=CONTENT_TYPE_JSON)
        else:
            response = Response(f'Invalid Input: Could not update attendee {uid}', status=500,
                            content_type=CONTENT_TYPE_PLAIN_TEXT)
        return response






    @api.doc(id='Delete attendee by uid', params={'uid': 'Attendee ID'})
    @api.doc(responses={
        200: 'Success',
        404: 'Not Found',
        500: 'Internal Server Error'
    })
    @jwt_required()
    def delete(self, uid):
        print(f'Input is: {uid}')
        result = Nimbus_Attendees.delete_attendee_by_uid(uid) 
        if result:
            response = Response(json.dumps(result,default=str), status=200,
                                content_type=CONTENT_TYPE_JSON)
        else:
            response = Response("NOT FOUND", status=404,
                                content_type=CONTENT_TYPE_PLAIN_TEXT)
        return response


@api.route("/attendees-list", endpoint='attendees_list')
class AttendeesList(Resource):
    attendee_model_create = copy.copy(attendee_model)
    del attendee_model_create['uid']
    @api.doc(id='Create new attendee', body=attendee_model_create)
    @api.doc(responses={
        202: 'Created',
        422: 'Validation Error',
        500: 'Server Error'
    })
    def post(self) -> Response:
        json_input = request.get_json()
        print(f'Input is: {json_input}')
        
        if not json_input:
            return {"message": "No input data provided"}, 400
        try:
            attendee_schema = AttendeeSchema(many=False)
            new_attendee = attendee_schema.load(json_input)
            print(vars(new_attendee))
            is_email = validate_the_email(new_attendee.email_address)

        except ValidationError as err:
            capture_exception(err)
            return {"errors": err.messages}, 422
        
        db_result = Nimbus_Attendees.create_attendee(new_attendee)
        
        if db_result:
          response = Response(attendee_schema.dumps(db_result), status=201,
                            content_type=CONTENT_TYPE_JSON)
        else:
            response = Response("Invalid Input: Could not create attendee", status=500,
                                content_type=CONTENT_TYPE_PLAIN_TEXT)
        return response
    
    
    # TODO: Add pagination 
    #@api.doc(id='Get list of attendees, PAGINATED')
    #@api.marshal_list_with(attendee_model)
    @api.doc(responses={
        200: 'Success',
        500: 'Internal Server Error'
    })
    @jwt_required()
    def get(self):
        print(f'Input is: ')
        db_result = Nimbus_Attendees.get_all_attendees()
        #print(db_result) 
        print(json.dumps(db_result,default=str))
        print('attend schema response')
        attendee_schema_response = AttendeeSchemaResponse(many=True)
        print(f'This is our resp attendee schema: {attendee_schema_response.dumps(db_result,default=str)}')
        if db_result:
            response = Response(json.dumps(db_result,default=str), status=200,
                                content_type=CONTENT_TYPE_JSON)
        else:
            response = Response("ERROR", status=500,
                                content_type=CONTENT_TYPE_PLAIN_TEXT)
        return response


class AWS_Exception(Exception):
    status_code = 500
    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
    
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@app.errorhandler(AWS_Exception)
def aws_exception(e):
    return jsonify(e.to_dict()), e.status_code


def validate_the_email(email_address):
    try:
        is_email = validate_email(email_address, check_deliverability=False)
        print(vars(is_email))
        return is_email
    except EmailNotValidError as e:
        print(str(e))
        capture_exception(e)
        raise(e)


class AttendeeSchemaResponse(Schema):
    class Meta:
        fields = ('attendee_id', 'first_name', 'last_name', 'email_address', 'birth_date', 'phone', 'gender','_links')
    #print(ma)
    _links = ma.Hyperlinks(
        {"collection": ma.URLFor('attendees_list'),
         "self":ma.URLFor('attendees_resource',uid='<attendee_id>')} 
    )


if __name__ == '__main__':
    app.run(host='localhost', port=5021, debug=False)