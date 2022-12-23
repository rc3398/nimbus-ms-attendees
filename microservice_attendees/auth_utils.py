import json, requests, six, os
from functools import wraps
from flask import request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    verify_jwt_in_request,
    get_jwt_identity,
    jwt_required,
    get_jwt,
)

# from six.moves import http_client
from google.auth import jwt, exceptions, environment_vars, default
from google.oauth2 import id_token, credentials, service_account
from google.auth.transport import requests as grequest
from google_auth_oauthlib import flow
from google_auth_oauthlib.helpers import credentials_from_session, session_from_client_config
from oauthlib.oauth2 import BearerToken
class NimbusJWT_Authentication():
  
    def __init__(self, user_id_from_id_token, parsed_idtoken):
        user_id_from_id_token
        parsed_idtoken
  
    def jwt_decode_token(token):
        header = jwt.get_unverified_header(token)
        jwks = requests.get('https://{}/.well-known/jwks.json'.format(
            settings.AUTH0_DOMAIN
        )).json()

        public_key = None
        for jwk in jwks['keys']:
            if jwk['kid'] == header['kid']:
                public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

        if public_key is None:
            raise Exception('Public key not found.')

        issuer = 'https://{}/'.format(settings.AUTH0_DOMAIN)
        payload = jwt.decode(
            token,
            public_key,
            audience=settings.AUTH0_AUDIENCE,
            issuer=issuer,
            algorithms=['RS256']
        )
        return payload


    def get_service_account_credentials():
        g2request = grequest.Request()
        script_dir = os.path.dirname(__file__)
        # rel_path = ""
        # GOOGLE_APPLICATION_CREDENTIALS = os.path.join(script_dir, rel_path)
        # credentials_filename = os.environ.get(environment_vars.CREDENTIALS)
        credentials_filename = '/Users/changR/Documents/Code/Columbia/6156/nimbus-ms-attendees/microservice_attendees/assets/nimbus-367902-d114b5ef65ab.json'
        target_audience = "766426913085-de28f0hch9n2lie4up7qo4jb5jpt23o3.apps.googleusercontent.com"

        try:
            with open(credentials_filename, "r") as f:
                info = json.load(f)
                credentials_content = (
                    (info.get("type") == "service_account") and info or None
                )

                credentials = service_account.IDTokenCredentials.from_service_account_info(
                    credentials_content, target_audience=target_audience
                )
        except ValueError as caught_exc:
            new_exc = exceptions.DefaultCredentialsError(
                "Neither metadata server or valid service account credentials are found.",
                caught_exc,
            )
            six.raise_from(new_exc, caught_exc)

        credentials.refresh(g2request)
        return credentials.token


    def id_token_required():
        def wrapper(fn):
            @wraps(fn)
            def decorator(*args, **kwargs):
                # full_access_token = request.headers['Authorization']
                # print(full_access_token)
                # request = requests.Request()
                
                access_token = request.headers['Authorization'].split(' ').pop()
                print(access_token)
                credentials2 = credentials.Credentials(access_token)
                print(credentials2)
                
                scopes=['https://www.googleapis.com/auth/userinfo.email', 
                'https://www.googleapis.com/auth/userinfo.profile']
                # credentials4, project4 = default(scopes)
                # print(credentials4)
                # print(project4)
                
                idtoken = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjAyYTYxZWZkMmE0NGZjMjE1MTQ4ZDRlZmZjMzRkNmE3YjJhYzI2ZjAiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI3NjY0MjY5MTMwODUtZGUyOGYwaGNoOW4ybGllNHVwN3FvNGpiNWpwdDIzbzMuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI3NjY0MjY5MTMwODUtZGUyOGYwaGNoOW4ybGllNHVwN3FvNGpiNWpwdDIzbzMuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDUzOTUyMDU2NDcwMDkwMTQyMTkiLCJoZCI6ImNvbHVtYmlhLmVkdSIsImVtYWlsIjoicmMzMzk4QGNvbHVtYmlhLmVkdSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiTWpNS3RxTHVTX3pOQU9mLTY3SlZlQSIsImlhdCI6MTY3MTgxNjk4NiwiZXhwIjoxNjcxODIwNTg2fQ.SHq6SkoEOX9f-1EIHuL0x1vMpLm1l5dKQeisjNKnkymKEX5W0_2ANQTIJaAOYLLayrr0nv8hFaksxoQEAweFPHLnXjW07q8mEj-6A1UeKzRuaVSP0KTBE00myEsyegVkikNYnU9IDeMqDF93-cYWpqDM9TOhU7oR0WZHUqurBqWxpwFvAcdm-9BtIWZTpIRevZAju1mtwuNucORVg7pjrtxpG4liU9r4CYMjIJw7R-hMWHLqhF6C_2YLgA_5YiuJdR1gr7urF5ak1opMtxRPpbvLUUN11g5KQdJGZtYyoq1ICu1PpioXWW1PV32qUTjwp97NvzOioIpktRgVCHP59g"
                # idtoken = NimbusJWT_Authentication.get_service_account_credentials()
                print(idtoken)
                
                # id_token_info : https://oauth2.googleapis.com/tokeninfo?id_token=                
                id_token_info_response = requests.get('https://oauth2.googleapis.com/tokeninfo?id_token='+idtoken)
                id_token_info = id_token_info_response.json()
                print(id_token_info)
                
                target_audience = "766426913085-de28f0hch9n2lie4up7qo4jb5jpt23o3.apps.googleusercontent.com"
                # _GOOGLE_OAUTH2_CERTS_URL = "https://www.googleapis.com/oauth2/v1/certs"
                certs_url2="https://www.googleapis.com/oauth2/v1/certs"
                grequest2 = grequest.Request()
                # fetched_id_token = id_token.fetch_id_token(grequest2, target_audience)
                # print(fetched_id_token)
                
                id_info = id_token.verify_oauth2_token(idtoken, grequest2, target_audience)
                # id_info = id_token.verify_token(idtoken, grequest2, target_audience, certs_url=certs_url2)
                print(id_info)

                userid = id_info['sub']
                print(userid)
                user_id_from_id_token=userid
                
                return fn(*args, **kwargs)
            return decorator
        return wrapper
    
    def get_userid_from_idtoken():
        return NimbusJWT_Authentication.user_id_from_id_token
      
    def get_parsed_idtoken():
        return NimbusJWT_Authentication.parsed_idtoken
      
    def get_credentials_from_session():
        flow1 = flow.Flow.from_client_secrets_file(
            '/Users/changR/Documents/Code/Columbia/6156/nimbus-ms-attendees/microservice_attendees/assets/client_secrets.json',
            scopes=['https://www.googleapis.com/auth/userinfo.email', 
                    'https://www.googleapis.com/auth/userinfo.profile'])
        scopes=['https://www.googleapis.com/auth/userinfo.email', 
                    'https://www.googleapis.com/auth/userinfo.profile']
        flow1.redirect_uri = 'http://localhost:5021/login/callback'
        print(flow1)
        file='/Users/changR/Documents/Code/Columbia/6156/nimbus-ms-attendees/microservice_attendees/assets/client_secrets.json'
        with open(file, "r") as json_file:
            client_config = json.load(json_file)
        
        session_cred3 = session_from_client_config(client_config, scopes)
        print(session_cred3)
        print(session_cred3[0])
        credentials3 = credentials_from_session(session_cred3[0])
        print(credentials3)
        # this returns the access token
        return credentials3

'''
Documentation
- https://developers.google.com/identity/protocols/oauth2
- https://google-auth.readthedocs.io/en/stable/_modules/google/oauth2/id_token.html
- https://google-auth.readthedocs.io/en/latest/user-guide.html#obtaining-credentials
- https://developers.google.com/identity/openid-connect/openid-connect#server-flow
- https://openid.net/specs/openid-connect-core-1_0.html#IDToken

'''