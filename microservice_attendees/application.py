from flask import Flask, Response, request,  abort, jsonify, session
from datetime import datetime
#from flask_marshmallow import Marshmallow
#from flask_sqlalchemy import SQLAlchemy
from nimbus_attendees import Nimbus_Attendees
from model.attendee import Attendee, AttendeeSchema
from flask_cors import CORS
import json
# import rds_db as db

# Create the Flask application object.
application = app = Flask(__name__,
                          static_url_path='/',
                          static_folder='static/class-ui/',
                          template_folder='web/templates')
CORS(app)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/db_name'
#db = SQLAlchemy(app)
#ma = Marshmallow(app)

# TODO: Add caching

# TODO: store these constants in a shared file
CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_PLAIN_TEXT = "text/plain"

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

CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_PLAIN_TEXT = "text/plain"


@app.route("/attendees", methods=["POST"])
def create_attendee(attendee):
    
    # TODO: store this in an object ORM
    print(f'Input is: {attendee}')
    first_name = json.request['first_name']
    last_name = json.request['last_name']
    gender = json.request['gender']
    gender = str.upper(gender)
    birth_date = json.request['birth_date']
    phone = json.request['phone']
    email_address = json.request['email_address']
    attendee_id = email_address
    
    new_attendee = Attendee(first_name, last_name, gender, email_address, birth_date, phone, attendee_id)
    
    db_result = Nimbus_Attendees.create_attendee(new_attendee)
    
    if db_result:
      response = Response(AttendeeSchema.dumps(db_result), status=200,
                        content_type=CONTENT_TYPE_JSON)
    else:
        response = Response("Invalid Input: Could not create attendee", status=500,
                            content_type=CONTENT_TYPE_PLAIN_TEXT)
    return response


@app.route("/attendees/<uid>", methods=["GET"])
def get_attendee_by_uid(uid):
    print(f'Input is: {uid}')
    result = Nimbus_Attendees.get_attendee_by_uid(uid)
    if result:
        response = Response(json.dumps(result,default=str), status=200,
                            content_type=CONTENT_TYPE_JSON)
    else:
        response = Response("NOT FOUND", status=404,
                            content_type=CONTENT_TYPE_PLAIN_TEXT)
    return response


@app.route("/attendees/<uid>", methods=["PUT"])
def update_attendee_by_uid(uid):
    print(f'Input is: {uid}')
    return ""


@app.route("/attendees/<uid>", methods=["DELETE"])
def delete_attendee_by_uid(uid):
    print(f'Input is: {uid}')
    result = Nimbus_Attendees.delete_attendee_by_uid(uid) 
    if result:
        response = Response(json.dumps(result,default=str), status=200,
                            content_type=CONTENT_TYPE_JSON)
    else:
        response = Response("NOT FOUND", status=404,
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


if __name__ == '__main__':
    app.run(host='localhost', port=5021, debug=False)
