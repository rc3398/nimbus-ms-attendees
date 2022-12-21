import json, sentry_sdk
from flask import Flask, Response, request,  abort, jsonify, session
from datetime import datetime
from email_validator import validate_email, EmailNotValidError
from marshmallow import ValidationError
from nimbus_attendees import Nimbus_Attendees
from model.attendee import AttendeeSchema
from flask_cors import CORS
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk import capture_exception


# Create the Flask application object.
application = app = Flask(__name__,
                          static_url_path='/',
                          static_folder='static/class-ui/',
                          template_folder='web/templates')
CORS(app)


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

@app.route("/attendees/", methods=["POST"])
def create_attendee():
    
    # TODO: store this in an object ORM
    json_input = request.get_json()
    print(f'Input is: {json_input}')
    
    if not json_input:
        return {"message": "No input data provided"}, 400
    # Validate and deserialize input
    try:
        attendee_schema = AttendeeSchema(many=False)
        new_attendee = attendee_schema.load(json_input)
        is_email = validate_the_email(new_attendee.email_address)

    except ValidationError as err:
        capture_exception(err)
        return {"errors": err.messages}, 422
    
    db_result = Nimbus_Attendees.create_attendee(new_attendee)
    
    if db_result:
      response = Response(attendee_schema.dumps(db_result), status=200,
                        content_type=CONTENT_TYPE_JSON)
    else:
        response = Response("Invalid Input: Could not create attendee", status=500,
                            content_type=CONTENT_TYPE_PLAIN_TEXT)
    return response


@app.route("/attendees/<uid>", methods=["GET"])
def get_attendee_by_uid(uid):
    print(f'Input is: {uid}')
    db_result = Nimbus_Attendees.get_attendee_by_uid(uid)
    
    if db_result:
        response = Response(json.dumps(db_result,default=str), status=200,
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


def validate_the_email(email_address):
    try:
        is_email = validate_email(email_address, check_deliverability=False)
        print(vars(is_email))
        return is_email
    except EmailNotValidError as e:
        print(str(e))
        capture_exception(e)
        raise(e)


if __name__ == '__main__':
    app.run(host='localhost', port=5021, debug=False)